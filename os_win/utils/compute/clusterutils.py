# Copyright 2016 Cloudbase Solutions Srl
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""
Utility class for VM related operations on Hyper-V Clusters.
"""

import re
import sys
import threading
import time

from eventlet import patcher
from eventlet import tpool
from oslo_log import log as logging
from oslo_utils import excutils

from os_win._i18n import _, _LI, _LE
from os_win import _utils
from os_win import constants
from os_win import exceptions
from os_win.utils import baseutils
from os_win.utils.compute import _clusapi_utils

LOG = logging.getLogger(__name__)


class ClusterUtils(baseutils.BaseUtils):

    _MSCLUSTER_NODE = 'MSCluster_Node'
    _MSCLUSTER_RES = 'MSCluster_Resource'

    _VM_BASE_NAME = 'Virtual Machine %s'
    _VM_TYPE = 'Virtual Machine'
    _VM_GROUP_TYPE = 111

    _MS_CLUSTER_NAMESPACE = '//%s/root/MSCluster'

    _LIVE_MIGRATION_TYPE = 4
    _IGNORE_LOCKED = 1
    _DESTROY_GROUP = 1

    _FAILBACK_TRUE = 1
    _FAILBACK_WINDOW_MIN = 0
    _FAILBACK_WINDOW_MAX = 23

    _WMI_EVENT_TIMEOUT_MS = 100
    _WMI_EVENT_CHECK_INTERVAL = 2

    _DEFAULT_LIVE_MIGRATION_TIMEOUT = 60  # seconds

    def __init__(self, host='.'):
        self._instance_name_regex = re.compile('Virtual Machine (.*)')
        self._clusapi_utils = _clusapi_utils.ClusApiUtils()

        if sys.platform == 'win32':
            self._init_hyperv_conn(host)
            self._watcher = self._get_failover_watcher()

    def _init_hyperv_conn(self, host):
        try:
            self._conn_cluster = self._get_wmi_conn(
                self._MS_CLUSTER_NAMESPACE % host)
            self._cluster = self._conn_cluster.MSCluster_Cluster()[0]

            # extract this node name from cluster's path
            path = self._cluster.path_()
            self._this_node = re.search(r'\\\\(.*)\\root', path,
                                        re.IGNORECASE).group(1)
        except AttributeError:
            raise exceptions.HyperVClusterException(
                _("Could not initialize cluster wmi connection."))

    def _get_failover_watcher(self):
        raw_query = ("SELECT * FROM __InstanceModificationEvent "
                     "WITHIN %(wmi_check_interv)s WHERE TargetInstance ISA "
                     "'%(cluster_res)s' AND "
                     "TargetInstance.Type='%(cluster_res_type)s' AND "
                     "TargetInstance.OwnerNode != PreviousInstance.OwnerNode" %
                     {'wmi_check_interv': self._WMI_EVENT_CHECK_INTERVAL,
                      'cluster_res': self._MSCLUSTER_RES,
                      'cluster_res_type': self._VM_TYPE})
        return self._conn_cluster.watch_for(raw_wql=raw_query)

    def check_cluster_state(self):
        if len(self._get_cluster_nodes()) < 1:
            raise exceptions.HyperVClusterException(
                _("Not enough cluster nodes."))

    def get_node_name(self):
        return self._this_node

    def _get_cluster_nodes(self):
        cluster_assoc = self._conn_cluster.MSCluster_ClusterToNode(
            Antecedent=self._cluster.path_())
        return [x.Dependent for x in cluster_assoc]

    def _get_vm_groups(self):
        assocs = self._conn_cluster.MSCluster_ClusterToResourceGroup(
            GroupComponent=self._cluster.path_())
        resources = [a.PartComponent for a in assocs]
        return (r for r in resources if
                hasattr(r, 'GroupType') and
                r.GroupType == self._VM_GROUP_TYPE)

    def _lookup_vm_group_check(self, vm_name):
        vm = self._lookup_vm_group(vm_name)
        if not vm:
            raise exceptions.HyperVVMNotFoundException(vm_name=vm_name)
        return vm

    def _lookup_vm_group(self, vm_name):
        return self._lookup_res(self._conn_cluster.MSCluster_ResourceGroup,
                                vm_name)

    def _lookup_vm_check(self, vm_name):
        vm = self._lookup_vm(vm_name)
        if not vm:
            raise exceptions.HyperVVMNotFoundException(vm_name=vm_name)
        return vm

    def _lookup_vm(self, vm_name):
        vm_name = self._VM_BASE_NAME % vm_name
        return self._lookup_res(self._conn_cluster.MSCluster_Resource, vm_name)

    def _lookup_res(self, resource_source, res_name):
        res = resource_source(Name=res_name)
        n = len(res)
        if n == 0:
            return None
        elif n > 1:
            raise exceptions.HyperVClusterException(
                _('Duplicate resource name %s found.') % res_name)
        else:
            return res[0]

    def get_cluster_node_names(self):
        nodes = self._get_cluster_nodes()
        return [n.Name for n in nodes]

    def get_vm_host(self, vm_name):
        return self._lookup_vm_group_check(vm_name).OwnerNode

    def list_instances(self):
        return [r.Name for r in self._get_vm_groups()]

    def list_instance_uuids(self):
        return [r.Id for r in self._get_vm_groups()]

    def add_vm_to_cluster(self, vm_name):
        LOG.debug("Add vm to cluster called for vm %s" % vm_name)
        self._cluster.AddVirtualMachine(vm_name)

        vm_group = self._lookup_vm_group_check(vm_name)
        vm_group.PersistentState = True
        vm_group.AutoFailbackType = self._FAILBACK_TRUE
        # set the earliest and latest time that the group can be moved
        # back to its preferred node. The unit is in hours.
        vm_group.FailbackWindowStart = self._FAILBACK_WINDOW_MIN
        vm_group.FailbackWindowEnd = self._FAILBACK_WINDOW_MAX
        vm_group.put()

    def bring_online(self, vm_name):
        vm = self._lookup_vm_check(vm_name)
        vm.BringOnline()

    def take_offline(self, vm_name):
        vm = self._lookup_vm_check(vm_name)
        vm.TakeOffline()

    def delete(self, vm_name):
        vm = self._lookup_vm_group_check(vm_name)
        vm.DestroyGroup(self._DESTROY_GROUP)

    def vm_exists(self, vm_name):
        return self._lookup_vm(vm_name) is not None

    def live_migrate_vm(self, vm_name, new_host,
                        timeout=_DEFAULT_LIVE_MIGRATION_TIMEOUT):
        self._migrate_vm(vm_name, new_host, self._LIVE_MIGRATION_TYPE,
                         constants.CLUSTER_GROUP_ONLINE,
                         timeout)

    def _migrate_vm(self, vm_name, new_host, migration_type,
                    exp_state_after_migr, timeout):
        syntax = _clusapi_utils.CLUSPROP_SYNTAX_LIST_VALUE_DWORD
        migr_type = _clusapi_utils.DWORD(migration_type)

        prop_entries = [
            self._clusapi_utils.get_property_list_entry(
                _clusapi_utils.CLUSPROP_NAME_VM, syntax, migr_type),
            self._clusapi_utils.get_property_list_entry(
                _clusapi_utils.CLUSPROP_NAME_VM_CONFIG, syntax, migr_type)
        ]
        prop_list = self._clusapi_utils.get_property_list(prop_entries)

        flags = (
            _clusapi_utils.CLUSAPI_GROUP_MOVE_RETURN_TO_SOURCE_NODE_ON_ERROR |
            _clusapi_utils.CLUSAPI_GROUP_MOVE_QUEUE_ENABLED |
            _clusapi_utils.CLUSAPI_GROUP_MOVE_HIGH_PRIORITY_START)

        cluster_handle = None
        group_handle = None
        dest_node_handle = None

        try:
            cluster_handle = self._clusapi_utils.open_cluster()
            group_handle = self._clusapi_utils.open_cluster_group(
                cluster_handle, vm_name)
            dest_node_handle = self._clusapi_utils.open_cluster_node(
                cluster_handle, new_host)

            previous_host = self._clusapi_utils.get_cluster_group_state(
                group_handle)['owner_node']

            event_type = _clusapi_utils.CLUSTER_CHANGE_GROUP_STATE
            event_filter = (
                lambda event:
                event['cluster_object_name'].lower() == vm_name.lower())
            with ClusterEventListener(event_type, event_filter,
                                      cluster_handle) as listener:
                self._clusapi_utils.move_cluster_group(group_handle,
                                                       dest_node_handle,
                                                       flags,
                                                       prop_list)
                try:
                    self._wait_for_cluster_group_migration(listener,
                                                           vm_name,
                                                           group_handle,
                                                           exp_state_after_migr,
                                                           new_host,
                                                           timeout)
                except exceptions.ClusterGroupMigrationTimeOut:
                    with excutils.save_and_reraise_exception() as ctxt:
                        self._cancel_cluster_group_migration(
                            listener, vm_name, group_handle, timeout)

                        group_state_info = (
                            self._clusapi_utils.get_cluster_group_state(
                                group_handle))
                        group_state = group_state_info['state']
                        current_host = group_state_info['owner_node']
                        if (group_state == exp_state_after_migr and
                                current_host.lower() ==
                                new_host.lower()):
                            LOG.info(_LI("Cluster group migration finished "
                                         "successfully after cancel attempt. "
                                         "Supressing timeout error."))
                            ctxt.reraise = False
        finally:
            if group_handle:
                self._clusapi_utils.close_cluster_group(group_handle)
            if dest_node_handle:
                self._clusapi_utils.close_cluster_node(dest_node_handle)
            if cluster_handle:
                self._clusapi_utils.close_cluster(cluster_handle)

    def _cancel_cluster_group_migration(self, event_listener,
                                        group_name, group_handle,
                                        timeout=None):
        try:
            cancel_finished = self._clusapi_utils.cancel_cluster_group_operation(
                group_handle)
        except exceptions.Win32Exception as ex:
            group_state = self._clusapi_utils.get_cluster_group_state(
                group_handle)['state']

            if (ex.error_code == _clusapi_utils.ERROR_INVALID_STATE and
                    group_state != constants.CLUSTER_GROUP_PENDING):
                LOG.debug("Ignoring group migration cancel error. Group "
                          "state is not 'pending', currently: %s.", group_state)
                cancel_finished = True
            else:
                raise

        if not cancel_finished:
            LOG.debug("Waiting for group migration to be canceled.")
            try:
                self._wait_for_cluster_group_migration(
                    event_listener, group_name, group_handle,
                    timeout=timeout)
            except Exception:
                LOG.exception(_LE("Failed to cancel cluster group migration."))
                raise exceptions.JobTerminateFailed()

        LOG.info(_LI("Cluster group migration canceled."))

    def _wait_for_cluster_group_migration(self, event_listener,
                                          group_name, group_handle,
                                          desired_state=None, desired_node=None,
                                          timeout=None):
        time_start = time.time()
        time_left = timeout if timeout else 'undefined'

        migration_started = False
        while not timeout or time_left > 0:
            time_elapsed = time.time() - time_start
            time_left = timeout - time_elapsed if timeout else 'undefined'

            LOG.debug("Waiting for cluster group '%(group_name)s' "
                      "migration to finish. "
                      "Expected node: %(desired_node)s. "
                      "Expected state: %(desired_state)s. "
                      "Time left: %(time_left)s.",
                      dict(group_name=group_name,
                           desired_node=desired_node,
                           desired_state=desired_state,
                           time_left=time_left))

            # Some events may be missed, for which reason we ensure this won't
            # block undefinetely.
            event_listener.wait(time_left if timeout
                                else self._DEFAULT_LIVE_MIGRATION_TIMEOUT)

            state_info = self._clusapi_utils.get_cluster_group_state(
                group_handle)
            owner_node = state_info['owner_node']
            group_state = state_info['state']

            reached_desired_state = (desired_state is None or
                                     desired_state == group_state)
            reached_desired_node = (desired_node is None or
                                   desired_node.lower() == owner_node.lower())

            migration_completed = (reached_desired_state and reached_desired_node
                                   and group_state != constants.CLUSTER_GROUP_PENDING)
            if migration_completed:
                LOG.debug("Cluster group migration finished.")
                return

            if group_state == constants.CLUSTER_GROUP_PENDING:
                migration_started = True
            # The migration started, is not running anymore but the group
            # did not reach the expected state. We're treating this as a
            # failure.
            elif (migration_started or
                    group_state == constants.CLUSTER_GROUP_FAILED):
                LOG.error(_LE("Cluster group migration failed."))
                raise exceptions.ClusterGroupMigrationFailed(
                    group_name=group_name,
                    expected_state=desired_state,
                    expected_node=desired_node,
                    group_state=group_state,
                    owner_node=owner_node)

        LOG.error(_LE("Cluster group migration timed out."))
        raise exceptions.ClusterGroupMigrationTimeOut(
            group_name=group_name,
            time_elapsed=time_elapsed,
            expected_state=desired_state,
            expected_node=desired_node,
            group_state=group_state,
            owner_node=owner_node)

    def monitor_vm_failover(self, callback):
        """Creates a monitor to check for new WMI MSCluster_Resource

        events.

        This method will poll the last _WMI_EVENT_CHECK_INTERVAL + 1
        seconds for new events and listens for _WMI_EVENT_TIMEOUT_MS
        miliseconds, since listening is a thread blocking action.

        Any event object caught will then be processed.
        """

        vm_name = None
        new_host = None
        try:
            # wait for new event for _WMI_EVENT_TIMEOUT_MS miliseconds.
            if patcher.is_monkey_patched('thread'):
                wmi_object = tpool.execute(self._watcher,
                                           self._WMI_EVENT_TIMEOUT_MS)
            else:
                wmi_object = self._watcher(self._WMI_EVENT_TIMEOUT_MS)

            old_host = wmi_object.previous.OwnerNode
            new_host = wmi_object.OwnerNode
            # wmi_object.Name field is of the form:
            # 'Virtual Machine nova-instance-template'
            # wmi_object.Name filed is a key and as such is not affected
            # by locale, so it will always be 'Virtual Machine'
            match = self._instance_name_regex.search(wmi_object.Name)
            if match:
                vm_name = match.group(1)

            if vm_name:
                try:
                    callback(vm_name, old_host, new_host)
                except Exception:
                    LOG.exception(
                        _LE("Exception during failover callback."))
        except exceptions.x_wmi_timed_out:
            pass


class ClusterEventListener(object):
    _EVENT_WAIT_TIMEOUT_MS = 10000

    _notif_handle = None
    _cluster_handle = None
    _external_cluster_handle = False
    _running = False

    def __init__(self, event_type, event_filter=None, cluster_handle=None):
        if cluster_handle is not None:
            self._cluster_handle = cluster_handle
            self._external_cluster_handle = True

        self._event_type = event_type
        self._event_filter = (event_filter if event_filter is not None
                              else lambda event: True)
        self._event_received = threading.Event()

        self._clusapi_utils = _clusapi_utils.ClusApiUtils()

        self._setup()

    def __enter__(self):
        self._ensure_listener_running()
        return self

    def _setup(self):
        if not self._external_cluster_handle:
            self._cluster_handle = self._clusapi_utils.open_cluster()

        self._notif_handle = self._clusapi_utils.create_cluster_notify_port(
            self._cluster_handle, self._event_type)

        # If eventlet monkey patching is used, this will actually be a
        # greenthread. We just don't want to enforce eventlet usage.
        worker = threading.Thread(target=self._listen)
        worker.setDaemon(True)
        worker.start()

        self._running = True

    def __exit__(self, exc_type, exc_value, traceback):
        self.stop()

    def _signal_stopped(self):
        self._running = False
        self._event_received.set()

    def stop(self):
        self._signal_stopped()

        if self._cluster_handle and not self._external_cluster_handle:
            self._clusapi_utils.close_cluster(self._cluster_handle)
        if self._notif_handle:
            self._clusapi_utils.close_cluster_notify_port(self._notif_handle)

    def _listen(self):
        try:
            while self._running:
                try:
                    event = _utils.avoid_blocking_call(
                        self._clusapi_utils.get_cluster_notify,
                        self._notif_handle,
                        self._event_type,
                        self._EVENT_WAIT_TIMEOUT_MS)
                except exceptions.Win32Exception as ex:
                    if ex.error_code == _clusapi_utils.ERROR_WAIT_TIMEOUT:
                        continue
                    else:
                        raise
                if self._event_filter(event):
                    self._event_received.set()
        except Exception as ex:
            if self._running:
                LOG.exception(
                    _LE("Unexpected exception in event listener loop."))
                self._signal_stopped()

    def wait(self, timeout=None):
        self._ensure_listener_running()

        self._event_received.wait(timeout)

        self._ensure_listener_running()
        self._event_received.clear()

    def _ensure_listener_running(self):
        if not self._running:
            raise exceptions.OSWinException(
                _("Cluster event listener is not running."))

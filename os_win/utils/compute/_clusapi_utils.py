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

import ctypes
import sys

if sys.platform == 'win32':
    clusapi = ctypes.windll.clusapi

from os_win import constants
from os_win import exceptions
from os_win.utils import win32utils

DWORD = ctypes.c_ulong

# TODO(lpetrut): aggregate windows specific constants
INVALID_HANDLE_VALUE = -1

CLUSPROP_SYNTAX_NAME = 262147
CLUSPROP_SYNTAX_ENDMARK = 0
CLUSPROP_SYNTAX_LIST_VALUE_DWORD = 65538

CLUSAPI_GROUP_MOVE_RETURN_TO_SOURCE_NODE_ON_ERROR = 2
CLUSAPI_GROUP_MOVE_QUEUE_ENABLED = 4
CLUSAPI_GROUP_MOVE_HIGH_PRIORITY_START = 8

CLUSTER_CHANGE_GROUP_STATE = 0x00001000
CLUSTER_CHANGE_GROUP_PROPERTY = 0x00008000

ERROR_INVALID_STATE = 5023
ERROR_WAIT_TIMEOUT = 258
ERROR_IO_PENDING = 997

CLUSPROP_NAME_VM = 'Virtual Machine'
CLUSPROP_NAME_VM_CONFIG = 'Virtual Machine Configuration'


class ClusApiUtils(object):
    _MAX_NODE_NAME = 255

    _open_handle_check_flags = dict(ret_val_is_err_code=False,
                                    error_on_nonzero_ret_val=False,
                                    error_ret_vals=[0, None])

    def __init__(self):
        self._win32utils = win32utils.Win32Utils()

    def _run_and_check_output(self, *args, **kwargs):
        kwargs['failure_exc'] = exceptions.ClusterWin32Exception
        return self._win32utils.run_and_check_output(*args, **kwargs)

    def _dword_align(self, value):
        return (value + 3) & ~3

    def _get_clusprop_value_struct(self, val_type):
        def _get_padding():
            # The cluster property entries must be 4B aligned.
            val_sz = ctypes.sizeof(val_type)
            return self._dword_align(val_sz) - val_sz

        # For convenience, as opposed to the homonymous ClusAPI
        # structure, we add the actual value as well.
        class CLUSPROP_VALUE(ctypes.Structure):
            _fields_ = [('syntax', DWORD),
                        ('length', DWORD),
                        ('value', val_type),
                        ('_padding', ctypes.c_ubyte * _get_padding())]
        return CLUSPROP_VALUE

    def get_property_list_entry(self, name, syntax, value):
        # The value argument must have a ctypes type.
        name_len = len(name) + 1
        val_sz = ctypes.sizeof(value)

        class CLUSPROP_LIST_ENTRY(ctypes.Structure):
            _fields_ = [
                ('name', self._get_clusprop_value_struct(
                    val_type=ctypes.c_wchar * name_len)),
                ('value', self._get_clusprop_value_struct(
                    val_type=ctypes.c_ubyte * val_sz)),
                ('_endmark', DWORD)
            ]

        entry = CLUSPROP_LIST_ENTRY()
        entry.name.syntax = CLUSPROP_SYNTAX_NAME
        entry.name.length = name_len * ctypes.sizeof(ctypes.c_wchar)
        entry.name.value = name

        entry.value.syntax = syntax
        entry.value.length = val_sz
        entry.value.value[0:val_sz] = bytearray(value)

        entry._endmark = CLUSPROP_SYNTAX_ENDMARK

        return entry

    def get_property_list(self, property_entries):
        prop_entries_sz = sum([ctypes.sizeof(entry)
                              for entry in property_entries])

        class CLUSPROP_LIST(ctypes.Structure):
            _fields_ = [('count', DWORD),
                        ('entries_buff', ctypes.c_ubyte * prop_entries_sz)]

        prop_list = CLUSPROP_LIST(count=len(property_entries))

        pos = 0
        for prop_entry in property_entries:
            prop_entry_sz = ctypes.sizeof(prop_entry)
            prop_list.entries_buff[pos:prop_entry_sz + pos] = bytearray(
                prop_entry)
            pos += prop_entry_sz

        return prop_list

    def open_cluster(self, cluster_name=None):
        """Returns a handle for the requested cluster.

        :param cluster_name: (Optional) specifies the name of the cluster
                             to be opened. If None, the cluster that the
                             local node belongs to will be opened.
        """
        p_clus_name = ctypes.c_wchar_p(cluster_name) if cluster_name else None
        handle = self._run_and_check_output(clusapi.OpenCluster,
                                            p_clus_name,
                                            **self._open_handle_check_flags)
        return handle

    def open_cluster_group(self, cluster_handle, group_name):
        handle = self._run_and_check_output(clusapi.OpenClusterGroup,
                                            cluster_handle,
                                            ctypes.c_wchar_p(group_name),
                                            **self._open_handle_check_flags)
        return handle

    def open_cluster_node(self, cluster_handle, node_name):
        handle = self._run_and_check_output(clusapi.OpenClusterNode,
                                            cluster_handle,
                                            ctypes.c_wchar_p(node_name),
                                            **self._open_handle_check_flags)
        return handle

    def close_cluster(self, cluster_handle):
        # This function will always return 'True'. Closing the cluster
        # handle will also invalidate handles opened using it.
        clusapi.CloseCluster(cluster_handle)

    def close_cluster_group(self, group_handle):
        # TODO(lpetrut): The following functions can fail, in which case
        # 'False' will be returned. We may want to handle this situation.
        clusapi.CloseClusterGroup(group_handle)

    def close_cluster_node(self, node_handle):
        clusapi.CloseClusterNode(node_handle)

    def cancel_cluster_group_operation(self, group_handle):
        """Requests a pending move operation to be canceled.
           return: True if the cancel request completed succesfuly,
                   False if it's still in proggress.
        """
        # This only applies to move operations requested by
        # MoveClusterGroup(Ex), thus it will not apply to fail overs.
        ret_val = self._run_and_check_output(
            clusapi.CancelClusterGroupOperation,
            group_handle,
            0,  # cancel flags (reserved for future use by MS)
            ignored_error_codes=[ERROR_IO_PENDING])

        cancel_completed = ret_val != ERROR_IO_PENDING
        return cancel_completed

    def move_cluster_group(self, group_handle, destination_node_handle,
                           move_flags, property_list):
        prop_list_p = ctypes.byref(property_list) if property_list else None
        prop_list_sz = ctypes.sizeof(property_list) if property_list else 0

        self._run_and_check_output(clusapi.MoveClusterGroupEx,
                                   group_handle,
                                   destination_node_handle,
                                   move_flags,
                                   prop_list_p,
                                   prop_list_sz,
                                   ignored_error_codes=[ERROR_IO_PENDING])

    def get_cluster_group_state(self, group_handle):
        node_name_len = DWORD(self._MAX_NODE_NAME)
        node_name_buff = (ctypes.c_wchar * node_name_len.value)()

        group_state = self._run_and_check_output(
            clusapi.GetClusterGroupState,
            group_handle,
            ctypes.byref(node_name_buff),
            ctypes.byref(node_name_len),
            error_ret_vals=[constants.CLUSTER_GROUP_STATE_UNKNOWN],
            error_on_nonzero_ret_val=False,
            ret_val_is_err_code=False)

        return {'state': group_state,
                'owner_node': node_name_buff.value}

    def create_cluster_notify_port(self, cluster_handle, notif_filter,
                                   notif_handle=None, notif_key=None):
        notif_key = notif_key or notif_filter
        notif_handle = notif_handle or INVALID_HANDLE_VALUE
        # If INVALID_HANDLE_VALUE is passed as the notification handle,
        # a new one will be created. Otherwise, new events are added to the
        # specified notification port.
        notif_handle = self._run_and_check_output(
            clusapi.CreateClusterNotifyPort,
            notif_handle,
            cluster_handle,
            notif_filter,
            ctypes.byref(ctypes.c_ulong(notif_key)),
            **self._open_handle_check_flags)
        return notif_handle

    def close_cluster_notify_port(self, notif_handle):
        # Always returns True.
        clusapi.CloseClusterNotifyPort(notif_handle)

    def get_cluster_notify(self, notif_handle, notif_key, timeout_ms=0):
        filter_type = ctypes.c_ulong()
        obj_name_buff_sz = ctypes.c_ulong(self._MAX_NODE_NAME)
        obj_name_buff = (ctypes.c_wchar * obj_name_buff_sz.value)()

        self._run_and_check_output(
            clusapi.GetClusterNotify,
            notif_handle,
            ctypes.byref(ctypes.c_ulong(notif_key)),
            ctypes.byref(filter_type),
            ctypes.byref(obj_name_buff),
            ctypes.byref(obj_name_buff_sz),
            timeout_ms)

        event = {'cluster_object_name': obj_name_buff.value,
                 'cluster_change': filter_type.value}
        return event

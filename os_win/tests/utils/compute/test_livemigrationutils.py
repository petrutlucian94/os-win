# Copyright 2014 Cloudbase Solutions Srl
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

import mock
from oslotest import base

from os_win import exceptions
from os_win.utils.compute import livemigrationutils
from os_win.utils.compute import vmutils


class LiveMigrationUtilsTestCase(base.BaseTestCase):
    """Unit tests for the Hyper-V LiveMigrationUtils class."""

    _FAKE_VM_NAME = 'fake_vm_name'
    _FAKE_RET_VAL = 0

    _RESOURCE_TYPE_VHD = 31
    _RESOURCE_TYPE_DISK = 17
    _RESOURCE_SUB_TYPE_VHD = 'Microsoft:Hyper-V:Virtual Hard Disk'
    _RESOURCE_SUB_TYPE_DISK = 'Microsoft:Hyper-V:Physical Disk Drive'

    def setUp(self):
        self.liveutils = livemigrationutils.LiveMigrationUtils()
        self.liveutils._vmutils = mock.MagicMock()
        self.liveutils._jobutils = mock.Mock()

        self._conn = mock.MagicMock()
        self.liveutils._get_conn_v2 = mock.MagicMock(return_value=self._conn)

        super(LiveMigrationUtilsTestCase, self).setUp()

    def test_check_live_migration_config(self):
        mock_migr_svc = self._conn.Msvm_VirtualSystemMigrationService()[0]

        vsmssd = mock.MagicMock()
        vsmssd.EnableVirtualSystemMigration = True
        mock_migr_svc.associators.return_value = [vsmssd]
        mock_migr_svc.MigrationServiceListenerIPAdressList.return_value = [
            mock.sentinel.FAKE_HOST]

        self.liveutils.check_live_migration_config()
        self.assertTrue(mock_migr_svc.associators.called)

    def test_get_vm(self):
        expected_vm = mock.MagicMock()
        mock_conn_v2 = mock.MagicMock()
        mock_conn_v2.Msvm_ComputerSystem.return_value = [expected_vm]

        found_vm = self.liveutils._get_vm(mock_conn_v2, self._FAKE_VM_NAME)

        self.assertEqual(expected_vm, found_vm)

    def test_get_vm_duplicate(self):
        mock_vm = mock.MagicMock()
        mock_conn_v2 = mock.MagicMock()
        mock_conn_v2.Msvm_ComputerSystem.return_value = [mock_vm, mock_vm]

        self.assertRaises(exceptions.HyperVException, self.liveutils._get_vm,
                          mock_conn_v2, self._FAKE_VM_NAME)

    def test_get_vm_not_found(self):
        mock_conn_v2 = mock.MagicMock()
        mock_conn_v2.Msvm_ComputerSystem.return_value = []

        self.assertRaises(exceptions.HyperVVMNotFoundException,
                          self.liveutils._get_vm,
                          mock_conn_v2, self._FAKE_VM_NAME)

    def test_destroy_planned_vm(self):
        mock_conn_v2 = mock.MagicMock()
        mock_planned_vm = mock.MagicMock()
        mock_vs_man_svc = mock.MagicMock()
        mock_conn_v2.Msvm_VirtualSystemManagementService.return_value = [
            mock_vs_man_svc]
        mock_planned_vm.path_.return_value = mock.sentinel.planned_vm_path
        mock_vs_man_svc.DestroySystem.return_value = (
            mock.sentinel.job_path, mock.sentinel.ret_val)

        self.liveutils._destroy_planned_vm(mock_conn_v2, mock_planned_vm)

        mock_msvms_cls = mock_conn_v2.Msvm_VirtualSystemManagementService
        mock_msvms_cls.assert_called_once_with()
        mock_vs_man_svc.DestroySystem.assert_called_once_with(
            mock.sentinel.planned_vm_path)
        self.liveutils._jobutils.check_ret_val.assert_called_once_with(
            mock.sentinel.ret_val,
            mock.sentinel.job_path)

    def test_get_planned_vms(self):
        mock_conn_v2 = mock.MagicMock()
        mock_vm = self._get_vm()
        mock_conn_v2.Msvm_PlannedComputerSystem.return_value = (
            mock.sentinel.planned_vms)

        planned_vms = self.liveutils._get_planned_vms(mock_conn_v2, mock_vm)

        mock_conn_v2.Msvm_PlannedComputerSystem.assert_called_once_with(
            Name=self._FAKE_VM_NAME)
        self.assertEqual(mock.sentinel.planned_vms, planned_vms)

    @mock.patch.object(livemigrationutils.LiveMigrationUtils,
                       '_destroy_planned_vm')
    @mock.patch.object(livemigrationutils.LiveMigrationUtils,
                       '_get_planned_vms')
    def test_destroy_existing_planned_vms(self, mock_get_planned_vms,
                                          mock_destroy_planned_vm):
        mock_conn_v2 = mock.sentinel.conn_v2
        mock_planned_vms = [mock.sentinel.planned_vm,
                            mock.sentinel.another_planned_vm]
        mock_get_planned_vms.return_value = mock_planned_vms

        self.liveutils._destroy_existing_planned_vms(mock_conn_v2,
                                                     mock.sentinel.vm)

        mock_get_planned_vms.assert_called_once_with(mock_conn_v2,
                                                     mock.sentinel.vm)
        mock_destroy_planned_vm.assert_has_calls(
            [mock.call(mock_conn_v2, mock.sentinel.planned_vm),
             mock.call(mock_conn_v2, mock.sentinel.another_planned_vm)])

    def test_create_planned_vm_helper(self):
        mock_vsmsd = self._conn.query()[0]
        mock_vm = mock.MagicMock()
        mock_v2 = mock.MagicMock()
        mock_v2.Msvm_PlannedComputerSystem.return_value = [mock_vm]

        migr_svc = self._conn.Msvm_VirtualSystemMigrationService()[0]
        migr_svc.MigrateVirtualSystemToHost.return_value = (
            self._FAKE_RET_VAL, mock.sentinel.job_path)

        resulted_vm = self.liveutils._create_planned_vm(
            mock_v2, self._conn, mock_vm, [mock.sentinel.FAKE_REMOTE_IP_ADDR],
            mock.sentinel.FAKE_HOST)

        self.assertEqual(mock_vm, resulted_vm)

        migr_svc.MigrateVirtualSystemToHost.assert_called_once_with(
            ComputerSystem=mock_vm.path_.return_value,
            DestinationHost=mock.sentinel.FAKE_HOST,
            MigrationSettingData=mock_vsmsd.GetText_.return_value)
        self.liveutils._jobutils.check_ret_val.assert_called_once_with(
            mock.sentinel.job_path,
            self._FAKE_RET_VAL)

    def test_get_disk_data(self):
        mock_vmutils_remote = mock.MagicMock()
        mock_disk = mock.MagicMock()
        mock_disk_path_mapping = {
            mock.sentinel.serial: mock.sentinel.disk_path}

        mock_disk.path.return_value.RelPath = mock.sentinel.rel_path
        mock_vmutils_remote.get_vm_disks.return_value = [
            None, [mock_disk]]
        mock_disk.ElementName = mock.sentinel.serial

        resulted_disk_paths = self.liveutils._get_disk_data(
            self._FAKE_VM_NAME, mock_vmutils_remote, mock_disk_path_mapping)

        mock_vmutils_remote.get_vm_disks.assert_called_once_with(
            self._FAKE_VM_NAME)
        mock_disk.path.assert_called_once_with()
        expected_disk_paths = {mock.sentinel.rel_path: mock.sentinel.disk_path}
        self.assertEqual(expected_disk_paths, resulted_disk_paths)

    def test_update_planned_vm_disk_resources(self):
        self._prepare_vm_mocks(self._RESOURCE_TYPE_DISK,
                               self._RESOURCE_SUB_TYPE_DISK)
        mock_vm = self._conn.Msvm_ComputerSystem.return_value[0]
        sasd = mock_vm.associators()[0].associators()[0]

        mock_vsmsvc = self._conn.Msvm_VirtualSystemManagementService()[0]

        self.liveutils._update_planned_vm_disk_resources(
            self._conn, mock_vm, mock.sentinel.FAKE_VM_NAME,
            {sasd.path.return_value.RelPath: mock.sentinel.FAKE_RASD_PATH})

        mock_vsmsvc.ModifyResourceSettings.assert_called_once_with(
            ResourceSettings=[sasd.GetText_.return_value])

    def test_get_vhd_setting_data(self):
        self._prepare_vm_mocks(self._RESOURCE_TYPE_VHD,
                               self._RESOURCE_SUB_TYPE_VHD)
        mock_vm = self._conn.Msvm_ComputerSystem.return_value[0]
        mock_sasd = mock_vm.associators()[0].associators()[0]

        vhd_sds = self.liveutils._get_vhd_setting_data(mock_vm)
        self.assertEqual([mock_sasd.GetText_.return_value], vhd_sds)

    def test_live_migrate_vm_helper(self):
        mock_conn_local = mock.MagicMock()
        mock_vm = mock.MagicMock()
        mock_vsmsd = mock_conn_local.query()[0]

        mock_vsmsvc = mock_conn_local.Msvm_VirtualSystemMigrationService()[0]
        mock_vsmsvc.MigrateVirtualSystemToHost.return_value = (
            self._FAKE_RET_VAL, mock.sentinel.FAKE_JOB_PATH)

        self.liveutils._live_migrate_vm(
            mock_conn_local, mock_vm, None,
            [mock.sentinel.FAKE_REMOTE_IP_ADDR],
            mock.sentinel.FAKE_RASD_PATH, mock.sentinel.FAKE_HOST)

        mock_vsmsvc.MigrateVirtualSystemToHost.assert_called_once_with(
            ComputerSystem=mock_vm.path_.return_value,
            DestinationHost=mock.sentinel.FAKE_HOST,
            MigrationSettingData=mock_vsmsd.GetText_.return_value,
            NewResourceSettingData=mock.sentinel.FAKE_RASD_PATH)

    def _test_live_migrate_vm(self, multiple_planned_vms=False):
        mock_vm = self._get_vm()

        mock_migr_svc = self._conn.Msvm_VirtualSystemMigrationService()[0]
        mock_migr_svc.MigrationServiceListenerIPAddressList = [
            mock.sentinel.remote_ip_addr]

        # patches, call and assertions.
        with mock.patch.multiple(
                self.liveutils,
                _get_vhd_setting_data=mock.DEFAULT,
                _live_migrate_vm=mock.DEFAULT):

            if not multiple_planned_vms:
                self._conn.Msvm_PlannedComputerSystem.return_value = [mock_vm]
                self.liveutils.live_migrate_vm(mock.sentinel.vm_name,
                                               mock.sentinel.host)
                self.liveutils._live_migrate_vm.assert_called_once_with(
                    self._conn, mock_vm, mock_vm,
                    [mock.sentinel.remote_ip_addr],
                    self.liveutils._get_vhd_setting_data.return_value,
                    mock.sentinel.host)
            else:
                self._conn.Msvm_PlannedComputerSystem.return_value = [
                    mock_vm, mock_vm]
                self.assertRaises(exceptions.OSWinException,
                                  self.liveutils.live_migrate_vm,
                                  mock.sentinel.vm_name,
                                  mock.sentinel.host)

    def test_live_migrate_multiple_planned_vms(self):
        self._test_live_migrate_vm(multiple_planned_vms=True)

    def test_live_migrate_single_planned_vm(self):
        self._test_live_migrate_vm()

    @mock.patch.object(vmutils, 'VMUtils')
    @mock.patch.object(livemigrationutils.LiveMigrationUtils, '_get_vm')
    @mock.patch.object(livemigrationutils.LiveMigrationUtils,
                       '_get_ip_address_list')
    @mock.patch.object(livemigrationutils.LiveMigrationUtils,
                       '_update_planned_vm_disk_resources')
    @mock.patch.object(livemigrationutils.LiveMigrationUtils,
                       '_create_planned_vm')
    @mock.patch.object(livemigrationutils.LiveMigrationUtils,
                       '_destroy_existing_planned_vms')
    @mock.patch.object(livemigrationutils.LiveMigrationUtils,
                       '_get_disk_data')
    @mock.patch.object(livemigrationutils, 'platform', create=True)
    def test_create_planned_vm(self, mock_platform, mock_get_disk_data,
                               mock_destroy_existing_planned_vm,
                               mock_create_planned_vm,
                               mock_update_planned_vm_disk_resources,
                               mock_get_ip_address_list, mock_get_vm,
                               mock_cls_vmutils):
        self.liveutils._get_conn_v2.side_effect = [
            mock.sentinel.conn_v2_local, mock.sentinel.conn_v2_remote]
        mock_vm = self._get_vm()
        mock_get_vm.return_value = mock_vm

        mock_get_disk_data.return_value = mock.sentinel.disk_data
        mock_platform.node.return_value = mock.sentinel.dest_host
        mock_get_ip_address_list.return_value = mock.sentinel.ip_address_list

        mock_vsmsvc = self._conn.Msvm_VirtualSystemManagementService()[0]
        mock_vsmsvc.ModifyResourceSettings.return_value = (
            mock.sentinel.res_setting,
            mock.sentinel.job_path,
            self._FAKE_RET_VAL)

        self.liveutils.create_planned_vm(mock_vm.Name,
                                         mock.sentinel.host,
                                         mock.sentinel.disk_path_mapping)

        mock_get_vm.assert_called_once_with(
            mock.sentinel.conn_v2_remote, mock_vm.Name)
        mock_destroy_existing_planned_vm.assert_called_once_with(
            mock.sentinel.conn_v2_local, mock_vm)
        mock_get_ip_address_list.assert_called_once_with(
            mock.sentinel.conn_v2_local, mock.sentinel.dest_host)
        mock_get_disk_data.assert_called_once_with(
            mock_vm.Name,
            mock_cls_vmutils.return_value,
            mock.sentinel.disk_path_mapping)
        mock_create_planned_vm.assert_called_once_with(
            mock.sentinel.conn_v2_local,
            mock.sentinel.conn_v2_remote,
            mock_vm,
            mock.sentinel.ip_address_list,
            mock.sentinel.dest_host)
        mock_update_planned_vm_disk_resources.assert_called_once_with(
            mock.sentinel.conn_v2_local,
            mock_create_planned_vm.return_value,
            mock_vm.Name,
            mock.sentinel.disk_data)

    def _prepare_vm_mocks(self, resource_type, resource_sub_type):
        mock_vm_svc = self._conn.Msvm_VirtualSystemManagementService()[0]
        vm = self._get_vm()
        self._conn.Msvm_PlannedComputerSystem.return_value = [vm]
        mock_vm_svc.DestroySystem.return_value = (mock.sentinel.FAKE_JOB_PATH,
                                                  self._FAKE_RET_VAL)
        mock_vm_svc.ModifyResourceSettings.return_value = (
            None, mock.sentinel.FAKE_JOB_PATH, self._FAKE_RET_VAL)

        sasd = mock.MagicMock()
        other_sasd = mock.MagicMock()
        sasd.ResourceType = resource_type
        sasd.ResourceSubType = resource_sub_type
        sasd.HostResource = [mock.sentinel.FAKE_SASD_RESOURCE]
        sasd.path.return_value.RelPath = mock.sentinel.FAKE_DISK_PATH

        vm_settings = mock.MagicMock()
        vm.associators.return_value = [vm_settings]
        vm_settings.associators.return_value = [sasd, other_sasd]

    def _get_vm(self):
        mock_vm = mock.MagicMock()
        self._conn.Msvm_ComputerSystem.return_value = [mock_vm]
        mock_vm.path_.return_value = mock.sentinel.vm_path
        mock_vm.Name = self._FAKE_VM_NAME
        return mock_vm

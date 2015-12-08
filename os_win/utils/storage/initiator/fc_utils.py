# Copyright 2015 Cloudbase Solutions Srl
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

import sys

if sys.platform == 'win32':
    import wmi

from os_win import _utils

HBA_STATUS_OK = 0
HBA_STATUS_ERROR_MORE_DATA = 7


class FCUtils(object):
    def __init__(self, host='.'):
        wmi_ns = '//%s/root/wmi' % host
        cimv2_ns = '//%s/root/cimv2' % host

        self._conn_wmi = wmi.WMI(moniker=wmi_ns)
        self._conn_cimv2 = wmi.WMI(moniker=cimv2_ns)

    def get_fc_hba_ports(self):
        # TBD: how do we handle offline ports?
        hba_ports_info = []
        hba_ports_attributes = self._conn_wmi.MSFC_FibrePortHBAAttributes()
        for port in hba_ports_attributes:
            hba_port_info = dict(port_name=port.Attributes.PortWWN,
                                 node_name=port.Attributes.NodeWWN,
                                 instance_name=port.InstanceName)
            hba_ports_info.append(hba_port_info)
        return hba_ports_info

    def _get_hba_fcp_info(self, instance_name=None):
        fcps_info = self._conn_wmi.MSFC_HBAFCPInfo()
        if instance_name:
            for fcp_info in fcps_info:
                if fcp_info.InstanceName == instance_name:
                    return fcp_info
        else:
            return fcps_info

    def _get_fcp_target_mappings(self, fcp_info, wwnp):
        entry_count = 10
        more_entries = True
        # import pdb; pdb.set_trace()
        while more_entries:
            (mappings, hba_result,
             entry_count,
             total_entry_count) = fcp_info.GetFcpTargetMapping(wwnp, entry_count)
            # TODO(lpetrut): handle possible HBA results
            more_entries = hba_result == HBA_STATUS_ERROR_MORE_DATA
            entry_count = total_entry_count
        return mappings

    def refresh_hbas(self):
        for hba in self._conn_wmi.MSFC_HBAAdapterMethods():
            hba.RefreshInformation()

    def rescan_disks(self):
        # TODO: find a better way to do this.
        cmd = ("cmd", "/c", "echo", "rescan", "|", "diskpart.exe")
        _utils.execute(*cmd)

    def _get_disk_drive(self, scsi_bus, scsi_target_id, scsi_lun):
        return self._conn_cimv2.Win32_DiskDrive(
            ScsiBus=scsi_bus,
            SCSITargetId=scsi_target_id,
            SCSILogicalUnit=scsi_lun)

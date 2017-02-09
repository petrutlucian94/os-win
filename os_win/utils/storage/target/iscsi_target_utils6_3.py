# Copyright 2017 Cloudbase Solutions Srl
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

from oslo_log import log as logging
from oslo_utils import units

from os_win._i18n import _, _LI
from os_win import constants
from os_win import exceptions
from os_win.utils.storage.target import iscsi_target_utils

LOG = logging.getLogger(__name__)


class ISCSITargetUtils6_3(iscsi_target_utils.ISCSITargetUtils):
    def create_wt_disk(self, vhd_path, wtd_name, size_mb=None):
        size_bytes = size_mb * units.Mi
        try:
            self._conn_wmi.WT_Disk.CreateVhdWTDisk(
                DevicePath=vhd_path,
                Description=wtd_name,
                MaxInternalSize=size_bytes,
                VhdType=constants.VHD_TYPE_DYNAMIC)
        except exceptions.x_wmi as wmi_exc:
            err_msg = _('Failed to create WT Disk. '
                        'VHD path: %(vhd_path)s '
                        'WT disk name: %(wtd_name)s')
            raise exceptions.ISCSITargetWMIException(
                err_msg % dict(vhd_path=vhd_path,
                               wtd_name=wtd_name),
                wmi_exc=wmi_exc)

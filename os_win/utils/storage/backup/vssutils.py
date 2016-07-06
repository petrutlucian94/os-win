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
    from ctypes import wintypes
    kernel32 = ctypes.windll.kernel32
    vssapi = ctypes.windll.vssapi

    from os_win.utils.storage.backup import vss_interfaces as vss_ifaces

from os_win._i18n import _
from os_win import constants
from os_win import exceptions
from os_win.utils import win32utils


class VSSUtils(object):
    def __init__(self):
        self._win32_utils = win32utils.Win32Utils()

    def _run_and_check_output(self, *args, **kwargs):
        kwargs.update(failure_exc=exceptions.Win32VssException,
                      error_on_nonzero_ret_val=True,
                      ret_val_is_err_code=True)
        return self._win32_utils.run_and_check_output(*args, **kwargs)

    def create_backup_components(self):
        p_backup_components = vss_ifaces.pIVssBackupComponents()
        vssapi.CreateVssBackupComponentsInternal(
            ctypes.byref(p_backup_components))
        return p_backup_components

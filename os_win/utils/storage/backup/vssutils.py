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
    vssapi = ctypes.windll.vssapi
    from os_win.utils.storage.backup import vss_interfaces as vss_ifaces

from os_win._i18n import _
from os_win import constants
from os_win import exceptions
from os_win.utils import win32utils
from os_win.utils.storage.backup import vss_constants as vss_const


class VSSBackup(object):
    def __init__(self, select_components=True,
                 backup_type=vss_const.VSS_BT_FULL,
                 writer_classes=None):
        # Note(lpetrut): we may use versioned objects for backup opts.
        self._select_components = select_components
        self._backup_type = backup_type

        self._set_writer_classes(writer_classes)
        self._initialize()

    def _initialize(self):
        p_backup_components = vss_ifaces.pIVssBackupComponents()
        vssapi.CreateVssBackupComponentsInternal(
            ctypes.byref(p_backup_components))
        self._backup_components = p_backup_components

        self._backup_components.InitializeForBackup()
        self._backup_components.SetBackupState(
            bSelectComponents=self._select_components,
            bBackupBootableSystemState=False,
            backupType=self._backup_type,
            bPartialFileSupport=False)
        self._backup_components.EnableWriterClasses(
            rgWriterClassId=self._writer_classes,
            cClassId=len(self._writer_classes))

    def _set_writer_classes(self, writer_classes=None):
        writer_classes = writer_classes or []
        writer_classes = [vss_ifaces.GUID(writer_guid)
                          for writer_guid in writer_classes]
        # This will be an array of GUIDs.
        self._writer_classes = (
            vss_ifaces.GUID * len(writer_classes))(*writer_classes)

    def _get_writer_metadata(self):
        writer_metadata = []
        # Retrieve the metadata for all the writers. Should be called only
        # once for each iVssBackupComponents instance.
        async = self._backup_components.GatherWriterMetadata()
        self._wait_async_job(async)

        wmd_count = self._backup_components.GetWriterMetadataCount()
        for wmd_idx in range(wmd_count):
            (writer_id,
             wmd) = self._backup_components.GetWriterMetadata(wmd_idx)
            writer_metadata.append(wmd)
        return writer_metadata

    def _wait_async_job(self, async, successful_return_values=None):
        # TODO(lpetrut): we probably should add a timeout argument.
        successful_return_values = successful_return_values or []
        successful_return_values.append(vss_const.VSS_S_ASYNC_FINISHED)

        async.Wait()
        hresult = async.QueryStatus()

        if hresult in successful_return_values:
            return
        elif hresult == vss_const.VSS_S_ASYNC_PENDING:
            LOG.debug("The async job is still pending. Waiting...")
        elif hresult == vss_const.VSS_S_ASYNC_CANCELED:
            raise exceptions.VSSJobCanceled()
        else:
            err_msg = _("Async job failed.")
            raise exceptions.VSSComError(err_msg, hresult=hresult.value)

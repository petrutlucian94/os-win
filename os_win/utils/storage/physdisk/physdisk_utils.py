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

import ctypes

from os_win.utils.io import ioutils
from os_win.utils.storage.physdisk import physdisk_struct
from os_win.utils import win32utils


class PhysDiskUtils(object):
    def __init__(self):
        self._win32utils = win32utils.Win32Utils()
        self._ioutils = ioutils.IOUtils()

    def _run_and_check_output(self, *args, **kwargs):
        kwargs['kernel32_lib_func'] = True
        self._win32utils.run_and_check_output(*args, **kwargs)

    def _get_page_83_id_data(self, handle, out_buff_size):
        out_buff = self._ioutils.get_buffer(out_buff_size)

        control_code = physdisk_struct.IOCTL_STORAGE_QUERY_PROPERTY
        query = physdisk_struct.STORAGE_PROPERTY_QUERY()
        query.PropertyId = physdisk_struct.STORAGE_PROPERTY_DEVICE_ID
        query.QueryType = (
            physdisk_struct.STORAGE_QUERY_TYPE_STANDARD_QUERY)

        bytes_returned = self._ioutils.device_io_control(
            handle, control_code=control_code,
            in_buff=query, in_buff_size=ctypes.sizeof(query),
            out_buff=out_buff, out_buff_size=out_buff_size)
        return out_buff, bytes_returned

    def get_scsi_unique_id(self, disk_path):
        desired_access = ioutils.GENERIC_READ | ioutils.GENERIC_WRITE
        share_mode = ioutils.FILE_SHARE_READ | ioutils.FILE_SHARE_WRITE
        creation_disposition = ioutils.OPEN_EXISTING
        handle = self._ioutils.open(
            disk_path,
            desired_access=desired_access,
            share_mode=share_mode,
            creation_disposition=creation_disposition)

        try:
            buff, buff_sz = self._get_page_83_id_data(handle, 8192)
            return self._parse_page_83_data(buff)
        finally:
            self._ioutils.close_handle(handle)

    def _parse_page_83_data(self, buff):
        identifiers = []
        descriptor = ctypes.cast(
            buff, physdisk_struct.PSTORAGE_DEVICE_ID_DESCRIPTOR).contents
        identifiers_count = descriptor.NumberOfIdentifiers
        import pdb; pdb.set_trace()
        identifier_addr = (ctypes.addressof(descriptor) +
                           3 * ctypes.sizeof(ctypes.c_ulong))

        for idx in range(identifiers_count):
            identifier = physdisk_struct.STORAGE_IDENTIFIER.from_address(identifier_addr)
            identifiers.append(identifier)
            identifier_addr += identifier.NextOffset

        return identifiers
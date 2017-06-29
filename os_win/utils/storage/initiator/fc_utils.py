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

import contextlib
import ctypes
import textwrap

from oslo_log import log as logging
import six

from os_win._i18n import _
from os_win import _utils
import os_win.conf
from os_win import exceptions
from os_win.utils.storage import diskutils
from os_win.utils import win32utils
from os_win.utils.winapi import constants as w_const
from os_win.utils.winapi import libs as w_lib
from os_win.utils.winapi.libs import hbaapi as fc_struct

CONF = os_win.conf.CONF

hbaapi = w_lib.get_shared_lib_handle(w_lib.HBAAPI)

LOG = logging.getLogger(__name__)

HBA_STATUS_OK = 0
HBA_STATUS_ERROR_MORE_DATA = 7


class FCUtils(object):
    def __init__(self):
        self._win32_utils = win32utils.Win32Utils()
        self._diskutils = diskutils.DiskUtils()

    def _run_and_check_output(self, *args, **kwargs):
        kwargs['failure_exc'] = exceptions.FCWin32Exception
        return self._win32_utils.run_and_check_output(*args, **kwargs)

    def get_fc_hba_count(self):
        return hbaapi.HBA_GetNumberOfAdapters()

    def _open_adapter_by_name(self, adapter_name):
        handle = self._run_and_check_output(
            hbaapi.HBA_OpenAdapter,
            ctypes.c_char_p(six.b(adapter_name)),
            ret_val_is_err_code=False,
            error_on_nonzero_ret_val=False,
            error_ret_vals=[0])
        return handle

    def _open_adapter_by_wwn(self, adapter_wwn):
        handle = fc_struct.HBA_HANDLE()
        hba_wwn = fc_struct.HBA_WWN()
        hba_wwn.wwn[:] = adapter_wwn

        self._run_and_check_output(
            hbaapi.HBA_OpenAdapterByWWN,
            ctypes.byref(handle),
            hba_wwn)

        return handle

    def _close_adapter(self, hba_handle):
        hbaapi.HBA_CloseAdapter(hba_handle)

    @contextlib.contextmanager
    def _get_hba_handle(self, adapter_name=None, adapter_wwn=None):
        if adapter_name:
            hba_handle = self._open_adapter_by_name(adapter_name)
        elif adapter_wwn:
            hba_handle = self._open_adapter_by_wwn(adapter_wwn)
        else:
            err_msg = _("Could not open HBA adapter. "
                        "No HBA name or WWN was specified")
            raise exceptions.FCException(err_msg)

        try:
            yield hba_handle
        finally:
            self._close_adapter(hba_handle)

    def _get_adapter_name(self, adapter_index):
        buff = (ctypes.c_char * w_const.MAX_ISCSI_HBANAME_LEN)()
        self._run_and_check_output(hbaapi.HBA_GetAdapterName,
                                   ctypes.c_uint32(adapter_index),
                                   buff)

        return buff.value.decode('utf-8')

    def _get_target_mapping(self, hba_handle):
        entry_count = 0
        hba_status = HBA_STATUS_ERROR_MORE_DATA

        while hba_status == HBA_STATUS_ERROR_MORE_DATA:
            mapping = fc_struct.get_target_mapping_struct(entry_count)
            hba_status = self._run_and_check_output(
                hbaapi.HBA_GetFcpTargetMapping,
                hba_handle,
                ctypes.byref(mapping),
                ignored_error_codes=[HBA_STATUS_ERROR_MORE_DATA])
            entry_count = mapping.NumberOfEntries

        return mapping

    def _get_adapter_port_attributes(self, hba_handle, port_index):
        port_attributes = fc_struct.HBA_PortAttributes()

        self._run_and_check_output(
            hbaapi.HBA_GetAdapterPortAttributes,
            hba_handle, port_index,
            ctypes.byref(port_attributes))
        return port_attributes

    def _get_adapter_attributes(self, hba_handle):
        hba_attributes = fc_struct.HBA_AdapterAttributes()

        self._run_and_check_output(
            hbaapi.HBA_GetAdapterAttributes,
            hba_handle, ctypes.byref(hba_attributes))
        return hba_attributes

    def _get_fc_hba_adapter_ports(self, adapter_name):
        hba_ports = []
        with self._get_hba_handle(
                adapter_name=adapter_name) as hba_handle:
            adapter_attributes = self._get_adapter_attributes(hba_handle)
            port_count = adapter_attributes.NumberOfPorts

            for port_index in range(port_count):
                port_attributes = self._get_adapter_port_attributes(
                    hba_handle,
                    port_index)
                wwnn = self._wwn_array_to_hex_str(port_attributes.NodeWWN.wwn)
                wwpn = self._wwn_array_to_hex_str(port_attributes.PortWWN.wwn)

                hba_port_info = dict(node_name=wwnn,
                                     port_name=wwpn)
                hba_ports.append(hba_port_info)
        return hba_ports

    def get_fc_hba_ports(self):
        hba_ports = []

        adapter_count = self.get_fc_hba_count()
        for adapter_index in range(adapter_count):
            # We'll ignore unsupported FC HBA ports.
            try:
                adapter_name = self._get_adapter_name(adapter_index)
            except Exception as exc:
                msg = ("Could not retrieve FC HBA adapter name for "
                       "adapter number: %(adapter_index)s. "
                       "Exception: %(exc)s")
                LOG.warning(msg, dict(adapter_index=adapter_index, exc=exc))
                continue

            try:
                hba_ports += self._get_fc_hba_adapter_ports(adapter_name)
            except Exception as exc:
                msg = ("Could not retrieve FC HBA ports for "
                       "adapter: %(adapter_name)s. "
                       "Exception: %(exc)s")
                LOG.warning(msg, dict(adapter_name=adapter_name, exc=exc))

        return hba_ports

    def _wwn_hex_string_to_array(self, wwn):
        return [int(hex_byte, 16) for hex_byte in textwrap.wrap(wwn, 2)]

    def _wwn_array_to_hex_str(self, wwn):
        return ''.join('{:02X}'.format(b) for b in wwn)

    def get_fc_target_mappings(self, node_wwn):
        mappings = []
        node_wwn = self._wwn_hex_string_to_array(node_wwn)

        with self._get_hba_handle(adapter_wwn=node_wwn) as hba_handle:
            fcp_mappings = self._get_target_mapping(hba_handle)
            for entry in fcp_mappings.Entries:
                wwnn = self._wwn_array_to_hex_str(entry.FcpId.NodeWWN.wwn)
                wwpn = self._wwn_array_to_hex_str(entry.FcpId.PortWWN.wwn)
                mapping = dict(node_name=wwnn,
                               port_name=wwpn,
                               device_name=entry.ScsiId.OSDeviceName,
                               lun=entry.ScsiId.ScsiOSLun)
                mappings.append(mapping)
        return mappings

    @_utils.avoid_blocking_call_decorator
    def refresh_hba_configuration(self):
        hbaapi.HBA_RefreshAdapterConfiguration()

    def _send_scsi_inquiry_v2(self, hba_handle, port_wwn, remote_port_wwn,
                              fcp_lun, cdb_byte1, cdb_byte2):
        resp_buffer_sz = ctypes.c_uint32(256)
        resp_buffer = (ctypes.c_ubyte * resp_buffer_sz.value)()

        sense_buffer_sz = ctypes.c_uint32(256)
        sense_buffer = (ctypes.c_ubyte * sense_buffer_sz.value)()

        scsi_status = ctypes.c_ubyte()

        port_wwn_struct = fc_struct.HBA_WWN()
        port_wwn_struct.wwn[:] = port_wwn

        remote_port_wwn_struct = fc_struct.HBA_WWN()
        remote_port_wwn_struct.wwn[:] = remote_port_wwn

        self._run_and_check_output(
            hbaapi.HBA_ScsiInquiryV2,
            hba_handle,
            port_wwn_struct,
            remote_port_wwn_struct,
            ctypes.c_uint64(fcp_lun),
            ctypes.c_uint8(cdb_byte1),
            ctypes.c_uint8(cdb_byte2),
            ctypes.byref(resp_buffer),
            ctypes.byref(resp_buffer_sz),
            ctypes.byref(scsi_status),
            ctypes.byref(sense_buffer),
            ctypes.byref(sense_buffer_sz))

        return resp_buffer

    def _get_scsi_device_id_vpd(self, hba_handle, port_wwn,
                                remote_port_wwn, fcp_lun):
        cdb_byte1 = 1
        cdb_byte2 = 0x83
        return self._send_scsi_inquiry_v2(hba_handle, port_wwn,
                                          remote_port_wwn, fcp_lun,
                                          cdb_byte1, cdb_byte2)

    def get_scsi_device_identifiers(self, node_wwn, port_wwn,
                                    remote_port_wwn, fcp_lun,
                                    select_supported_identifiers=True):
        node_wwn = self._wwn_hex_string_to_array(node_wwn)
        port_wwn = self._wwn_hex_string_to_array(port_wwn)
        remote_port_wwn = self._wwn_hex_string_to_array(remote_port_wwn)

        with self._get_hba_handle(adapter_wwn=node_wwn) as hba_handle:
            vpd_data = self._get_scsi_device_id_vpd(hba_handle, port_wwn,
                                                    remote_port_wwn, fcp_lun)
            identifiers = self._diskutils._parse_scsi_page_83(
                vpd_data,
                select_supported_identifiers=select_supported_identifiers)
            return identifiers

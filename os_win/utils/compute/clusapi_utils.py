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

DWORD = ctypes.c_ulong

CLUSPROP_SYNTAX_NAME = 262147
CLUSPROP_SYNTAX_ENDMARK = 0
CLUSPROP_SYNTAX_LIST_VALUE_DWORD = 65538

CLUSAPI_GROUP_MOVE_RETURN_TO_SOURCE_NODE_ON_ERROR = 2
CLUSAPI_GROUP_MOVE_QUEUE_ENABLED = 4
CLUSAPI_GROUP_MOVE_HIGH_PRIORITY_START = 8


class ClusApiUtils(object):
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
                    val_type=value.__class__)),
                ('_endmark', DWORD)
            ]

        entry = CLUSPROP_LIST_ENTRY()
        entry.name.syntax = CLUSPROP_SYNTAX_NAME
        entry.name.length = name_len * ctypes.sizeof(ctypes.c_wchar)
        entry.name.value = name

        entry.value.syntax = syntax
        entry.value.length = val_sz
        entry.value.value = value

        entry._endmark = 0

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

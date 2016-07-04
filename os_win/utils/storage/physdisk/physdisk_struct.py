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


STORAGE_IDENTIFIER_CODE_SET = ctypes.c_uint
STORAGE_IDENTIFIER_CODE_SET_BINARY = 1
STORAGE_IDENTIFIER_CODE_SET_ASCII = 2
STORAGE_IDENTIFIER_CODE_SET_UTF8 = 3

STORAGE_IDENTIFIER_TYPE = ctypes.c_uint
STORAGE_IDENTIFIER_TYPE_VENDOR_SPECIFIC = 0
STORAGE_IDENTIFIER_TYPE_VENDOR_ID = 1
STORAGE_IDENTIFIER_TYPE_EUI64 = 2
STORAGE_IDENTIFIER_TYPE_FCPH_NAME = 3
STORAGE_IDENTIFIER_TYPE_SCSI_NAME_STRING = 8

STORAGE_ASSOCIATION_TYPE = ctypes.c_uint
STORAGE_ASSOCIATION_TYPE_DEVICE = 0

STORAGE_PROPERTY_ID = ctypes.c_uint
STORAGE_PROPERTY_DEVICE_ID = 2

STORAGE_QUERY_TYPE = ctypes.c_uint
STORAGE_QUERY_TYPE_STANDARD_QUERY = 0

IOCTL_STORAGE_QUERY_PROPERTY = 0x2d1400


class STORAGE_DEVICE_ID_DESCRIPTOR(ctypes.Structure):
    _fields_ = [("Version", ctypes.c_ulong),
                ("Size", ctypes.c_ulong),
                ("NumberOfIdentifiers", ctypes.c_ulong),
                ("Identifiers", ctypes.c_ubyte)]


class STORAGE_IDENTIFIER(ctypes.Structure):
    _fields_ = [("CodeSet", STORAGE_IDENTIFIER_CODE_SET),
                ("Type", STORAGE_IDENTIFIER_TYPE),
                ("IdentifierSize", ctypes.c_ushort),
                ("NextOffset", ctypes.c_ushort),
                ("Association", STORAGE_ASSOCIATION_TYPE),
                ("Identifier", ctypes.c_ubyte)]


class STORAGE_PROPERTY_QUERY(ctypes.Structure):
    _fields_ = [("PropertyId", STORAGE_PROPERTY_ID),
                ("QueryType", STORAGE_QUERY_TYPE),
                ("AdditionalParameters", ctypes.c_ubyte * 1)]


PSTORAGE_DEVICE_ID_DESCRIPTOR = ctypes.POINTER(STORAGE_DEVICE_ID_DESCRIPTOR)

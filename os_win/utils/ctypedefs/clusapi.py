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
from ctypes import wintypes

clusapi = ctypes.windll.clusapi


clusapi.CancelClusterGroupOperation.argtypes = [
    wintypes.HANDLE,
    wintypes.DWORD
]
clusapi.CancelClusterGroupOperation.restype = wintypes.DWORD

clusapi.CloseCluster.argtypes = [wintypes.HANDLE]
clusapi.CloseCluster.restype = wintypes.BOOL

clusapi.CloseClusterGroup.argtypes = [wintypes.HANDLE]
clusapi.CloseClusterGroup.restype = wintypes.BOOL

clusapi.CloseClusterNode.argtypes = [wintypes.HANDLE]
clusapi.CloseClusterNode.restype = wintypes.BOOL

clusapi.CloseClusterNotifyPort.argtypes = [wintypes.HANDLE]
clusapi.CloseClusterNotifyPort.restype = wintypes.BOOL

clusapi.ClusterGroupControl.argtypes = [
    wintypes.HANDLE,
    wintypes.HANDLE,
    wintypes.DWORD,
    ctypes.c_void_p,
    wintypes.DWORD,
    ctypes.c_void_p,
    wintypes.DWORD,
    ctypes.c_void_p
]
clusapi.ClusterGroupControl.restype = wintypes.DWORD

clusapi.GetClusterGroupState.argtypes = [
    wintypes.HANDLE,
    ctypes.c_void_p,
    ctypes.POINTER(wintypes.DWORD)
]
clusapi.GetClusterGroupState.restype = wintypes.DWORD

clusapi.CreateClusterNotifyPortV2.argtypes = [
    wintypes.HANDLE,
    wintypes.HANDLE,
    ctypes.c_void_p,
    wintypes.DWORD,
    ctypes.POINTER(wintypes.DWORD)
]
clusapi.CreateClusterNotifyPortV2.restype = wintypes.HANDLE

clusapi.GetClusterNotifyV2.argtypes = [
    wintypes.HANDLE,
    ctypes.c_void_p,
    ctypes.c_void_p,
    ctypes.c_void_p,
    ctypes.POINTER(wintypes.DWORD),
    ctypes.c_void_p,
    ctypes.POINTER(wintypes.DWORD),
    ctypes.c_void_p,
    ctypes.POINTER(wintypes.DWORD),
    ctypes.c_void_p,
    ctypes.POINTER(wintypes.DWORD),
    ctypes.c_void_p,
    ctypes.POINTER(wintypes.DWORD),
    wintypes.DWORD
]
clusapi.GetClusterNotifyV2.restype = wintypes.DWORD

clusapi.MoveClusterGroupEx.argtypes = [
    wintypes.HANDLE,
    wintypes.HANDLE,
    wintypes.DWORD,
    ctypes.c_void_p,
    wintypes.DWORD
]
clusapi.MoveClusterGroupEx.restype = wintypes.DWORD

clusapi.OpenCluster.argtypes = [ctypes.c_wchar_p]
clusapi.OpenCluster.restype = wintypes.HANDLE

clusapi.OpenClusterGroup.argtypes = [
    wintypes.HANDLE,
    ctypes.c_void_p
]
clusapi.OpenClusterGroup.restype = wintypes.HANDLE

clusapi.OpenClusterNode.argtypes = [
    wintypes.HANDLE,
    ctypes.c_void_p
]
clusapi.OpenClusterNode.restype = wintypes.HANDLE

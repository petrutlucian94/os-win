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

"""VSS COM interfaces, defined based on the original headers."""

import ctypes
from ctypes import wintypes

import comtypes

BYTE = ctypes.c_byte
BOOL = wintypes.BOOL
UINT = ctypes.c_uint
ULONG = ctypes.c_ulong
LONG = ctypes.c_long
DWORD = wintypes.DWORD
POINTER = ctypes.POINTER
HRESULT = comtypes.HRESULT
BSTR = comtypes.BSTR
LPCWSTR = wintypes.LPCWSTR

COMMETHOD = comtypes.COMMETHOD
helpstring = comtypes.helpstring

CLSID = comtypes.GUID
VSS_ID = comtypes.GUID
VSS_PWSZ = ctypes.c_wchar_p
VSS_TIMESTAMP = ctypes.c_longlong

# enum declarations
VSS_OBJECT_TYPE = UINT
VSS_BACKUP_TYPE = UINT
VSS_COMPONENT_TYPE = UINT
VSS_PROVIDER_TYPE = UINT
VSS_RESTORE_TYPE = UINT
VSS_USAGE_TYPE = UINT
VSS_SOURCE_TYPE = UINT

VSS_SNAPSHOT_STATE = UINT
VSS_WRITER_STATE = UINT
VSS_FILE_RESTORE_STATUS = UINT
VSS_RESTOREMETHOD_ENUM = UINT
VSS_WRITERRESTORE_ENUM = UINT
VSS_RESTORE_TARGET = UINT

NULL_UUID = comtypes.GUID()


class VSS_SNAPSHOT_PROP(ctypes.Structure):
    _fields_ = [
        ('m_SnapshotId', VSS_ID),
        ('m_SnapshotSetId', VSS_ID),
        ('m_lSnapshotsCount', LONG),
        ('m_pwszSnapshotDeviceObject', VSS_PWSZ),
        ('m_pwszOriginalVolumeName', VSS_PWSZ),
        ('m_pwszOriginatingMachine', VSS_PWSZ),
        ('m_pwszServiceMachine', VSS_PWSZ),
        ('m_pwszExposedName', VSS_PWSZ),
        ('m_pwszExposedPath', VSS_PWSZ),
        ('m_ProviderId', VSS_ID),
        ('m_lSnapshotAttributes', LONG),
        ('m_tsCreationTimestamp', VSS_TIMESTAMP),
        ('m_eStatus', VSS_SNAPSHOT_STATE),
    ]


class VSS_PROVIDER_PROP(ctypes.Structure):
    _fields_ = [
        ('m_ProviderId', VSS_ID),
        ('m_pwszProviderName', VSS_PWSZ),
        ('m_eProviderType', VSS_PROVIDER_TYPE),
        ('m_pwszProviderVersion', VSS_PWSZ),
        ('m_ProviderVersionId', VSS_ID),
        ('m_ClassId', CLSID)
    ]


class VSS_OBJECT_UNION(ctypes.Union):
    _fields_ = [
        ('Snap', VSS_SNAPSHOT_PROP),
        ('Prov', VSS_PROVIDER_PROP)
    ]


class VSS_OBJECT_PROP(ctypes.Structure):
    _fields_ = [
        ('Type', VSS_OBJECT_TYPE),
        ('Obj', VSS_OBJECT_UNION)
    ]


class FILETIME(ctypes.Structure):
    _fields_ = [
        ('dwLowDateTime', DWORD),
        ('dwHighDateTime', DWORD)
    ]


class VSS_COMPONENTINFO(ctypes.Structure):
    _fields_ = [
        #  either VSS_CT_DATABASE or VSS_CT_FILEGROUP
        ('type', VSS_COMPONENT_TYPE),
        #  logical path to component
        ('bstrLogicalPath', BSTR),
        #  component name
        ('bstrComponentName', BSTR),
        #  description of component
        ('bstrCaption', BSTR),
        #  icon
        ('pbIcon', POINTER(BYTE)),
        #  icon
        ('cbIcon', UINT),
        #  whether component supplies restore metadata
        ('bRestoreMetadata', BOOL),
        #  whether component needs to be informed if backup was successful
        ('bNotifyOnBackupComplete', BOOL),
        #  is component selectable
        ('bSelectable', BOOL),
        #  is component selectable for restore
        ('bSelectableForRestore', BOOL),
        #  extra attribute flags for the component
        ('dwComponentFlags', DWORD),
        #  # of files in file group
        ('cFileCount', UINT),
        #  # of database files
        ('cDatabases', UINT),
        #  # of log files
        ('cLogFiles', UINT),
        #  # of components that this component depends on
        ('cDependencies', UINT),
    ]

PVSSCOMPONENTINFO = POINTER(VSS_COMPONENTINFO)


class IVssWMDependency(comtypes.IUnknown):
    _iid_ = NULL_UUID
    _methods_ = [
        COMMETHOD(
            [], HRESULT, 'GetWriterId',
            (['out'], POINTER(VSS_ID), 'pWriterId')
        ),
        COMMETHOD(
            [], HRESULT, 'GetLogicalPath',
            (['out'], POINTER(BSTR), 'pbstrLogicalPath')
        ),
        COMMETHOD(
            [], HRESULT, 'GetComponentName',
            (['out'], POINTER(BSTR), 'pbstrComponentName')
        )
    ]


class IVssAsync(comtypes.IUnknown):
    _iid_ = comtypes.GUID("{507C37B4-CF5B-4e95-B0AF-14EB9767467E}")
    _methods_ = [
        COMMETHOD(
            [], HRESULT, 'Cancel'
        ),
        COMMETHOD(
            [], HRESULT, 'Wait',
            (['in', 'optional'], DWORD, 'dwMilliseconds', 0xffffffff)
        ),
        COMMETHOD(
            [], HRESULT, 'QueryStatus',
            (['in', 'out'], POINTER(HRESULT), 'pHrResult'),
            (['in', 'out'], POINTER(UINT), 'pReserved')
        )
    ]


class IVssWMFiledesc(comtypes.IUnknown):
    _iid_ = NULL_UUID
    _methods = [
        COMMETHOD(
            [helpstring('get path to toplevel directory')],
            HRESULT, 'GetPath',
            (['out'], POINTER(BSTR), 'pbstrPath')
        ),
        COMMETHOD(
            [helpstring('get filespec (may include wildcards)')],
            HRESULT, 'GetFilespec',
            (['out'], POINTER(BSTR), 'pbstrFilespec')
        ),
        COMMETHOD(
            [helpstring('is path a directory or root of a tree')],
            HRESULT, 'GetRecursive',
            (['out'], POINTER(BOOL), 'pbRecursive')
        ),
        COMMETHOD(
            [helpstring('alternate location for files')],
            HRESULT, 'GetAlternateLocation',
            (['out'], POINTER(BSTR), 'pbstrAlternateLocation')
        ),
        COMMETHOD(
            [helpstring('backup type')],
            HRESULT, 'GetBackupTypeMask',
            (['out'], POINTER(DWORD), 'pdwTypeMask')
        )
    ]


class IVssWMComponent(comtypes.IUnknown):
    _iid_ = NULL_UUID
    _methods_ = [
        COMMETHOD(
            [helpstring('get component information')],
            HRESULT, 'GetComponentInfo',
            (['out'], POINTER(PVSSCOMPONENTINFO), 'ppInfo')
        ),
        COMMETHOD(
            [helpstring('free component information')],
            HRESULT, 'FreeComponentInfo',
            (['in'], PVSSCOMPONENTINFO, 'pInfo')
        ),
        COMMETHOD(
            [helpstring('obtain a specific file in a file group')],
            HRESULT, 'GetFile',
            (['in'], UINT, 'iFile'),
            (['out'], POINTER(POINTER(IVssWMFiledesc)), 'ppFiledesc')
        ),
        COMMETHOD(
            [helpstring('obtain a specific physical database '
                        'file for a database')],
            HRESULT, 'GetDatabaseFile',
            (['in'], UINT, 'iDBFile'),
            (['out'], POINTER(POINTER(IVssWMFiledesc)), 'ppFiledesc')
        ),
        COMMETHOD(
            [helpstring('obtain a specific physical log file for a database')],
            HRESULT, 'GetDatabaseLogFile',
            (['in'], UINT, 'iDbLogFile'),
            (['out'], POINTER(POINTER(IVssWMFiledesc)), 'ppFiledesc')
        ),
        COMMETHOD(
            [], HRESULT, 'GetDependency',
            (['in'], UINT, 'iDependency'),
            (['out'], POINTER(POINTER(IVssWMDependency)), 'ppDependency')
        )
    ]


class IVssExamineWriterMetadata(comtypes.IUnknown):
    _iid_ = comtypes.GUID("{902fcf7f-b7fd-42f8-81f1-b2e400b1e5bd}")
    _methods_ = [
        COMMETHOD(
            [helpstring('obtain identity of the writer')],
            HRESULT, 'GetIdentity',
            (['out'], POINTER(VSS_ID), 'pidInstance'),
            (['out'], POINTER(VSS_ID), 'pidWriter'),
            (['out'], POINTER(BSTR), 'pbstrWriterName'),
            (['out'], POINTER(VSS_USAGE_TYPE), 'pUsage'),
            (['out'], POINTER(VSS_SOURCE_TYPE), 'pSource')
        ),
        COMMETHOD(
            [helpstring('obtain number of include files, '
                        'exclude files, and components')],
            HRESULT, 'GetFileCounts',
            (['out'], POINTER(UINT), 'pcIncludeFiles'),
            (['out'], POINTER(UINT), 'pcExcludeFiles'),
            (['out'], POINTER(UINT), 'pcComponents')
        ),
        COMMETHOD(
            [helpstring('obtain specific include files')],
            HRESULT, 'GetIncludeFile',
            (['in'], UINT, 'iFile'),
            (['out'], POINTER(POINTER(IVssWMFiledesc)), 'ppFiledesc')
        ),
        COMMETHOD(
            [helpstring('obtain specific exclude files')],
            HRESULT, 'GetExcludeFile',
            (['in'], UINT, 'iFile'),
            (['out'], POINTER(POINTER(IVssWMFiledesc)), 'ppFiledesc')
        ),
        COMMETHOD(
            [helpstring('obtain specific component')],
            HRESULT, 'GetComponent',
            (['in'], UINT, 'iComponent'),
            (['out'], POINTER(POINTER(IVssWMComponent)), 'ppComponent')
        ),
        COMMETHOD(
            [helpstring('obtain restoration method')],
            HRESULT, 'GetRestoreMethod',
            (['out'], POINTER(VSS_RESTOREMETHOD_ENUM), 'pMethod'),
            (['out'], POINTER(BSTR), 'pbstrService'),
            (['out'], POINTER(BSTR), 'pbstrUserProcedure'),
            (['out'], POINTER(VSS_WRITERRESTORE_ENUM), 'pwriterRestore'),
            (['out'], POINTER(BOOL), 'pbRebootRequired'),
            (['out'], POINTER(UINT), 'pcMappings')
        ),
        COMMETHOD(
            [helpstring('obtain a specific alternative location mapping')],
            HRESULT, 'GetAlternateLocationMapping',
            (['in'], UINT, 'iMapping'),
            (['out'], POINTER(POINTER(IVssWMFiledesc)), 'ppFiledesc')
        ),
        COMMETHOD(
            [helpstring('get the backup schema')],
            HRESULT, 'GetBackupSchema',
            (['out'], POINTER(DWORD), 'pdwSchemaMask')
        ),
        COMMETHOD(
            [helpstring('unsupported: obtain reference '
                        'to actual XML document')],
            HRESULT, 'GetDocument',
            (['out'], POINTER(ctypes.c_void_p), 'pDoc')
        ),
        COMMETHOD(
            [helpstring('convert document to a XML string')],
            HRESULT, 'SaveAsXML',
            (['in'], POINTER(BSTR), 'pbstrXML')
        ),
        COMMETHOD(
            [helpstring('load document from an XML string')],
            HRESULT, 'LoadFromXML',
            (['in'], BSTR, 'bstrXML')
        )
    ]


class IVssComponent(comtypes.IUnknown):
    """Backup components interface."""
    _iid_ = comtypes.GUID('{d2c72c96-c121-4518-b627-e5a93d010ead}')
    _methods_ = [
        COMMETHOD(
            [helpstring('obtain logical path of component')],
            HRESULT, 'GetLogicalPath',
            (['out'], POINTER(BSTR), 'pbstrPath')
        ),
        COMMETHOD(
            [helpstring('obtain component type '
                        '(VSS_CT_DATABASE or VSS_CT_FILEGROUP)')],
            HRESULT, 'GetComponentType',
            (['out'], POINTER(VSS_COMPONENT_TYPE), 'pct')
        ),
        COMMETHOD(
            [helpstring('get component name')],
            HRESULT, 'GetComponentName',
            (['out'], POINTER(BSTR), 'pbstrName')
        ),
        COMMETHOD(
            [helpstring('determine whether the component '
                        'was successfully backed up.')],
            HRESULT, 'GetBackupSucceeded',
            (['out'], POINTER(BOOL), 'pbSucceeded')
        ),
        COMMETHOD(
            [helpstring('get altermative location mapping count')],
            HRESULT, 'GetAlternateLocationMappingCount',
            (['out'], POINTER(UINT), 'pcMappings')
        ),
        COMMETHOD(
            [helpstring('get a paraticular alternative location mapping')],
            HRESULT, 'GetAlternateLocationMapping',
            (['in'], UINT, 'iMapping'),
            (['out'], POINTER(POINTER(IVssWMFiledesc)), 'ppFiledesc')
        ),
        COMMETHOD(
            [helpstring('set the backup metadata for a component')],
            HRESULT, 'SetBackupMetadata',
            (['in'], LPCWSTR, 'wszData')
        ),
        COMMETHOD(
            [helpstring('get the backup metadata for a component')],
            HRESULT, 'GetBackupMetadata',
            (['out'], POINTER(BSTR), 'pbstrData')
        ),
        COMMETHOD(
            [helpstring('indicate that only ranges in the '
                        'file are to be backed up')],
            HRESULT, 'AddPartialFile',
            (['in'], LPCWSTR, 'wszPath'),
            (['in'], LPCWSTR, 'wszFilename'),
            (['in'], LPCWSTR, 'wszRanges'),
            (['in'], LPCWSTR, 'wszMetadata')
        ),
        COMMETHOD(
            [helpstring('get count of partial file declarations')],
            HRESULT, 'GetPartialFileCount',
            (['out'], POINTER(UINT), 'pcPartialFiles')
        ),
        COMMETHOD(
            [helpstring('get a partial file declaration')],
            HRESULT, 'GetPartialFile',
            (['in'], UINT, 'iPartialFile'),
            (['out'], POINTER(BSTR), 'pbstrPath'),
            (['out'], POINTER(BSTR), 'pbstrFilename'),
            (['out'], POINTER(BSTR), 'pbstrRange'),
            (['out'], POINTER(BSTR), 'pbstrMetadata')
        ),
        COMMETHOD(
            [helpstring('determine if the component '
                        'is selected to be restored')],
            HRESULT, 'IsSelectedForRestore',
            (['out'], POINTER(BOOL), 'pbSelectedForRestore')
        ),
        COMMETHOD(
            [], HRESULT, 'GetAdditionalRestores',
            (['out'], POINTER(BOOL), 'pbAdditionalRestores')
        ),
        COMMETHOD(
            [helpstring('get count of new target specifications')],
            HRESULT, 'GetNewTargetCount',
            (['out'], POINTER(UINT), 'pcNewTarget')
        ),
        COMMETHOD(
            [], HRESULT, 'GetNewTarget',
            (['in'], UINT, 'iNewTarget'),
            (['out'], POINTER(POINTER(IVssWMFiledesc)), 'ppFiledesc')
        ),
        COMMETHOD(
            [helpstring('add a directed target specification')],
            HRESULT, 'AddDirectedTarget',
            (['in'], LPCWSTR, 'wszSourcePath'),
            (['in'], LPCWSTR, 'wszSourceFilename'),
            (['in'], LPCWSTR, 'wszSourceRangeList'),
            (['in'], LPCWSTR, 'wszDestinationPath'),
            (['in'], LPCWSTR, 'wszDestinationFilename'),
            (['in'], LPCWSTR, 'wszDestinationRangeList')
        ),
        COMMETHOD(
            [helpstring('get count of directed target specifications')],
            HRESULT, 'GetDirectedTargetCount',
            (['out'], POINTER(UINT), 'pcDirectedTarget')
        ),
        COMMETHOD(
            [helpstring('obtain a particular directed target specification')],
            HRESULT, 'GetDirectedTarget',
            (['in'], UINT, 'iDirectedTarget'),
            (['out'], POINTER(BSTR), 'pbstrSourcePath'),
            (['out'], POINTER(BSTR), 'pbstrSourceFileName'),
            (['out'], POINTER(BSTR), 'pbstrSourceRangeList'),
            (['out'], POINTER(BSTR), 'pbstrDestinationPath'),
            (['out'], POINTER(BSTR), 'pbstrDestinationFilename'),
            (['out'], POINTER(BSTR), 'pbstrDestinationRangeList')
        ),
        COMMETHOD(
            [helpstring('set restore metadata associated with the component')],
            HRESULT, 'SetRestoreMetadata',
            (['in'], LPCWSTR, 'wszRestoreMetadata')
        ),
        COMMETHOD(
            [helpstring('obtain restore metadata associated '
                        'with the component')],
            HRESULT, 'GetRestoreMetadata',
            (['out'], POINTER(BSTR), 'pbstrRestoreMetadata')
        ),
        COMMETHOD(
            [helpstring('set the restore target')],
            HRESULT, 'SetRestoreTarget',
            (['in'], VSS_RESTORE_TARGET, 'target')
        ),
        COMMETHOD(
            [helpstring('obtain the restore target')],
            HRESULT, 'GetRestoreTarget',
            (['out'], POINTER(VSS_RESTORE_TARGET), 'pTarget')
        ),
        COMMETHOD(
            [helpstring('set failure message during pre restore event')],
            HRESULT, 'SetPreRestoreFailureMsg',
            (['in'], LPCWSTR, 'wszPreRestoreFailureMsg')
        ),
        COMMETHOD(
            [helpstring('obtain failure message during pre restore event')],
            HRESULT, 'GetPreRestoreFailureMsg',
            (['out'], POINTER(BSTR), 'pbstrPreRestoreFailureMsg')
        ),
        COMMETHOD(
            [helpstring('set the failure message during '
                        'the post restore event')],
            HRESULT, 'SetPostRestoreFailureMsg',
            (['in'], LPCWSTR, 'wszPostRestoreFailureMsg')
        ),
        COMMETHOD(
            [helpstring('obtain the failure message set '
                        'during the post restore event')],
            HRESULT, 'GetPostRestoreFailureMsg',
            (['out'], POINTER(BSTR), 'pbstrPostRestoreFailureMsg')
        ),
        COMMETHOD(
            [helpstring('set the backup stamp of the backup')],
            HRESULT, 'SetBackupStamp',
            (['in'], LPCWSTR, 'wszBackupStamp')
        ),
        COMMETHOD(
            [helpstring('obtain the stamp of the backup')],
            HRESULT, 'GetBackupStamp',
            (['out'], POINTER(BSTR), 'pbstrBackupStamp')
        ),
        COMMETHOD(
            [helpstring('obtain the backup stamp that the differential '
                                 'or incrementalbackup is based on')],
            HRESULT, 'GetPreviousBackupStamp',
            (['out'], POINTER(BSTR), 'pbstrBackupStamp')
        ),
        COMMETHOD(
            [helpstring('obtain backup options for the writer')],
            HRESULT, 'GetBackupOptions',
            (['out'], POINTER(BSTR), 'pbstrBackupOptions')
        ),
        COMMETHOD(
            [helpstring('obtain the restore options')],
            HRESULT, 'GetRestoreOptions',
            (['out'], POINTER(BSTR), 'pbstrRestoreOptions')
        ),
        COMMETHOD(
            [helpstring('obtain count of subcomponents to be restored')],
            HRESULT, 'GetRestoreSubcomponentCount',
            (['out'], POINTER(UINT), 'pcRestoreSubcomponent')
        ),
        COMMETHOD(
            [helpstring('obtain a particular subcomponent to be restored')],
            HRESULT, 'GetRestoreSubcomponent',
            (['in'], UINT, 'iComponent'),
            (['out'], POINTER(BSTR), 'pbstrLogicalPath'),
            (['out'], POINTER(BSTR), 'pbstrComponentName'),
            (['out'], POINTER(BOOL), 'pbRepair')
        ),
        COMMETHOD(
            [helpstring('obtain whether files were successfully restored')],
            HRESULT, 'GetFileRestoreStatus',
            (['out'], POINTER(VSS_FILE_RESTORE_STATUS), 'pStatus')
        ),
        COMMETHOD(
            [helpstring('add differenced files by last modify time')],
            HRESULT, 'AddDifferencedFilesByLastModifyTime',
            (['in'], LPCWSTR, 'wszPath'),
            (['in'], LPCWSTR, 'wszFilespec'),
            (['in'], BOOL, 'bRecursive'),
            (['in'], FILETIME, 'ftLastModifyTime')
        ),
        COMMETHOD(
            [], HRESULT, 'AddDifferencedFilesByLastModifyLSN',
            (['in'], LPCWSTR, 'wszPath'),
            (['in'], LPCWSTR, 'wszFilespec'),
            (['in'], BOOL, 'bRecursive'),
            (['in'], BSTR, 'bstrLsnString')
        ),
        COMMETHOD(
            [], HRESULT, 'GetDifferencedFilesCount',
            (['out'], POINTER(UINT), 'pcDifferencedFiles')
        ),
        COMMETHOD(
            [], HRESULT, 'GetDifferencedFile',
            (['in'], UINT, 'iDifferencedFile'),
            (['out'], POINTER(BSTR), 'pbstrPath'),
            (['out'], POINTER(BSTR), 'pbstrFilespec'),
            (['out'], POINTER(BOOL), 'pbRecursive'),
            (['out'], POINTER(BSTR), 'pbstrLsnString'),
            (['out'], POINTER(FILETIME), 'pftLastModifyTime')
        )
    ]


class IVssWriterComponentsExt(comtypes.IUnknown):
    _iid_ = NULL_UUID
    _methods_ = [
        COMMETHOD(
            [helpstring('get count of components')],
            HRESULT, 'GetComponentCount',
            (['OUT'], POINTER(UINT), 'pcComponents')
        ),
        COMMETHOD(
            [helpstring('get information about the writer')],
            HRESULT, 'GetWriterInfo',
            (['out'], POINTER(VSS_ID), 'pidInstance'),
            (['out'], POINTER(VSS_ID), 'pidWriter')
        ),
        COMMETHOD(
            [helpstring('obtain a specific component')],
            HRESULT, 'GetComponent',
            (['in'], UINT, 'iComponent'),
            (['out'], POINTER(POINTER(IVssComponent)), 'ppComponent')
        )
    ]


class IVssEnumObject(comtypes.IUnknown):
    _iid_ = comtypes.GUID("{AE1C7110-2F60-11d3-8A39-00C04F72D8E3}")
    _methods_ = [
        COMMETHOD(
            [], HRESULT, 'Next',
            (['in'], ULONG, 'celt'),
            (['out'], POINTER(VSS_OBJECT_PROP), 'rgelt'),
            (['out'], POINTER(ULONG), 'pceltFetched')
        ),
        COMMETHOD(
            [], HRESULT, 'Skip',
            (['in'], ULONG, 'celt'),
        ),
        COMMETHOD(
            [], HRESULT, 'Reset',
        )
    ]

IVssEnumObject._methods_.append(
    COMMETHOD(
        [], HRESULT, 'Clone',
        (['in', 'out'], POINTER(POINTER(IVssEnumObject)), 'ppenum')
    )
)


class IVssBackupComponents(comtypes.IUnknown):
    _iid_ = comtypes.GUID("{665c1d5f-c218-414d-a05d-7fef5f9d5c86}")
    _methods_ = [
        COMMETHOD(
            [], HRESULT, 'GetWriterComponentsCount',
            (['out'], POINTER(UINT), 'pcComponents')
        ),
        COMMETHOD(
            [helpstring('obtain a specific writer component')],
            HRESULT, 'GetWriterComponents',
            (['in'], UINT, 'iWriter'),
            (['out'], POINTER(
                POINTER(IVssWriterComponentsExt)), 'ppWriter')
        ),
        COMMETHOD(
            [helpstring('initialize and create BACKUP_COMPONENTS document')],
            HRESULT, 'InitializeForBackup',
            (['in', 'optional'], BSTR, 'bstrXML', None)
        ),
        COMMETHOD(
            [helpstring('set state describing backup')],
            HRESULT, 'SetBackupState',
            (['in'], BOOL, 'bSelectComponents'),
            (['in'], BOOL, 'bBackupBootableSystemState'),
            (['in'], VSS_BACKUP_TYPE, 'backupType'),
            (['in'], BOOL, 'bPartialFileSupport', False)
        ),
        COMMETHOD(
            [], HRESULT, 'InitializeForRestore',
            (['in'], BSTR, 'bstrXML')
        ),
        COMMETHOD(
            [helpstring('set state describing restore')],
            HRESULT, 'SetRestoreState',
            (['in'], VSS_RESTORE_TYPE, 'restoreType')
        ),
        COMMETHOD(
            [helpstring('gather writer metadata')],
            HRESULT, 'GatherWriterMetadata',
            (['out'], POINTER(POINTER(IVssAsync)), 'pAsync')
        ),
        COMMETHOD(
            [helpstring('get count of writers with metadata')],
            HRESULT, 'GetWriterMetadataCount',
            (['out'], POINTER(UINT), 'pcWriters')
        ),
        COMMETHOD(
            [helpstring('get writer metadata for a specific writer')],
            HRESULT, 'GetWriterMetadata',
            (['in'], UINT, 'iWriter'),
            (['out'], POINTER(VSS_ID), 'pidInstance'),
            (['out'], POINTER(
                POINTER(IVssExamineWriterMetadata)), 'ppMetadata')
        ),
        COMMETHOD(
            [helpstring('free writer metadata')],
            HRESULT, 'FreeWriterMetadata'),
        COMMETHOD(
            [helpstring('add a component to the BACKUP_COMPONENTS document')],
            HRESULT, 'AddComponent',
            (['in'], VSS_ID, 'instanceId'),
            (['in'], VSS_ID, 'writerId'),
            (['in'], VSS_COMPONENT_TYPE, 'ct'),
            (['in'], LPCWSTR, 'wszLogicalPath'),
            (['in'], LPCWSTR, 'wszComponentName')
        ),
        COMMETHOD(
            [helpstring('dispatch PrepareForBackup event to writers')],
            HRESULT, 'PrepareForBackup',
            (['out'], POINTER(POINTER(IVssAsync)), 'ppAsync')
        ),
        COMMETHOD(
            [helpstring('abort the backup')],
            HRESULT, 'AbortBackup'),
        COMMETHOD(
            [helpstring('dispatch the Identify event so writers '
                        'can expose their metadata')],
            HRESULT, 'GatherWriterStatus',
            (['out'], POINTER(POINTER(IVssAsync)), 'pAsync')
        ),
        COMMETHOD(
            [helpstring('get count of writers with status')],
            HRESULT, 'GetWriterStatusCount',
            (['out'], POINTER(UINT), 'pcWriters')
        ),
        COMMETHOD(
            [], HRESULT, 'FreeWriterStatus'),
        COMMETHOD(
            [], HRESULT, 'GetWriterStatus',
            (['in'], UINT, 'iWriter'),
            (['out'], POINTER(VSS_ID), 'pidInstance'),
            (['out'], POINTER(VSS_ID), 'pidWriter'),
            (['out'], POINTER(BSTR), 'pbstrWriter'),
            (['out'], POINTER(VSS_WRITER_STATE), 'pnStatus'),
            (['out'], POINTER(HRESULT), 'phResultFailure')
        ),
        COMMETHOD(
            [helpstring('indicate whether backup succeeded on a component')],
            HRESULT, 'SetBackupSucceeded',
            (['in'], VSS_ID, 'instanceId'),
            (['in'], VSS_ID, 'writerId'),
            (['in'], VSS_COMPONENT_TYPE, 'ct'),
            (['in'], LPCWSTR, 'wszLogicalPath'),
            (['in'], LPCWSTR, 'wszComponentName'),
            (['in'], BOOL, 'bSucceded')
        ),
        COMMETHOD(
            [helpstring('set backup options for the writer')],
            HRESULT, 'SetBackupOptions',
            (['in'], VSS_ID, 'writerId'),
            (['in'], VSS_COMPONENT_TYPE, 'ct'),
            (['in'], LPCWSTR, 'wszLogicalPath'),
            (['in'], LPCWSTR, 'wszComponentName'),
            (['in'], LPCWSTR, 'wszBackupOptions')
        ),
        COMMETHOD(
            [helpstring('indicate that a given component is '
                        'selected to be restored')],
            HRESULT, 'SetSelectedForRestore',
            (['in'], VSS_ID, 'writerId'),
            (['in'], VSS_COMPONENT_TYPE, 'ct'),
            (['in'], LPCWSTR, 'wszLogicalPath'),
            (['in'], LPCWSTR, 'wszComponentName'),
            (['in'], BOOL, 'bSelectedForRestore')
        ),
        COMMETHOD(
            [helpstring('set restore options for the writer')],
            HRESULT, 'SetRestoreOptions',
            (['in'], VSS_ID, 'writerId'),
            (['in'], VSS_COMPONENT_TYPE, 'ct'),
            (['in'], LPCWSTR, 'wszLogicalPath'),
            (['in'], LPCWSTR, 'wszComponentName'),
            (['in'], LPCWSTR, 'wszRestoreOptions')
        ),
        COMMETHOD(
            [helpstring('indicate that additional restores will follow')],
            HRESULT, 'SetAdditionalRestores',
            (['in'], VSS_ID, 'writerId'),
            (['in'], VSS_COMPONENT_TYPE, 'ct'),
            (['in'], LPCWSTR, 'wszLogicalPath'),
            (['in'], LPCWSTR, 'wszComponentName'),
            (['in'], BOOL, 'bAdditionalRestores')
        ),
        COMMETHOD(
            [helpstring('set the backup stamp that the differential '
                        'or incremental backup is based on')],
            HRESULT, 'SetPreviousBackupStamp',
            (['in'], VSS_ID, 'writerId'),
            (['in'], VSS_COMPONENT_TYPE, 'ct'),
            (['in'], LPCWSTR, 'wszLogicalPath'),
            (['in'], LPCWSTR, 'wszComponentName'),
            (['in'], LPCWSTR, 'wszPreviousBackupStamp')
        ),
        COMMETHOD(
            [helpstring('save BACKUP_COMPONENTS document as XML string')],
            HRESULT, 'SaveAsXML',
            (['in'], POINTER(BSTR), 'pbstrXML')
        ),
        COMMETHOD(
            [helpstring('signal BackupComplete event to the writers')],
            HRESULT, 'BackupComplete',
            (['out'], POINTER(POINTER(IVssAsync)), 'ppAsync')
        ),
        COMMETHOD(
            [helpstring('add an alternate mapping on restore')],
            HRESULT, 'AddAlternativeLocationMapping',
            (['in'], VSS_ID, 'writerId'),
            (['in'], VSS_COMPONENT_TYPE, 'componentType'),
            (['in'], LPCWSTR, 'wszLogicalPath'),
            (['in'], LPCWSTR, 'wszComponentName'),
            (['in'], LPCWSTR, 'wszPath'),
            (['in'], LPCWSTR, 'wszFilespec'),
            (['in'], BOOL, 'bRecursive'),
            (['in'], LPCWSTR, 'wszDestination')
        ),
        COMMETHOD(
            [helpstring('add a subcomponent to be restored')],
            HRESULT, 'AddRestoreSubcomponent',
            (['in'], VSS_ID, 'writerId'),
            (['in'], VSS_COMPONENT_TYPE, 'componentType'),
            (['in'], LPCWSTR, 'wszLogicalPath'),
            (['in'], LPCWSTR, 'wszComponentName'),
            (['in'], LPCWSTR, 'wszSubComponentLogicalPath'),
            (['in'], LPCWSTR, 'wszSubComponentName'),
            (['in'], BOOL, 'bRepair')
        ),
        COMMETHOD(
            [helpstring('requestor indicates whether files '
                        'were successfully restored')],
            HRESULT, 'SetFileRestoreStatus',
            (['in'], VSS_ID, 'writerId'),
            (['in'], VSS_COMPONENT_TYPE, 'ct'),
            (['in'], LPCWSTR, 'wszLogicalPath'),
            (['in'], LPCWSTR, 'wszComponentName'),
            (['in'], VSS_FILE_RESTORE_STATUS, 'status')
        ),
        COMMETHOD(
            [helpstring('add a new location target for '
                        'a file to be restored')],
            HRESULT, 'AddNewTarget',
            (['in'], VSS_ID, 'writerId'),
            (['in'], VSS_COMPONENT_TYPE, 'ct'),
            (['in'], LPCWSTR, 'wszLogicalPath'),
            (['in'], LPCWSTR, 'wszComponentName'),
            (['in'], LPCWSTR, 'wszPath'),
            (['in'], LPCWSTR, 'wszFileName'),
            (['in'], BOOL, 'bRecursive'),
            (['in'], LPCWSTR, 'wszAlternatePath')
        ),
        COMMETHOD(
            [helpstring('add a new location for the ranges file in case it '
                        'was restored to a different location')],
            HRESULT, 'SetRangesFilePath',
            (['in'], VSS_ID, 'writerId'),
            (['in'], VSS_COMPONENT_TYPE, 'ct'),
            (['in'], LPCWSTR, 'wszLogicalPath'),
            (['in'], LPCWSTR, 'wszComponentName'),
            (['in'], UINT, 'iPartialFile'),
            (['in'], LPCWSTR, 'wszRangesFile')
        ),
        COMMETHOD(
            [helpstring('signal PreRestore event to the writers')],
            HRESULT, 'PreRestore',
            (['out'], POINTER(POINTER(IVssAsync)), 'ppAsync')
        ),
        COMMETHOD(
            [helpstring('signal PostRestore event to the writers')],
            HRESULT, 'PostRestore',
            (['out'], POINTER(POINTER(IVssAsync)), 'ppAsync')
        ),
        COMMETHOD(
            [helpstring('Called to set the context for subsequent '
                        'snapshot-related operations')],
            HRESULT, 'SetContext',
            (['in'], LONG, 'lContext')
        ),
        COMMETHOD(
            [helpstring('start a snapshot set')],
            HRESULT, 'StartSnapshotSet',
            (['out'], POINTER(VSS_ID), 'pSnapshotSetId')
        ),
        COMMETHOD(
            [helpstring('add a volume to a snapshot set')],
            HRESULT, 'AddToSnapshotSet',
            (['in'], VSS_PWSZ, 'pwszVolumeName'),
            (['in'], VSS_ID, 'ProviderId'),
            (['out'], POINTER(VSS_ID), 'pidSnapshot')
        ),
        COMMETHOD(
            [helpstring('create the snapshot set')],
            HRESULT, 'DoSnapshotSet',
            (['out'], POINTER(POINTER(IVssAsync)), 'ppAsync')
        ),
        COMMETHOD(
            [], HRESULT, 'DeleteSnapshots',
            (['in'], VSS_ID, 'SourceObjectId'),
            (['in'], VSS_OBJECT_TYPE, 'eSourceObjectType'),
            (['in'], BOOL, 'bForceDelete'),
            (['in'], POINTER(LONG), 'plDeletedSnapshots'),
            (['in'], POINTER(VSS_ID), 'pNondeletedSnapshotID')
        ),
        COMMETHOD(
            [], HRESULT, 'ImportSnapshots',
            (['out'], POINTER(POINTER(IVssAsync)), 'ppAsync')
        ),
        COMMETHOD(
            [], HRESULT, 'BreakSnapshotSet',
            (['in'], VSS_ID, 'SnapshotSetId')
        ),
        COMMETHOD(
            [], HRESULT, 'GetSnapshotProperties',
            (['in'], VSS_ID, 'SnapshotId'),
            (['out'], POINTER(VSS_SNAPSHOT_PROP), 'pProp')
        ),
        COMMETHOD(
            [], HRESULT, 'Query',
            (['in'], VSS_ID, 'QueriedObjectId'),
            (['in'], VSS_OBJECT_TYPE, 'eQueriedObjectType'),
            (['in'], VSS_OBJECT_TYPE, 'eReturnedObjectsType'),
            (['in'], POINTER(POINTER(IVssEnumObject)), 'ppEnum')
        ),
        COMMETHOD(
            [], HRESULT, 'IsVolumeSupported',
            (['in'], VSS_ID, 'ProviderId'),
            (['in'], VSS_PWSZ, 'pwszVolumeName'),
            (['in'], POINTER(BOOL),
                'pbSupportedByThisProvider')
        ),
        COMMETHOD(
            [], HRESULT, 'DisableWriterClasses',
            (['in'], POINTER(VSS_ID), 'rgWriterClassId'),
            (['in'], UINT, 'cClassId')
        ),
        COMMETHOD(
            [], HRESULT, 'EnableWriterClasses',
            (['in'], POINTER(VSS_ID), 'rgWriterClassId'),
            (['in'], UINT, 'cClassId')
        ),
        COMMETHOD(
            [], HRESULT, 'DisableWriterInstances',
            (['in'], POINTER(VSS_ID), 'rgWriterInstanceId'),
            (['in'], UINT, 'cInstanceId')
        ),
        COMMETHOD(
            [helpstring('called to expose a snapshot')],
            HRESULT, 'ExposeSnapshot',
            (['in'], VSS_ID, 'SnapshotId'),
            (['in'], VSS_PWSZ, 'wszPathFromRoot'),
            (['in'], LONG, 'lAttributes'),
            (['in'], VSS_PWSZ, 'wszExpose'),
            (['out'], POINTER(VSS_PWSZ), 'pwszExposed')
        ),
        COMMETHOD(
            [], HRESULT, 'RevertToSnapshot',
            (['in'], VSS_ID, 'SnapshotId'),
            (['in'], BOOL, 'bForceDismount')
        ),
        COMMETHOD(
            [], HRESULT, 'QueryRevertStatus',
            (['in'], VSS_PWSZ, 'pwszVolume'),
            (['out'], POINTER(POINTER(IVssAsync)), 'ppAsync')
        ),
   ]

pIVssBackupComponents = POINTER(IVssBackupComponents)

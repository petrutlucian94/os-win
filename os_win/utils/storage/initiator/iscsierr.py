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

# Error codes and descriptions, as provided by iscsierr.h
ISDSC_NON_SPECIFIC_ERROR = 0xEFFF0001L
ISDSC_LOGIN_FAILED = 0xEFFF0002L
ISDSC_CONNECTION_FAILED = 0xEFFF0003L
ISDSC_INITIATOR_NODE_ALREADY_EXISTS = 0xEFFF0004L
ISDSC_INITIATOR_NODE_NOT_FOUND = 0xEFFF0005L
ISDSC_TARGET_MOVED_TEMPORARILY = 0xEFFF0006L
ISDSC_TARGET_MOVED_PERMANENTLY = 0xEFFF0007L
ISDSC_INITIATOR_ERROR = 0xEFFF0008L
ISDSC_AUTHENTICATION_FAILURE = 0xEFFF0009L
ISDSC_AUTHORIZATION_FAILURE = 0xEFFF000AL
ISDSC_NOT_FOUND = 0xEFFF000BL
ISDSC_TARGET_REMOVED = 0xEFFF000CL
ISDSC_UNSUPPORTED_VERSION = 0xEFFF000DL
ISDSC_TOO_MANY_CONNECTIONS = 0xEFFF000EL
ISDSC_MISSING_PARAMETER = 0xEFFF000FL
ISDSC_CANT_INCLUDE_IN_SESSION = 0xEFFF0010L
ISDSC_SESSION_TYPE_NOT_SUPPORTED = 0xEFFF0011L
ISDSC_TARGET_ERROR = 0xEFFF0012L
ISDSC_SERVICE_UNAVAILABLE = 0xEFFF0013L
ISDSC_OUT_OF_RESOURCES = 0xEFFF0014L
ISDSC_CONNECTION_ALREADY_EXISTS = 0xEFFF0015L
ISDSC_SESSION_ALREADY_EXISTS = 0xEFFF0016L
ISDSC_INITIATOR_INSTANCE_NOT_FOUND = 0xEFFF0017L
ISDSC_TARGET_ALREADY_EXISTS = 0xEFFF0018L
ISDSC_DRIVER_BUG = 0xEFFF0019L
ISDSC_INVALID_TEXT_KEY = 0xEFFF001AL
ISDSC_INVALID_SENDTARGETS_TEXT = 0xEFFF001BL
ISDSC_INVALID_SESSION_ID = 0xEFFF001CL
ISDSC_SCSI_REQUEST_FAILED = 0xEFFF001DL
ISDSC_TOO_MANY_SESSIONS = 0xEFFF001EL
ISDSC_SESSION_BUSY = 0xEFFF001FL
ISDSC_TARGET_MAPPING_UNAVAILABLE = 0xEFFF0020L
ISDSC_ADDRESS_TYPE_NOT_SUPPORTED = 0xEFFF0021L
ISDSC_LOGON_FAILED = 0xEFFF0022L
ISDSC_SEND_FAILED = 0xEFFF0023L
ISDSC_TRANSPORT_ERROR = 0xEFFF0024L
ISDSC_VERSION_MISMATCH = 0xEFFF0025L
ISDSC_TARGET_MAPPING_OUT_OF_RANGE = 0xEFFF0026L
ISDSC_TARGET_PRESHAREDKEY_UNAVAILABLE = 0xEFFF0027L
ISDSC_TARGET_AUTHINFO_UNAVAILABLE = 0xEFFF0028L
ISDSC_TARGET_NOT_FOUND = 0xEFFF0029L
ISDSC_LOGIN_USER_INFO_BAD = 0xEFFF002AL
ISDSC_TARGET_MAPPING_EXISTS = 0xEFFF002BL
ISDSC_HBA_SECURITY_CACHE_FULL = 0xEFFF002CL
ISDSC_INVALID_PORT_NUMBER = 0xEFFF002DL
ISDSC_OPERATION_NOT_ALL_SUCCESS = 0xAFFF002EL
ISDSC_HBA_SECURITY_CACHE_NOT_SUPPORTED = 0xEFFF002FL
ISDSC_IKE_ID_PAYLOAD_TYPE_NOT_SUPPORTED = 0xEFFF0030L
ISDSC_IKE_ID_PAYLOAD_INCORRECT_SIZE = 0xEFFF0031L
ISDSC_TARGET_PORTAL_ALREADY_EXISTS = 0xEFFF0032L
ISDSC_TARGET_ADDRESS_ALREADY_EXISTS = 0xEFFF0033L
ISDSC_NO_AUTH_INFO_AVAILABLE = 0xEFFF0034L
ISDSC_NO_TUNNEL_OUTER_MODE_ADDRESS = 0xEFFF0035L
ISDSC_CACHE_CORRUPTED = 0xEFFF0036L
ISDSC_REQUEST_NOT_SUPPORTED = 0xEFFF0037L
ISDSC_TARGET_OUT_OF_RESORCES = 0xEFFF0038L
ISDSC_SERVICE_DID_NOT_RESPOND = 0xEFFF0039L
ISDSC_ISNS_SERVER_NOT_FOUND = 0xEFFF003AL
ISDSC_OPERATION_REQUIRES_REBOOT = 0xAFFF003BL
ISDSC_NO_PORTAL_SPECIFIED = 0xEFFF003CL
ISDSC_CANT_REMOVE_LAST_CONNECTION = 0xEFFF003DL
ISDSC_SERVICE_NOT_RUNNING = 0xEFFF003EL
ISDSC_TARGET_ALREADY_LOGGED_IN = 0xEFFF003FL
ISDSC_DEVICE_BUSY_ON_SESSION = 0xEFFF0040L
ISDSC_COULD_NOT_SAVE_PERSISTENT_LOGIN_DATA = 0xEFFF0041L
ISDSC_COULD_NOT_REMOVE_PERSISTENT_LOGIN_DATA = 0xEFFF0042L
ISDSC_PORTAL_NOT_FOUND = 0xEFFF0043L
ISDSC_INITIATOR_NOT_FOUND = 0xEFFF0044L
ISDSC_DISCOVERY_MECHANISM_NOT_FOUND = 0xEFFF0045L
ISDSC_IPSEC_NOT_SUPPORTED_ON_OS = 0xEFFF0046L
ISDSC_PERSISTENT_LOGIN_TIMEOUT = 0xEFFF0047L
ISDSC_SHORT_CHAP_SECRET = 0xAFFF0048L
ISDSC_EVALUATION_PEROID_EXPIRED = 0xEFFF0049L
ISDSC_INVALID_CHAP_SECRET = 0xEFFF004AL
ISDSC_INVALID_TARGET_CHAP_SECRET = 0xEFFF004BL
ISDSC_INVALID_INITIATOR_CHAP_SECRET = 0xEFFF004CL
ISDSC_INVALID_CHAP_USER_NAME = 0xEFFF004DL
ISDSC_INVALID_LOGON_AUTH_TYPE = 0xEFFF004EL
ISDSC_INVALID_TARGET_MAPPING = 0xEFFF004FL
ISDSC_INVALID_TARGET_ID = 0xEFFF0050L
ISDSC_INVALID_ISCSI_NAME = 0xEFFF0051L
ISDSC_INCOMPATIBLE_ISNS_VERSION = 0xEFFF0052L
ISDSC_FAILED_TO_CONFIGURE_IPSEC = 0xEFFF0053L
ISDSC_BUFFER_TOO_SMALL = 0xEFFF0054L
ISDSC_INVALID_LOAD_BALANCE_POLICY = 0xEFFF0055L
ISDSC_INVALID_PARAMETER = 0xEFFF0056L
ISDSC_DUPLICATE_PATH_SPECIFIED = 0xEFFF0057L
ISDSC_PATH_COUNT_MISMATCH = 0xEFFF0058L
ISDSC_INVALID_PATH_ID = 0xEFFF0059L
ISDSC_MULTIPLE_PRIMARY_PATHS_SPECIFIED = 0xEFFF005AL
ISDSC_NO_PRIMARY_PATH_SPECIFIED = 0xEFFF005BL
ISDSC_DEVICE_ALREADY_PERSISTENTLY_BOUND = 0xEFFF005CL
ISDSC_DEVICE_NOT_FOUND = 0xEFFF005DL
ISDSC_DEVICE_NOT_ISCSI_OR_PERSISTENT = 0xEFFF005EL
ISDSC_DNS_NAME_UNRESOLVED = 0xEFFF005FL
ISDSC_NO_CONNECTION_AVAILABLE = 0xEFFF0060L
ISDSC_LB_POLICY_NOT_SUPPORTED = 0xEFFF0061L
ISDSC_REMOVE_CONNECTION_IN_PROGRESS = 0xEFFF0062L
ISDSC_INVALID_CONNECTION_ID = 0xEFFF0063L
ISDSC_CANNOT_REMOVE_LEADING_CONNECTION = 0xEFFF0064L
ISDSC_RESTRICTED_BY_GROUP_POLICY = 0xEFFF0065L
ISDSC_ISNS_FIREWALL_BLOCKED = 0xEFFF0066L
ISDSC_FAILURE_TO_PERSIST_LB_POLICY = 0xEFFF0067L
ISDSC_INVALID_HOST = 0xEFFF0068L

err_msg_dict = {
    ISDSC_NON_SPECIFIC_ERROR: 'A non specific error occurred.',
    ISDSC_LOGIN_FAILED: 'Login Failed.',
    ISDSC_CONNECTION_FAILED: 'Connection Failed.',
    ISDSC_INITIATOR_NODE_ALREADY_EXISTS: 'Initiator Node Already Exists.',
    ISDSC_INITIATOR_NODE_NOT_FOUND: 'Initiator Node Does Not Exist.',
    ISDSC_TARGET_MOVED_TEMPORARILY: 'Target Moved Temporarily.',
    ISDSC_TARGET_MOVED_PERMANENTLY: 'Target Moved Permanently.',
    ISDSC_INITIATOR_ERROR: 'Initiator Error.',
    ISDSC_AUTHENTICATION_FAILURE: 'Authentication Failure.',
    ISDSC_AUTHORIZATION_FAILURE: 'Authorization Failure.',
    ISDSC_NOT_FOUND: 'Not Found.',
    ISDSC_TARGET_REMOVED: 'Target Removed.',
    ISDSC_UNSUPPORTED_VERSION: 'Unsupported Version.',
    ISDSC_TOO_MANY_CONNECTIONS: 'Too many Connections.',
    ISDSC_MISSING_PARAMETER: 'Missing Parameter.',
    ISDSC_CANT_INCLUDE_IN_SESSION: 'Can not include in session.',
    ISDSC_SESSION_TYPE_NOT_SUPPORTED: 'Session type not supported.',
    ISDSC_TARGET_ERROR: 'Target Error.',
    ISDSC_SERVICE_UNAVAILABLE: 'Service Unavailable.',
    ISDSC_OUT_OF_RESOURCES: 'Out of Resources.',
    ISDSC_CONNECTION_ALREADY_EXISTS: 'Connections already exist on initiator '
                                     'node.',
    ISDSC_SESSION_ALREADY_EXISTS: 'Session Already Exists.',
    ISDSC_INITIATOR_INSTANCE_NOT_FOUND: 'Initiator Instance Does Not Exist.',
    ISDSC_TARGET_ALREADY_EXISTS: 'Target Already Exists.',
    ISDSC_DRIVER_BUG: 'The iscsi driver implementation did not complete an '
                      'operation correctly.',
    ISDSC_INVALID_TEXT_KEY: 'An invalid key text was encountered.',
    ISDSC_INVALID_SENDTARGETS_TEXT: 'Invalid SendTargets response '
                                    'text was encountered.',
    ISDSC_INVALID_SESSION_ID: 'Invalid Session Id.',
    ISDSC_SCSI_REQUEST_FAILED: 'The scsi request failed.',
    ISDSC_TOO_MANY_SESSIONS: 'Exceeded max sessions for this initiator.',
    ISDSC_SESSION_BUSY: 'Session is busy since a request is '
                        'already in progress.',
    ISDSC_TARGET_MAPPING_UNAVAILABLE: 'The target mapping requested '
                                      'is not available.',
    ISDSC_ADDRESS_TYPE_NOT_SUPPORTED: 'The Target Address type given '
                                      'is not supported.',
    ISDSC_LOGON_FAILED: 'Logon Failed.',
    ISDSC_SEND_FAILED: 'TCP Send Failed.',
    ISDSC_TRANSPORT_ERROR: 'TCP Transport Error',
    ISDSC_VERSION_MISMATCH: 'iSCSI Version Mismatch',
    ISDSC_TARGET_MAPPING_OUT_OF_RANGE: 'The Target Mapping Address passed '
                                       'is out of range for the '
                                       'adapter configuration.',
    ISDSC_TARGET_PRESHAREDKEY_UNAVAILABLE: 'The preshared key for the target '
                                           'or IKE identification payload '
                                           'is not available.',
    ISDSC_TARGET_AUTHINFO_UNAVAILABLE: 'The authentication information for '
                                       'the target is not available.',
    ISDSC_TARGET_NOT_FOUND: 'The target name is not found or is '
                            'marked as hidden from login.',
    ISDSC_LOGIN_USER_INFO_BAD: 'One or more parameters specified in '
                               'LoginTargetIN structure is invalid.',
    ISDSC_TARGET_MAPPING_EXISTS: 'Given target mapping already exists.',
    ISDSC_HBA_SECURITY_CACHE_FULL: 'The HBA security information cache '
                                   'is full.',
    ISDSC_INVALID_PORT_NUMBER: 'The port number passed is not valid '
                               'for the initiator.',
    ISDSC_OPERATION_NOT_ALL_SUCCESS: 'The operation was not successful for '
                                     'all initiators or discovery methods.',
    ISDSC_HBA_SECURITY_CACHE_NOT_SUPPORTED: 'The HBA security information '
                                            'cache is not supported by '
                                            'this adapter.',
    ISDSC_IKE_ID_PAYLOAD_TYPE_NOT_SUPPORTED: 'The IKE id payload type '
                                             'specified is not supported.',
    ISDSC_IKE_ID_PAYLOAD_INCORRECT_SIZE: 'The IKE id payload size specified '
                                         'is not correct.',
    ISDSC_TARGET_PORTAL_ALREADY_EXISTS: 'Target Portal Structure '
                                        'Already Exists.',
    ISDSC_TARGET_ADDRESS_ALREADY_EXISTS: 'Target Address Structure '
                                         'Already Exists.',
    ISDSC_NO_AUTH_INFO_AVAILABLE: 'There is no IKE authentication '
                                  'information available.',
    ISDSC_NO_TUNNEL_OUTER_MODE_ADDRESS: 'There is no tunnel mode outer '
                                        'address specified.',
    ISDSC_CACHE_CORRUPTED: 'Authentication or tunnel '
                           'address cache is corrupted.',
    ISDSC_REQUEST_NOT_SUPPORTED: 'The request or operation '
                                 'is not supported.',
    ISDSC_TARGET_OUT_OF_RESORCES: 'The target does not have enough '
                                  'resources to process the given request.',
    ISDSC_SERVICE_DID_NOT_RESPOND: 'The initiator service did '
                                   'not respond to the request sent '
                                   'by the driver.',
    ISDSC_ISNS_SERVER_NOT_FOUND: 'The Internet Storage Name Server (iSNS) '
                                 'server was not found or is unavailable.',
    ISDSC_OPERATION_REQUIRES_REBOOT: 'The operation was successful but '
                                     'requires a driver reload or reboot '
                                     'to become effective.',
    ISDSC_NO_PORTAL_SPECIFIED: 'There is no target portal available '
                               'to complete the login.',
    ISDSC_CANT_REMOVE_LAST_CONNECTION: 'Cannot remove the last '
                                       'connection for a session.',
    ISDSC_SERVICE_NOT_RUNNING: 'The Microsoft iSCSI initiator '
                               'service has not been started.',
    ISDSC_TARGET_ALREADY_LOGGED_IN: 'The target has already been'
                                    'logged in via an iSCSI session.',
    ISDSC_DEVICE_BUSY_ON_SESSION: 'The session cannot be logged out '
                                  'since a device on that session is '
                                  'currently being used.',
    ISDSC_COULD_NOT_SAVE_PERSISTENT_LOGIN_DATA: 'Failed to save persistent '
                                                'login information.',
    ISDSC_COULD_NOT_REMOVE_PERSISTENT_LOGIN_DATA: 'Failed to remove '
                                                  'persistent login '
                                                  'information.',
    ISDSC_PORTAL_NOT_FOUND: 'The specified portal was not found.',
    ISDSC_INITIATOR_NOT_FOUND: 'The specified initiator name was not found.',
    ISDSC_DISCOVERY_MECHANISM_NOT_FOUND: 'The specified discovery '
                                         'mechanism was not found.',
    ISDSC_IPSEC_NOT_SUPPORTED_ON_OS: 'iSCSI does not support IPSEC '
                                     'for this version of the OS.',
    ISDSC_PERSISTENT_LOGIN_TIMEOUT: 'The iSCSI service timed out waiting '
                                    'for all persistent logins to complete.',
    ISDSC_SHORT_CHAP_SECRET: 'The specified CHAP secret is less than '
                             '96 bits and will not be usable for '
                             'authenticating over non ipsec connections.',
    ISDSC_EVALUATION_PEROID_EXPIRED: 'The evaluation period for the '
                                     'iSCSI initiator service has expired.',
    ISDSC_INVALID_CHAP_SECRET: 'CHAP secret given does not conform '
                               'to the standard. Please see system '
                               'event log for more information.',
    ISDSC_INVALID_TARGET_CHAP_SECRET: 'Target CHAP secret given is invalid. '
                                      'Maximum size of CHAP secret is 16 '
                                      'bytes. Minimum size is 12 bytes if '
                                      'IPSec is not used.',
    ISDSC_INVALID_INITIATOR_CHAP_SECRET: 'Initiator CHAP secret given is '
                                         'invalid. Maximum size of CHAP '
                                         'secret is 16 bytes. Minimum size '
                                         'is 12 bytes if IPSec is not used.',
    ISDSC_INVALID_CHAP_USER_NAME: 'CHAP Username given is invalid.',
    ISDSC_INVALID_LOGON_AUTH_TYPE: 'Logon Authentication type '
                                   'given is invalid.',
    ISDSC_INVALID_TARGET_MAPPING: 'Target Mapping information '
                                   'given is invalid.',
    ISDSC_INVALID_TARGET_ID: 'Target Id given in Target Mapping is invalid.',
    ISDSC_INVALID_ISCSI_NAME: 'The iSCSI name specified contains '
                              'invalid characters or is too long.',
    ISDSC_INCOMPATIBLE_ISNS_VERSION: 'The version number returned from '
                                     'the Internet Storage Name Server (iSNS) '
                                     'server is not compatible with this '
                                     'version of the iSNS client.',
    ISDSC_FAILED_TO_CONFIGURE_IPSEC: 'Initiator failed to configure IPSec for '
                                     'the given connection. This could be '
                                     'because of low resources.',
    ISDSC_BUFFER_TOO_SMALL: 'The buffer given for processing '
                            'the request is too small.',
    ISDSC_INVALID_LOAD_BALANCE_POLICY: 'The given Load Balance '
                                       'policy is not recognized '
                                       'by iScsi initiator.',
    ISDSC_INVALID_PARAMETER: 'One or more paramaters '
                             'specified is not valid.',
    ISDSC_DUPLICATE_PATH_SPECIFIED: 'Duplicate PathIds were '
                                    'specified in the call to '
                                    'set Load Balance Policy.',
    ISDSC_PATH_COUNT_MISMATCH: 'Number of paths specified in '
                               'Set Load Balance Policy does not '
                               'match the number of paths to the target.',
    ISDSC_INVALID_PATH_ID: 'Path Id specified in the call to '
                           'set Load Balance Policy is not valid',
    ISDSC_MULTIPLE_PRIMARY_PATHS_SPECIFIED: 'Multiple primary paths '
                                            'specified when only one '
                                            'primary path is expected.',
    ISDSC_NO_PRIMARY_PATH_SPECIFIED: 'No primary path specified when '
                                     'at least one is expected.',
    ISDSC_DEVICE_ALREADY_PERSISTENTLY_BOUND: 'Device is already a '
                                             'persistently bound device.',
    ISDSC_DEVICE_NOT_FOUND: 'Device was not found.',
    ISDSC_DEVICE_NOT_ISCSI_OR_PERSISTENT: 'The device specified does not '
                                          'originate from an iSCSI disk '
                                          'or a persistent iSCSI login.',
    ISDSC_DNS_NAME_UNRESOLVED: 'The DNS name specified was not resolved.',
    ISDSC_NO_CONNECTION_AVAILABLE: 'There is no connection available '
                                   'in the iSCSI session to '
                                   'process the request.',
    ISDSC_LB_POLICY_NOT_SUPPORTED: 'The given Load Balance '
                                   'policy is not supported.',
    ISDSC_REMOVE_CONNECTION_IN_PROGRESS: 'A remove connection request is '
                                         'already in progress for '
                                         'this session.',
    ISDSC_INVALID_CONNECTION_ID: 'Given connection was not '
                                 'found in the session.',
    ISDSC_CANNOT_REMOVE_LEADING_CONNECTION: 'The leading connection in '
                                            'the session cannot be removed.',
    ISDSC_RESTRICTED_BY_GROUP_POLICY: 'The operation cannot be performed '
                                      'since it does not conform with '
                                      'the group policy assigned to '
                                      'this computer.',
    ISDSC_ISNS_FIREWALL_BLOCKED: 'The operation cannot be performed since '
                                 'the Internet Storage Name Server '
                                 '(iSNS) firewall exception has '
                                 'not been enabled.',
    ISDSC_FAILURE_TO_PERSIST_LB_POLICY: 'Failed to persist load '
                                        'balancing policy parameters.',
    ISDSC_INVALID_HOST: 'The name could not be resolved to an IP Address.',
}

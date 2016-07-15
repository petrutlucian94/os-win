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

# VSS backup type
VSS_BT_UNDEFINED     = 0
VSS_BT_FULL          = 1
VSS_BT_INCREMENTAL   = 2
VSS_BT_DIFFERENTIAL  = 3
VSS_BT_LOG           = 4
VSS_BT_COPY          = 5
VSS_BT_OTHER         = 6

HV_WRITER_GUID = '{66841cd4-6ded-4f4b-8f17-fd23f8ddc3de}'

VSS_S_ASYNC_PENDING = 0x00042309
VSS_S_ASYNC_FINISHED = 0x0004230A
VSS_S_ASYNC_CANCELLED = 0x0004230B

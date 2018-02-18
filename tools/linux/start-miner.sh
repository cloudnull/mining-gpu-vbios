#!/usr/bin/env bash

# Mining start script. Change the user options to meet the needs of your rig.
#
# Copyright (C) 2018  Kevin Carter
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# USER OPTIONS
export USER_ETH_ADDRESS="0x9242fD08644595bC02f95DAf351AdF84f2B273eA"
export USER_RIG_NAME="txrig2"
export USER_STRATUM_URL="us1.ethermine.org:4444"
export USER_STRATUM_URL_FAILOVER="us2.ethermine.org:4444"

# GPU OPTIONS
export GPU_FORCE_64BIT_PTR=1
export GPU_MAX_HEAP_SIZE=100
export GPU_USE_SYNC_OBJECTS=1
export GPU_MAX_ALLOC_PERCENT=100
export GPU_SINGLE_ALLOC_PERCENT=100

pushd /opt/mining/
  /opt/mining/ethminer -HWMON \
                       --report-hashrate \
                       --farm-recheck 350 \
                       --stratum ${USER_STRATUM_URL} \
                       --stratum-failover ${USER_STRATUM_URL_FAILOVER} \
                       --stratum-protocol 0 \
                       --opencl-platform 0 \
                       --opencl \
                       --cl-kernel 0 \
                       --userpass ${USER_ETH_ADDRESS}.${USER_RIG_NAME}
popd

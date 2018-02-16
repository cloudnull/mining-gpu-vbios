#!/usr/bin/env bash

# USER OPTIONS
export USER_ETH_ADDRESS="0x9242fD08644595bC02f95DAf351AdF84f2B273eA"
export USER_RIG_NAME="txrig1"
export USER_STRATUM_URL="us1.ethermine.org:4444"
export USER_STRATUM_URL_FAILOVER="us2.ethermine.org:4444"

# GPU OPTIONS
export GPU_FORCE_64BIT_PTR=1
export GPU_MAX_HEAP_SIZE=100
export GPU_USE_SYNC_OBJECTS=1
export GPU_MAX_ALLOC_PERCENT=100
export GPU_SINGLE_ALLOC_PERCENT=100

pushd /opt/mining/
  /opt/mining/ethminer -RH \
                       -HWMON \
                       --farm-recheck 200 \
                       --stratum ${USER_STRATUM_URL} \
                       --stratum-failover ${USER_STRATUM_URL_FAILOVER} \
                       --stratum-protocol 0 \
                       --opencl-platform 0 \
                       --opencl \
                       --cl-kernel 0 \
                       -O ${USER_ETH_ADDRESS}.${USER_RIG_NAME}
popd

#!/usr/bin/env bash

# Force reboot. Useful if the miner locks up, becomes defunct or, a zombie
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

echo "1" > /proc/sys/kernel/sysrq
echo "b" > /proc/sysrq-trigger

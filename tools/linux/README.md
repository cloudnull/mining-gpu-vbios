# Linux based mining tools

These tools make the assumption they've been copied to the `/opt/mining`
directory.

## Installation

Install your appropriate miner into the `/opt/mining` directory. In general,
when mining ETH, I use https://github.com/ethereum-mining/ethminer/releases.

## When running on AMD (Ryzen)

* Disable IOMMU in the BIOS and add `iommu=soft` to the kernel command line.

* Run the following command ``echo rcu_nocbs=0-$(($(nproc)-1))`` and amend the
output to the kernel command line. Requires Kernel 4.13+

* Disable C6 in the BIOS and limit the available c-states by appending
`processor.max_cstate=1` to the kernel command line.

* Disable ASLR by running the following command `echo 0 > /proc/sys/kernel/randomize_va_space`. This can be made permanent via sysctl.

### Using the systemd service Unit

Copy the ethminer.service file into `/etc/systemd/system/` then reload the
systemd daemon `systemctl daemon-reload`. Once added into the system enable
the systemd unit `systemctl enable ethminer.service`. To start mining
run `systemctl start ethminer.service`. With the unit installed and enabled
it will automatically start on system boot.

### Force rebooting

If the host machine becomes unresponsive or if `ethminer` locks up resulting in
in a zombie process you may need to hard reboot the machine. If you do need to
hard reboot and you're not able to hard reboot using the power button the
`force-reboot.sh` script can be used to cold cycle the linux server. If you have
ethminer setup using the above systemd service unit, the miner will be back
online just as soon as it reboots.

### ATIFLASH

This program was lifted from https://github.com/d13g0s0uz4/atiflash

# Linux based mining tools

These tools make the assumption they've been copied to the `/opt/mining`
directory.

## Installation

Install your appropriate miner into the `/opt/mining` directory. In general,
when mining ETH, I use https://github.com/ethereum-mining/ethminer/releases.

You can find the claymore miner here, https://bitcointalk.org/index.php?topic=1433925.0

## When running on AMD (Ryzen)

* Disable IOMMU in the BIOS and add `iommu=soft` to the kernel command line.

* Run the following command ``echo rcu_nocbs=0-$(($(nproc)-1))`` and amend the
  output to the kernel command line. Requires Kernel 4.13+

* Disable C6 in the BIOS and limit the available c-states by appending
  `processor.max_cstate=1` to the kernel command line.

* If using AMD GPUs, enable large page sizes by appending
  `amdgpu.vm_fragment_size=9` to the kernel command line.

* Disable ASLR by running the following command
  `sysctl -w kernel.randomize_va_space=0 | tee -a /etc/sysctl.d/10-kernel-randomize-va-space.conf`.

* Update grub `update-grub2` and reboot `shutdown -r now`

### Using the systemd service Unit

Copy the ethminer.service file into `/etc/systemd/system/` then reload the
systemd daemon `systemctl daemon-reload`. Once added into the system enable
the systemd unit `systemctl enable ethminer.service`. To start mining, create
a symlink in the mining directory to the mining script being used, example
`ln -s start-claymore.sh start-miner.sh` then run
`systemctl start ethminer.service`.

If using the claymore miner, make sure the library `libcurl` is installed.
On Ubuntu this can be done like so `apt install libcurl3`.

With the unit installed and enabled it will automatically start on system boot.

### Force rebooting

If the host machine becomes unresponsive or if `ethminer` locks up resulting in
in a zombie process you may need to hard reboot the machine. If you do need to
hard reboot and you're not able to hard reboot using the power button the
`force-reboot.sh` script can be used to cold cycle the linux server. If you have
ethminer setup using the above systemd service unit, the miner will be back
online just as soon as it reboots.

### ATIFLASH

This program was lifted from https://github.com/d13g0s0uz4/atiflash

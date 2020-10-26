#!/usr/bin/env python3.7
#
# Backup script written in Python using ZFS and SSH.
#
# \author sebhtml
#

import libzfs_core
import datetime
import subprocess
import sys

#
#   +----------+               +---------+
#   |          |               |         |
#   | atlantis |  ---------->  | pikachu |
#   |          |               |         |
#   +----------+               +---------+
#
#    ZFS SEND        SSH         ZFS RECV
#
#

#  atlantis:
#      * AMD Ryzen 2600
#      * 8 GB ECC
#      * 1 Toshiba NVMe 1 TB
#      * 4 x Seagate IronWolf 4 TB
#      * ASRock Fatal1ty
#      * Fractal Design Node 304
#      * Gigabit Ethernet
#      * https://ca.pcpartpicker.com/user/sebhtml/saved/#view=nGkJf7

#  pikachu:
#      * Raspberry Pi 4 Model B Rev 1.1
#      * Quad core Cortex-A72 (ARM v8) 64-bit SoC
#      * 4GB LPDDR4-3200 SDRAM
#      * Gigabit Ethernet
#      * SATA-over-USB-3.0
#      * 1 x Seagate Barracuda 4 TB
#      * https://www.raspberrypi.org/products/raspberry-pi-4-model-b/specifications/?resellerType=home

def make_iso_date():
	tz = datetime.timezone.utc
	now = datetime.datetime.now(tz)
	iso_date = now.isoformat()
	# The + in a ISO-8601 date is a forbidden character in a ZFS snapshot name
	# Since +0 and -0 does the same thing, do that.
	iso_date = iso_date.replace("+", "-")
	return iso_date

def make_snapshot_name(pool_name, iso_date):
	format_string = "{}@{}"
	return format_string.format(pool_name, iso_date)

def make_snapshot(snapshot_name):
	#         -r      Recursively create snapshots of all descendent datasets
	argv = ["zfs", "snapshot", "-r", snapshot_name]
	subprocess.run(argv)

def get_last_remote_snapshot(backup_server_user, backup_server_fqdn):
	command = [
		"ssh", "-l", backup_server_user, backup_server_fqdn,  # SSH part
		"zfs list -t snapshot -d 1 -o name -p|tail -n1"
		]
	result = subprocess.run(command, capture_output=True)
	output = result.stdout
	snapshot_name = output.strip()
	return snapshot_name

def send_snapshot(backup_server_user, backup_server_fqdn, snapshot_name, pool_name):
	# Idea: send | pv | recv

	send_command = [
		# -R, --replicate Generate a replication stream package
		"zfs", "send", "-R", snapshot_name]
	send_process = subprocess.Popen(send_command,
		stdin  = None,
		stdout = subprocess.PIPE,
		stderr = sys.stderr)

	speedometer_command = ["pv"]
	speedometer_process = subprocess.Popen(speedometer_command,
		stdin  = send_process.stdout,
		stdout = subprocess.PIPE,
		stderr = sys.stderr)

	recv_command = [
		"ssh", "-l", backup_server_user, backup_server_fqdn,  # SSH part
		#          -F      Force a rollback of the file system to the most recent
		"zfs", "recv", "-F", pool_name                  # ZFS part
		]
	recv_process = subprocess.Popen(recv_command,
		stdin  = speedometer_process.stdout,
		stdout = subprocess.PIPE,
		stderr = sys.stderr)
	recv_process.wait()

def main():
	pool_name = "tank"
	backup_server_user = "root"
	backup_server_fqdn = "pikachu.domain"

	iso_date = make_iso_date()
	snapshot_name = make_snapshot_name(pool_name, iso_date)
	#print("snapshot_name: {}".format(snapshot_name))

	# libzfs_core does not seem to work as documented
	#libzfs_core.lzc_snapshot(snapshot_name)

	make_snapshot(snapshot_name)

	send_snapshot(backup_server_user, backup_server_fqdn, snapshot_name, pool_name)

# zfs list -t snapshot|grep tank@

if __name__ == "__main__":
	main()


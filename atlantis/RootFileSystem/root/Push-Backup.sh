#!/usr/local/bin/bash

log_file=/tank/samba/Informatique/Atlantis/Backup-Logs/`date -Iseconds | sed 's/:/_/g'`.xml

function run_commands
{
	echo "<isoDate>"
	date -Iseconds
	echo "</isoDate>"

	for server in atlantis.domain pikachu.domain
	do
		echo "<server>"
		echo "${server}"
		echo "</server>"

		for command in "hostname" "uptime" "uname -a" \
		"ifconfig" \
		"vmstat" \
		"bash --version" \
		"df -h" "mount" \
		"zpool status tank" "zpool status" "zpool list" \
		"zfs get version tank" "zfs list" "zfs list -t snapshot |grep tank@"
		do
			echo "<commandResult>"
			echo "<command>"
			echo "ssh ${server} \"${command}\""
			echo "</command>"
			echo "<output>"
			echo "<![CDATA["
			ssh ${server} ${command}
			echo "]]>"
			echo "</output>"
			echo "</commandResult>"
		done
	done
}

(
echo '<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>'
echo "<backupLogReport>"
cd ${HOME}
echo "<sshAgentNoise>"
source ssh-agent.txt
echo "</sshAgentNoise>"

echo "<rootRsync>"
rsync -av --delete `ls -d /*|grep -v dev|grep -v tank` /tank/backups/zroot-nvme/
echo "</rootRsync>"

echo "<pushBackupOutput>"
./Push-Backup.py
echo "</pushBackupOutput>"

run_commands

echo "</backupLogReport>"
) &> ${log_file}



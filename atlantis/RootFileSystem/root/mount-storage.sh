#!/bin/sh

# Decrypt
geli attach \
	/dev/gpt/Blazkowicz-0 \
	/dev/gpt/Blazkowicz-1 \
	/dev/gpt/Blazkowicz-2 \
	/dev/gpt/Blazkowicz-3 \
	/dev/gpt/read-cache \
	/dev/gpt/write-cache \

# /home
zfs mount tank/home

# /tank/samba
zfs mount tank/samba

# jails
zfs mount tank/jails
zfs mount tank/jails/orion-redmine-issue-tracker

# vm bhyve
zfs mount tank/vm-bhyve
zfs mount tank/vm-bhyve/capside
zfs mount tank/vm-bhyve/orion-redmine

vm init
vm start capside
vm start orion-redmine


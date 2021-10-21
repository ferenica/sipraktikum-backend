#!/bin/bash

if [[ $(whoami) != "root" ]]; then
    echo "[-] Please run as root user..."
    exit 1
fi

# Check health and state of Server OS
echo "[+] Update and upgrade server..."
apt-get update && apt upgrade -y

echo "[+] Apt get install tools..." 
apt-get install curl
apt-get install net-tools
apt-get install bind-tools
apt-get install postgresql
apt-get install nslookup
apt-get install tmux
apt-get install unzip
apt-get install hostname
apt-get install progress

# Multiserver web interface
apt-get install cockpit

# Set iptables config to false by default true for docker
echo "{
\"iptables\": false
}" > /etc/docker/daemon.json

# Restructured DEFAULT_FORWARD_POLICY from DROP to ACCEPT
echo "[+] Forward Policy Update for UFW..."
sed -i -e 's/DEFAULT_FORWARD_POLICY="DROP"/DEFAULT_FORWARD_POLICY="ACCEPT"/g' /etc/default/ufw
echo "[+] UFW Reloaded...."
ufw reload

# Iptables configuration for docker to egress
echo "[+] Postrouting Update"
iptables -t nat -A POSTROUTING ! -o docker0 -s 172.17.0.0/16 -j MASQUERADE

#!/bin/sh
set -e

# Setup network
# Use netconf to configure networking.
echo '\n\n\n' | netconf
# Restart networking service.
service network restart

# Setup pkgin package manager
MIRROR="http://10.0.2.2:8000"
# Install pkgin from the mirror.
pkg_add -f "$MIRROR/pkgin-0.6.4nb5.tgz"
# Configure repository path.
echo "$MIRROR/" > /usr/pkg/etc/pkgin/repositories.conf
# Update package database.
echo 'y' | pkgin update

# Install benchmarking packages.
PKGS="openssh vim whetstone-1.2 ubench-0.32nb1 sysbench-0.4.12nb4 randread-0.2 \
  ramspeed-2.6.0 postmark-1.5 postgresql84-pgbench-8.4.21 pipebench-0.40 \
  nsieve-1.2b netperf-2.4.5 netio-1.26 nbench-2.2.2 linpack-bench-940225 \
  httperf-0.8nb1 hint.serial-98.06.12 heapsort-1.0 flops-2.0 fib-980203 \
  dhrystone-2.1nb1 dbench-3.04nb1 bytebench-4.1.0nb5 blogbench-1.0nb1"
# Install packages without prompting.
echo 'y' | pkgin in "$PKGS"

# Install formal verification dependencies.
apt-get update
apt-get install -y openjdk-11-jdk python3-pip z3 unzip wget bmake flake8 shellcheck

# Download TLA+ tools for model checking.
wget -nv -O /tmp/tla.zip \
  https://github.com/tlaplus/tlaplus/releases/download/v1.8.0/TLAToolbox-1.8.0-linux.gtk.x86_64.zip
unzip -q /tmp/tla.zip -d /opt/tla-toolbox

# Install Python requirements for proof automation.
pip3 install --upgrade pyvmt pysmt spot z3-solver black

# Start ssh server.

/usr/pkg/etc/rc.d/sshd onestart
# Enable sshd at boot.
sed -i 's|sshd=NO|sshd=YES|' /etc/defaults/rc.conf

# Setup complete.
echo '[+] Setup done. Goodbye !'

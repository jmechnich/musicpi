#!/bin/sh

./cleanup.sh || exit 1

do_symlink()
{
    echo "Symlinking $1 to $2"
    sudo ln -sf "$1" "$2"
}

(cd src && make) || exit 1
(cd src && sudo make install) || exit 1

for f in bin/*;  do do_symlink "$PWD/$f" /usr/local/bin;  done
for f in sbin/*; do do_symlink "$PWD/$f" /usr/local/sbin; done

do_symlink "$PWD/etc/interfaces"    /etc/network/interfaces
do_symlink "$PWD/etc/dnsmasq.conf"  /etc/dnsmasq.conf.musicpi
do_symlink "$PWD/etc/dnsmasq.hosts" /etc/dnsmasq.hosts
do_symlink "$PWD/etc/hostapd.conf"  /etc/hostapd.conf.musicpi

echo "Updating rc.local"
if grep -q '^\. .*etc/rc\.local' /etc/rc.local; then
    sudo sed -i s,'^\. .*etc/rc\.local',". $PWD/etc/rc.local", /etc/rc.local
else
    sudo sed -i '$ d' /etc/rc.local
    echo ". $PWD/etc/rc.local" | sudo tee -a /etc/rc.local
    echo 'exit 0' | sudo tee -a /etc/rc.local
fi


#!/bin/sh

DEV=hci0
DEVNAME=ISSCBTA

#if hcitool dev | grep -q $DEV; then
#    echo "Bluetooth device already up"
#    exit 0
#fi

sysfspath=`grep "$DEVNAME" /sys/bus/usb/devices/*/product | grep -o '.*/'`
echo $sysfspath

if [ x"$sysfspath" = x ]; then
    echo "Could not find device in sysfs"
    exit 1
fi

CHARDEV=`cat $sysfspath/dev`

sudo usbreset "/dev/char/$CHARDEV"

sleep 2

echo "Re-enabling $DEVNAME"
echo 0 | sudo tee $sysfspath/authorized
sleep 1
echo 1 | sudo tee $sysfspath/authorized

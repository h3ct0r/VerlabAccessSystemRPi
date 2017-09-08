#! /usr/bin/bash

BLACKLIST=/etc/modprobe.d/raspi-blacklist.conf
CONFIG=/boot/config.txt
SETTING=on

# DEFINE RPI SPI
set_config_var dtparam=spi $SETTING $CONFIG &&
if ! [ -e $BLACKLIST ]; then
    touch $BLACKLIST
fi
sed $BLACKLIST -i -e "s/^\(blacklist[[:space:]]*spi[-_]bcm2708\)/#\1/"
dtparam spi=$SETTING

# DEFINE RPI I2C
set_config_var dtparam=i2c_arm $SETTING $CONFIG &&
if ! [ -e $BLACKLIST ]; then
    touch $BLACKLIST
fi
sed $BLACKLIST -i -e "s/^\(blacklist[[:space:]]*i2c[-_]bcm2708\)/#\1/"
sed /etc/modules -i -e "s/^#[[:space:]]*\(i2c[-_]dev\)/\1/"
if ! grep -q "^i2c[-_]dev" /etc/modules; then
    printf "i2c-dev\n" >> /etc/modules
fi
dtparam i2c_arm=$SETTING
modprobe i2c-dev
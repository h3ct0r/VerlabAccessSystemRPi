# VeRLab access system - RPi/RFID/Face Recognition

[![N|Solid](http://www.verlab.dcc.ufmg.br/verlab/wp-content/uploads/2014/06/logo-verlab-small-transp-300x572.png)](www.verlab.dcc.ufmg.br)

This is the main repo of the verlab access system using a Raspberry Pi as main hardware. The authentication is based on RFID or by Face Recognition (beta). List of valid users is updated from an LDAP server.

### Why using Rpi instead of Arduino?

We love using arduino too, but our previous project using Arduino and compatible hardware we were able to find in Brazil was not very reliable. It seems that the ethernet shield is not the most reliable piece of hardware out there, and it was a key part for that project.

Using the full power of a Raspberry Pi allow us to develop other methods of authentication and/or implement sound, screens, logging and other kind of funcionalities without the 16Kb space limitation. And since all Raspberrys are made from the same vendor, we can be certain of the hardware reliability.

### Hardware list

This access sytem need the following hardware to work properly:

* Raspberry Pi - version 2 or up
* RFID Reader - use the best RFID readers available, we use the ones from Funduino (available on MercadoLivre.com.br)
* Door lock - we use one from HDL ([FEC-91 LA](http://www.hdl.com.br/produtos/fechaduras/fecho-eletrico/fecho-eletrico-mod-fec-91-la-espelho-longo-trinco-ajustavel))
* Relay switch - We use common relays used with arduino
* Jumper cables - a lot of them

### Installation

To do, based on https://www.sunfounder.com/wiki/index.php?title=How_to_Use_an_RFID_RC522_on_Raspberry_Pi

- Rename config/config.json.rename to config.json to begin

### Todos
 - RFID robust search
 - Face detection
 - Web config interface
 - Write Tests
 - http://blog.scphillips.com/posts/2013/07/getting-a-python-script-to-run-in-the-background-as-a-service-on-boot/

### Commands

- `sudo apt-get install python-smbus`
- `sudo i2cdetect -y 1` to test if i2c interface is working and have connected devices 
- `sudo pip install unidecode`
- `sudo apt-get install libsasl2-dev python-dev libldap2-dev libssl-dev`
- `sudo pip install python-ldap`
- `sudo update-rc.d lcd_daemon.sh defaults`
- Add to /etc/crontab `*/5 * * * * pi cd /home/pi/Git/DoorAccessRpi/system/cron && python synch_RFID.py`

License
----

MIT

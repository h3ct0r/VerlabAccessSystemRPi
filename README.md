# VeRLab Access System - RPi/RFID/Face Recognition

[![](https://www.verlab.dcc.ufmg.br/wp-content/uploads/2019/05/SVG_Verlab_210x86dpi.png)](https://www.verlab.dcc.ufmg.br)

This is the main repo of the Verlab Access System using a Raspberry Pi as main hardware. The authentication is based on RFID or by Face Recognition (beta). List of valid users is updated from an LDAP server and maintained on the device for offline verification.

### Authors
----
- [Hector Azpurua](https://github.com/h3ct0r)
- [Elerson Rubens](https://github.com/elerson)
- [Mauricio Ferrari](https://github.com/mauferrari)

### Why using Rpi instead of Arduino?
----

We love arduino too, but our previous project using Arduino and using the compatible hardware we were able to find in Brazil ended up beign not very reliable. It seems that the ethernet shield is not the most robust piece of hardware out there, and it was a key part for that project.

Using the full power of a Raspberry Pi, it allow us to develop other methods of authentication and/or implement sound, screens, logging and other kind of funcionalities without the 16Kb space limitation. And since all Raspi-berrys are made from the same vendor and quality, we can be certain of the hardware reliability.

### Hardware Information
----
[**Hardware folder**](/hardware) has more information about 3D Printer files, connections, and assembly. 

#### Components List

This access system needs the following parts to work properly:

* *Raspberry Pi* - version 2 or up (We tested Pi2b and 3).
* *RFID Reader* - use the best RFID readers available, we use the **red ones from Funduino** (available fromm MercadoLivre.com.br sellers, look specifically the red ones). The [PN532](https://www.filipeflop.com/produto/kit-modulo-leitor-rfid-nfc-pn532/) is an excellent choice.
* *Door lock* - we used one from HDL ([FEC-91 LA](http://www.hdl.com.br/produtos/fechaduras/fecho-eletrico/fecho-eletrico-mod-fec-91-la-espelho-longo-trinco-ajustavel)).
* *Door lock Power Supply* - we used the HDL's power supply compatible with our door lock ([TRA-400](https://www.hdl.com.br/produtos/fechaduras/acessorios/fonte-tra-400-para-fechaduras-porteiros-e-centrais))
* *Relay switch* - We used common arduino relays.
* *Jumper cables* - a lot of them.
* *Two Patch Painel Female RJ45 Femal* - to leave the pinout to connect the RFID reader and Raspberry pins
* *Ethernet Cable* -  arbitrary size, to connect the RPi to the RFID reader
* Probably, will be necessary other parts for your building infrastructure that are not listed here (e.g. wall mounted plug for power, networking, electric cables, etc)

### Software Installation
----

We rely on Ansible for software installation on the Raspberry. Ansible is a 'automation' tool for configuring servers that we use to simplify the installation process on the door (for a simple guide for Ansible see [Simple Ansible Tutorial](https://serversforhackers.com/c/an-ansible-tutorial)). With this tool is very easy to deploy one or more installations of the Door System at the same time!

The installation begins on the raspberry Pi, first installing the image and then getting the right information for Ansible later make a remote installation.

##### On the Raspberry Pi

- Download the *img* file for **Raspbian LITE** and install it on an SD card [Raspbian downloads](https://www.raspberrypi.org/downloads/raspbian/).
- Connect a network cable on the Raspberry pi.
- Perform the *Hardware Installation* (of the previous section).
- Boot the SD card and activate SSH using the [raspi-config utility](https://www.raspberrypi.org/documentation/configuration/raspi-config.md).
- Change the default password for the *pi* user of this device (also possible using [raspi-config utility](https://www.raspberrypi.org/documentation/configuration/raspi-config.md)).
- Take note of the **hostname and password** you set to this device. *We will need them later*.

After the Raspberry Pi is prepared the next step is performed on the end user machine. **This GitHub repo is downloaded on the user machine and NOT on the Raspberry directly.**

##### On the user machine
- Install local dependencies to begin installation:

    `sudo apt install git ansible sshpass`


- Then clone this repository:

    `cd ~/`
    
    `git clone https://github.com/h3ct0r/VerlabAccessSystemRPi`
    
    `cd ~/VerlabAccessSystemRPi`

- Prepare Ansible and define the hosts where we will connect and perform the install:
    
    `nano ansible_install/playbooks/hosts`
    
    *Edit the fields **HOST_IP_ADDRESS** and **APPLIANCE_PASSWORD***

- Edit the configurations for the system on the *config.json* file:
    
    `nano system/config/config.json.rename`
    
    You must set at least **ldap_uri**, **ldap_username**, **ldap_passwd** and **ldap_basedn**.

- Then run the installation:
    
    `cd ansible_install/playbooks/`
    
    `ansible-playbook -s -v full_raspi_config.yaml`

##### Finalizing installation

- Enter the device machine via SSH:
    
    `ssh pi@HOST_IP_ADDRESS`
    
- Open the syslog file:

    `sudo tail -f /var/log/syslog`
    
- Test if there are I2C devices connected:

    `sudo i2cdetect -y 1`
    
- Use a RFID card and test it on the device. If all went OK you will see DEBUG information on the log.

This installation was lousy based on [How to Rpi RFID](https://www.sunfounder.com/wiki/index.php?title=How_to_Use_an_RFID_RC522_on_Raspberry_Pi) and [Rpi services](http://blog.scphillips.com/posts/2013/07/getting-a-python-script-to-run-in-the-background-as-a-service-on-boot/).

### Manage services
---

The system is based on daemons, to restart a service the commands are:
- `sudo /etc/init.d/relay_server.sh restart`
- `sudo /etc/init.d/rfid_server.sh restart`

All services log to *syslog* so to verify installation or real time operation just need to:
- `sudo tail -f /var/log/syslog`

### Todos
----

 - RFID robust search.
 - Face detection (?).
 - Web config interface.
 - Write moar tests.

License
----

Custom license, please see [Our license agreement](https://github.com/h3ct0r/VerlabAccessSystemRPi/blob/master/LICENSE) first before using this software.

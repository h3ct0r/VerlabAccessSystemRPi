# [VeRLab Access System](https://github.com/h3ct0r/VerlabAccessSystemRPi/)
[![](https://www.verlab.dcc.ufmg.br/wp-content/uploads/2019/05/SVG_Verlab_210x86dpi.png)](https://www.verlab.dcc.ufmg.br)

# Hardware Information

## RPi Connections
---
RFID reader PCB pins:

|Signal Name|J8 Pin#|RPi Pin Name|
|---|---|---|
|VCC|17|3V3|
|RST|22|GPIO25|
|GND|20|Ground|
|MISO|21|GPIO9|
|MOSI|19|GPIO10|
|SCK|23|GPIO11|
|SDA|24|GPIO8|
|IRQ|None|Not Connected|

Relay PCB pins:

|Signal Name|J8 Pin#|RPi Pin Name|
|---|---|---|
|VCC|4|5V|
|GND|6|Ground|
|Relay_on|7|GPIO4|


## Casing files
---
The casing has two parts: cover and case. There are some different file extensions:

- *.stl: 3D model files, that could be loaded in a slicer software and used to print your casing with a 3D printer.

- *.pdf: some dimensions of the casing  parts

- *.png: just images to visualize the casing parts. They are screeshots of the *.stl files loaded in the 
[ideaMaker Software](https://www.raise3d.com/ideamaker/)


<img style="float: left; margin:0 50px 50px 0" src="/hardware/casing/casing-door-system_v3.2-ideamaker.png" width="400">
<img style="float: rigth; margin:0 50px 50px 0" src="/hardware/casing/cover-casing-door-system_v3.2-ideamaker.png" width="400">


## Assembly example
---
- Casing and parts mounted in a place inside the room. Its
  necessary a wall-mounted power plug, and a network access plug to control the system remotely.

PS: The system casing is important to be in a safe place, just for authorized persons, because there are security data saved inside the SD Card.


<img src="/hardware/assembly-example/P_20170626_152344-mini2.jpg" width="400">
<img src="/hardware/assembly-example/P_20170626_152014-mini.jpg" width="400">

- An Ethernet cable and RJ45 panel connectors were used to connect the RFID reader from the wall outside the room to the System casing. in our practical experience, it was the best solution to make the connection of the 7 SPI signals in a robust way and avoiding bad contact. 

Note: This ethernet cable is just a medium for the signals, it doesn't transmit network ethernet data!


<img src="/hardware/assembly-example/P_20170626_141153-mini.jpg" width="400">

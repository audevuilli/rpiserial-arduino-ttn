# Raspberry Pi - Arduino Serial Communication 

This repository aims to document how to send messages from a Raspberry Pi to an Arduino using serial communication. It also shows how an Arduino can read the serial messages and send them via LoRa to [The Things Network (TTN)](https://console.cloud.thethings.network/) console. 

### Repository Structure
- [Arduino Code](/Arduino%20Code/) folder contains (1) the arduino code [mkrwan1310_readserial](/Arduino%20Code/mkrwan1310_readserial) to read the incoming serial messages and send them to the TTN console and (2) a javascript function [decodeUplink.js](/Arduino%20Code/decodeUplink.js) to decode the payload on the TTN.
- [Rpi Code](/RPi%20Code/) folder contains two scripts. (1) A bash script [setup_serial.sh](/RPi%20Code/setup_serial.sh) to install the python libraries required for serial communication, and (2) a python script [rpi_sendserial.py](/RPi%20Code/rpi_sendserial.py) to get raspberry pi system data and send it via serial. 

## SetUp Instructions Overview
**Arduino Device**
1. Register Arduino MKR1310 to a TTN Application.
2. Upload .ino script to Arduino MKR1310.

**Raspberry Pi Device**
1. Install python libraries and create .py script
2. Setup cronjob to run .py script on repeating schedule
3. [Optional] Configure external harddrive.

### Arduino SetUp 
1. Find DeviceEUI from MKRWAN 1310 Board. 
    - Open the Arduino IDE. Install the MKRWAN Arduino library.
    - Go to File -> Examples -> MKRWAN -> FirstConfiguration 
    - Connect MKRWAN 1310 to Laptop, select the MKRWAN1310 COM Port and upload sketch. Follow instructions to get the DevEUI. 
2. Create new application on TTN Console.
    - Chose application ID and write few words to describe it. 
    - Click register end device for application -> Select Brand (here Arduino SA) -> Select Model (here MKRWAN 1310) -> Select newest version for HW and SW. -> Select Freqeuncy Plan. 
    - Enter information to activate the application: DevEUI, AppEUI (if none enter 0000000000000000). 
    - Create AppKey, copy AppKey and paste somewhere you won't lose it (you will need to add it into the arduino_secrets.h) 
3. Upload Code to MKRWAN 1310 Board. 
    - Make sure to modify the arduino_secrets.h with your credentials.
    - Once uploaded, disconnect the board and plug it into a USB port of your raspberry pi. 

Great links that document the process: 
- [Arduino Tutorials: Connecting MKR WAN 1310 to TTN](https://docs.arduino.cc/tutorials/mkr-wan-1310/the-things-network)
- [Encoding and Decoding Payloads on TTN](https://core-electronics.com.au/guides/encoding-and-decoding-payloads-on-the-things-network/)

### Raspberry Pi SetUp
1. Install python libraries for serial communication
```
    bash setup_serial.sh
```
2. Create and test the rpi_sendserial.py script. 
    - Paste the content of the script `rpi_sendserial.py`, 
    - Test the script to see if everything work correctly. 
    - Setup a cronjob to run the script on repeating schedule. Note the Minute Hour Day Month Weekday pattern of crontab.
    - For rpi_sendserial running 2x a day at 9am and 9pm add the following line at the end of crontab list `0 9,21 * * * /usr/bin/python3 /home/pi/rpi_sendsrial.py`
```
    nano rpi_sendserial.py 
```
```
    python3 rpi_sendserial.py 
```
```
    crontab -e
```
3. Pay Attention to the following
    - You may need to check the port the Arduino is connected to on your rpi (it will be either `/dev/ttyACM0` or `/dev/ttyACM1` ). Enter `ls /dev/ttyACM*` to check. 
    - With no external harddrive: (1) Modify the path of the logging file, and (2) comment out `get_extdrive_storage()` in the .py script. 

Great links that document the process: 
- [Crontab Guru: The quick and simple editor for cron shedule expression](https://crontab.guru/)
- [Serial communication between Raspberry Pi and Arduino](https://www.aranacorp.com/en/serial-communication-between-raspberry-pi-and-arduino/)

### Raspberry Pi Setup - With External Drive



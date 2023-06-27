# Raspberry Pi - Arduino Serial Communication 

This repository aims to document how to send messages from a Raspberry Pi to an Arduino using serial communication. It also shows how an Arduino can read the serial messages and send them via LoRa to [The Things Network (TTN)](https://console.cloud.thethings.network/) console.

### Repository Structure
- [Arduino Code](/Arduino%20Code/) folder contains (1) the Arduino code [mkrwan1310_readserial](/Arduino%20Code/mkrwan1310_readserial) to read the incoming serial messages and send them to the TTN console and (2) a javascript function [decodeUplink.js](/Arduino%20Code/decodeUplink.js) to decode the payload on the TTN.
- [RPi Code](/RPi%20Code/) folder contains two scripts. (1) A bash script [setup_serial.sh](/RPi%20Code/setup_serial.sh) to install the python libraries required for serial communication, and (2) a python script [rpi_sendserial.py](/RPi%20Code/rpi_sendserial.py) to get raspberry pi system data and send it via serial.
- [Google Apps Script](/GApps%20Script/) folder contains (1) the Apps Script code []()  to update a Google sheet every time new data arrives in the TTN console. 

## Setup Instructions Overview
**Arduino Device**
1. Register Arduino MKR1310 to a TTN Application.
2. Upload .ino script to Arduino MKR1310.

**Raspberry Pi Device**
1. Install Python libraries and create a .py script
2. Setup cronjob to run .py script on repeating schedule
3. [Optional] Configure external hard drive.

**Google Apps Script**
1. Setup a script to a google spreadsheet.
2. Deploy gsheet script as a web app. 
3. Integrate web app to the TTN using Webhooks.

### Arduino SetUp 
1. Find DeviceEUI from MKRWAN 1310 Board. 
    - Open the Arduino IDE. Install the MKRWAN Arduino library.
    - Go to File -> Examples -> MKRWAN -> FirstConfiguration 
    - Connect MKRWAN 1310 to Laptop, select the MKRWAN1310 COM Port and upload the sketch. Please follow the instructions to get the DevEUI. 
2. Create a new application on TTN Console.
    - Choose an application ID and write a few words to describe it. 
    - Click register end device for application -> Select Brand (here Arduino SA) -> Select Model (here MKRWAN 1310) -> Select newest version for HW and SW. -> Select Frequency Plan. 
    - Enter information to activate the application: DevEUI, AppEUI (if none enter 0000000000000000). 
    - Create AppKey, copy AppKey and paste it somewhere you won't lose it (you will need to add it into the arduino_secrets.h) 
3. Upload Code to MKRWAN 1310 Board. 
    - Make sure to modify the arduino_secrets.h with your credentials.
    - Once uploaded, disconnect the board and plug it into a USB port of your raspberry pi. 

Excellent links that document the process: 
- [Arduino Tutorials: Connecting MKR WAN 1310 to TTN](https://docs.arduino.cc/tutorials/mkr-wan-1310/the-things-network)
- [Encoding and Decoding Payloads on TTN](https://core-electronics.com.au/guides/encoding-and-decoding-payloads-on-the-things-network/)

### Raspberry Pi Setup
1. Install Python libraries for serial communication
```
    bash setup_serial.sh
```
2. Create and test the rpi_sendserial.py script. 
    - Paste the content of the script `rpi_sendserial.py`, 
    - Test the script to see if everything works correctly. 
    - Set up a cronjob to run the script on a repeating schedule. Note the Minute Hour Day Month Weekday pattern of crontab.
    - For rpi_sendserial.py running 2x a day at 9am and 9pm add the following line at the end of the crontab list `0 9,21 * * * /usr/bin/python3 /home/pi/rpi_sendserial.py`
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
    - You may need to check the port the Arduino is connected to on your RPi (it will be either `/dev/ttyACM0` or `/dev/ttyACM1` ). Enter `ls /dev/ttyACM*` to check. 
    - With no external hard drive: (1) Modify the path of the logging file, and (2) comment out `get_extdrive_storage()` in the .py script. 

Excellent links that document the process: 
- [Crontab Guru: The quick and simple editor for cron schedule expression](https://crontab.guru/)
- [Serial communication between Raspberry Pi and Arduino](https://www.aranacorp.com/en/serial-communication-between-raspberry-pi-and-arduino/)

### GSheet Apps Script
1. Create a new gsheet `sheet.new` in your google account.
2. Copy the sheet address `https://docs.google.com/spreadsheets/d/`YOUR-SHEET-ID`/edit#gid=0`
3. Navigate to Extensions, click on Apps Script. 
4. Copy and paste the [ttn_gsheet.js](/GApps%20Script/ttn_gsheet.js) into the script editor. Replace `YOUR-SHEET-ID` with the one from your sheet. 
5. Save and select deploy as a web app. Select *Execute as Me* and *Who has access: Anyone*. 
6. Copy the address that is deplayed. Paste the address *Base URL* of your TTN application -> Integration -> Webhooks.
7. In TTN Integration Webhooks, select *Add Webhook*. Make sure to tick the box *Uplink message*. 

Excellent links that document the process: 
- [TTN-Google-Script by @uspizig](https://github.com/Uspizig/Ttn-gooogle-script)
- [How to use Google spreadsheet to log data by @squix78](https://blog.squix.org/2017/07/thethingsnetwork-how-to-use-google-spreadsheet-to-log-data.html)


### Raspberry Pi Setup - With External Drive
When plugging external storage into a Raspberry Pi, the storage needs to be mounted to be accessible for reading, writing, and deleting. Good articles explaining the steps to mount an external drive can be found on [PiMyLife Up](https://pimylifeup.com/raspberry-pi-mount-usb-drive/) or [GeekWorm](https://geekworm.com/blogs/news/how-to-mount-usb-storage-on-raspberry-pi).

The steps are the following:
1. Plug a USB drive into the RPi and check that storage is attached. Copy the UUID and pay attention to disk type (i.e., ext4, ntfs, vfat)
```
    sudo blikd 
```
2. Create a location to mount the drive
```
    sudo mkdir /mnt/external-drive 
```
3. Give permission to the RPi to access the folder
```
    sudo chown -R pi:pi /mnt/external-drive/
    sudo chmod 775 /mnt/external-drive/
```
4. Mount the drive into the created folder
```
    sudo mount /dev/sda1 /mnt/external-drive
```
5. Allow the drive to automatically mount on boot, and modify the `/etc/fstab` file by adding a line with the drive UUID, path, type, defaults, 0 0
```
    sudo nano /etc/fstab
```

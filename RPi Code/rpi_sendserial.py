import serial
import time
import os
import psutil
import shutil
import logging

CONST_BAUD_RATE = 115200
SERIAL_PORT = '/dev/ttyACM0'
EXT_HDRIVE_PATH = '/mnt/external-drive'
log_file_path = ''.join(EXT_HDRIVE_PATH+'/rpi_status.log')

# Setup the main logger
logging.basicConfig(
	filename=log_file_path,
	filemode='w',
	format='%(levelname)s - %(message)s',
	level=logging.INFO,
)

## Function to check available disk space in GB
def get_available_disk_space():
	st = os.statvfs("/")
	total = st.f_blocks * st.f_frsize
	free = st.f_bfree * st.f_frsize
	available = st.f_bavail * st.f_frsize
	return	available / (1024 ** 3)

## Function to get the current CPU temperature in °C
def get_cpu_temperature():
	with open("/sys/class/thermal/thermal_zone0/temp","r") as f:
		return float(f.read().strip())/1000

## Function to get the current memory usage in MB
def get_rpi_memory_usage():
	mem = psutil.virtual_memory()
	return mem.used / 1024 ** 2

def get_extdrive_storage():
	total, used, free = shutil.disk_usage(EXT_HDRIVE_PATH)
	return free / (1024 ** 3)

## Function to get the list of running services
def get_running_services():
	services=[]
	for service in psutil.process_iter(["pid","name"]):
		if "service" in service.info["name"]:
			services.append(service.info["name"])
	return services

def send_serial():
	# Open serial port (change the port and baud rate to match your setup)
	ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
	print(f'Sending RPi Data to TTN: {time.asctime()}')
	logging.info(f"Sending RPi status to TTN: {time.asctime()}")

	# Get RaspberryPi Monitored Values
	cpu_temp = f"{get_cpu_temperature():.2f}"
	disk_space = f"{get_available_disk_space():.2f}"
	#rpi_mem = f"{get_memory_usage():.2f}"
	ext_hdrive = f"{get_extdrive_storage():.2f}"

	# Send monitored valued over serial
	msg0 = f"Status Active\n"
	msg1 = f"CPU Temp.: {cpu_temp} C\n"
	msg2 = f"RPi Disk space: {disk_space} GB\n"
	msg3 = f"Ext HDrive Free Space: {ext_hdrive} GB\n"
	
	print(f'Sending Message 0: {msg0}')
	ser.write(msg0.encode())
	print(f'Message 0 has been sent.')
	time.sleep(10)
	ser.write(msg1.encode())
	time.sleep(10)
	ser.write(msg2.encode())
	time.sleep(10)
	ser.write(msg3.encode())

	# Save message sent to logging file
	logging.info(f'Messages sent via TTN: {msg0,msg1,msg2,msg3} at {time.asctime()}')

	# Close Serial Connection
	ser.close()
	return

# Run the RPi Status Function - Use cron job - send data every 6 hours
send_serial()

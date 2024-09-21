# Imports
import time as t
import threading
from redacted_file_paths import data_path

# Constants
BATTERY_FILE_PATH = "/sys/class/power_supply/BAT0/capacity"
LOW_END = 30.0
HIGH_END = 100.0

class OutOfRangeError(BaseException): ...

def find_battery():
	with open(BATTERY_FILE_PATH, "r") as f:
		capacity = float(f.read())
	return capacity

def store_current_battery(battery:float):
	print("Storing...")
	with open(data_path, "a") as f:
		f.write(f"{battery}\n")

def update_current_battery():
	battery = find_battery()
	if battery < LOW_END or battery > HIGH_END:
		raise OutOfRangeError("Out of range. Quitting...")
	store_current_battery(battery)

def update_battery_periodically(interval):
	def wrapper():
		try:
			update_current_battery()
		except OutOfRangeError as e:
			print(e)
			exit()
		threading.Timer(interval, wrapper).start()  # Reschedule the next execution

	# Start the first execution
	threading.Timer(interval, wrapper).start()
update_battery_periodically(20)
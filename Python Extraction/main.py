# Imports
import time as t
import threading
import glob
import os
from redacted_file_paths import battery_folder_path

# Constants
CAPACITY_FILE_PATH = "/sys/class/power_supply/BAT0/capacity"
STATUS_FILE_PATH = "/sys/class/power_supply/BAT0/status" # potential refactor to one constant and then change as required
LOW_END = 0.0 # was previously set to 30 but not doing that for now
HIGH_END = 100.0

class OutOfRangeError(BaseException): ...

def read_previous_session_ID():
	# Use glob to get all files in the folder
	files = glob.glob(os.path.join(battery_folder_path, '*'))

	if not files:
		return get_default_ID()

	most_recent_file = max(files, key=os.path.getctime) # Gets the last created
	file_name = os.path.basename(most_recent_file)
	previous_ID = os.path.splitext(file_name)[0]
	return previous_ID

def get_default_ID():
	return "0"

def increment_session_ID(previous_ID, count: int):
	# This is based on arbritary convention. For now just using numbers but could include dates, times, etc
	return str(int(previous_ID) + count)

def create_output_file(session_ID:str):
	with open(f"{battery_folder_path}{session_ID}", 'w') as f:
		pass

def make_new_ID():
	previous_ID = read_previous_session_ID()
	new_ID = increment_session_ID(previous_ID,1)
	return new_ID # ik, ik, bad practice. Side effects I'll refactor at some point

def find_battery_status():
	with open(CAPACITY_FILE_PATH, "r") as f:
		capacity = float(f.read())
	with open(STATUS_FILE_PATH, "r") as f:
		status = f.read()
	return capacity, status # don't wanna use oop cuz ott. might use dataclass or a dict (probably dict)

def store_current_battery(battery:float, status:str):
	print("Storing...")
	with open(f"{battery_folder_path}{CURRENT_ID}.csv", "a") as f:
		f.write(f"{battery},{status}")

def initialise_data_file():
	with open(f"{battery_folder_path}{CURRENT_ID}.csv", "a") as f:
		f.write(f"battery,status")

def update_current_battery():
	capacity, status = find_battery_status()
	if capacity < LOW_END or capacity > HIGH_END:
		raise OutOfRangeError("Out of range. Quitting...")
	store_current_battery(capacity, status)

def update_battery_periodically(interval_in_secs):
	initialise_data_file()
	update_current_battery()
	def wrapper():
		try:
			update_current_battery()
		except OutOfRangeError as e:
			print(e)
			exit()
		threading.Timer(interval_in_secs, wrapper).start()  # Reschedule the next execution

	# Start the first execution
	threading.Timer(interval_in_secs, wrapper).start()

CURRENT_ID = make_new_ID()
update_battery_periodically(interval_in_secs=30)
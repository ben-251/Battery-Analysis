# Imports
import time as t
import math
from redacted_file_paths import data_path

# Constants
BATTERY_FILE_PATH = "/sys/class/power_supply/BAT0/capacity"
LOW_END = 30.0
HIGH_END = 100.0

# Main Body
def find_battery():
	with open(BATTERY_FILE_PATH, "r") as f:
		capacity = float(f.read())
	return capacity

def import_periodically(interval_in_mins: float):
	battery = find_battery()
	interval_in_secs = interval_in_mins * 60

	START = t.time()
	while battery > LOW_END and battery < HIGH_END:
		battery = find_battery()
		elapsed_time = t.time()-START # written relative to start time (seconds)
		time_ratio = round(elapsed_time/interval_in_secs)
		if math.floor(time_ratio) == time_ratio:
			store_current_battery(battery, time_ratio)

def store_current_battery(battery:float, time_ratio:float):
	with open(data_path, "a") as f:
		f.write(f"{time_ratio},{battery}")

import_periodically(0.1)



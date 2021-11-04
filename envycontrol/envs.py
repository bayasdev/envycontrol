import os

# This file is responsible for storing environment vars

VERSION = '0.1'

BLACKLIST_PATH = '/etc/modprobe.d/blacklist-nvidia.conf'
UDEV_PATH = '/lib/udev/rules.d/50-remove-nvidia.rules'

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LOG_FILE_PATH = ROOT_DIR + '/logs/envycontrol.log'

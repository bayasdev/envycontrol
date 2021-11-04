import os
import sys
from args import parse_args
from logger import log
from envs import BLACKLIST_PATH, BLACKLIST_CONTENT, UDEV_PATH, UDEV_CONTENT


def switch_on():
    # Remove the EnvyControl generated files
    try:
        os.remove(BLACKLIST_PATH)
        os.remove(UDEV_PATH)
    except Exception as e:
        log.error(f'An error ocurred: {e}')
        sys.exit(1)
    print('Nvidia dGPU enabled!')
    print('Please reboot your computer for changes to take effect')

def switch_off():
    # Blacklist all Nvidia related modules
    try:
        with open(BLACKLIST_PATH, mode='w', encoding='utf-8') as f:
            print(os.path.realpath(f.name))
            f.write(BLACKLIST_CONTENT)
            log.debug(f'File written: {BLACKLIST_PATH}')
    except IOError:
        log.error(f'Not enough permissions to write file: {BLACKLIST_PATH}')
        sys.exit(1)

    # Power off the Nvidia card at startup with Udev rules
    try:
        with open(UDEV_PATH, mode='w', encoding='utf-8') as f:
            f.write(UDEV_CONTENT)
            log.debug(f'File written: {UDEV_PATH}')
    except IOError:
        log.error(f'Not enough permissions to write file: {UDEV_PATH}')
        sys.exit(1)
    print('Nvidia dGPU disabled!')
    print('Please reboot your computer for changes to take effect')

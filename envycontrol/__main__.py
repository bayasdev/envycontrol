import os
import sys
import subprocess
from args import parse_args
from logger import log
import switcher
from envs import VERSION, BLACKLIST_PATH, UDEV_PATH


def main():
    args = parse_args()
    if args.status:
        _query_dgpu()
    elif args.version:
        _show_version()
    elif args.switch:
        if args.switch == 'on':
            switcher.switch_on()
        elif args.switch == 'off':
            switcher.switch_off()
        else:
            log.error('Invalid argument for --switch')
            sys.exit(1)

def _query_dgpu():
    # Check if EnvyControl generated files exist
    blacklist_exists = os.path.isfile(BLACKLIST_PATH)
    rules_exists = os.path.isfile(UDEV_PATH)
    if blacklist_exists and rules_exists:
        print('EnvyControl dGPU Mode: off')
    else:
        print('EnvyControl dGPU Mode: on')
    # Check if Nvidia exists on PCI bus
    cmd = 'lspci | grep -i nvidia'
    p = subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL)
    if p.returncode == 0:
        print('PCI: Nvidia dGPU detected')
    else:
        print('PCI: Nvidia dGPU not detected')

def _show_version():
    print(f'EnvyControl version: {VERSION}')
    print('https://github.com/geminis3/EnvyControl\n')
    print('(C) 2021 Victor Bayas')

if __name__ == '__main__':
    main()

import sys
import subprocess
import os
from args import parse_args
from logger import log
import envs


def main():
    args = parse_args()
    if args.status:
        _query_dgpu()
    elif args.version:
        _show_version()
    elif args.switch:
        if args.switch in ['on', 'off']:
            _switch_mode(args.switch)
        else:
            log.error('Invalid argument for --switch')
            sys.exit(1)
    else:
        pass

def _query_dgpu():
    blacklist, rules = _check_files()
    if blacklist and rules:
        print('dGPU Mode: off')
    else:
        print('dGPU Mode: on')
    cmd = 'lspci | grep -i nvidia'
    p = subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL)
    if p.returncode == 0:
        print('PCI: Nvidia dGPU detected')
    else:
        print('PCI: Nvidia dGPU not detected')

def _check_files():
    blacklist = os.path.isfile(envs.BLACKLIST_PATH)
    rules = os.path.isfile(envs.UDEV_PATH)
    return blacklist, rules

def _switch_mode(mode):
    print(f'Mode is: {mode}')

def _show_version():
    print(f'EnvyControl version: {envs.VERSION}')


if __name__ == '__main__':
    main()

import argparse
import sys
import os
import envs

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--status', action='store_true', help='Query the current graphics mode set by EnvyControl')
    parser.add_argument('--switch', type=str, metavar='MODE', action='store',
                        help='Switch the graphics mode. You need to reboot for changes to apply. Supported modes: integrated, nvidia, hybrid')
    parser.add_argument('--version', '-v', action='store_true', help='Print the current version and exit')

    # print help if no arg is provided
    if len(sys.argv)==1:
        parser.print_help()
        sys.exit(1)
    
    args = parser.parse_args()

    if args.status:
        _check_status()
    elif args.version:
        _print_version()
    elif args.switch:
        _switcher(args.switch)

def _check_root():
    if not os.geteuid() == 0:
        print('Error: this operation requires root privileges')
        sys.exit(1)

def _check_status():
    if os.path.exists(envs.BLACKLIST_PATH) and os.path.exists(envs.UDEV_PATH):
        mode = 'integrated'
    elif os.path.exists(envs.XORG_PATH) and os.path.exists(envs.NVIDIA_MODESET_PATH):
        mode = 'Nvidia'
    else:
        mode = 'hybrid'
    print(f'Current graphics mode is: {mode}')

def _file_remover():
    # utility function to cleanup environment before setting any mode
    # don't raise warning if file is not found
    try:
        os.remove(envs.BLACKLIST_PATH)
    except OSError as e:
        if e.errno != 2:
            print(f'Error: {e}')
            sys.exit(1)
    try:
        os.remove(envs.UDEV_PATH)
    except OSError as e:
        if e.errno != 2:
            print(f'Error: {e}')
            sys.exit(1)
    try:
        os.remove(envs.XORG_PATH)
    except OSError as e:
        if e.errno != 2:
            print(f'Error: {e}')
            sys.exit(1)
    try:
        os.remove(envs.NVIDIA_MODESET_PATH)
    except OSError as e:
        if e.errno != 2:
            print(f'Error: {e}')
            sys.exit(1)

def _switcher(mode):
    # exit if not running as root
    _check_root()

    if mode == 'integrated':
        _file_remover()
        try:
            # blacklist all nouveau and Nvidia modules
            with open(envs.BLACKLIST_PATH, mode='w', encoding='utf-8') as f:
                f.write(envs.BLACKLIST_CONTENT)
            # power off the Nvidia GPU with Udev rules
            with open(envs.UDEV_PATH, mode='w', encoding='utf-8') as f:
                f.write(envs.UDEV_CONTENT)
        except Exception as e:
            print(f'Error: {e}')
            sys.exit(1)
    
    elif mode == 'nvidia':
        _file_remover()
        try:
            # create X.org config
            with open(envs.XORG_PATH, mode='w', encoding='utf-8') as f:
                f.write(envs.XORG_CONTENT)
            # modeset for Nvidia driver is required to prevent tearing on internal screen
            with open(envs.NVIDIA_MODESET_PATH, mode='w', encoding='utf-8') as f:
                f.write(envs.NVIDIA_MODESET_CONTENT)
        except Exception as e:
            print(f'Error: {e}')
            sys.exit(1)
    
    elif mode == 'hybrid':
        # remove all files created by other EnvyControl modes
        # Nvidia and nouveau drivers fallback to hybrid mode by default
        _file_remover()
        
    else:
        print('Error: provided graphics mode is not valid')
        print('Supported modes: integrated, nvidia, hybrid')
        sys.exit(1)

    print(f'Graphics mode set to: {mode}')
    print('Please reboot your computer for changes to apply')

def _print_version():
        print(f'EnvyControl {envs.VERSION}')

if __name__ == '__main__':
    main()

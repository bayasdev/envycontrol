#!/usr/bin/env python
import argparse
import sys
import os
import re
import subprocess

# constants declaration

VERSION = '1.1'

# for integrated mode

BLACKLIST_PATH = '/etc/modprobe.d/blacklist-nvidia.conf'
BLACKLIST_CONTENT = '''# Do not modify this file
# Generated by EnvyControl

blacklist nouveau
blacklist nvidia
blacklist nvidia_drm
blacklist nvidia_uvm
blacklist nvidia_modeset
'''

UDEV_PATH = '/lib/udev/rules.d/50-remove-nvidia.rules'
UDEV_CONTENT = '''# Do not modify this file
# Generated by EnvyControl

# Remove NVIDIA USB xHCI Host Controller devices, if present
ACTION=="add", SUBSYSTEM=="pci", ATTR{vendor}=="0x10de", ATTR{class}=="0x0c0330", ATTR{remove}="1"

# Remove NVIDIA USB Type-C UCSI devices, if present
ACTION=="add", SUBSYSTEM=="pci", ATTR{vendor}=="0x10de", ATTR{class}=="0x0c8000", ATTR{remove}="1"

# Remove NVIDIA Audio devices, if present
ACTION=="add", SUBSYSTEM=="pci", ATTR{vendor}=="0x10de", ATTR{class}=="0x040300", ATTR{remove}="1"

# Finally, remove the NVIDIA dGPU
ACTION=="add", SUBSYSTEM=="pci", ATTR{vendor}=="0x10de", ATTR{class}=="0x03[0-9]*", ATTR{remove}="1"
'''

# for Nvidia mode

XORG_PATH = '/etc/X11/xorg.conf.d/90-nvidia.conf'
XORG_CONTENT = '''# Do not modify this file
# Generated by EnvyControl

Section "ServerLayout"
    Identifier "layout"
    Screen 0 "nvidia"
    Inactive "intel"
EndSection

Section "Screen"
    Identifier "nvidia"
    Device "nvidia"
    Option "AllowEmptyInitialConfiguration"
EndSection

Section "Device"
    Identifier "nvidia"
    Driver "nvidia"
    BusID "PCI:1:0:0"
EndSection

Section "Screen"
    Identifier "intel"
    Device "intel"
EndSection

Section "Device"
    Identifier "intel"
    Driver "modesetting"
EndSection
'''

NVIDIA_MODESET_PATH = '/etc/modprobe.d/nvidia.conf'

NVIDIA_MODESET_CONTENT = '''# Do not modify this file
# Generated by EnvyControl
options nvidia-drm modeset=1
'''

# SDDM and LightDM require this for Nvidia mode

SDDM_SCRIPT_PATH = '/usr/share/sddm/scripts/Xsetup'

LIGHTDM_SCRIPT_PATH = '/etc/lightdm/nvidia.sh'

XRANDR_SCRIPT = '''#!/bin/sh

# Do not modify this file
# Generated by EnvyControl

xrandr --setprovideroutputsource modesetting NVIDIA-0
xrandr --auto
'''

# function declaration

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--status', action='store_true', help='Query the current graphics mode set by EnvyControl')
    parser.add_argument('--switch', type=str, metavar='MODE', action='store',
                        help='Switch the graphics mode. You need to reboot for changes to apply. Supported modes: integrated, nvidia, hybrid')
    parser.add_argument('--dm', type=str, metavar='DISPLAY_MANAGER', action='store',
                        help='Manually specify your Display Manager. This is required only for systems without systemd. Supported DMs: gdm, sddm, lightdm')
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
        if args.dm and args.switch == 'nvidia':
            _switcher(args.switch, args.dm)
        else:
            _switcher(args.switch)
    elif args.dm and not args.switch:
        print('Error: this option is intended to be used with --switch nvidia')
        print('Example: sudo envycontrol --switch nvidia --dm sddm')
        sys.exit(1)

def _check_root():
    if not os.geteuid() == 0:
        print('Error: this operation requires root privileges')
        sys.exit(1)

def _check_status():
    if os.path.exists(BLACKLIST_PATH) and os.path.exists(UDEV_PATH):
        mode = 'integrated'
    elif os.path.exists(XORG_PATH) and os.path.exists(NVIDIA_MODESET_PATH):
        mode = 'nvidia'
    else:
        mode = 'hybrid'
    print(f'Current graphics mode is: {mode}')

def _file_remover():
    # utility function to cleanup environment before setting any mode
    # don't raise warning if file is not found
    try:
        os.remove(BLACKLIST_PATH)
    except OSError as e:
        if e.errno != 2:
            print(f'Error: {e}')
            sys.exit(1)
    try:
        os.remove(UDEV_PATH)
    except OSError as e:
        if e.errno != 2:
            print(f'Error: {e}')
            sys.exit(1)
    try:
        os.remove(XORG_PATH)
    except OSError as e:
        if e.errno != 2:
            print(f'Error: {e}')
            sys.exit(1)
    try:
        os.remove(NVIDIA_MODESET_PATH)
    except OSError as e:
        if e.errno != 2:
            print(f'Error: {e}')
            sys.exit(1)
    try:
        os.remove(SDDM_SCRIPT_PATH)
    except OSError as e:
        if e.errno != 2:
            print(f'Error: {e}')
            sys.exit(1)
    try:
        os.remove(LIGHTDM_SCRIPT_PATH)
    except OSError as e:
        if e.errno != 2:
            print(f'Error: {e}')
            sys.exit(1)

def _check_display_manager():
    # automatically detect the current Display Manager
    # this depends on systemd
    pattern = re.compile(r'(?<=/usr/bin/).*|(?<=/usr/sbin/).*')
    try:
        with open('/etc/systemd/system/display-manager.service',mode='r', encoding='utf-8') as f:
            display_manager = pattern.findall(f.read())[0]
    except Exception:
        print('Warning: automatic Display Manager detection is not available')
        display_manager = ''
    finally:
        return display_manager

def _setup_display_manager(display_manager):
    # setup the Xrandr script if necessary
    if display_manager == 'sddm':
        try:
            with open(SDDM_SCRIPT_PATH, mode='w', encoding='utf-8') as f:
                f.write(XRANDR_SCRIPT)
        except Exception as e:
            print(f'Error: {e}')
            sys.exit(1)
        subprocess.run(['chmod','+x',SDDM_SCRIPT_PATH], stdout=subprocess.DEVNULL)
    elif display_manager == 'lightdm':
        try:
            with open(LIGHTDM_SCRIPT_PATH, mode='w', encoding='utf-8') as f:
                f.write(XRANDR_SCRIPT)
        except Exception as e:
            print(f'Error: {e}')
            sys.exit(1)
        subprocess.run(['chmod','+x',LIGHTDM_SCRIPT_PATH], stdout=subprocess.DEVNULL)
    elif display_manager != ('' or 'gdm' or 'gdm3'):
        print('Error: provided Display Manager is not valid')
        print('Supported Display Managers: gdm, sddm, lightdm')
        sys.exit(1)

def _rebuild_initramfs():
    # Debian and its derivatives require rebuilding the initramfs after switching modes
    is_debian = os.path.exists('/etc/debian_version')
    if is_debian:
        print('Rebuilding initramfs...')
        p = subprocess.run(['update-initramfs', '-u', '-k', 'all'], stdout=subprocess.DEVNULL)
        if p.returncode == 0:
            print('Successfully rebuilt initramfs!')
        else:
            print('Error: an error ocurred rebuilding the initramfs')

def _switcher(mode, display_manager = ''):
    # exit if not running as root
    _check_root()

    if mode == 'integrated':
        _file_remover()
        try:
            # blacklist all nouveau and Nvidia modules
            with open(BLACKLIST_PATH, mode='w', encoding='utf-8') as f:
                f.write(BLACKLIST_CONTENT)
            # power off the Nvidia GPU with Udev rules
            with open(UDEV_PATH, mode='w', encoding='utf-8') as f:
                f.write(UDEV_CONTENT)
        except Exception as e:
            print(f'Error: {e}')
            sys.exit(1)
        _rebuild_initramfs()
    
    elif mode == 'nvidia':
        _file_remover()
        # detect Display Manager if not provided
        if display_manager == '':
            display_manager = _check_display_manager()
        _setup_display_manager(display_manager)
        try:
            # create X.org config
            with open(XORG_PATH, mode='w', encoding='utf-8') as f:
                f.write(XORG_CONTENT)
            # modeset for Nvidia driver is required to prevent tearing on internal screen
            with open(NVIDIA_MODESET_PATH, mode='w', encoding='utf-8') as f:
                f.write(NVIDIA_MODESET_CONTENT)
        except Exception as e:
            print(f'Error: {e}')
            sys.exit(1)
        _rebuild_initramfs()
    
    elif mode == 'hybrid':
        # remove all files created by other EnvyControl modes
        # Nvidia and nouveau drivers fallback to hybrid mode by default
        _file_remover()
        _rebuild_initramfs()
        
    else:
        print('Error: provided graphics mode is not valid')
        print('Supported modes: integrated, nvidia, hybrid')
        sys.exit(1)

    print(f'Graphics mode set to: {mode}')
    print('Please reboot your computer for changes to apply')

def _print_version():
        print(f'EnvyControl {VERSION}')

if __name__ == '__main__':
    main()

#!/usr/bin/env python
import argparse
import sys
import os
import re
import subprocess

# constants declaration

VERSION = '1.3.1'

# for integrated mode

BLACKLIST_PATH = '/etc/modprobe.d/blacklist-nvidia.conf'
BLACKLIST_CONTENT = '''# Do not modify this file
# Generated by EnvyControl

blacklist nouveau
blacklist nvidia
blacklist nvidia_drm
blacklist nvidia_uvm
blacklist nvidia_modeset

alias nouveau off
alias nvidia off
alias nvidia_drm off
alias nvidia_uvm off
alias nvidia_modeset off
'''

UDEV_PATH = '/lib/udev/rules.d/50-remove-nvidia.rules'
UDEV_CONTENT = '''# Do not modify this file
# Generated by EnvyControl

# Remove NVIDIA USB xHCI Host Controller devices, if present
ACTION=="add", SUBSYSTEM=="pci", ATTR{vendor}=="0x10de", ATTR{class}=="0x0c0330", ATTR{power/control}="auto", ATTR{remove}="1"

# Remove NVIDIA USB Type-C UCSI devices, if present
ACTION=="add", SUBSYSTEM=="pci", ATTR{vendor}=="0x10de", ATTR{class}=="0x0c8000", ATTR{power/control}="auto", ATTR{remove}="1"

# Remove NVIDIA Audio devices, if present
ACTION=="add", SUBSYSTEM=="pci", ATTR{vendor}=="0x10de", ATTR{class}=="0x040300", ATTR{power/control}="auto", ATTR{remove}="1"

# Finally, remove the NVIDIA dGPU
ACTION=="add", SUBSYSTEM=="pci", ATTR{vendor}=="0x10de", ATTR{class}=="0x03[0-9]*", ATTR{power/control}="auto", ATTR{remove}="1"
'''

# for Nvidia mode

XORG_PATH = '/etc/X11/xorg.conf.d/90-nvidia.conf'

XORG_CONTENT_INTEL = '''# Do not modify this file
# Generated by EnvyControl

Section "ServerLayout"
    Identifier "layout"
    Screen 0 "nvidia"
    Inactive "intel"
EndSection

Section "Device"
    Identifier "nvidia"
    Driver "nvidia"
    BusID "PCI:{}"
EndSection

Section "Screen"
    Identifier "nvidia"
    Device "nvidia"
    Option "AllowEmptyInitialConfiguration"
EndSection

Section "Device"
    Identifier "intel"
    Driver "modesetting"
EndSection

Section "Screen"
    Identifier "intel"
    Device "intel"
EndSection
'''

XORG_CONTENT_AMD = '''# Do not modify this file
# Generated by EnvyControl

Section "ServerLayout"
    Identifier "layout"
    Screen 0 "nvidia"
    Inactive "amdgpu"
EndSection

Section "Device"
    Identifier "nvidia"
    Driver "nvidia"
    BusID "PCI:{}"
EndSection

Section "Screen"
    Identifier "nvidia"
    Device "nvidia"
    Option "AllowEmptyInitialConfiguration"
EndSection

Section "Device"
    Identifier "amdgpu"
    Driver "amdgpu"
EndSection

Section "Screen"
    Identifier "amd"
    Device "amdgpu"
EndSection
'''

NVIDIA_MODESET_PATH = '/etc/modprobe.d/nvidia.conf'

NVIDIA_MODESET_CONTENT = '''# Do not modify this file
# Generated by EnvyControl
options nvidia-drm modeset=1
'''

# SDDM and LightDM require additional setup for Nvidia mode

XRANDR_SCRIPT_INTEL = '''#!/bin/sh

# Do not modify this file
# Generated by EnvyControl

xrandr --setprovideroutputsource modesetting NVIDIA-0
xrandr --auto
'''

SDDM_SCRIPT_PATH = '/usr/share/sddm/scripts/Xsetup'

LIGHTDM_SCRIPT_PATH = '/etc/lightdm/nvidia.sh'

LIGHTDM_CONFIG_PATH = '/etc/lightdm/lightdm.conf.d/20-nvidia.conf'

LIGHTDM_CONFIG_CONTENT = '''# Do not modify this file
# Generated by EnvyControl

[Seat:*]
display-setup-script=/etc/lightdm/nvidia.sh
'''

# function declaration

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
    try:
        os.remove(LIGHTDM_CONFIG_PATH)
    except OSError as e:
        if e.errno != 2:
            print(f'Error: {e}')
            sys.exit(1)

def _get_igpu_vendor():
    # automatically detect whether Intel or AMD iGPU is present
    pattern_intel = re.compile(r'(VGA).*(Intel)')
    pattern_amd = re.compile(r'(VGA).*(ATI|AMD|AMD\/ATI)')
    lspci = subprocess.run(['lspci'], capture_output=True, text=True).stdout
    if pattern_intel.findall(lspci):
        return 'intel'
    elif pattern_amd.findall(lspci):
        return 'amd'
    else:
        print('Error: could not find Intel or AMD iGPU')
        sys.exit(1)

def _get_amd_igpu_name():    
    pattern = re.compile(r'(name:).*(ATI*|AMD*|AMD\/ATI)*')
    xrandr = subprocess.run(['xrandr', '--listproviders'], capture_output=True, text=True).stdout

    if pattern.findall(xrandr):
        name = re.search(pattern, xrandr).group(0)[5:]
    else:
        name = "Error: could not find AMD iGPU"
    return name

def _get_xrandr_script_amd():
    name = _get_amd_igpu_name()
    xrandr_script = f'''#!/bin/sh

# Do not modify this file
# Generated by EnvyControl

xrandr --setprovideroutputsource "{name}" NVIDIA-0
xrandr --auto
'''
    return xrandr_script


def _get_pci_bus():
    # dynamically get the PCI bus of the Nvidia dGPU
    # exit if not found
    pattern = re.compile(r'([0-9]{2}:[0-9a-z]{2}.[0-9]).*(VGA compatible controller: NVIDIA|3D controller: NVIDIA)')
    lspci = subprocess.run(['lspci'], capture_output=True, text=True).stdout
    try:
        # X.org requires PCI:X:X:X format
        return ':'.join([str(int(element)) for element in pattern.findall(lspci)[0][0].replace('.', ':').split(':')])
    except Exception:
        print('Error: could not find Nvidia GPU on PCI bus, please switch to hybrid mode first')
        sys.exit(1)

def _check_display_manager():
    # automatically detect the current Display Manager
    # this depends on systemd
    pattern = re.compile(r'(\/usr\/bin\/|\/usr\/sbin\/)(.*)')
    try:
        with open('/etc/systemd/system/display-manager.service',mode='r', encoding='utf-8') as f:
            display_manager = pattern.findall(f.read())[0][1]
    except Exception:
        display_manager = ''
        print('Warning: automatic Display Manager detection is not available')
    finally:
        return display_manager

def _setup_display_manager(display_manager):
    # setup the Xrandr script if necessary
    # get igpu vendor to use if needed
    igpu_vendor = _get_igpu_vendor()
    
    # if amd igpu generate xrandr script for AMD iGPU
    if igpu_vendor == "amd":
        xrandr_script_amd = _get_xrandr_script_amd()

    if display_manager == 'sddm':
        try:
            with open(SDDM_SCRIPT_PATH, mode='w', encoding='utf-8') as f:
                if igpu_vendor == "amd":
                    f.write(xrandr_script_amd)
                else:
                    f.write(XRANDR_SCRIPT_INTEL)
        except Exception as e:
            print(f'Error: {e}')
            sys.exit(1)
        subprocess.run(['chmod','+x',SDDM_SCRIPT_PATH], stdout=subprocess.DEVNULL)
    elif display_manager == 'lightdm':
        try:
            with open(LIGHTDM_SCRIPT_PATH, mode='w', encoding='utf-8') as f:
                if igpu_vendor == "amd":
                    f.write(xrandr_script_amd)
                else:
                    f.write(XRANDR_SCRIPT_INTEL)
        except Exception as e:
            print(f'Error: {e}')
            sys.exit(1)
        subprocess.run(['chmod','+x',LIGHTDM_SCRIPT_PATH], stdout=subprocess.DEVNULL)
        # create config
        if not os.path.exists(os.path.dirname(LIGHTDM_CONFIG_PATH)):
            try:
                os.makedirs(os.path.dirname(LIGHTDM_CONFIG_PATH))
            except Exception as e:
                print(f'Error: {e}')
                sys.exit(1)
        with open(LIGHTDM_CONFIG_PATH, mode='w', encoding='utf-8') as f:
                    f.write(LIGHTDM_CONFIG_CONTENT)
    elif display_manager not in ['', 'gdm', 'gdm3']:
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
        # detect if Intel or AMD iGPU
        igpu_vendor = _get_igpu_vendor()
        # get the Nvidia dGPU PCI bus
        pci_bus = _get_pci_bus()
        # detect Display Manager if not provided
        if display_manager == '':
            display_manager = _check_display_manager()
        _setup_display_manager(display_manager)
        try:
            # create X.org config
            with open(XORG_PATH, mode='w', encoding='utf-8') as f:
                if igpu_vendor == 'intel':
                    f.write(XORG_CONTENT_INTEL.format(pci_bus))
                elif igpu_vendor == 'amd':
                    f.write(XORG_CONTENT_AMD.format(pci_bus))
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
        # modeset for Nvidia driver is required for Wayland on hybrid mode
        with open(NVIDIA_MODESET_PATH, mode='w', encoding='utf-8') as f:
            f.write(NVIDIA_MODESET_CONTENT)
        _rebuild_initramfs()
        
    else:
        print('Error: provided graphics mode is not valid')
        print('Supported modes: integrated, nvidia, hybrid')
        sys.exit(1)

    print(f'Graphics mode set to: {mode}')
    print('Please reboot your computer for changes to apply')

def _print_version():
        print(f'EnvyControl {VERSION}')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--status', action='store_true', help='Query the current graphics mode set by EnvyControl')
    parser.add_argument('--switch', type=str, metavar='MODE', action='store',
                        help='Switch the graphics mode. You need to reboot for changes to apply. Supported modes: integrated, nvidia, hybrid')
    parser.add_argument('--amdigpu', action='store_true', help='Check if your amd igpu name is reported correctly')
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
    elif args.amdigpu:
        print(_get_amd_igpu_name())
    elif args.switch:
        if args.dm and args.switch == 'nvidia':
            _switcher(args.switch, args.dm)
        else:
            _switcher(args.switch)
    elif args.dm and not args.switch:
        print('Error: this option is intended to be used with --switch nvidia')
        print('Example: sudo envycontrol --switch nvidia --dm sddm')
        sys.exit(1)

if __name__ == '__main__':
    main()

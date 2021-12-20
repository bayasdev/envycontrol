# EnvyControl

# Introduction

EnvyControl is a program aimed to provide an easy way to switch GPU modes on Nvidia Optimus systems (i.e laptops with Intel + Nvidia or AMD + Nvidia configurations) under Linux.

## Compatible distros

**This program was developed for Arch Linux** but it should work on any other Linux distribution.

Debian and Ubuntu derivates might require rebuilding the initramfs after switching modes, you can rebuild the initramfs by running `sudo update-initramfs -u -k all`.

## Tested devices
- Acer Predator Helios 300 2017 (G3-571)
    - Intel Core i7-7700HQ
    - Intel HD630 iGPU
    - Nvidia GTX 1060 dGPU
    - Arch Linux with Gnome

## A note on AMD + Nvidia systems

I don't own any device with this particular hardware combination (in theory `integrated` and `hybrid` modes should work), please contact me if you do.

# Installation

Installation it's not required since you can directly run `envycontrol.py` from source, however for convenience sake you can install EnvyControl globally:

## From the AUR

Install [envycontrol](https://aur.archlinux.org/packages/envycontrol/) with the AUR helper of your choice.

## Using pip

1. Clone or download this GitHub repository
2. Run `sudo pip install .`

# Usage

```
usage: envycontrol [-h] [--status] [--switch MODE] [--version]

options:
  -h, --help     show this help message and exit
  --status       Query the current graphics mode set by EnvyControl
  --switch MODE  Switch the graphics mode. You need to reboot for changes to
                 apply. Supported modes: integrated, nvidia, hybrid
  --version, -v  Print the current version and exit
```

## Examples

Set graphics mode to `integrated` (disable the Nvidia GPU):

```
sudo envycontrol --switch integrated
```

Show the current graphics mode:

```
envycontrol --status
```

# Graphics modes explained

The current state of Nvidia Optimus laptops on Linux is sad, each mode comes with a downside so you may find yourself switching modes quite often.

## integrated

This mode will power off the Nvidia GPU by blacklisting the Nvidia and nouveau drivers, as well as removing the card from the PCI bus using Udev rules.

Since the dGPU is turned off your battery may last longer than on Windows, also you will be able to use Wayland and enjoy Linux without having to worry about overheating. **The downside is that you can't use any external screen because on most laptops the HDMI ports are wired to the dGPU.**

## nvidia

This mode will render both internal and external screens using the Nvidia GPU, it requires the propietary Nvidia drivers to be installed and currently it's only compatible with Intel + Nvidia systems.

It works by creating a X.org config file with the Intel iGPU attached to an inactive screen forcing the system to render all screens with the Nvidia dGPU. It will also enable modesetting for the Nvidia driver which is required for PRIME synchronzation.

**The downsides are that you can't use Wayland, your battery will drain in a couple of minutes, the laptop will overheat even if doing nothing and the fans will go brrrrr.**

**This is the recommended mode for working with external screens.**

## hybrid

This is the default behavior for both Nvidia and nouveau drivers, the dGPU can be accesed on-demand with `DRI_PRIME=1` for nouveau or `__NV_PRIME_RENDER_OFFLOAD=1 __VK_LAYER_NV_optimus=NVIDIA_only __GLX_VENDOR_LIBRARY_NAME=nvidia` for the propietary driver.

The propietary driver implements dynamic power management (like Windows) only on Turing and newer cards paired with Intel 8th+ gen processors. [Read the official documentation to enable it if you're eligible.](http://us.download.nvidia.com/XFree86/Linux-x86_64/495.46/README/dynamicpowermanagement.html)

**The downsides are poor battery life on cards that don't support dynamic power management (like mine), external screens are laggy due to a broken reverse PRIME implementation on X.org and Wayland crashes if an external screen is connected (tested on Gnome).**

Well, nouveau supports external screens on Wayland but it's laggy and prone to make your system crash.

## Closing words

**Don't buy Nvidia hardware!**

[![Linus Torvalds to Nvidia](https://img.youtube.com/vi/_36yNWw_07g/hqdefault.jpg)](https://youtu.be/_36yNWw_07g)

# EnvyControl

EnvyControl is a program aimed to provide an easy way to switch GPU modes on Nvidia Optimus systems (i.e laptops with Intel + Nvidia or AMD + Nvidia configurations) under Linux.

### License

Envycontrol is licensed under the MIT license which is a permissive, free software license (see <a href="https://github.com/geminis3/envycontrol/blob/main/LICENSE">LICENSE</a>).

### Compatible distros

EnvyControl should work on any distribution of Linux, see [tested distros](https://github.com/geminis3/envycontrol/wiki/Frequently-Asked-Questions#tested-distros).

**If you're using Ubuntu please [read this](https://github.com/geminis3/envycontrol/wiki/Frequently-Asked-Questions#a-note-for-ubuntu-users).**

### Supported display managers 

- GDM
- SDDM
- LightDM

If your display manager isn't currently supported by EnvyControl you might have to [manually configure it](https://github.com/geminis3/envycontrol/wiki/Frequently-Asked-Questions#what-to-do-if-my-display-manager-is-not-supported).

### A note for SDDM users

If `/usr/share/sddm/scripts/Xsetup` file is missing on your system please run `sudo envycontrol --reset_sddm`.

### Supported graphics modes

- integrated
- hybrid
- nvidia (X.org only)

Read a detailed explanation [here](https://github.com/geminis3/envycontrol/wiki/Frequently-Asked-Questions#graphics-modes-explained).

## Get EnvyControl

### Arch Linux and its derivatives

Install the [envycontrol](https://aur.archlinux.org/packages/envycontrol/) package from the AUR manually or by using an AUR helper:

```
# with Paru
paru -S envycontrol

# with Yay
yay -S envycontrol

# with Pamac (Manjaro)
pamac install envycontrol
```

Now you can run `sudo envycontrol -s <MODE>` to switch graphics modes.

### Other distros

- Clone this repository with `git clone https://github.com/geminis3/envycontrol.git` or download the latest tarball from the releases page.
- Run `sudo python envycontrol.py -s <MODE>` from the root of the repository to switch to a different graphics mode. 
 
You can also install EnvyControl globally as a pip package:

- From the root of the cloned repository run `sudo pip install .`
- Now you can run `sudo envycontrol -s <MODE>` from any directory to switch graphics modes.

## Usage

```
usage: envycontrol.py [-h] [-v] [-s MODE] [-q] [--dm DISPLAY_MANAGER] [--reset_sddm]

options:
  -h, --help            show this help message and exit
  -v, --version         show this program's version number and exit
  -s MODE, --switch MODE
                        switch the graphics mode, supported modes: integrated, hybrid, nvidia
  -q, --query           query the current graphics mode set by EnvyControl
  --dm DISPLAY_MANAGER  Manually specify your Display Manager. This is required only for systems without systemd. Supported DMs: gdm, sddm, lightdm
  --reset_sddm          restore original SDDM Xsetup file
```

### Examples

Set current graphics mode to `integrated` (power off the Nvidia dGPU):

```
sudo envycontrol -s integrated
```

Set current graphics mode to `nvidia` (automatic display manager setup)

```
sudo envycontrol -s nvidia
```

Set current graphics mode to `nvidia` and setup `SDDM` display manager

```
sudo envycontrol -s nvidia --dm sddm
```

Query the current graphics mode:

```
envycontrol --query
```

### Gnome Extension

The [GPU profile selector](https://github.com/LorenzoMorelli/GPU_profile_selector) extension provides a simple way to switch between graphics modes in a few clicks, you can get it from [here](https://extensions.gnome.org/extension/5009/gpu-profile-selector/).

PD: Just make sure to have EnvyControl installed globally ;)

![gpu profile selector screenshot](https://github.com/LorenzoMorelli/GPU_profile_selector/raw/main/extension_screenshot.png)

## New in 2.0

The following options can now be enabled when switching graphics mode:

### hybrid

- RTD3 power management (for Turing and newer GPUs)

### nvidia

- ForceCompositionPipeline (fixes tearing on external screens wired to the Nvidia GPU)
- Coolbits (allows overclocking on supported GPUs)

## Frequently Asked Questions

[See here](https://github.com/geminis3/envycontrol/wiki/Frequently-Asked-Questions).

Also read [fixes for some common problems](https://github.com/DaVikingMan/EnvyControl/wiki/Fixes-for-some-common-problems)

## What to do if you have found a bug

Feel free to open an issue, don't forget to provide some basic info.

- Linux distribution
- Linux kernel version and type
- Desktop Environment or Window Manager as well as your Display Manager
- Nvidia driver version
- EnvyControl version

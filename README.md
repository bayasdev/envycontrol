# EnvyControl

```
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED
```

## Introduction ℹ️

EnvyControl is a program aimed to provide an easy way to switch GPU modes on Nvidia Optimus systems (i.e laptops with Intel + Nvidia or AMD + Nvidia configurations) under Linux.

### Compatible distros 🐧

**This program was originally developed for Arch Linux** but it should work on any other Linux distribution.

On Debian and Ubuntu derivates the initramfs is rebuilt automatically after switching modes.

### Compatible display managers 🖥

- GDM
- SDDM
- LightDM

Other display managers might require [manual configuration](https://github.com/geminis3/envycontrol/wiki/Frequently-Asked-Questions#what-to-do-if-my-display-manager-is-not-supported-%EF%B8%8F).

### Supported graphics modes 🖼

- integrated
- nvidia
- hybrid

Read a detailed explanation [here](https://github.com/geminis3/envycontrol/wiki/Frequently-Asked-Questions#what-to-do-if-my-display-manager-is-not-supported-%EF%B8%8F).

### Tested devices 💻

- Acer Predator Helios 300 2017 (G3-571)
    - CPU: Intel Core i7-7700HQ
    - iGPU: Intel HD630
    - dGPU: Nvidia GTX 1060
    - OS: Arch Linux with Gnome

### A note on AMD + Nvidia systems ⚠️

I don't own any device with this particular hardware combination (in theory `integrated` and `hybrid` modes should work), please contact me if you do.

## Get EnvyControl ⬇️

Install the [envycontrol](https://aur.archlinux.org/packages/envycontrol/) package with the AUR helper of your choice. If not on Arch Linux you can run `envycontrol.py` from source.

## Usage 📖

```
usage: envycontrol.py [-h] [--status] [--switch MODE] [--dm DISPLAY_MANAGER] [--version]

options:
  -h, --help            show this help message and exit
  --status              Query the current graphics mode set by EnvyControl
  --switch MODE         Switch the graphics mode. You need to reboot for changes to apply. Supported modes: integrated, nvidia, hybrid
  --dm DISPLAY_MANAGER  Manually specify your Display Manager. This is required only for systems without systemd. Supported DMs: gdm, sddm, lightdm
  --version, -v         Print the current version and exit
```

### Examples 🚀

Set graphics mode to `integrated` (disable the Nvidia GPU):

```
sudo envycontrol --switch integrated
```

Set graphics mode to `nvidia` (automatic display manager detection):

```
sudo envycontrol --switch nvidia
```

Manually specify your display manager for `nvidia` mode (useful for non-systemd users):

```
sudo envycontrol --switch nvidia --dm sddm
```

Show the current graphics mode:

```
envycontrol --status
```

## Frequently Asked Questions ❓

Of course, [see here](https://github.com/geminis3/envycontrol/wiki/Frequently-Asked-Questions).

## I found a bug 🐞

Feel free to open an issue, don't forget to provide some basic info.

- Linux distribution
- Desktop Environment or Window Manager as well as your Display Manager
- Nvidia drivers version
- EnvyControl version

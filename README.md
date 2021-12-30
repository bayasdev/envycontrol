# EnvyControl

EnvyControl is a program aimed to provide an easy way to switch GPU modes on Nvidia Optimus systems (i.e laptops with Intel + Nvidia or AMD + Nvidia configurations) under Linux.

### License

Envycontrol is licensed under the MIT license which is a permissive, free software license (see <a href="https://github.com/geminis3/envycontrol/blob/main/LICENSE">LICENSE</a>).

### Compatible distros

**This program was originally developed for Arch Linux** but it should work on any other Linux distribution.

On Debian and Ubuntu derivates the initramfs is rebuilt automatically after switching modes.

### Compatible display managers

The following display managers are currently compatible with envycontrol : 

- GDM
- SDDM
- LightDM

If your display manager isn't currently supported by envycontrol, you might have to [manually configure it](https://github.com/geminis3/envycontrol/wiki/Frequently-Asked-Questions#what-to-do-if-my-display-manager-is-not-supported).

### Supported graphics modes

- integrated
- nvidia
- hybrid

Read a detailed explanation [here](https://github.com/geminis3/envycontrol/wiki/Frequently-Asked-Questions#graphics-modes-explained).

### Tested devices

- Acer Predator Helios 300 2017 (G3-571)
    - CPU: Intel Core i7-7700HQ
    - iGPU: Intel HD630
    - dGPU: Nvidia GTX 1060
    - OS: Arch Linux with Gnome

### A note on AMD + Nvidia systems

I don't own any device with this hardware combination, however experimental support for AMD systems under `nvidia` mode has been added. **Please send me your feedback.**

## Get EnvyControl

If you're on archlinux, you can install the [envycontrol](https://aur.archlinux.org/packages/envycontrol/) package from AUR by running:

- `git clone https://aur.archlinux.org/envycontrol.git`
- `cd /path/to/envycontrol`
- `makepkg -si`

OR

- `paru -S envycontrol` or by using the aur helper of your choice

If not on Arch Linux, you would have to:

- Run `git clone https://github.com/geminis3/envycontrol.git` in a terminal window or install the tarball from the release page
- Run `sudo python envycontrol.py --switch <MODE>` in the root of the repository to switch to a different graphic mode.
 
 OR
 
- Extract the tarball with `tar -xvf envycontrol-version.tar.gz`
- And run `sudo python envycontrol.py --switch <MODE>` to switch graphic modes.

## Usage

```
usage: envycontrol.py [-h] [--status] [--switch MODE] [--dm DISPLAY_MANAGER] [--version]

options:
  -h, --help            show this help message and exit
  --status              Query the current graphics mode set by EnvyControl
  --switch MODE         Switch the graphics mode. You need to reboot for changes to apply. Supported modes: integrated, nvidia, hybrid
  --dm DISPLAY_MANAGER  Manually specify your Display Manager. This is required only for systems without systemd. Supported DMs: gdm, sddm, lightdm
  --version, -v         Print the current version and exit
```

### Examples

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

## Frequently Asked Questions

[See here](https://github.com/geminis3/envycontrol/wiki/Frequently-Asked-Questions).

## What to do if you have found a bug

Feel free to open an issue, don't forget to provide some basic info.

- Linux distribution
- Desktop Environment or Window Manager as well as your Display Manager
- Nvidia drivers version
- EnvyControl version

# EnvyControl

EnvyControl is a program aimed to provide an easy way to switch GPU modes on Nvidia Optimus systems (i.e laptops with Intel + Nvidia or AMD + Nvidia configurations) under Linux.

### License

Envycontrol is licensed under the MIT license which is a permissive, free software license (see <a href="https://github.com/geminis3/envycontrol/blob/main/LICENSE">LICENSE</a>).

### Compatible distros

**This program was originally developed for Arch Linux** but it should work on any other Linux distribution.

For a detailed list of tested distros [see here](https://github.com/geminis3/envycontrol/wiki/Frequently-Asked-Questions#tested-distros).

**If you're using Ubuntu please [read this](https://github.com/geminis3/envycontrol/wiki/Frequently-Asked-Questions#a-note-for-ubuntu-users).**

### Supported display managers 

- GDM
- SDDM
- LightDM

If your display manager isn't currently supported by EnvyControl, you might have to [manually configure it](https://github.com/geminis3/envycontrol/wiki/Frequently-Asked-Questions#what-to-do-if-my-display-manager-is-not-supported).

### Supported graphics modes

- integrated
- nvidia
- hybrid

Read a detailed explanation [here](https://github.com/geminis3/envycontrol/wiki/Frequently-Asked-Questions#graphics-modes-explained).

### A note on AMD + Nvidia systems

I don't own any device with this hardware combination, however experimental support for AMD systems under `nvidia` mode has been added. **Please send me your feedback.**

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

Now you can run `sudo envycontrol --switch <MODE>` to switch graphics modes.

### Other distros

- Clone this repository with `git clone https://github.com/geminis3/envycontrol.git` or download the latest tarball from the releases page.
- Run `sudo python envycontrol.py --switch <MODE>` from the root of the repository to switch to a different graphics mode. 
 
You can also install EnvyControl globally as a pip package:

- From the root of the cloned repository run `sudo pip install .`
- Now you can run `sudo envycontrol --switch <MODE>` from any directory to switch graphics modes.

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

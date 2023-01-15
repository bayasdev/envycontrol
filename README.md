<div align="center">
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./logos/dark.png">
  <img alt="EnvyControl Logo" src="./logos/light.png" height="100px">
</picture>
</div>
<br>

# 👁‍🗨 EnvyControl

EnvyControl is a program aimed to provide an easy way to switch GPU modes on Nvidia Optimus systems (i.e laptops with hybrid Intel + Nvidia or AMD + Nvidia graphics configurations) under Linux.

### 📖 License

EnvyControl is free and open-source software released under the [MIT](https://github.com/bayasdev/envycontrol/blob/main/LICENSE) license.

### ⚠️ Disclaimer

**This software is provided 'as-is' without any express or implied warranty.** 

Keep it mind any custom X.org configuration may get deleted or overwritten when switching modes, please review this README and the source code before proceeding.

## 🐧 Compatible distros

EnvyControl should work on any distribution of Linux, see [tested distros](https://github.com/bayasdev/envycontrol/wiki/Frequently-Asked-Questions#tested-distros).

**If you're using Ubuntu or its derivatives please follow [these instructions](https://github.com/bayasdev/envycontrol/wiki/Frequently-Asked-Questions#instructions-for-ubuntu-and-its-derivatives).**

### 🖥️ Supported display managers 

- GDM
- SDDM
- LightDM

If your display manager isn't currently supported by EnvyControl you might have to [manually configure it](https://github.com/bayasdev/envycontrol/wiki/Frequently-Asked-Questions#what-to-do-if-my-display-manager-is-not-supported).

## 💡 Tips

### Wayland session is missing on Gnome 43+

Latest changes in GDM now require `NVreg_PreserveVideoMemoryAllocations` kernel parameter to be set to 1 as well as `nvidia-suspend` services to be enabled for Wayland sessions to appear.

```
# 1. Re-run EnvyControl 2.2+ (either nvidia or hybrid mode)
sudo envycontrol -s nvidia

# 2. Now enable the required Nvidia services
sudo systemctl enable nvidia-{suspend,resume,hibernate}

# 3. Reboot
```

### `/usr/share/sddm/scripts/Xsetup` is missing on my system

Please run `sudo envycontrol --reset-sddm`.

## ⬇️ Getting EnvyControl

### Arch Linux ([AUR](https://aur.archlinux.org/packages/envycontrol))
1. `yay -S envycontrol`.
2. Run `sudo envycontrol -s <MODE>` to switch graphics modes.

### From source

1. Clone this repository with `git clone https://github.com/bayasdev/envycontrol.git` or download the latest tarball from the releases page.
2. Run `sudo python envycontrol.py -s <MODE>` from the root of the repository to switch to a different graphics mode. 
 
### Install globally as a pip package

- From the root of the cloned repository run `sudo pip install .`
- Now you can run `sudo envycontrol -s <MODE>` from any directory to switch graphics modes.

## ⚡️ Usage

```
usage: envycontrol.py [-h] [-v] [-s MODE] [-q] [--dm DISPLAY_MANAGER] [--reset] [--reset-sddm]

options:
  -h, --help            show this help message and exit
  -v, --version         show this program's version number and exit
  -s MODE, --switch MODE
                        switch the graphics mode, supported modes: integrated, hybrid, nvidia
  -q, --query           query the current graphics mode set by EnvyControl
  --dm DISPLAY_MANAGER  Manually specify your Display Manager. This is required only for systems without systemd.
                        Supported DMs: gdm, sddm, lightdm
  --reset               remove EnvyControl settings
  --reset-sddm          restore original SDDM Xsetup file
```

**Read a detailed explanation about EnvyControl graphics modes [here](https://github.com/bayasdev/envycontrol/wiki/Frequently-Asked-Questions#graphics-modes-explained).**

### Usage examples

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

## 📦 Gnome Extension

The [GPU profile selector](https://github.com/LorenzoMorelli/GPU_profile_selector) extension provides a simple way to switch between graphics modes in a few clicks, you can get it from [here](https://extensions.gnome.org/extension/5009/gpu-profile-selector/).

**Make sure to have EnvyControl installed globally!**

![gpu profile selector screenshot](https://github.com/LorenzoMorelli/GPU_profile_selector/raw/main/img/extension_screenshot.png)

## ❓ Frequently Asked Questions (FAQ)

- [See here](https://github.com/bayasdev/envycontrol/wiki/Frequently-Asked-Questions).

- Also read [fixes for some common problems](https://github.com/DaVikingMan/EnvyControl/wiki/Fixes-for-some-common-problems)

## 📝 Roadmap for v3

- [ ] Make customizable options available as switches (eg: RTD3, composition pipeline, etc).
- [ ] Nvidia mode on Wayland (Nvidia needs to fix their Linux drivers first).
- [ ] Plasma applet.
- [ ] COPR package.

## 🐞 I found a bug

Feel free to open an issue, don't forget to provide some basic info such as:

- Linux distribution
- Linux kernel version and type
- Desktop Environment or Window Manager as well as your Display Manager
- Nvidia driver version
- EnvyControl version

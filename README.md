<div align="center">
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://github.com/bayasdev/envycontrol/raw/main/logos/dark.png">
  <img alt="EnvyControl Logo" src="https://github.com/bayasdev/envycontrol/raw/main/logos/light.png" height="100px">
</picture>
<br>
Optimus made easy
</div>
<br>

# 👁‍🗨 EnvyControl

EnvyControl is a CLI tool that provides an easy way to switch between GPU modes on Nvidia Optimus systems (i.e laptops with hybrid Intel + Nvidia or AMD + Nvidia graphics configurations) under Linux.

### 📖 License

EnvyControl is free and open-source software released under the [MIT](https://github.com/bayasdev/envycontrol/blob/main/LICENSE) license.

### ⚠️ Disclaimer

**This software is provided 'as-is' without any express or implied warranty.**

Keep it mind any custom X.org configuration may get deleted or overwritten when switching modes.

## ✨ Features

- 🐍 Written in Python 3+ for portability and compatibility
- 🐧 Works across all major Linux distros ([tested distros](https://github.com/bayasdev/envycontrol/wiki/Frequently-Asked-Questions#tested-distros))
- 🖥️ Supports GDM, SDDM and LightDM display managers ([manual setup instructions](https://github.com/bayasdev/envycontrol/wiki/Frequently-Asked-Questions#what-to-do-if-my-display-manager-is-not-supported) also available)
- 🔋 Save battery with integrated graphics mode
- 💻 PCI-Express Runtime D3 (RTD3) Power Management support for Turing and later
- 🎮 Coolbits support for GPU overclocking
- 🔥 Fix screen tearing with ForceCompositionPipeline

## Graphics modes

## ⚡️ Usage

```
usage: envycontrol.py [-h] [-v] [-q] [-s MODE] [--dm DISPLAY_MANAGER] [--force-comp] [--coolbits [VALUE]] [--rtd3 [VALUE]] [--reset-sddm] [--reset] [--verbose]

options:
  -h, --help            show this help message and exit
  -v, --version         Output the current version
  -q, --query           Query the current graphics mode
  -s MODE, --switch MODE
                        Switch the graphics mode. Available choices: integrated, hybrid, nvidia
  --dm DISPLAY_MANAGER  Manually specify your Display Manager for Nvidia mode. Available choices: gdm, gdm3, sddm, lightdm
  --force-comp          Enable ForceCompositionPipeline on Nvidia mode
  --coolbits [VALUE]    Enable Coolbits on Nvidia mode. Default if specified: 28
  --rtd3 [VALUE]        Setup PCI-Express Runtime D3 (RTD3) Power Management on Hybrid mode. Available choices: 0, 1, 2, 3. Default if specified: 2
  --reset-sddm          Restore default Xsetup file
  --reset               Revert changes made by EnvyControl
  --verbose             Enable verbose mode
```

### 📖 Some examples

Set graphics mode to integrated:

```
sudo envycontrol -s integrated
```

Set graphics mode to hybrid and enable coarse-grained power control:

```
sudo envycontrol -s hybrid --rtd3
```

Set graphics mode to nvidia, enable ForceCompositionPipeline and Coolbits with a value of 24:

```
sudo envycontrol -s nvidia --force-comp --coolbits 24
```

Set current graphics mode to nvidia and specify to setup LightDM display manager

```
sudo envycontrol -s nvidia --dm lightdm
```

Query the current graphics mode:

```
envycontrol --query
```

Revert all changes made by EnvyControl:

```
sudo envycontrol --reset
```

## ⬇️ Getting EnvyControl

### Arch Linux ([AUR](https://aur.archlinux.org/packages/envycontrol))

1. `yay -S envycontrol`
2. Run `sudo envycontrol -s <MODE>` to switch graphics modes

### From source

1. Clone this repository with `git clone https://github.com/bayasdev/envycontrol.git` or download the latest tarball from the releases page
2. Run the script from the root of the repository like this `python envycontrol.py -s <MODE>`

💡 Replace `python` with `python3` on Ubuntu/Debian

### Install globally as a pip package

- From the root of the cloned repository run `sudo pip install .`
- Now you can run `sudo envycontrol -s <MODE>` from any directory to switch graphics modes.

## 📦 Gnome Extension

The [GPU profile selector](https://github.com/LorenzoMorelli/GPU_profile_selector) extension provides a simple way to switch between graphics modes in a few clicks, you can get it from [here](https://extensions.gnome.org/extension/5009/gpu-profile-selector/).

**Make sure to have EnvyControl installed globally!**

![gpu profile selector screenshot](https://github.com/LorenzoMorelli/GPU_profile_selector/raw/main/img/extension_screenshot.png)

## 💡 Tips

### Wayland session is missing on Gnome 43+

Latest changes in GDM now require `NVreg_PreserveVideoMemoryAllocations` kernel parameter to be set to 1 as well as `nvidia-suspend` services to be enabled for Wayland sessions to appear.

```
sudo systemctl enable nvidia-{suspend,resume,hibernate}
```

### `/usr/share/sddm/scripts/Xsetup` is missing on my system

Please run `sudo envycontrol --reset-sddm`.

## ❓ Frequently Asked Questions (FAQ)

[Read here](https://github.com/bayasdev/envycontrol/wiki/Frequently-Asked-Questions)

## 🐞 I found a bug

Feel free to open an issue, don't forget to provide some basic info such as:

- Linux distribution
- Linux kernel version and type
- Desktop Environment or Window Manager as well as your Display Manager
- Nvidia driver version
- EnvyControl version

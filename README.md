# RPI

--
RPI LED Matrix driving -- the new neon and video monitors

Works are started with running the player.py 

player.py takes 3 arguments:

1. device name or machine name (mname)
2. local path to where files are (can ./ if run from inside RPI)
3. the configuration to load in the form [config directory]/[config file name]

e.g. 
```python3 player.py -path . -mname studio -cfg prod/p4-4x7-slope-quilt..cfg&```


--> Config files specify which work to play. <br>
--> "Works" are located in the /pieces/ directory with some shared classes in the /modules/ directory
--> The pieces_modules contains versions of pieces that can be used when playing multiple pieces
    simultaneously i.e. the multiplayer - to layer or combine different works into the same window

There is also a working TKinter demo app used to launch various works in progress
```python3 cntrlscripts/full_list.py&```


Set up the environment:

On a Mac
Python3 with Tkinter, python3-pil, numpy, noise
matplotlib, scipy

Lubuntu / Linux flavors -
As of 2022 using Linux Mint for most things

--> these are not necessary with Linux Mint
sudo apt-get remove xfce4-power-manager
sudo apt install gnome-power-manager
gsettings set org.gnome.settings-daemon.plugins.power button-power shutdown
sudo apt-get install xscreensaver

--> basic setup
sudo apt-get update
sudo apt-get install git
sudo apt-get install openssh-server
sudo apt-get install python3-pip

sudo apt-get install python3-pil.imagetk
pip3 install numpy
pip3 install noise
pip3 install matplotlib
pip3 install scipy

git clone -b MAIN-PRODUCTION https://github.com/LukeMurphy/RPI.git


--> to have a piece startup when a machine boots up
if there is not an ~/.config/autostart directory already:
mkdir ~/.config/autostart

Make the startup script:
nano ~/.config/autostart/StartArt.desktop
```
[Desktop Entry]
Encoding=UTF-8
Name=startupscript
Comment=startupscript
Icon=gnome-info
Exec=python3 /home/daemon21/Documents/RPI/player.py -mname d21 -path /home/daemon21/Documents/RPI -cfg prod/p4-6x16-chimney-2.cfg
Terminal=false
Type=Application
Categories=
X-GNOME-Autostart-enabled=true
X-GNOME-Autostart-Delay=1
```
``` 

TEST --
python3 player.py -mname d11 -path ~/Documents/RPI -cfg p4-8x10/repeater.cfg&

--> older setups on Lubuntu needed this to prevent the screensaver kicking in
```
AUTOSTART
create folder & file
~/.config/autostart/startup0.desktop
[Desktop Entry]
Encoding=UTF-8
Name=startupscripto
Comment=startupscript_to_start_xscreensaver
Icon=gnome-info
Exec=xscreensaver
Terminal=false
Type=Application
Categories=
X-GNOME-Autostart-enabled=true
X-GNOME-Autostart-Delay=1
```


Overview
This Python script, player.py, is the main entry point for running LED art installations. It loads configuration files, initializes the system, and starts the artwork playback. It supports command-line arguments for specifying the configuration file, machine name, and an optional brightness override. The script is designed to be run directly and also supports reloading configurations.

Key Components
Configuration Loading: The script uses the configparser library to parse configuration files (.cfg). It prioritizes command-line arguments for specifying the config file path. If no configuration is provided via command line, it defaults to a hardcoded path and configuration. The configuration files contain settings for the artwork.
Command-line Arguments: The script uses argparse to handle command-line arguments:
-mname: Specifies the machine name (defaults to "local").
-path: Specifies the base directory for relative paths (defaults to "./").
-cfg: Specifies the path to the configuration file (required).
-brightnessOverride: An optional argument to override the brightness specified in the configuration file.
loadFromArguments() function: This function is the core of the initialization process. It reads the command-line arguments, loads the specified configuration file, and initializes the config object with the loaded settings. It also handles reloading configurations when called with the reloading parameter set to True.
player.configure(): This function, imported from the modules.player module, is called by loadFromArguments() to set up the artwork based on the loaded configuration. This is where the specific artwork logic is initialized and started.
main() function: The entry point of the script. It calls loadFromArguments() to start the process.
Default Configuration: If no -cfg argument is provided, the script defaults to loading a configuration specified by defaultpiece.defaultPieceToRun within the configs directory. This allows for a fallback behavior when no configuration is explicitly specified.
Error Handling: Basic error handling is implemented using try...except blocks to catch configuration loading errors.
Path Resolution: The script uses __file__ to determine the absolute path of the script's location, which is used to resolve relative paths in the configuration. This ensures that the script can be run from different locations without issues.

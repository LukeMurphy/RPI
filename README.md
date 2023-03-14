# RPI

--
RPI LED Matrix driving -- the new neon

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

git clone -b F22 https://github.com/LukeMurphy/RPI.git


--> to have a piece startup when a machine boots up
mkdir ~/.config/autostart
nano ~/.config/autostart/startup0.desktop

nano ~/.config/autostart/startup1.desktop
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
X-GNOME-Autostart-Delay=2
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




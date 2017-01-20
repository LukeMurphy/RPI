# RPI

--
RPI LED Matrix driving -- the new neon


Works are started with running the player.py 

e.g. 
```sudo python ./RPI/player.py studio-mac ./ configs/fludd.cfg&```
player.py takes 3 arguments:
1 - device name
2 - local path to where files are (can ./ if run from inside RPI)
3 - the configuration to load in the form [config directory]/[config file name]

Config files specify which work to play. 
"Works" are located in the /pieces/ directory


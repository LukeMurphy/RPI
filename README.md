# RPI

--
RPI LED Matrix driving -- the new neon
--- borrowing authority of lumens and color -
---
No illusions
---
The crontab

# -- Check if pause, change or shutdown is called from remote page
*/1 * * * * sudo python /home/pi/RPI/cntrlscripts/off_signal.py&

# -- RTC not running yet so times are UTC...
# -- Regular reboot every hour
0 15,16,17,18,19,20,21,22,23,0 * * * /home/pi/RPI/cntrlscripts/reboot.sh&

# -- Shut down at 8PM EST or 1AM UTC
0 1 * * * /home/pi/RPI/cntrlscripts/shutdown.sh&

# -- Run default animation
@reboot /home/pi/RPI/cntrlscripts/run.sh seq 3&

# -- Run test for off-button
@reboot sudo python /home/pi/RPI/cntrlscripts/stest.py&

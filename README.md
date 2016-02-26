# RPI

--
RPI LED Matrix driving -- the new neon
--- borrowing authority of lumens and color -
---
No illusions
---
The crontab
*/1 * * * * python /home/pi/RPI/cntrlscripts/off_signal.py&
0 */1 * * * /home/pi/RPI/cntrlscripts/reboot.sh&
@reboot /home/pi/RPI/cntrlscripts/run.sh seq 3&
@reboot sudo python /home/pi/RPI/cntrlscripts/stest.py&

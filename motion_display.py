#!/usr/bin/env python

import os
import time
import subprocess
import RPi.GPIO as GPIO


pir_pin = 23
button_light_pin = 12
shutoff_delay = 30  # seconds
GPIO.setmode(GPIO.BCM)
os.environ['DISPLAY'] = ":0"  # set the DISPLAY variable in the environment


def main():

    GPIO.setup(pir_pin, GPIO.IN)
    GPIO.setup(button_light_pin, GPIO.OUT)
    GPIO.output(button_light_pin, 1)  # turn button light ON
    display_on = True
    last_motion_time = time.time()

    while True:
        if GPIO.input(pir_pin):
            last_motion_time = time.time()
            if not display_on:
                # Power ON HDMI with preferred settings and force DPMS on
                subprocess.call('/opt/vc/bin/tvservice --preferred && xset dpms force on', shell=True)
                display_on = True
                GPIO.output(button_light_pin, 1)  # turn button light ON
        else:
            if display_on and time.time() > (last_motion_time + shutoff_delay):
                # Power OFF the display
                subprocess.call('/opt/vc/bin/tvservice -off', shell=True)
                display_on = False
                GPIO.output(button_light_pin, 0)  # turn button light OFF
        time.sleep(1)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        GPIO.cleanup()


"""
########################################################################################################################
# backlight stays on
os.system("xscreensaver-command -deactivate")  # turn screensaver off
os.system("xscreensaver-command -activate")  # turn screensaver on
subprocess.call('xscreensaver -no-splash')  # enable screensaver
subprocess.call('xset s off', shell=True)  # disable screen saver blanking
subprocess.call('xset s noblank', shell=True)  # disable blanking
subprocess.call('xset -dpms', shell=True)  # disable DPMS (Display Power Management Signaling)
subprocess.call('xset +dpms', shell=True)  # enable DPMS (Display Power Management Signaling)
subprocess.call('xset dpms force off', shell=True)  # Turn off screen immediately
subprocess.call('xset dpms force standby', shell=True)  # Standby screen
subprocess.call('xset dpms force suspend', shell=True)  # Suspend screen
########################################################################################################################

########################################################################################################################
# testing
/opt/vc/bin/tvservice --preferred  # Power on HDMI with preferred settings  # may produce blank screen after a few seconds
/opt/vc/bin/tvservice --preferred && xset dpms force on  # Power on HDMI with preferred settings  but requires command export DISPLAY=:0
/opt/vc/bin/tvservice --preferred && fbset -depth 8 && fbset -depth 16  # bring back the framebuffer
/opt/vc/bin/tvservice --preferred && xrefresh  # what does xrefresh do?

/opt/vc/bin/tvservice -off  # Power off the display  # but the monitor's menu temporarily comes up
vcgencmd display_power 0  # Power off the display  # but the monitor's menu temporarily comes up and consumes more energy than above
########################################################################################################################
"""
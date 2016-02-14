#!/usr/bin/env python

import time
import itertools
import RPi.GPIO as GPIO
from selenium import webdriver


def main():

    # GPIO configuration
    button_push_pin = 16
    button_light_pin = 12
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(button_push_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(button_light_pin, GPIO.OUT)
    GPIO.output(button_light_pin, 1)  # turn button light ON

    # Iceweasel configuration
    rkiosk_ext_file = "/home/pi/magicmirror/r_kiosk-0.9.0-fx.xpi"  # location of the "R-kiosk" extension
    profile = webdriver.FirefoxProfile()
    profile.add_extension(rkiosk_ext_file)
    driver = webdriver.Firefox(profile)
    driver.get('http://localhost/')
    websites_list = ['http://www.google.com', 'http://www.yahoo.com', 'http://localhost/']
    websites_cycle = itertools.cycle(websites_list)

    # Wait for button push
    try:
        while True:
            input_state = GPIO.input(button_push_pin)
            if not input_state:  # Button push
                GPIO.output(button_light_pin, 0)  # turn button light OFF
                driver.get(websites_cycle.next())  # load next website from list
                time.sleep(1)
                GPIO.output(button_light_pin, 1)  # turn button light ON
            else:
                time.sleep(0.1)
    except KeyboardInterrupt:
        GPIO.cleanup()
        driver.quit()

if __name__ == '__main__':
        main()
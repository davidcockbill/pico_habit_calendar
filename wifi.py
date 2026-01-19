#!/usr/bin/env python3

import time
import network
import ntptime
from wifi_config import WIFI_SSID, WIFI_PASSWORD


class Wifi:
    def __init__(self, context):
        self.context = context
        self.status = 'connecting'

    def sync_time(self):
        last_timestamp = time.ticks_ms()
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)

        connection_check_duration = 500
        retry = 0
        while True:
            timestamp = time.ticks_ms()
            if timestamp - last_timestamp > connection_check_duration:
                last_timestamp = timestamp
                if wlan.status() < 0 or wlan.status() >= 3:
                    break
                print(f'[{retry}] Waiting for wifi connection...')

            brightness_range = [70, 60, 50, 40, 30, 40, 50, 60]
            brightness = brightness_range[retry%8]
            self._display_wifi(brightness=brightness)
            time.sleep(0.1)
            retry += 1

        self.status = 'connected'
        print(self.status)
        self._display_wifi(max(brightness_range))

        self.status = 'setting time'    
        self._display_wifi(max(brightness_range))    
        while True:
            print(self.status)
            try:
                ntptime.settime()
                self.status = 'Time set'
                print(self.status)
                break
            except OSError as e:
                print(f'e={e}')
            time.sleep(0.05)

        wlan.disconnect()
        wlan.active(False)

    def display_status(self):
        self.context.set_pen(self.context.white())
        scale=2
        self.context.graphics.text(
            self.status,
            self.context.centre_text(self.status, scale=scale),
            200,
            scale=scale,
            spacing=1)

    def _display_wifi(self, brightness=50):
        foreground=self.context.blue()
        background=self.context.black()
        self.context.set_brightness(brightness)
        self.context.clear_display(background)

        band_width = 20
        bands = 8
    
        max_x = 320
        max_y = 240
        centre_x = int(max_x/2)
        centre_y = int(max_y/3) * 2

        # Concentric rings
        for band in reversed(range(bands)):
            if band % 2 == 0:
                self.context.graphics.set_pen(foreground)
            else:
                self.context.set_pen(background)
            radius = int((band_width * band) + band_width)
            self.context.graphics.circle(centre_x, centre_y, radius)

        # Cut off bottom of rings
        self.context.set_pen(background)
        self.context.graphics.rectangle(0, centre_y+1, max_x, max_y)

        #  Clear to 45 degrees
        self.context.graphics.triangle(centre_x, centre_y+1, 0, centre_y+1, 0, 0) # left triangle
        self.context.graphics.triangle(centre_x, centre_y+1, max_x, centre_y+1, max_x, 0) # right triangle

        # Centre circle
        self.context.graphics.set_pen(foreground)
        self.context.graphics.circle(centre_x, centre_y, band_width)

        self.display_status()

        self.context.update_display()
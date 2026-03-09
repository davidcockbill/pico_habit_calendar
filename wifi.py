#!/usr/bin/env python3

import time
import network
import ntptime
from wifi_config import WIFI_SSID, WIFI_PASSWORD


class Wifi:
    def __init__(self, context):
        self.context = context
        self.status = 'initialised'
        self.wlan = network.WLAN(network.STA_IF)

    def is_connected(self):
        return  self.wlan.status() < 0 or self.wlan.status() >= 3
    
    def is_time_set(self):
        return self.status is 'time set'
    
    def start_wifi(self):
        if self.wlan.active():
            self.wlan.active(False)
            time.sleep(0.5)

        self.wlan.active(True)
        time.sleep(1)

    def connect(self):
        self.status = 'connecting'
        last_timestamp = time.ticks_ms()

        self.start_wifi()

        print(f"Connecting to ssid='{WIFI_SSID}', pwd='{WIFI_PASSWORD}'")
        self.scan_wifi()
        self.wlan.connect(WIFI_SSID, WIFI_PASSWORD)

        connection_check_duration = 500
        retry = 0
        while retry < 20:
            timestamp = time.ticks_ms()
            if timestamp - last_timestamp > connection_check_duration:
                last_timestamp = timestamp
                if self.is_connected():
                    self.status = 'connected'
                    break
                status = self.wlan.status()
                print(f'[{retry}] Waiting for wifi connection. status={status}')

            brightness_range = [70, 60, 50, 40, 30, 40, 50, 60]
            brightness = brightness_range[retry%8]
            self._display_wifi(brightness=brightness)
            time.sleep(0.1)
            retry += 1

        print(f'retry={retry}, status={self.status}')
        self._display_wifi(max(brightness_range))

    def sync_time(self):
        self.status = 'setting time'
        retry = 0  
        while retry < 10 and self.is_connected():
            print(self.status)
            try:
                ntptime.settime()
                self.status = 'time set'
                print(self.status)
                break
            except OSError as e:
                print(f'e={e}')
            time.sleep(0.1)

    def scan_wifi(self):
        print('Scanning for available networks...')
        networks = self.wlan.scan()
        
        print(f"{'SSID':<20} | {'Channel':<7} | {'RSSI':<5} | {'Security'}")
        print("-" * 50)
        
        for net in networks:
            ssid = net[0].decode('utf-8')
            channel = net[2]
            rssi = net[3]
            sec = net[4]
            print(f'{ssid:<20} | {channel:<7} | {rssi:<5} | {sec}')

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
        self.context.set_brightness(brightness, verbose=False)
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
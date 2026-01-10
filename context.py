#!/usr/bin/env python3

import time
from machine import RTC
from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY_2


class Context:
    def __init__(self):
        self.graphics = PicoGraphics(display=DISPLAY_PICO_DISPLAY_2)
        self.rtc = RTC()

        self.pens = {
            'white': self.graphics.create_pen(255, 255, 255),
            'black': self.graphics.create_pen(0, 0, 0),
            'blue': self.graphics.create_pen(0, 0, 255),
            'dark_blue': self.graphics.create_pen(0, 0, 20),
            'dark_background_blue': self.graphics.create_pen(0, 0, 10),
            'green': self.graphics.create_pen(0, 255, 0),
            'light_green': self.graphics.create_pen(0, 80, 0),
            'dark_green': self.graphics.create_pen(0, 40, 0),
            'pink': self.graphics.create_pen(255, 20, 147),
            'orange': self.graphics.create_pen(255, 102, 0),
            'light_grey': self.graphics.create_pen(20, 20, 20),
        }

        self.graphics.set_font('bitmap8')

    def datetime(self):
        return self.rtc.datetime()

    def update_display(self):
        self.graphics.update()

    def set_brightness(self, brightness):
        print(f'Setting brightness to {brightness}')
        self.brightness = brightness
        self.graphics.set_backlight(self.brightness / 100)

    def increment_brightness(self):
        if (self.brightness < 100):
            self.set_brightness(self.brightness + 10)
 
    def decrement_brightness(self):
        if (self.brightness > 20):
            self.set_brightness(self.brightness - 10)

    def restore_brightness(self):
        self.set_brightness(self.brightness)

    def get_brightness(self):
        return self.brightness

    def clear_display(self, background=None):
        self.set_pen(self.black() if background is None else background)
        self.graphics.clear()

    def centre_text(self, text, scale=4):
        screen_width, _ = self.graphics.get_bounds()
        text_width = self.graphics.measure_text(text, scale)
        return int(max((screen_width - text_width)/2, 0))

    def set_pen(self, pen):
        self.graphics.set_pen(pen)

    def white(self):
        return self.pens.get('white')
    
    def black(self):
        return self.pens.get('black')

    def blue(self):
        return self.pens.get('blue')
    
    def dark_blue(self):
        return self.pens.get('dark_blue')
    
    def dark_background_blue(self):
        return self.pens.get('dark_background_blue')

    def green(self):
        return self.pens.get('green')
    
    def light_green(self):
        return self.pens.get('light_green')
    
    def dark_green(self):
        return self.pens.get('dark_green')
    
    def pink(self):
        return self.pens.get('pink')
        
    def orange(self):
        return self.pens.get('orange')
    
    def light_grey(self):
        return self.pens.get('light_grey')


#!/usr/bin/env python3

from machine import Pin
import time


class Button():
    A = 1
    B = 2
    X = 3
    Y = 4


class ButtonPress():
    NONE = 1
    SHORT = 2
    LONG = 3


class ButtonHandler:
    def __init__(self):
        self.short_press = 100
        self.long_press = 1000

        self.buttons = {
            Button.A: Pin(12, Pin.IN, Pin.PULL_UP),
            Button.B: Pin(13, Pin.IN, Pin.PULL_UP),
            Button.X: Pin(14, Pin.IN, Pin.PULL_UP),
            Button.Y: Pin(15, Pin.IN, Pin.PULL_UP),
        }

    def process_buttons(self):
        for button_id, pin in self.buttons.items():
            press = self._process_button(pin)
            if press is not ButtonPress.NONE:
                return button_id, press
        return None, ButtonPress.NONE

    def _process_button(self, pin):
        if pin.value() != 0:
            return ButtonPress.NONE

        start = time.ticks_ms()

        while pin.value() == 0:
            time.sleep_ms(1)

        duration = time.ticks_diff(time.ticks_ms(), start)

        if duration < self.short_press:
            return ButtonPress.NONE
        elif duration < self.long_press:
            return ButtonPress.SHORT
        else:
            return ButtonPress.LONG

#!/usr/bin/env python3

import time
from context import Context
from sugar_view import SugarView
from habit_calendar import HabitCalendar
from brightness import Brightness
from button_handler import ButtonHandler, ButtonPress, Button
from wifi_setup import WifiSetup

class Controller:
    def __init__(self):
        self.context = Context()
        self.page_idx = 0
        self.page = [
            SugarView(self.context),
            HabitCalendar(self.context),
            Brightness(self.context),
            WifiSetup(self.context),
        ]
        self.wifi_setup_idx = next(i for i, p in enumerate(self.page) if isinstance(p, WifiSetup))
        self.button_handler = ButtonHandler()

    def connect_wifi(self):
        from wifi import Wifi
        connected = False
        wifi = Wifi(self.context)
        wifi.connect()
        if wifi.is_connected():
            connected = True
            wifi.sync_time()            
        else:
            print('Wifi down')
        return connected
        
    def run(self):
        if not self.connect_wifi():
            self.page_idx = self.wifi_setup_idx
        self.context.set_brightness(70)
        self._current_page().enter()
        while True:
            self._loop()
            time.sleep(0.001)

    def _loop(self):
        button, press = self.button_handler.process_buttons()
        if press is not ButtonPress.NONE:
            if button is Button.A:
                self._increment_page()
            else:
                self._current_page().button_pressed(button, press)
        self._current_page().refresh_display()

    def _current_page(self):
        return self.page[self.page_idx]
    
    def _increment_page(self):
        self.page_idx = (self.page_idx + 1) % len(self.page)
        self._current_page().enter()


if __name__ == "__main__":
    Controller().run()


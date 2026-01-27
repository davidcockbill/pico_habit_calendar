#!/usr/bin/env python3
from libre_link import LibreLink
from arrows import draw_arrow
import time
from context import Context
from wifi import Wifi
from libre_config import USER, PASSWORD

     
class SugarView:
    def __init__(self, context):
        self.context = context
        self.libre_link = LibreLink(user=USER, pwd=PASSWORD)
        self.last_refresh = 0
        self.refresh_interval_ms = 2 * 60 * 1000
        self.sugar_colour = {
            1: context.green(),
            2: context.amber(),
            3: context.red(),
        }

    def enter(self):
        print(f'Sugar View Entry')
        (value, trend, colour) = self.get_reading()
        self.display(value, trend, colour)
        
    def refresh_display(self):
        now = time.ticks_ms()
        if time.ticks_diff(now, self.last_refresh) >= self.refresh_interval_ms:
            self.last_refresh = now

            (value, trend, colour) = self.get_reading()
            self.display(value, trend, colour)

    def display(self, value, trend, colour):
            print(f'Displaying: value={value}, trend={trend}, colour={colour}')
            context = self.context
            graphics = context.graphics
            foreground = context.white()
            background = context.dark_background_blue()

            context.clear_display(background)
            context.set_title('Sugar View')

            context.set_pen(self.sugar_colour.get(colour))
            text = f'{value:.1f}'
            scale=15
            graphics.text(text, self.context.centre_text(text, scale=scale), 80, scale=scale, spacing=1)
            draw_arrow(graphics, trend, foreground, background, 250, 15)

            self.context.update_display()

    def get_reading(self):
        return self.libre_link.get_reading()


    def button_pressed(self, button, press):
        pass


if __name__ == '__main__':
    context = Context()
    # Wifi(context).connect()
    view = SugarView(context)
    view.enter()

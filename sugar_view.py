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
        self.refresh_interval_ms = 1 * 45 * 1000
        self.sugar_colour = {
            1: context.green(),
            2: context.amber(),
            3: context.red(),
            4: context.red(),
        }

    def enter(self):
        print(f'Sugar View Entry')
        self.display('', 6, 1)
        
    def refresh_display(self):
        now = time.ticks_ms()
        if time.ticks_diff(now, self.last_refresh) >= self.refresh_interval_ms:
            self.update_display()
 
    def update_display(self):
        self.last_refresh = time.ticks_ms()
        try:
            value, trend, colour = self.get_reading()
            self.display(value, trend, colour)
        except Exception as e:
            msg = str(e)
            print(f'{msg=}')
            self.display_error(msg)


    @staticmethod
    def truncate(s, n=10):
        return s if len(s) <= n else s[:n] + '...'

    def display_error(self, msg):
        graphics = self.context.graphics
        self.display_header(trend=6)

        self.context.set_pen(self.context.red())
        scale = 4
        text = self.truncate(msg, 15)
        graphics.text(text, self.context.centre_text(text, scale=scale), 100, scale=scale, spacing=1)
        self.context.update_display()

    def display_header(self, trend):
        context = self.context
        graphics = context.graphics
        foreground = context.white()
        background = context.dark_background_blue()

        context.clear_display(background)
        context.set_title('Sugar View')
        draw_arrow(graphics, trend, foreground, background, 250, 15)

    def display(self, value, trend, colour):
            print(f'Displaying: value={value}, trend={trend}, colour={colour}')
            context = self.context
            graphics = context.graphics
            self.display_header(trend)

            context.set_pen(self.sugar_colour.get(colour))
            try:
                text = f"{float(value):.1f}"
            except (TypeError, ValueError):
                text = str(value)

            scale=15
            graphics.text(text, self.context.centre_text(text, scale=scale), 80, scale=scale, spacing=1)

            self.context.update_display()


    def get_reading(self):
        return self.libre_link.get_reading()

    def button_pressed(self, button, press):
        pass


if __name__ == '__main__':
    context = Context()
    # Wifi(context).connect()
    view = SugarView(context)
    view.display_error('Status: 404')

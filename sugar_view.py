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
        self.last_refresh = time.ticks_ms()
        self.refresh_interval_ms = 1 * 45 * 1000
        self.sugar_colour = {
            1: context.green(),
            2: context.amber(),
            3: context.red(),
            4: context.red(),
        }
        self.current_bar_colour = context.white()
        self.last_progress_update = 0
        self.progress_update_ms = 500
        self.last_factory_timestamp = ''
        self.last_factory_timestamp_seen_at = 0
        self.stale_timeout_ms = 10 * 60 * 1000

        self.bar_x = 10
        self.bar_y = 225
        self.bar_w = 300
        self.bar_h = 2

    def enter(self):
        print(f'Sugar View Entry')
        self.last_progress_update = 0
        self.display('', 6, 1)
        self.update_display()

    def refresh_display(self):
        now = time.ticks_ms()
        if time.ticks_diff(now, self.last_refresh) >= self.refresh_interval_ms:
            self.update_display()
        elif time.ticks_diff(now, self.last_progress_update) >= self.progress_update_ms:
            self._draw_progress_bar()

    def _progress(self):
        elapsed = time.ticks_diff(time.ticks_ms(), self.last_refresh)
        return min(elapsed / self.refresh_interval_ms, 1.0)

    def _draw_progress_bar(self, update=True):
        self.last_progress_update = time.ticks_ms()
        progress = self._progress()

        context = self.context
        graphics = context.graphics

        width = int(self.bar_w * progress)

        context.set_pen(context.dark_background_blue())
        graphics.rectangle(self.bar_x, self.bar_y, self.bar_w, self.bar_h)

        if width > 0:
            context.set_pen(self.current_bar_colour)
            graphics.rectangle(self.bar_x, self.bar_y, width, self.bar_h)

        if update:
            context.update_display()

    def _is_stale(self, factory_timestamp):
        now = time.ticks_ms()
        if not factory_timestamp:
            return False
        if factory_timestamp == self.last_factory_timestamp:
            return time.ticks_diff(now, self.last_factory_timestamp_seen_at) > self.stale_timeout_ms
        self.last_factory_timestamp = factory_timestamp
        self.last_factory_timestamp_seen_at = now
        return False

    def update_display(self):
        self.last_refresh = time.ticks_ms()
        try:
            value, trend, colour, factory_timestamp = self.get_reading()
            stale = self._is_stale(factory_timestamp)
            self.display(value, trend, colour, stale)
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

        self.current_bar_colour = self.context.red()
        self._draw_progress_bar(update=False)
        self.context.update_display()

    def display_header(self, trend):
        context = self.context
        graphics = context.graphics
        foreground = context.white()
        background = context.dark_background_blue()

        context.clear_display(background)
        context.set_title('Sugar View')
        draw_arrow(graphics, trend, foreground, background, 250, 15)

    def display(self, value, trend, colour, stale=False):
            print(f'Displaying: value={value}, trend={trend}, colour={colour}, stale={stale}')
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

            if stale:
                context.set_pen(context.red())
                label = 'stale'
                label_scale = 2
                graphics.text(label, self.context.centre_text(label, scale=label_scale), 202, scale=label_scale, spacing=1)

            self.current_bar_colour = self.sugar_colour.get(colour, context.white())
            self._draw_progress_bar(update=False)
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

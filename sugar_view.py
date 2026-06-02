#!/usr/bin/env python3
from libre_link import LibreLink, StatusCodeError
from arrows import draw_arrow
import time
from context import Context
from libre_config import USER, PASSWORD

     
class SugarView:
    def __init__(self, context):
        self.context = context
        self.libre_link = LibreLink(user=USER, pwd=PASSWORD)
        self.last_refresh = time.ticks_ms()
        self.refresh_interval_ms = 20 * 1000
        self.sugar_colour = {
            1: context.green(),
            2: context.amber(),
            3: context.red(),
            4: context.red(),
        }
        self.last_progress_update = 0
        self.progress_update_ms = 500
        self.last_factory_timestamp = ''
        self.last_factory_timestamp_seen_at = 0
        self.stale_timeout_ms = 10 * 60 * 1000

        self.bar_x = 10
        self.bar_y = 235
        self.bar_w = 300
        self.bar_h = 2

        self.stale = False

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
            self.context.update_display()

    def _progress(self):
        elapsed = time.ticks_diff(time.ticks_ms(), self.last_refresh)
        return min(elapsed / self.refresh_interval_ms, 1.0)

    def _draw_progress_bar(self):
        self.last_progress_update = time.ticks_ms()
        progress = self._progress()

        context = self.context
        graphics = context.graphics

        width = int(self.bar_w * progress)

        context.set_pen(context.dark_background_blue())
        graphics.rectangle(self.bar_x, self.bar_y, self.bar_w, self.bar_h)

        if width > 0:
            colour = context.red() if self.stale else context.green()
            context.set_pen(colour)
            graphics.rectangle(self.bar_x, self.bar_y, width, self.bar_h)
            
    def _update_stale(self, factory_timestamp):
        now = time.ticks_ms()
        stale = False
        if factory_timestamp:
            if factory_timestamp == self.last_factory_timestamp:
                stale = time.ticks_diff(now, self.last_factory_timestamp_seen_at) > self.stale_timeout_ms
            else:
                self.last_factory_timestamp = factory_timestamp
                self.last_factory_timestamp_seen_at = now
        self.stale = stale

    def update_display(self):
        self.last_refresh = time.ticks_ms()
        try:
            value, trend, colour, factory_timestamp = self.get_reading()
            self._update_stale(factory_timestamp)
            self.display(value, trend, colour)
        except StatusCodeError as e:
            print(f'{e.status_code}: {e}')
            self.display_error(str(e))
            if e.status_code == 429:
                self.refresh_interval_ms += 5 * 1000
                self.last_refresh = time.ticks_add(self.last_refresh, 30000 - self.refresh_interval_ms)
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

        self._draw_progress_bar()
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
            print(f'Displaying: value={value}, trend={trend}, colour={colour}, stale={self.stale}')
            context = self.context
            graphics = context.graphics
            self.display_header(trend)

            context.set_pen(self.sugar_colour.get(colour))
            try:
                text = f'{float(value):.1f}'
            except (TypeError, ValueError):
                text = str(value)

            scale=15
            graphics.text(text, self.context.centre_text(text, scale=scale), 80, scale=scale, spacing=1)

            self._draw_progress_bar()
            self.context.update_display()


    def get_reading(self):
        return self.libre_link.get_reading()

    def button_pressed(self, button, press):
        pass


if __name__ == '__main__':
    from wifi import Wifi
    context = Context()
    Wifi(context).connect()
    view = SugarView(context)
    view.display_error('Status: 404')

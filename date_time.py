#!/usr/bin/env python3

import time

MONTHS = ['January','Febuary','March','April','May','June','July','August','September','October','November','December']


class DateTime:
    def __init__(self, context):
        self.context = context
        self.last_refresh_minute = int(0)

    def enter(self):
        print(f'Date Time Entry')
        self.update_display()

    def background(self):
        return self.context.dark_background_blue()

    def update_display(self):
        self.context.clear_display(self.background())
        self.display_date()
        self.display_time()
        self.context.update_display()

    def refresh_display(self):
        _, _, _, _, _, current_minute, _, _ = self.context.datetime()
        if current_minute != self.last_refresh_minute:
            self.update_display()

    def display_date(self):
        scale = 6
        month, day = self.current_date()
        date = f'{MONTHS[month-1]} {day}'

        self.context.set_pen(self.context.orange())
        self.context.graphics.text(date, self.context.centre_text(date, scale=scale), 2, scale=scale, spacing=1)

    def display_time(self):
        year = time.localtime()[0]
        mar_change = time.mktime((year,3 ,(31-(int(5*year/4+4))%7),1,0,0,0,0,0))
        oct_change = time.mktime((year,10,(31-(int(5*year/4+1))%7),1,0,0,0,0,0))
        now = time.time()
        if now < mar_change:
            localtime = time.localtime(now)
        elif now < oct_change:  
            localtime = time.localtime(now+3600)
        else:
            localtime = time.localtime(now)
        hour = localtime[3]
        minute = localtime[4]
        self.context.set_pen(self.context.green())
        text = f'{hour:02d}:{minute:02d}'
        scale=5
        self.context.graphics.text(text, self.context.centre_text(text, scale=scale), 120, scale=scale, spacing=1)

        self.last_refresh_minute = minute

    def current_date(self):
        _, month, day, _, _, _, _, _ = self.context.datetime()
        return month, day

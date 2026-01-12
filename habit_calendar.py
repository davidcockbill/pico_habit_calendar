#!/usr/bin/env python3

from date_matrix import DateMatrix
import time
from button_handler import Button

MONTHS = ['January','Febuary','March','April','May','June','July','August','September','October','November','December']


class HabitCalendar:
    def __init__(self, context):
        grid_width = 32
        grid_height = 12
        self.cell_gap = 1
        width, height = context.graphics.get_bounds()
        self.cell_width = (width - (grid_width - 1) * self.cell_gap) // grid_width
        self.cell_height = (height - (grid_height - 1) * self.cell_gap) // grid_height

        self.context = context
        self.date_matrix = DateMatrix()
        self.last_refresh_minute = int(0)
        self.view = [
            self.display_summary_view,
            self.display_year_view,
        ]
        self.view_idx = 0

        self.restore_matrix()

    def enter(self):
        print(f'Habit Calendar Entry')
        self.context.restore_brightness()
        self.update_display()

    def display_summary_view(self):
        self.display_date()
        self.display_time()
        self.display_percentage()
        self.display_month()

    def update_display(self):
        self.context.clear_display(self.background())
        self.view[self.view_idx]()
        self.context.update_display()

    def button_pressed(self, button, press):
        if button is Button.X:
            self.toggle_day()
        elif button is Button.Y:
            self.view_idx = (self.view_idx + 1) % len(self.view)
        self.update_display()

    def restore_matrix(self):
        print(f'Restoring Matrix...')
        self.date_matrix.restore()
        print(f'Matrix Restored')

    def toggle_day(self):
        month, day = self.current_date()
        print(f'Setting month={month}, day={day}')
        self.date_matrix.toggle(month-1, day-1)
        self.date_matrix.store()

    def current_date(self):
        _, month, day, _, _, _, _, _ = self.context.datetime()
        return month, day
    
    def update_matrix(self, x, y):
        px = x * (self.cell_width + self.cell_gap)
        py = y * (self.cell_height+ self.cell_gap)
        self.context.graphics.rectangle(px, py, self.cell_width, self.cell_height)

    def display_percentage(self):
        current_month, current_day = self.current_date()

        total_days = 0
        set_days = 0
        today = False
        for month in DateMatrix.month_range():
            for day in DateMatrix.day_range(month):
                total_days += 1
                if (self.date_matrix.isSet(month, day)):
                    set_days += 1
                today = day == current_day-1 and month == current_month-1
                if today:
                    break
            if today:
                break
        percentage = int(set_days/total_days * 100)
        text = f'{percentage:02d}%'
        scale=3
        self.context.set_pen(self.context.green())
        self.context.graphics.text(text, self.context.centre_text(text, scale=scale), 140, scale=scale, spacing=1)

    def display_year_view(self):
        current_month, current_day = self.current_date()

        for month in DateMatrix.month_range():
            self.context.set_pen(self.off())
            for day in DateMatrix.day_range(month):
                today = day == current_day-1 and month == current_month-1
                pen = self.today_off() if today else self.off()
                if (self.date_matrix.isSet(month, day)):
                    pen = self.today_on() if today else self.on()
                self.context.set_pen(pen)
                self.update_matrix(day, month)

    def display_month(self):
        current_month, current_day = self.current_date()

        month = current_month-1
        for day in DateMatrix.day_range(current_month):
            today = day == current_day-1
            pen = self.today_off() if today else self.off()
            if (self.date_matrix.isSet(month, day)):
                print(f'day={day} is set')
                pen = self.today_on() if today else self.on()
            self.context.set_pen(pen)
            self.update_matrix(day, 10)

    def refresh_display(self):
        _, _, _, _, _, current_minute, _, _ = self.context.datetime()
        if current_minute != self.last_refresh_minute:
            self.update_display()

    def on(self):
        return self.context.blue()
        
    def off(self):
        return self.context.black()
        
    def today_on(self):
        return self.context.green()
        
    def today_off(self):
        return self.context.pink()
        
    def matrix_border(self):
        return self.context.dark_blue()

    def background(self):
        return self.context.dark_background_blue()
    
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
        self.context.graphics.text(text, self.context.centre_text(text, scale=scale), 80, scale=scale, spacing=1)

        self.last_refresh_minute = minute

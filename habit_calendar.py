#!/usr/bin/env python3

from date_matrix import DateMatrix
import time


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

        self.restore_matrix()

    def enter(self):
        print(f'Habit Calendar Entry')
        self.context.restore_brightness()
        self.update_display()

    def update_display(self):
        self.context.clear_display(self.background())
        self.display_date_matrix()
        self.context.update_display()

    def button_pressed(self):
        self.toggle_day()

    def restore_matrix(self):
        print(f'Restoring Matrix...')
        self.date_matrix.restore()
        print(f'Matrix Restored')

    def toggle_day(self):
        month, day = self.current_date()
        print(f'Setting month={month}, day={day}')
        self.date_matrix.toggle(month-1, day-1)
        self.date_matrix.store()
        self.display_date_matrix()

    def current_date(self):
        _, month, day, _, _, _, _, _ = self.context.datetime()
        return month, day
    
    def update_matrix(self, x, y):
        px = x * (self.cell_width + self.cell_gap)
        py = y * (self.cell_height+ self.cell_gap)
        self.context.graphics.rectangle(px, py, self.cell_width, self.cell_height)

    def display_date_matrix(self):
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
        self.context.update_display()

    def refresh_display(self):
        _, _, _, _, _, current_minute, _, _ = self.context.datetime()
        if current_minute != self.last_refresh_minute:
            self.update_display()

    def on(self):
        return self.context.dark_green()
        
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

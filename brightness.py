#!/usr/bin/env python3


class Brightness:
    def __init__(self, context):
        self.context = context

    def enter(self):
        print(f'Brightness Entry')
        self.context.clear_display()
        self.context.update_display()

    def refresh_display(self):
        self.context.clear_display()
        self.context.graphics.set_font('bitmap16')
        self.context.set_pen(self.context.blue())
        self.context.graphics.text('Brightness:', 2, 4, scale=5, spacing=1)

        self.context.graphics.set_font('bitmap8')
        self.context.set_pen(self.context.green())
        self.context.graphics.text(f'{self.context.get_brightness()}%', 100, 150, scale=5, spacing=1)
        self.context.update_display()

    def button_pressed(self):
        print(f'Increment brightness')
        self.context.increment_brightness()
        self.refresh_display()


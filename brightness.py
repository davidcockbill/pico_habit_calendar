#!/usr/bin/env python3

from button_handler import Button


class Brightness:
    def __init__(self, context):
        self.context = context

    def enter(self):
        print(f'Brightness Entry')
        self.context.clear_display()
        self.context.update_display()

    def refresh_display(self):
        self.context.clear_display()

        self.context.set_title('Brightness')

        display = self.context.graphics
        self.context.set_pen(self.context.green())
        text = f'{self.context.get_brightness()}%'
        scale = 5
        display.text(text, self.context.centre_text(text, scale=scale), 90, scale=scale, spacing=1)

        self.context.set_controls({
            'x': 'up',
            'y': 'down',
        })

        self.context.update_display()

    def button_pressed(self, button, press):
        if button is Button.X:
            print(f'Increment brightness')
            self.context.increment_brightness()
        elif button is Button.Y:
            print(f'Decrement brightness')
            self.context.decrement_brightness()
        self.refresh_display()

#!/usr/bin/env python3

from button_handler import ButtonHandler, ButtonPress, Button
import time


CHARACTER_SET = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-.'

class WifiSetup:
    def __init__(self, context):
        self.width, self.height = context.graphics.get_bounds()
        self.context = context
        self.button_handler = ButtonHandler()

    def enter(self):
        print(f'Wifi Setup Entry')
        self.display_setup_page()

    def refresh_display(self):
        pass

    def display_setup_page(self):
        self.clear_display()
        self.context.set_title('WiFi Setup')
        self.context.set_controls({
            'b': 'start configuration',
        })
        self.context.update_display()

    def collect_details(self):
        ssid = self.text_input('Enter SSID')
        pwd = self.text_input('Enter Password')
        self.save_wifi_config(ssid, pwd)
        self.display_setup_page()

    def button_pressed(self, button, press):
        if button is Button.B:
            self.collect_details()

    def clear_display(self):
        self.context.clear_display(self.context.dark_background_blue())

    def text_input(self, prompt):
        display = self.context.graphics
        text = ''
        cursor = 0
        character_index = 0

        while True:
            current_char = CHARACTER_SET[character_index]

            preview = (
                text[:cursor] +
                f'[{current_char}]' +
                text[cursor:]
            )

            self.clear_display()
            self.context.set_title(prompt)
            display.text(preview, 10, 70, 3, spacing=1)

            self.context.set_controls({
                'x': 'up',
                'y': 'down',
                'b': 'select',
                'a': 'finish',
            })
            display.update()

            button, press = self.button_handler.process_buttons()
            if press is not ButtonPress.NONE:
                if button is Button.A:
                    return text
                if button is Button.B:
                    text = text[:cursor] + current_char + text[cursor:]
                    cursor += 1  
                if button is Button.X:
                    character_index = (character_index + 1) % len(CHARACTER_SET)
                if button is Button.Y:
                    character_index = (character_index - 1) % len(CHARACTER_SET)
            else:
                time.sleep(0.001)

    def save_wifi_config(self, ssid, pwd):
        print(f'Saving ssid={ssid}, pwd={pwd}')
        # with open('wifi_config.py', 'w') as f:
        #     f.write(f'WIFI_SSID = "{ssid}"\n')
        #     f.write(f'WIFI_PASSWORD = "{pwd}"\n')

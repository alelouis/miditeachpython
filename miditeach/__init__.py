#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""Let's find some podcasts!"""

__version__ = "0.1.0"


import arcade
from miditeach.views.WelcomeScreen import WelcomeScreen

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 500

if __name__ == "__main__":
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, "midiTeacher")
    start_view = WelcomeScreen()
    window.show_view(start_view)
    arcade.run()
#!/usr/bin/python
# -*- coding: UTF-8 -*-

import arcade
from miditeach.views.WelcomeScreen import WelcomeScreen

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 500

def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, "midiTeacher")
    start_view = WelcomeScreen()
    window.show_view(start_view)
    arcade.run()
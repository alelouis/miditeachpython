#!/usr/bin/python
# -*- coding: UTF-8 -*-

from miditeach.views.LaunchView import LaunchView
import arcade

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 500

def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, "midiTeacher")
    start_view = LaunchView()
    window.show_view(start_view)
    arcade.run()
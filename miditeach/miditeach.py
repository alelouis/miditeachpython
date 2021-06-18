#!/usr/bin/python
# -*- coding: UTF-8 -*-

from miditeach.views.LaunchView import LaunchView
import arcade
import sys, os
from pathlib import Path

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 500

if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    os.chdir(sys._MEIPASS)
else:
    os.chdir(Path(__file__).absolute().parent)

def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, "midiTeacher")
    start_view = LaunchView()
    window.show_view(start_view)
    arcade.run()

if __name__ == "__main__":
    main()

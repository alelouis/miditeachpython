#!/usr/bin/python
# -*- coding: UTF-8 -*-

import arcade
import mido
import mido.backends.pygame # for bundle
import poetry_version

from arcade.gui import UIManager
from miditeach.views.GameView import GameView
from pathlib import Path

mido.set_backend('mido.backends.pygame')

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 500

class Selector(arcade.gui.UIImageToggle):
    def __init__(self, center_x, center_y):
        select_off = arcade.load_texture("assets/images/select_off.png")
        select_on = arcade.load_texture("assets/images/select_on.png")
        super().__init__(center_x=center_x, center_y=center_y, true_texture=select_on, false_texture=select_off)
    
    def on_click(self):
        self.value = not self.value

class LaunchView(arcade.View):
    """ Welcome screen and credits """

    def __init__(self):
        super().__init__()
        self.input_select = 0
        self.ui_manager = UIManager()
        self.version = poetry_version.extract(source_file=__file__)

    def on_show(self):
        """ This is run once when we switch to this view """
        arcade.set_background_color(arcade.csscolor.BLACK)

    def on_hide_view(self):
        self.ui_manager.unregister_handlers()

    def get_selector_status(self):
        d = {}
        for chord in self.buttons:
            d[chord] = self.buttons[chord].value
        return d

    def setup(self):
        self.buttons = {}
        for e, chord in enumerate(['min', 'maj', 'dim', 'aug', 'm7', 'M7', '7']):
            self.buttons[chord] = Selector(SCREEN_WIDTH* (1-1/6), SCREEN_HEIGHT / 4 + 36 * e)
            label = arcade.gui.UILabel(center_x = SCREEN_WIDTH* (1-1/6) + 50, center_y = SCREEN_HEIGHT / 4 + 36 * e, text = chord, align = "right")
            self.ui_manager.add_ui_element(label)
            self.ui_manager.add_ui_element(self.buttons[chord])

    def on_draw(self):
        """ Draw this view """
        arcade.start_render()
        arcade.draw_text(f"midiTeacher V{self.version}", SCREEN_WIDTH / 2, SCREEN_HEIGHT * (1-1/4),
                         arcade.color.WHITE, font_size=30, anchor_x="center")
        arcade.draw_text("Alexis LOUIS - github.com/alelouis", SCREEN_WIDTH-15, 15,
                         arcade.color.WHITE, font_size=15, anchor_x="right")
        arcade.draw_text("Select MIDI input (UP/DOWN)", SCREEN_WIDTH / 2, SCREEN_HEIGHT * (1-1/4) - 40,
                         arcade.color.WHITE, font_size=20, anchor_x="center")
        arcade.draw_text("(Press ENTER to start)", SCREEN_WIDTH / 2, SCREEN_HEIGHT * (1/4) - 40,
                    arcade.color.YELLOW, font_size=20, anchor_x="center")

        inputs = mido.get_input_names()
        for e, i in enumerate(inputs):
            color = arcade.color.GREEN if e == self.input_select else arcade.color.WHITE
            arcade.draw_text(f'({e+1}) '+ i, SCREEN_WIDTH / 2 - SCREEN_WIDTH/8, SCREEN_HEIGHT * (1-1/4) - (e+5)*20,
                         color, font_size=18, anchor_x="left")
   
    def on_show_view(self):
        """ Show this view """

        self.setup()

    def on_key_press(self, key, modifiers):
        """ If the user presses the mouse button, start the game. """
        if key == arcade.key.DOWN:
            self.input_select += 1
            self.input_select = min(self.input_select, len(mido.get_input_names()))
        if key == arcade.key.UP:
            self.input_select -= 1
            self.input_select = max(self.input_select, 0)
        if key == arcade.key.RETURN:
            game_view = GameView(
                input_select = self.input_select, 
                chords_selected = self.get_selector_status(),
                launch_view=self)
            game_view.setup()
            self.window.show_view(game_view)
#!/usr/bin/python
# -*- coding: UTF-8 -*-

import arcade
import mido
from GameView import GameView

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 500

class WelcomeScreen(arcade.View):
    """ Welcome screen and credits """

    def __init__(self):
        super().__init__()
        self.input_select = 0

    def on_show(self):
        """ This is run once when we switch to this view """
        arcade.set_background_color(arcade.csscolor.BLACK)

    def on_draw(self):
        """ Draw this view """
        arcade.start_render()
        arcade.draw_text("midiTeacher V.0", SCREEN_WIDTH / 2, SCREEN_HEIGHT * (1-1/4),
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
    
    def on_key_press(self, key, modifiers):
        """ If the user presses the mouse button, start the game. """
        if key == arcade.key.DOWN:
            self.input_select += 1
            self.input_select = min(self.input_select, len(mido.get_input_names()))
        if key == arcade.key.UP:
            self.input_select -= 1
            self.input_select = max(self.input_select, 0)
        if key == arcade.key.RETURN:
            game_view = GameView(self.input_select)
            game_view.setup()
            self.window.show_view(game_view)
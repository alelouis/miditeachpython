#!/usr/bin/python
# -*- coding: UTF-8 -*-

import arcade

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 500

class PauseView(arcade.View):
    """ Pause view, resumes, resets and quits game """
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view

    def on_show(self):
        """ This is run once when we switch to this view """
        arcade.set_background_color(arcade.csscolor.BLACK)

    def on_draw(self):
        """ Draw this view """
        arcade.start_render()
        
        arcade.draw_text("Press Q to quit.\nPress R to restart.", 
            SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
            arcade.color.WHITE, font_size=20, anchor_x="center")

    def on_key_press(self, key, modifiers):
        """ Quit or resume game. """
        if key == arcade.key.Q:
            self.window.close()
            self.game_view.stats_file.close()
        if key == arcade.key.R:
            self.game_view.reset()
            self.window.show_view(self.game_view)

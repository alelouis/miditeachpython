#!/usr/bin/python
# -*- coding: UTF-8 -*-

import mido
import arcade
import random
import time
import pickle
from datetime import datetime
from PauseView import PauseView

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 500

class GameView(arcade.View):
    """ Main application class. """

    def __init__(self, input_select):
        super().__init__()
        self.played_notes = [0]*12
        self.notes = ['C', 'C#\nDb', 'D', 'D#\nEb', 'E', 'F', 'F#\nGb', 'G', 'G#\nAb', 'A', 'A#\nBb', 'B']
        self.intervals = ['1', '2m', '2', '3m', '3', '4', 'T', '5', '6m', '6', '7m', '7']
        self.formulas = {
            'min':['1', '3m', '5'],
            'maj':['1', '3', '5']}

        self.selected_device = mido.get_input_names()[input_select]
        self.stats_path = 'stats/' + datetime.now().strftime('%m%d%Y') + '.p'
        self.stats_file = open(self.stats_path, 'wb')

        self.inport = mido.open_input(self.selected_device)
        self.sample_next_chord()
        self.reset()


    def reset(self):
        """ Reset time and accuracy metrics """
        self.total_duration = 0
        self.total_chords = 0
        self.total_correct = 0
        self.total_incorrect = 0
        self.t_launch = datetime.now()


    def check_midi(self):
        """ Checks incoming midi data """
        for msg in self.inport.iter_pending(): 
            if msg.type == 'note_on':
                self.played_notes[msg.note%12] += 1
            if msg.type == 'note_off':
                self.played_notes[msg.note%12] -= 1


    def sample_next_chord(self):
        """ Sample a new root and formula """
        # Formula
        self.formula_name = random.choice(list(self.formulas.keys()))
        self.formula = self.formulas[self.formula_name]
        
        # Root
        self.root = random.choice(self.notes)
        self.root_select = random.choice(self.root.split('\n'))
        self.root_text = self.root_select + self.formula_name

        # Expected notes
        self.expected_notes = [0]*12
        for interval in self.formula: 
            self.expected_notes[(self.notes.index(self.root) + self.intervals.index(interval))%12] = 1
        

    def get_stat_dict(self):
        st = {}
        st['root'] = self.root_select
        st['formula'] = self.formula_name
        st['time'] = self.last_duration
        st['timestamp'] = datetime.now()
        return st

    def check_next(self):
        """ Checks if user misses or validate a chord """
        if self.is_incorrect() or self.is_correct():
            self.total_chords += 1

            if self.is_correct():
                arcade.play_sound(self.correct_sound)
            else:
                arcade.play_sound(self.wrong_sound)

            # Accuracy metrics
            self.total_correct += self.is_correct()
            self.total_incorrect += self.is_incorrect()

            # Time metrics
            self.t_end = datetime.now()
            self.last_duration = self.t_end - self.t_start
            self.last_duration = float(str(self.last_duration).split(':')[-1][1:6])
            self.total_duration += self.last_duration
            
            # Saving stats
            pickle.dump(self.get_stat_dict(), self.stats_file)

            # Next chords
            time.sleep(0.5)
            self.t_start = datetime.now()
            self.sample_next_chord()


    def is_incorrect(self):
        """ Checks if user inputs a wrong note """
        correct_notes = sum([a and b for a,b in zip(self.expected_notes, self.played_notes)])
        incorrect_notes = sum([a>0 for a in self.played_notes]) - correct_notes
        is_incorrect = incorrect_notes > 0
        return is_incorrect


    def is_correct(self):
        """ Checks if user inputs a correct chord """
        correct_notes = sum([a and b for a,b in zip(self.expected_notes, self.played_notes)])
        is_correct = correct_notes == len(self.formula)
        return is_correct


    def setup(self):
        """ Setup called before app run """
        arcade.set_background_color(arcade.color.BLACK)
        self.t_start = datetime.now()
        self.last_duration = datetime.now()-datetime.now()
        self.correct_sound = arcade.load_sound("assets/sounds/correct.wav")
        self.wrong_sound = arcade.load_sound("assets/sounds/wrong.wav")


    def on_draw(self):
        """ Render the screen """
        arcade.start_render()

        # Keyboard
        for note_index in range(12):
            if self.played_notes[note_index]:
                if self.expected_notes[note_index]: color = arcade.color.GREEN
                else: color = arcade.color.RED
            else: color = arcade.color.GRAY

            arcade.draw_text(self.notes[note_index], 
                SCREEN_WIDTH/24 + note_index * SCREEN_WIDTH/12 , 
                SCREEN_HEIGHT-SCREEN_HEIGHT/4, 
                color, 30, 
                anchor_x='center', anchor_y='center', font_name = 'Consolas')

        # Intervals
        for i, interval in enumerate(self.formula):
            interval_index = (self.intervals.index(interval) + self.notes.index(self.root))%12
            interval_color = arcade.color.GREEN if self.played_notes[interval_index] else arcade.color.GRAY
            offset = 0 if len(self.formula)%2 else 0.5
            arcade.draw_text(interval,
                SCREEN_WIDTH/2 + (i+ offset -len(self.formula)//2)*(SCREEN_WIDTH/8), 
                SCREEN_HEIGHT/2-SCREEN_HEIGHT/4, 
                interval_color, 50, 
                anchor_x='center', anchor_y='center', font_name = 'Consolas')

        # Root
        root_color = arcade.color.GREEN if self.is_correct() else arcade.color.RED if self.is_incorrect() else arcade.color.GRAY
        arcade.draw_text(self.root_text, 
            SCREEN_WIDTH/2 , 
            SCREEN_HEIGHT/2, 
            root_color, 70, 
            anchor_x='center', anchor_y='center', font_name = 'Consolas') 

        # Duration
        last_duration_text = 'undefined' if self.total_chords==0 else '%.2f'%self.last_duration
        mean_duration_text = 'undefined' if self.total_chords==0 else '%.2f'%(self.total_duration/self.total_chords)
        arcade.draw_text('last : ' + last_duration_text + ' s', 
            SCREEN_WIDTH*(1-1/12),
            SCREEN_HEIGHT/2, 
            root_color, 20, 
            anchor_x='right', anchor_y='center', font_name = 'Consolas')
        arcade.draw_text('mean: ' + mean_duration_text + ' s', 
            SCREEN_WIDTH*(1-1/12), 
            SCREEN_HEIGHT/2 - 25, 
            root_color, 20, 
            anchor_x='right', anchor_y='center', font_name = 'Consolas')    

        # Correct and wrong
        arcade.draw_text('correct : ' + str(self.total_correct), 
            SCREEN_WIDTH*(1/12),
            SCREEN_HEIGHT/2, 
            root_color, 20, 
            anchor_x='left', anchor_y='center', font_name = 'Consolas')
        arcade.draw_text('wrong : ' + str(self.total_incorrect), 
            SCREEN_WIDTH*(1/12), 
            SCREEN_HEIGHT/2 - 25, 
            root_color, 20, 
            anchor_x='left', anchor_y='center', font_name = 'Consolas')    

        # Timer
        elapsed_mins = (datetime.now() - self.t_launch).seconds//60
        elapsed_secs = (datetime.now() - self.t_launch).seconds%60
        elapsed_microsecs = (datetime.now() - self.t_launch).microseconds/10000
        arcade.draw_text('%02d:%02d:%02d'%(elapsed_mins,elapsed_secs,elapsed_microsecs), 
            SCREEN_WIDTH/2, SCREEN_HEIGHT*(1-1/10), 
            root_color, 20, 
            anchor_x='center', anchor_y='center', font_name = 'Consolas')  

        # Shortcuts
        arcade.draw_text('(Press SPACE to stop)', 
            SCREEN_WIDTH/2, SCREEN_HEIGHT*(1/10), 
            root_color, 10, 
            anchor_x='center', anchor_y='center', font_name = 'Consolas')  


    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        # If the player presses a key, update the speed
        if key == arcade.key.SPACE:
            pause_view = PauseView(self)
            self.window.show_view(pause_view)


    def update(self, delta_time):
        """ Game update """
        self.check_next()
        self.check_midi()


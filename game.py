from tkinter import *
from tkinter import messagebox

import os
import random
import sys
import time

class Minesweeper(Frame):
    def __init__(self, root, x, y, bomb_total):
        Frame.__init__(self, root)
        self.grid(row=0, column=0, sticky=N+S+E+W)

        self.dimensions = (x, y)
        self.bomb_count = 0
        self.total_flagged = 0
        self.bomb_total = bomb_total
        self.spots = []
        self.intermission = False

    def create_board(self):
        for x in range(0, self.dimensions[0]):
            Grid.rowconfigure(self, x, weight=1)
            for y in range(0, self.dimensions[1]):
                Grid.columnconfigure(self, y, weight=1)
                spot = Spot(self)
                spot.setup(x, y)
                self.spots.append(spot)
        
        for spot in self.spots:
            spot.get_spots_around()

    def generate_bombs(self):
        random.seed(os.urandom(10)) #Magic number time
        bombs = []

        while len(bombs) < self.bomb_total:
            bomb_sample = random.sample(self.spots, self.bomb_total - len(bombs))
            for bomb in bomb_sample.copy():
                s_spots = bomb.get_spots_around()
                for s_spot in s_spots:
                    if (s_spot.is_marked() or bomb.is_marked()) and bomb in bomb_sample:
                        bomb_sample.remove(bomb)
        
            bombs = list(set(bombs + bomb_sample))
                    
        for bomb in bombs:
            if not bomb.is_marked():
                bomb.prime()
                self.bomb_count += 1
    
    def reveal_spots(self, spot):
        for s_spot in spot.get_spots_around():
            if not s_spot.is_marked():
                s_spot.select()

    def reveal_all(self):
        self.intermission = True
        for spot in self.spots:
            spot.configure(text="\U0001F4A3") if spot.is_bomb() else spot.select()

    def win_check(self):
        marked = [spot for spot in self.spots if getattr(spot, "marked")]
        if len(self.spots) - len(marked) == self.get_bomb_total() or self.get_total_flagged() >= self.get_bomb_count():
            self.win()
    
    def win(self):
        self.reveal_all()
        self.prompt("You win!", "You won the game!\nWould you like to play again?", self.reset)
    
    def game_over(self):
        self.reveal_all()
        self.prompt("Game over!", "You hit a bomb!\nWould you like to play again?", self.reset)

    def reset(self):
        del self.spots[:]
        self.bomb_count = 0
        self.total_flagged = 0

        self.create_board()

    def prompt(self, title, msg, callback):
        option = messagebox.askyesno(title, msg)
        if option:
            return callback()
        sys.exit()
    
    def set_total_flagged(self, total_flagged):
        self.total_flagged = total_flagged

    def get_total_flagged(self):
        return self.total_flagged

    def get_bomb_count(self):
        return self.bomb_count

    def get_bomb_total(self):
        return self.bomb_total
    
    def get_spot_by_position(self, position):
        for spot in self.spots:
            if spot.get_position() == position:
                return spot

class Spot(Button):
    def __init__(self, *args, **kwargs):
        Button.__init__(self, *args, **kwargs)
        self.game = args[0]
        self.bomb = False
        self.flagged = False
        self.marked = False

        self.bombs_around = None
        self.position = (None, None)

        self.surrounding_spots = []
    
    def setup(self, x, y):
        self.grid(row=x, column=y, sticky=N+S+E+W)
        
        self.position = (x, y)
        self.configure(command=self.select)
        self.bind('<Button-3>', lambda e: self.toggle_flag())

    def toggle_flag(self):
        if self.game.get_bomb_count() > 0 and not self.is_marked():
            self.flagged = not self.flagged
            self.configure(text=("\u2691" if self.flagged else ""))
            if self.is_bomb():
                self.game.set_total_flagged(self.game.get_total_flagged() + (1 if self.flagged else -1))
                self.game.win_check()
    
    def select(self):
        if self.is_bomb():
            self.game.game_over()
            return
        
        self.marked = True

        if self.game.get_bomb_count() <= 0:
            self.game.generate_bombs()

        if self.get_bombs_around() == 0:
            self.game.reveal_spots(self)

        if not self.game.intermission:
            self.game.win_check()
        self.configure(text=self.get_bombs_around(), bg="white", state=DISABLED)
    
    def mark(self):
        self.marked = True

    def prime(self):
        self.bomb = True
    
    def get_position(self):
        return self.position
    
    def get_bombs_around(self):
        if self.bombs_around == None:
            self.bombs_around = 0
            for spot in self.get_spots_around():
                if spot.is_bomb():
                    self.bombs_around += 1

        return self.bombs_around
    
    def get_spots_around(self):
        if len(self.surrounding_spots) <= 0:
            row = self.get_position()[0]
            column = self.get_position()[1]

            for x in range(column-1, column+2):
                for y in range(row-1, row+2):
                    s_spot = self.game.get_spot_by_position((y,x))
                    if not s_spot:
                        continue

                    if s_spot.get_position() != self.get_position():
                        self.surrounding_spots.append(s_spot)

        return self.surrounding_spots
        
    def is_bomb(self):
        return self.bomb

    def is_flagged(self):
        return self.flagged
    
    def is_marked(self):
        return self.marked

root = Tk()

columns = 8
rows = 8
bombs = 32

game = Minesweeper(root, rows, columns, bombs)
game.create_board()

Grid.rowconfigure(root, 0, weight=1)
Grid.columnconfigure(root, 0, weight=1)

root.title('Minesweeper')
root.mainloop()
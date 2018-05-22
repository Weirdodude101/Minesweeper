from tkinter import *
from tkinter import messagebox
import sys
import random
"""
    Structure of button dict:
        self.buttons = {
            ButtonClass: {
                type: 0 1 2 3; KEY: (0 = Surrounded by nothing; 1 = Surrounded by at least 1 bomb; 2 = A bomb; 3 = Flagged)
                around: # of bombs it's around (-1 = is a bomb)
                flagged: true or false

            }
        }
"""

class Minesweeper(Frame):
    def __init__(self, root):
        Frame.__init__(self, root)
        self.grid(row=0, column=0, sticky=N+S+E+W)

        self.dimensions = (16, 16)
        self.bombs = 0
        self.buttons = {}

    def createBoard(self):
        # Generate the board
        for x in range(0, self.dimensions[0]):
            Grid.rowconfigure(self, x, weight=1)
            for y in range(0, self.dimensions[1]):
                Grid.columnconfigure(self, y, weight=1)
                button = Button(self)
                button.pack()
                button.grid(row=x, column=y, sticky=N+S+E+W)

                # Create the button dictionary. See the structure of how this works.

                self.buttons[button] = {
                    "id": None,
                    "type": None,
                    "around": 0,
                    "flagged": False
                }

        for button in list(self.buttons):
            # Assign the IDs to the buttons and configure them.
            self.buttons[button]['id'] = list(self.buttons).index(button)
            button.configure(command=lambda x=self.buttons[button], y=button:self.select(x, y))
            button.bind('<Button-2>', lambda e, x=self.buttons[button], y=button:self.flag(x, y))

    def select(self, obj, btn):
        # Select a button

        print(obj['id'])
        if not self.bombs:
            self.setup(obj, 64)

        if obj['type'] != 2:
            btn.configure(text=obj['around'])
            btn['state'] = 'disabled'
        else:
            self.bombed()


    def flag(self, obj, btn):
        # Flag a button
        if obj['flagged']:
            obj['flagged'] = False
            btn.configure(text='')
        else:
            obj['flagged'] = True
            btn.configure(text=u"\u2691")



    def setup(self, obj, amt):
        # Generate the bombs

        self.bombs = amt
        bbtnList = btnList = list(self.buttons)

        for x in range(0, amt):
            btn = random.choice(btnList)
            if self.buttons[btn]['type'] == None and self.buttons[btn]['id'] != obj['id']:
                self.buttons[btn]['type'] = 2
                self.buttons[btn]['around'] = -1
                btn.configure(text="X")
                bbtnList.remove(btn)

        # Get the bombs around each button that is not a bomb.

        areas = [-(self.dimensions[0]-1), -(self.dimensions[0]),-(self.dimensions[0]+1),
                 -1, 1,
                 self.dimensions[0]-1, self.dimensions[0], self.dimensions[0]+1]



        for object in btnList:
            if self.buttons[object]['type'] != 2:
                for y in areas:
                    v = self.buttons[object]['id'] + y
                    btn = [key for key, value in self.buttons.items() if value['id'] == v]
                    if btn:
                        if self.buttons[btn[0]]['type'] == 2:
                            if self.buttons[object]['id'] == 240:
                                print('ID: %s\nV: %s' % (self.buttons[btn[0]]['id'], v))
                            if self.buttons[object]['type'] != 1:
                                self.buttons[object]['type'] = 1
                            self.buttons[object]['around'] += 1
                        object.configure(text=self.buttons[object]['around'])

    def bombed(self):
        # Alert loss of game
        option = messagebox.askyesno('You lost!', "You hit a bomb!\nWould you like to play again?")
        if option != None:
            if not option:
                sys.exit()
            self.reset()

    def reset(self):
        # Reset the board
        for x in self.buttons:
            self.buttons[x]['type'] = None
            self.buttons[x]['around'] = 0
            self.buttons[x]['flagged'] = False
            self.bombs = 0
            x['state'] = 'normal'
            x.configure(text='')




root = Tk()

game = Minesweeper(root)
game.createBoard()

Grid.rowconfigure(root, 0, weight=1)
Grid.columnconfigure(root, 0, weight=1)

root.title('Minesweeper')
root.mainloop()

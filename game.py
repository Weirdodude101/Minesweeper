from tkinter import *
from tkinter import messagebox
import sys
import random


class Minesweeper(Frame):
    def __init__(self, root, x, y, b2Gen):
        Frame.__init__(self, root)
        self.grid(row=0, column=0, sticky=N+S+E+W)

        self.dimensions = (x, y)
        self.bombs = 0
        self.b2Gen = b2Gen
        self.regular = 0
        self.buttons = {}

        self.areas = ["-1:-1","-1:0","-1:1",
                      "0:-1", "0:0", "0:1",
                      "1:-1", "1:0", "1:1"]

    def createBoard(self):
        # Generate the board
        for x in range(0, self.dimensions[0]):
            Grid.rowconfigure(self, x, weight=1)
            for y in range(0, self.dimensions[1]):
                Grid.columnconfigure(self, y, weight=1)
                button = Button(self)
                button.pack()
                button.grid(row=x, column=y, sticky=N+S+E+W)
                self.regular += 1
                # Create the button dictionary.

                self.buttons[button] = {
                    "id": None,
                    "type": None,
                    "around": 0,
                    "flagged": False
                }

                self.buttons[button]['id'] = '%s:%s' % (x,y)

        for button in list(self.buttons):
            # Assign the IDs to the buttons and configure them.
            button.configure(command=lambda x=self.buttons[button], y=button:self.select(x, y))
            button.bind('<Button-2>', lambda e, x=self.buttons[button], y=button:self.flag(x, y))

    def select(self, obj, btn):
        # Select a button

        if not self.bombs:
            self.setup(obj, self.b2Gen)

        if obj['type'] != 2:
            if not obj['flagged']:
                btn.configure(text=obj['around'])
                if obj['around'] == 0:
                    self.revealAround(obj)
                btn['state'] = 'disabled'
                obj['type'] = -1
                self.check(obj)
        else:
            self.bombed()

    def revealAround(self, obj):
        areas = self.areas[:]
        remove = [0,2,6,8]
        for index in sorted(remove, reverse=True):
            del areas[index]
        for x in areas:
            objId = obj['id'].split(':')
            r = int(objId[0]) + int(x.split(':')[0])
            c = int(objId[1]) + int(x.split(':')[1])
            btn = [key for key, value in self.buttons.items() if value['id'] == f'{r}:{c}']
            if btn:
                if self.buttons[btn[0]]['around'] == 0:
                    btn[0].configure(text=self.buttons[btn[0]]['around'])
                    btn[0]['state'] = 'disabled'

                    obj = self.buttons[btn[0]]


    def flag(self, obj, btn):
        # Flag a button
        if obj['type'] != -1:
            if obj['flagged']:
                obj['flagged'] = False

                if obj['type'] == 2:
                    self.bombs += 1
                btn.configure(text='')
            else:
                obj['flagged'] = True
                if obj['type'] == 2:
                    self.bombs -= 1
                btn.configure(text=u"\u2691")
                self.check(obj)

    def check(self, obj):
        if self.bombs <= 0 or self.regular <= 0:
            self.askyesno(title='You won!', msg="You won the game!\nWould you like to play again?", cb1=sys.exit, cb2=self.reset)

    def setup(self, obj, amt):
        # Generate the bombs

        self.bombs = amt
        self.regular -= amt
        bbtnList = btnList = list(self.buttons)

        for x in range(0, amt):
            btn = random.choice(btnList)
            if self.buttons[btn]['type'] == None and self.buttons[btn]['id'] != obj['id']:
                self.buttons[btn]['type'] = 2
                self.buttons[btn]['around'] = -1
                bbtnList.remove(btn)

        # Get the bombs around each button that is not a bomb.

        for object in btnList:
            if self.buttons[object]['type'] != 2:
                objId = self.buttons[object]['id'].split(':')
                for y in self.areas:
                    r = int(objId[0]) + int(y.split(':')[0])
                    c = int(objId[1]) + int(y.split(':')[1])
                    btn = [key for key, value in self.buttons.items() if value['id'] == f'{r}:{c}']
                    if btn:
                        if self.buttons[btn[0]]['type'] == 2:
                            if self.buttons[object]['type'] != 1:
                                self.buttons[object]['type'] = 1
                            self.buttons[object]['around'] += 1

    def bombed(self):
        self.revealBoard()
        self.askyesno(title='You lost!', msg="You hit a bomb!\nWould you like to play again?", cb1=sys.exit, cb2=self.reset)

    def revealBoard(self):
        for obj in self.buttons:
            if self.buttons[obj]['type'] != 2:
                obj.configure(text=self.buttons[obj]['around'])
                obj['state'] = 'disabled'
                continue
            obj.configure(text='X')


    def askyesno(self, title="", msg="", cb1=None, cb2=None):
        option = messagebox.askyesno(title, msg)
        if option != None:
            if not option:
                cb1()
            cb2()

    def reset(self):
        # Reset the board

        for x in self.buttons:
            self.buttons[x]['type'] = None
            self.buttons[x]['around'] = 0
            self.buttons[x]['flagged'] = False
            self.bombs = 0
            self.regular = self.dimensions[0] * self.dimensions[1]
            x['state'] = 'normal'
            x.configure(text='')




root = Tk()
"""while True:
    x = int(input('Rows (Minimum 4): '))
    y = int(input('Columns (Minimum 4): '))
    if x < 4 or y < 4:
        print('Minimum amount of rows and/or columns is 4')
    else:
        break

while True:
    b = int(input('Bombs: '))
    if b >= x*y:
        print('Amount of bombs cannot be greater then or equal to the amount of spaces')
    else:
        break"""
x = 16
y = 16
b = 32
game = Minesweeper(root, x, y, b)
game.createBoard()

Grid.rowconfigure(root, 0, weight=1)
Grid.columnconfigure(root, 0, weight=1)

root.title('Minesweeper')
root.mainloop()

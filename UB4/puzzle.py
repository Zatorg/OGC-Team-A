from tkinter import Frame, Label, CENTER
import random
import numpy as np
import logic
import constants as c


class GameGrid(Frame):
    def __init__(self, size=4, use_manual=False):
        Frame.__init__(self)

        self.grid()
        self.master.title('2048')
        self.master.bind("<Key>", self.key_down)

        self.commands = {
            c.KEY_UP: logic.up,
            c.KEY_DOWN: logic.down,
            c.KEY_LEFT: logic.left,
            c.KEY_RIGHT: logic.right,
            c.KEY_UP_ALT1: logic.up,
            c.KEY_DOWN_ALT1: logic.down,
            c.KEY_LEFT_ALT1: logic.left,
            c.KEY_RIGHT_ALT1: logic.right,
            c.KEY_UP_ALT2: logic.up,
            c.KEY_DOWN_ALT2: logic.down,
            c.KEY_LEFT_ALT2: logic.left,
            c.KEY_RIGHT_ALT2: logic.right,
        }

        self.virtual_commands = {
            0: logic.up,
            2: logic.down,
            3: logic.left,
            1: logic.right
        }

        self.size = size
        self.grid_cells = []
        self.init_grid()
        self.matrix = logic.new_game(self.size)
        self.update_grid_cells()
        if use_manual:
            self.mainloop()
        else:
            self.update_idletasks()
            self.update()

    def gen(self):
        return random.randint(0, self.size - 1)

    def init_grid(self):
        background = Frame(self, bg=c.BACKGROUND_COLOR_GAME, width=c.SIZE, height=c.SIZE)
        background.grid()

        for i in range(self.size):
            grid_row = []
            for j in range(self.size):
                cell = Frame(
                    background,
                    bg=c.BACKGROUND_COLOR_CELL_EMPTY,
                    width=c.SIZE / self.size,
                    height=c.SIZE / self.size
                )
                cell.grid(
                    row=i,
                    column=j,
                    padx=c.GRID_PADDING,
                    pady=c.GRID_PADDING
                )
                t = Label(
                    master=cell,
                    text="",
                    bg=c.BACKGROUND_COLOR_CELL_EMPTY,
                    justify=CENTER,
                    font=c.FONT,
                    width=5,
                    height=2)
                t.grid()
                grid_row.append(t)
            self.grid_cells.append(grid_row)

    def update_grid_cells(self):
        for i in range(self.size):
            for j in range(self.size):
                new_number = self.matrix[i, j]
                if new_number == 0:
                    self.grid_cells[i][j].configure(text="", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
                else:
                    self.grid_cells[i][j].configure(
                        text=str(new_number),
                        bg=c.BACKGROUND_COLOR_DICT[new_number],
                        fg=c.CELL_COLOR_DICT[new_number]
                    )
        self.update_idletasks()

    def key_down(self, event):
        key = event.keysym
        print(event)
        if key == c.KEY_QUIT:
            exit()
        elif key in self.commands:
            self.matrix, done = self.commands[key](self.matrix)
            if done:
                self.matrix = logic.add_two(self.matrix)
                self.update_grid_cells()
                if logic.game_state(self.matrix) == 'win':
                    self.grid_cells[1][1].configure(text="You", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
                    self.grid_cells[1][2].configure(text="Win!", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
                if logic.game_state(self.matrix) == 'lose':
                    self.grid_cells[1][1].configure(text="You", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
                    self.grid_cells[1][2].configure(text="Lose!", bg=c.BACKGROUND_COLOR_CELL_EMPTY)

    def generate_next(self):
        index = (self.gen(), self.gen())
        while self.matrix[index[0], index[1]] != 0:
            index = (self.gen(), self.gen())
        self.matrix[index[0], index[1]] = 2

    #CONTROL
    # Up: 0, Right: 1, Down: 2, Left: 3
    def move(self, direction):
        if direction in self.virtual_commands:
            self.matrix, done = self.virtual_commands[direction](self.matrix)
            if done:
                self.matrix = logic.add_two(self.matrix)
                self.update_grid_cells()

    # CONTROL
    def reset(self):
        self.matrix = logic.new_game(self.size)
        self.update_grid_cells()

    #OBSERVE
    def state(self):
        over = False
        game_state = logic.game_state(self.matrix)
        if game_state == 'win' or game_state == 'lose':
            over = True
        return self.matrix, np.amax(self.matrix), over
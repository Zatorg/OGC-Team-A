from tkinter import Frame, Label, CENTER
import constants as c
import logic


class GameGrid(Frame):
    def __init__(self, grid_size):
        Frame.__init__(self, bg=c.BG_COLOR_GAME, width=c.SIZE, height=c.SIZE)

        self.grid_size = grid_size
        self.matrix = logic.new_game(grid_size)
        # OBSERVER
        self.state = logic.state(self.matrix)

        self.master.title('2048')
        self.master.bind("<Key>", self.key_down)
        self.commands = {
            c.UP: logic.up,
            c.DOWN: logic.down,
            c.LEFT: logic.left,
            c.RIGHT: logic.right
        }

        self.grid()
        self.grid_cells = []
        self.init_grid()
        self.update_grid_cells()

        #self.mainloop()

    def init_grid(self):
        for i in range(self.grid_size):
            grid_row = []
            for j in range(self.grid_size):
                cell = Frame(
                    master=self,
                    width=(c.SIZE - (self.grid_size-1)*c.GRID_PAD) / self.grid_size,
                    height=(c.SIZE - (self.grid_size-1)*c.GRID_PAD) / self.grid_size
                )
                cell.grid(row=i, column=j, padx=c.GRID_PAD, pady=c.GRID_PAD)

                t = Label(master=cell, text="", justify=CENTER, font=c.FONT, width=5, height=3)
                t.grid()
                grid_row.append(t)
            self.grid_cells.append(grid_row)

    def update_grid_cells(self):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                num = self.matrix[i][j]
                self.grid_cells[i][j].configure(
                    text=str(num),
                    bg=c.BG_COLOR_DICT[num],
                    fg=c.CELL_COLOR_DICT[num]
                )
        self.update_idletasks()

    def reset(self):
        self.matrix = logic.new_game(self.grid_size)
        self.update_grid_cells()

    def quit(self):
        self.destroy()

    # CONTROL
    def move(self, direction):
        self.matrix, was_changed = self.commands[direction](self.matrix)
        if was_changed:
            self.matrix = logic.add_two(self.matrix)
            self.update_grid_cells()

        # OBSERVER
        self.state = logic.state(self.matrix)

    def key_down(self, event):
        direction = event.keysym

        if direction == c.QUIT:
            exit()

        elif direction == c.RESET:
            self.reset()

        elif direction in self.commands:
            self.move(direction)

            # is this necessary??
            if self.state[2]:
                if self.state[1] == 2048:
                    self.grid_cells[0][0].configure(text="You", bg=c.BG_COLOR_CELL_EMPTY, fg="black")
                    self.grid_cells[0][1].configure(text="Win!", bg=c.BG_COLOR_CELL_EMPTY, fg="black")
                else:
                    self.grid_cells[0][0].configure(text="You", bg=c.BG_COLOR_CELL_EMPTY, fg="black")
                    self.grid_cells[0][1].configure(text="Lose!", bg=c.BG_COLOR_CELL_EMPTY, fg="black")

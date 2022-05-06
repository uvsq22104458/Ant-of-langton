#####################
# importing modules #
#####################
import tkinter as tk
from types import new_class
######################
# Defining constants #
######################
WIDTH = 800
HEIGHT = 800
MAX_SCALE = 200
# ant direction and rotation
UP, DOWN, LEFT, RIGHT = 0, 1, 2, 3
ROTATE_LEFT = (LEFT, RIGHT, DOWN, UP)
ROTATE_RIGHT = (RIGHT, LEFT, UP, DOWN)
MOVE = ((-1, 0), (1, 0), (0, -1), (0, 1))
COLORS = ('white', 'black')
WHITE, BLACK = 0, 1
####################
# Global variables #
####################
grid_scale = 50
offset_grid = WIDTH/grid_scale
grid = [[WHITE]*grid_scale for _ in range(grid_scale)]
grid_GUI = [[WHITE]*grid_scale for _ in range(grid_scale)]
paused = True
delay_value = 100
ants = []
root = tk.Tk()
root.title("Cellular automaton: Ant Of Langdon")
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT)
#############
# Functions #
#############


def create_ant(y, x):
    '''Ant of Langton, it can moves on the grid'''
    global ants
    ant = (y, x, RIGHT)
    ants.append(ant)


def rules():
    ''''''
    global ants, grid, grid_scale
    for i, ant in enumerate(ants):
        y, x, direction = ant
        if grid[y][x] == BLACK:
            new_direction = ROTATE_LEFT[direction]
            grid[y][x] = WHITE
            update_GUI(y, x, 'white')
            offset_y, offset_x = MOVE[new_direction]
            new_y, new_x = y+offset_y, x+offset_x
            if new_y >= grid_scale:
                new_y = 0
            if new_y < 0:
                new_y = grid_scale
            if new_x >= grid_scale:
                new_x = 0
            if new_x < 0:
                new_x = grid_scale
            update_GUI(new_y, new_x, 'red')
        else:
            new_direction = ROTATE_RIGHT[direction]
            grid[y][x] = BLACK
            update_GUI(y, x, 'black')
            offset_y, offset_x = MOVE[new_direction]
            new_y, new_x = y+offset_y, x+offset_x
            if new_y >= grid_scale:
                new_y = 0
            if new_y < 0:
                new_y = grid_scale
            if new_x >= grid_scale:
                new_x = 0
            if new_x < 0:
                new_x = grid_scale
            update_GUI(new_y, new_x, 'red')
        ants[i] = (new_y, new_x, new_direction)


def iteration():
    ''''''
    global id_after, delay_value
    rules()
    id_after = canvas.after(delay_value, iteration)


def draw_GUI():
    '''Create a grid in the canvas'''
    global grid_GUI, grid
    for i in range(grid_scale):
        y0 = offset_grid*i
        y1 = (offset_grid*i) + offset_grid
        for j in range(grid_scale):
            grid_GUI[i][j] = canvas.create_rectangle(
                (offset_grid*j, y0), ((offset_grid*j)+offset_grid, y1),
                fill=COLORS[grid[i][j]], outline='')
    # print(grid_GUI)


def update_GUI(y, x, color):
    canvas.itemconfig(grid_GUI[y][x], fill=color)


def clicked(event):
    ''''''
    global offset_grid, ants
    x, y = int(event.x // offset_grid), int(event.y // offset_grid)
    # print(x, y)
    if any((True for ant in ants if ant[0] == y and ant[1] == x)):
        return
    create_ant(y, x)
    update_GUI(y, x, 'red')
    print(ants)


def play():
    '''Switch between Play or Pause if the button is clicked'''
    global paused, id_after
    if paused:
        play_button.config(text="Pause")
        iteration()
    else:
        play_button.config(text="Play")
        canvas.after_cancel(id_after)
    paused = not paused


def next():
    '''A button'''
    global paused
    if paused:
        rules()
    else:
        return


def back():
    '''A button'''
    pass


def save():
    '''A button'''
    pass


def load():
    '''A button'''
    pass


def delay(int):
    '''A button'''
    global text_entry_delay, delay_value
    delay_value = text_entry_delay.get()
    text_entry_delay.set(int)


def entry_grid_scale(int):
    '''Changes the scale of the grid'''
    global text_entry_scale, offset_grid, grid_scale, grid, grid_GUI, ants
    new_scale = text_entry_scale.get()
    if new_scale > MAX_SCALE:
        grid_scale = MAX_SCALE
    else:
        grid_scale = new_scale
    offset_grid = WIDTH/grid_scale
    grid = [[WHITE]*grid_scale for _ in range(grid_scale)]
    grid_GUI = [[WHITE]*grid_scale for _ in range(grid_scale)]
    ants = []
    print(grid_scale)
    draw_GUI()
    text_entry_scale.set(int)


def GUI_widgets():
    '''Graphic interface using tkinter with buttons and canvas'''
    global text_entry_scale, text_entry_delay, play_button, save_button

    # Labelframe
    labelframe_delay = tk.LabelFrame(root,
                                     text='Changes the delay of the ants')
    labelframe_scale = tk.LabelFrame(root,
                                     text='Changes the scale of the grid')
    # Buttons creation
    quit_button = tk.Button(root, text='Quit', command=root.quit)
    play_button = tk.Button(root, text='Play', command=play)
    next_button = tk.Button(root, text='Next', command=next)
    save_button = tk.Button(root, text='Save', command=save)
    load_button = tk.Button(root, text='Load', command=load)
    back_button = tk.Button(root, text='Back', command=back)
    scale_button = tk.Button(
        labelframe_scale, text='Set', command=lambda: entry_grid_scale(0))
    delay_button = tk.Button(
        labelframe_delay, text='Set', command=lambda: delay(0))
    # IntVar
    text_entry_scale = tk.IntVar()
    text_entry_delay = tk.IntVar()
    # Entry
    delay_entry = tk.Entry(labelframe_delay, textvariable=text_entry_delay)
    scale_text = tk.Entry(labelframe_scale, textvariable=text_entry_scale)
    # widget placement
    canvas.grid(column=1, row=1, columnspan=15)
    play_button.grid(row=0, column=1)
    next_button.grid(row=0, column=2)
    back_button.grid(row=0, column=3)
    save_button.grid(row=0, column=4)
    load_button.grid(row=0, column=5)
    delay_entry.grid(row=0, column=6)
    delay_button.grid(row=0, column=7)
    scale_text.grid(row=0, column=8)
    labelframe_scale.grid(row=0, column=9)
    labelframe_delay.grid(row=0, column=7)
    scale_button.grid(row=0, column=9)
    quit_button.grid(row=0, column=15)
    # Bind
    canvas.bind('<Button-1>', clicked)

################
# Main program #
################


def main():
    '''Main program with tkinter instructions'''
    draw_GUI()
    GUI_widgets()
    root.mainloop()


if __name__ == '__main__':
    main()

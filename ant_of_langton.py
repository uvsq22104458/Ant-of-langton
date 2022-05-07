#####################
# importing modules #
#####################
import tkinter as tk
from tkinter import filedialog as fd
import os
from os.path import exists
from ast import literal_eval
######################
# Defining constants #
######################
WIDTH = 800
HEIGHT = 800
MAX_SCALE = 200
MAX_DELAY = 1000
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
offset_grid = WIDTH//grid_scale
grid = [[WHITE]*grid_scale for _ in range(grid_scale)]
grid_GUI = [[WHITE]*grid_scale for _ in range(grid_scale)]
paused = True
delay_value = 100
iteration_counter = 0
ants = []
root = tk.Tk()
root.title("Cellular automaton: Ant Of Langdon")
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT)
text_iteration_counter = tk.IntVar(
    root, value=iteration_counter)
# Directory creation
directory_name = 'Saves'
path = os.path.join(os.getcwd(), directory_name)
# File creation
file_counter = 0
file_name = f'save{file_counter}.txt'
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
    global ants, grid, grid_scale, iteration_counter, text_iteration_counter
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
                new_y = grid_scale-1
            if new_x >= grid_scale:
                new_x = 0
            if new_x < 0:
                new_x = grid_scale-1
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
                new_y = grid_scale-1
            if new_x >= grid_scale:
                new_x = 0
            if new_x < 0:
                new_x = grid_scale-1
            update_GUI(new_y, new_x, 'red')
        ants[i] = (new_y, new_x, new_direction)
        iteration_counter += 1
        update_value_counter()


def update_value_counter():
    ''''''
    text_iteration_counter.set(iteration_counter)


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


def update_GUI(y, x, color):
    ''''''
    canvas.itemconfig(grid_GUI[y][x], fill=color)


def clicked(event):
    ''''''
    global offset_grid, ants
    x, y = int(event.x // offset_grid), int(event.y // offset_grid)
    if any((True for ant in ants if ant[0] == y and ant[1] == x)):
        return
    create_ant(y, x)
    update_GUI(y, x, 'red')


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
    if not paused:
        return
    rules()


def back():
    '''Reverse rule'''
    global ants, grid, grid_scale, paused, iteration_counter, text_iteration_counter
    if not paused or iteration_counter == 0:
        return
    for i, ant in enumerate(ants):
        y, x, direction = ant
        offset_y, offset_x = MOVE[direction]
        new_y, new_x = y-offset_y, x-offset_x
        if new_y >= grid_scale:
            new_y = 0
        if new_y < 0:
            new_y = grid_scale-1
        if new_x >= grid_scale:
            new_x = 0
        if new_x < 0:
            new_x = grid_scale-1
        update_GUI(y, x, COLORS[grid[y][x]])
        if grid[new_y][new_x] == BLACK:
            new_direction = ROTATE_LEFT[direction]
            grid[new_y][new_x] = WHITE
            update_GUI(new_y, new_x, 'red')
        else:
            new_direction = ROTATE_RIGHT[direction]
            grid[new_y][new_x] = BLACK
            update_GUI(new_y, new_x, 'red')
        ants[i] = (new_y, new_x, new_direction)
        iteration_counter -= 1
        update_value_counter()


def save():
    '''A button'''
    global file_counter, file_name, grid, grid_scale, ants, offset_grid, iteration_counter
    if not exists(path):
        os.mkdir(path)
    for files in os.listdir(path):
        if files == file_name:
            file_counter += 1
            file_name = f'save{file_counter}.txt'
    with open(os.path.join(path, file_name), 'w') as file:
        file.write(
            f'{grid_scale}\n{iteration_counter}\n{offset_grid}\n{ants}\n{grid}')
        file.close()


def load():
    '''A button'''
    global grid, grid_scale, ants, offset_grid, grid_GUI, iteration_counter
    lines = []
    load_file = fd.askopenfilename(initialdir=path,
                                   title="Select a save",
                                   filetypes=(("Text files",
                                               "*.txt*"),
                                              ("all files",
                                               "*.*")))
    if load_file:
        load_file = load_file[load_file.rfind('save'):]
        with open(os.path.join(path, load_file), 'r') as file:
            content = file.readlines()
        for line in content:
            lines.append(line)
        print(lines)
        grid_scale = int(lines[0])
        grid_GUI = [[WHITE]*grid_scale for _ in range(grid_scale)]
        iteration_counter = int(lines[1])
        offset_grid = int(lines[2])
        ants = literal_eval(lines[3])
        grid = literal_eval(lines[4])
        update_value_counter()
        draw_GUI()


def delay(int):
    '''A button'''
    global text_entry_delay, delay_value
    delay_value = text_entry_delay.get()
    if delay_value > MAX_DELAY:
        delay_value = MAX_DELAY
    text_entry_delay.set(int)


def entry_grid_scale(int):
    '''Changes the scale of the grid'''
    global text_entry_scale, offset_grid, grid_scale, grid, grid_GUI, ants
    new_scale = text_entry_scale.get()
    if new_scale > MAX_SCALE:
        grid_scale = MAX_SCALE
    else:
        grid_scale = new_scale
    offset_grid = WIDTH//grid_scale
    grid = [[WHITE]*grid_scale for _ in range(grid_scale)]
    grid_GUI = [[WHITE]*grid_scale for _ in range(grid_scale)]
    ants = []
    draw_GUI()
    text_entry_scale.set(int)


def GUI_widgets():
    '''Graphic interface using tkinter with buttons and canvas'''
    global text_entry_scale, text_entry_delay, play_button, save_button, iteration_counter

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
    # Label
    label_interation_counter = tk.Label(
        root, textvariable=text_iteration_counter)
    # Entry
    delay_entry = tk.Entry(labelframe_delay, textvariable=text_entry_delay)
    scale_text = tk.Entry(labelframe_scale, textvariable=text_entry_scale)
    # widget placement
    canvas.grid(column=1, row=1, columnspan=15, rowspan=15)
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
    label_interation_counter.grid(row=1, column=1)
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

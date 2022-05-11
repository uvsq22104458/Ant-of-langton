#####################
# importing modules #
#####################
import tkinter as tk
from tkinter import filedialog as fd
import os
from os.path import exists
from ast import literal_eval
import re
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
# grid
grid_scale = 50
offset_grid = WIDTH//grid_scale
grid = [[WHITE]*grid_scale for _ in range(grid_scale)]
grid_GUI = [[WHITE]*grid_scale for _ in range(grid_scale)]
paused = True
delay_value = 100
iteration_counter = 0
ants = []
# tkinter
root = tk.Tk()
root.title("Cellular automaton: Ant Of Langdon")
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT)
text_iteration_counter = tk.IntVar(
    root, value=iteration_counter)
#############
# Functions #
#############


def create_ant(y, x):
    '''Creates a new ant with coordinates and a direction
    then add it to the list of ants'''
    global ants
    ant = (y, x, RIGHT)
    ants.append(ant)


def rules():
    '''Rules that dictate how the ants will move
    depending on the color of the square they are currently in'''
    global ants, grid, grid_scale, iteration_counter
    previous_ant = []
    for i, ant in enumerate(ants):
        y, x, direction = ant
        if grid[y][x] == BLACK:
            new_direction = ROTATE_LEFT[direction]
            grid[y][x] = WHITE
            if not (y, x) in previous_ant:
                update_square_color(y, x, 'white')
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
            update_square_color(new_y, new_x, 'red')
            previous_ant.append((new_y, new_x))
            ants[i] = (new_y, new_x, new_direction)
        else:
            new_direction = ROTATE_RIGHT[direction]
            grid[y][x] = BLACK
            if not (y, x) in previous_ant:
                update_square_color(y, x, 'black')
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
            update_square_color(new_y, new_x, 'red')
            previous_ant.append((new_y, new_x))
            ants[i] = (new_y, new_x, new_direction)
        iteration_counter += 1
        update_iteration_counter()


def back():
    '''Rules to return to a previous iteration'''
    global ants, grid, grid_scale, paused, iteration_counter
    global text_iteration_counter
    if not paused or iteration_counter == 0:
        return
    previous_ant = []
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
        if not (y, x) in previous_ant:
            update_square_color(y, x, COLORS[grid[y][x]])
        if grid[new_y][new_x] == BLACK:
            new_direction = ROTATE_LEFT[direction]
            grid[new_y][new_x] = WHITE
            update_square_color(new_y, new_x, 'red')
        else:
            new_direction = ROTATE_RIGHT[direction]
            grid[new_y][new_x] = BLACK
            update_square_color(new_y, new_x, 'red')
        ants[i] = (new_y, new_x, new_direction)
        iteration_counter -= 1
        update_iteration_counter()


def simulation_loop():
    '''Run the rules in a loop with a delay'''
    global id_after, delay_value
    rules()
    id_after = canvas.after(delay_value, simulation_loop)


def draw_GUI():
    '''Create a grid in the canvas with colored rectangles.'''
    global grid_GUI, grid
    for i in range(grid_scale):
        y0 = offset_grid*i
        y1 = (offset_grid*i) + offset_grid
        for j in range(grid_scale):
            grid_GUI[i][j] = canvas.create_rectangle(
                (offset_grid*j, y0), ((offset_grid*j)+offset_grid, y1),
                fill=COLORS[grid[i][j]], outline='')


def update_iteration_counter():
    '''Display in the canvas the updated iteration counter.'''
    text_iteration_counter.set(iteration_counter)


def update_square_color(y, x, color):
    '''Update the color of a square with given coordinates in the GUI'''
    canvas.itemconfig(grid_GUI[y][x], fill=color)


def clicked(event):
    '''Creates an ant on click and set the clicked square to red'''
    global offset_grid, ants
    x, y = int(event.x // offset_grid), int(event.y // offset_grid)
    if any((True for ant in ants if ant[0] == y and ant[1] == x)):
        return
    create_ant(y, x)
    update_square_color(y, x, 'red')


def play():
    '''Switch between Play or Pause if the button is clicked. When is Play,
    start the iteration of ants'''
    global paused, id_after
    if paused:
        play_button.config(text="Pause")
        simulation_loop()
    else:
        play_button.config(text="Play")
        canvas.after_cancel(id_after)
    paused = not paused


def next():
    '''Calls one time the rules function if the game is paused'''
    global paused
    if not paused:
        return
    rules()


def save(path):
    '''Save the current values of the simulation in a file'''
    global grid, grid_scale, ants, offset_grid, iteration_counter
    if not exists(path):
        os.mkdir(path)
    nb_files = sorted([int(n)
                       for n in re.findall(r"\d+", ''.join(os.listdir(path)))])
    file_name = f'save{len(nb_files)}.txt'
    for i, n in enumerate(nb_files):
        if i != n:
            file_name = f'save{i}.txt'
    with open(os.path.join(path, file_name), 'w') as file:
        file.write(f'{grid_scale}\n{iteration_counter}\n')
        file.write(f'{offset_grid}\n{ants}\n{grid}')
        file.close()


def load(path):
    '''Load the values of a selected file on the screen'''
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
        grid_scale = int(lines[0])
        grid_GUI = [[WHITE]*grid_scale for _ in range(grid_scale)]
        iteration_counter = int(lines[1])
        offset_grid = int(lines[2])
        ants = literal_eval(lines[3])
        grid = literal_eval(lines[4])
        update_iteration_counter()
        draw_GUI()
        for ant in ants:
            update_square_color(ant[0], ant[1], 'red')


def delay():
    '''Gets the delay between iterations'''
    global text_entry_delay, delay_value
    delay_value = text_entry_delay.get()
    if delay_value > MAX_DELAY:
        delay_value = MAX_DELAY
    text_entry_delay.set(0)


def entry_grid_scale():
    '''Changes and resets the grid scale'''
    global text_entry_scale, offset_grid, grid_scale, grid, grid_GUI, ants
    global iteration_counter
    new_scale = text_entry_scale.get()
    if new_scale > MAX_SCALE:
        grid_scale = MAX_SCALE
    else:
        grid_scale = new_scale
    # reset variables
    offset_grid = WIDTH//grid_scale
    grid = [[WHITE]*grid_scale for _ in range(grid_scale)]
    grid_GUI = [[WHITE]*grid_scale for _ in range(grid_scale)]
    ants = []
    iteration_counter = 0
    update_iteration_counter()
    draw_GUI()
    text_entry_scale.set(0)


def GUI_widgets():
    '''Graphic interface using tkinter with buttons, canvas,
    Labelframe, Intvar, entry, bind and the widget placement'''
    global text_entry_scale, text_entry_delay, play_button, save_button
    global iteration_counter
    path = os.path.join(os.getcwd(), 'Saves')
    # Labelframe
    labelframe_delay = tk.LabelFrame(root,
                                     text='Changes the delay of the ants')
    labelframe_scale = tk.LabelFrame(root,
                                     text='Changes the scale of the grid')
    # Buttons creation
    quit_button = tk.Button(root, text='Quit', command=root.quit)
    play_button = tk.Button(root, text='Play', command=play)
    next_button = tk.Button(root, text='Next', command=next)
    save_button = tk.Button(root, text='Save', command=lambda: save(path))
    load_button = tk.Button(root, text='Load', command=lambda: load(path))
    back_button = tk.Button(root, text='Back', command=back)
    scale_button = tk.Button(
        labelframe_scale, text='Set', command=entry_grid_scale)
    delay_button = tk.Button(
        labelframe_delay, text='Set', command=delay)
    # IntVar
    text_entry_scale = tk.IntVar()
    text_entry_delay = tk.IntVar()
    # Label
    label_iteration_counter = tk.Label(
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
    label_iteration_counter.grid(row=1, column=1)
    # Bind
    canvas.bind('<Button-1>', clicked)

################
# Main program #
################


def main():
    '''Main functions and variables'''
    draw_GUI()
    GUI_widgets()
    root.mainloop()


if __name__ == '__main__':
    main()

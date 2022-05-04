#####################
# importing modules #
#####################
import tkinter as tk
from functools import partial
######################
# Defining constants #
######################
WIDTH = 800
HEIGHT = 800
MAX_SCALE = 200
root = tk.Tk()
root.title("Cellular automaton: Ant Of Langdon")
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT)
####################
# Global variables #
####################
grid_scale = 6
offset_grid = WIDTH/grid_scale
grid = [[0]*grid_scale for _ in range(grid_scale)]
grid_GUI = [[0]*grid_scale for _ in range(grid_scale)]
has_stopped = True
#############
# Functions #
#############


def create_ant():
    '''Ant of Langton, it can moves on the grid'''


def draw_GUI():
    '''Create a grid in the canvas'''
    global grid_GUI, grid
    for i in range(grid_scale):
        y0 = offset_grid*i
        y1 = (offset_grid*i) + offset_grid
        for j in range(grid_scale):
            grid_GUI[i][j] = canvas.create_rectangle(
                (offset_grid*j, y0), ((offset_grid*j)+offset_grid, y1),
                fill='white' if grid[i][j] == 0 else 'black', outline='black')
    print(grid_GUI)


def clicked(event):
    ''''''
    x, y = event.x, event.y
    for y in range(grid_scale):
        for x in range(grid_scale):
            if x and y:
                grid[y][x] = 1
    print(x, y)
    draw_GUI()


def play():
    '''Switch between Play or Pause if the button is clicked'''
    global has_stopped
    if has_stopped:
        play_button.config(text="Pause")
    else:
        play_button.config(text="Play")
    has_stopped = not has_stopped


def next():
    '''A button'''
    pass


def back():
    '''A button'''
    pass


def save():
    '''A button'''
    pass


def load():
    '''A button'''
    pass


def speed_step(int):
    '''A button'''
    global text_entry_speed, speed
    speed = text_entry_speed.get()
    text_entry_speed.set(int)


def entry_grid_scale(int):
    '''Changes the scale of the grid'''
    global text_entry_scale, offset_grid, grid_scale, grid, grid_GUI
    new_scale = text_entry_scale.get()
    if new_scale > MAX_SCALE:
        grid_scale = MAX_SCALE
    else:
        grid_scale = new_scale
    offset_grid = WIDTH/grid_scale
    grid = [[0]*grid_scale for _ in range(grid_scale)]
    grid_GUI = [[0]*grid_scale for _ in range(grid_scale)]
    print(grid_scale)
    draw_GUI()
    text_entry_scale.set(int)


def GUI_widgets():
    '''Graphic interface using tkinter with buttons and canvas'''
    global text_entry_scale, text_entry_speed, play_button, save_button

    # Labelframe
    labelframe_speed = tk.LabelFrame(root,
                                     text='Changes the speed of the ants')
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
    speed_button = tk.Button(
        labelframe_speed, text='Set', command=lambda: speed_step(0))
    # IntVar
    text_entry_scale = tk.IntVar()
    text_entry_speed = tk.IntVar()
    # Entry
    speed_entry = tk.Entry(labelframe_speed, textvariable=text_entry_speed)
    scale_text = tk.Entry(labelframe_scale, textvariable=text_entry_scale)
    # widget placement
    canvas.grid(column=1, row=1, columnspan=15)
    play_button.grid(row=0, column=1)
    next_button.grid(row=0, column=2)
    back_button.grid(row=0, column=3)
    save_button.grid(row=0, column=4)
    load_button.grid(row=0, column=5)
    speed_entry.grid(row=0, column=6)
    speed_button.grid(row=0, column=7)
    scale_text.grid(row=0, column=8)
    labelframe_scale.grid(row=0, column=9)
    labelframe_speed.grid(row=0, column=7)
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

#####################
# importing modules #
#####################
import tkinter as tk
from functools import partial

######################
# Defining constants #
######################
WIDTH = 600
HEIGHT = 600
GRID_SCALE = 6
OFFSET_GRID = WIDTH/GRID_SCALE
####################
# Global variables #
####################
grid = []

#############
# Functions #
#############


def config_ini():
    '''Creation of the grid'''
    grid = [[0]*GRID_SCALE for _ in range(GRID_SCALE)]
    print(f"0: {grid}")


def grid_creation(root, canvas):
    '''Create a grid with create_rectangle() using config_ini'''
    for i in range(GRID_SCALE):
        y0 = OFFSET_GRID*i
        y1 = (OFFSET_GRID*i) + OFFSET_GRID
        for j in range(GRID_SCALE):
            canvas.create_rectangle(
                (OFFSET_GRID*j, y0), ((OFFSET_GRID*j)+OFFSET_GRID, y1), fill='white')


def GUI_widgets(root, canvas):
    '''Graphic interface using tkinter with buttons and canvas'''
    # Buttons creation
    quit_button = tk.Button(root, text='Quit', command=root.quit)
    # widget placement
    canvas.grid(column=1, row=1, rowspan=4)
    quit_button.grid(row=4)

################
# Main program #
################


def main():
    '''Main program with tkinter instructions'''
    root = tk.Tk()
    root.title("Cellular automaton: Ant Of Langdon")
    canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT)
    config_ini()
    grid_creation(root, canvas)
    GUI_widgets(root, canvas)
    root.mainloop()


if __name__ == '__main__':
    main()

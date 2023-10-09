from tkinter import *
from cell import Cell
import settings
import util

root = Tk() # root is convention for tkinter

root.geometry(f'{settings.width}x{settings.height}') # window size in pixels
root.configure(bg='black') # background color chose
root.title('MineSweeper Game') # change window name
root.resizable(False, False) # Disable window resize 


# top frame for title and other info
top_frame = Frame(root, bg='black', width = settings.width, height = util.height_prct(25))
top_frame.place(x=0, y=0)

# left frame for additional information
left_frame = Frame(root, bg='black', width = util.width_prct(25), height = util.height_prct(75))
left_frame.place(x=0, y= util.height_prct(25))

game_title = Label(
    top_frame,
    bg = 'black',
    fg = 'white',
    text = 'MineSweeper Game',
    font = ('Arial', 48),
)

game_title.place(
    x=util.width_prct(25),
    y=0
)

# creating the fram where the main game will be played
center_frame = Frame(root, bg='black', width = util.width_prct(75), height = util.height_prct(75))
center_frame.place(x = util.width_prct(25), y = util.height_prct(25))


for x in range(settings.grid_size):
    for y in range(settings.grid_size):
        c = Cell(x,y)
        c.create_button_object(center_frame)
        c.cell_button_object.grid(column=x, row = y)

# Call label from cell class
Cell.create_cell_count_label(left_frame)
Cell.cell_count_label_object.place(x=0,y=0)

Cell.randomize_mines()

root.mainloop() # initiates the program
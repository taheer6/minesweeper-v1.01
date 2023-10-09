from tkinter import Button, Label
import random
import settings
import ctypes 
import sys

class Cell:

    all = [] # list of all cells
    cell_count_label_object = None
    cell_count = settings.cell_count

    # x and y are the coordinates of the cell
    def __init__(self, x, y, is_mine=False):
        self.is_mine = is_mine
        self.cell_button_object = None
        self.is_mine_candidate = False
        self.x = x
        self.y = y
        self.revealed = False

        Cell.all.append(self)

    # creates a button object for the cell and binds the left and right click events
    def create_button_object(self, location):
        btn = Button(location, width = 12, height = 4)
        btn.bind('<Button-1>', self.left_click)
        btn.bind('<Button-3>', self.right_click) 
        self.cell_button_object = btn

    @staticmethod
    def create_cell_count_label(location):
        lbl = Label(
            location,
            bg = 'black',
            fg = 'white',
            text = f"Cells Left:{Cell.cell_count}",
            width = 12,
            height = 4,
            font = ('Arial', 30)
        )
        Cell.cell_count_label_object = lbl

    # 
    def left_click(self, event):
        # if the cell is a mine, show the mine
        if self.is_mine:
            self.show_mine()
        else:
            self.reveal_zero_mines_around()   

        if cell.cell_count == settings.mines_count:
            ctypes.windll.user32.MessageBoxW(0, "You Won", "Game Over", 0)
            sys.exit()

        self.cell_button_object.unbind('<Button-1>')
        self.cell_button_object.unbind('<Button-3>')

        
    def reveal_zero_mines_around(self):
        if self.revealed:  # stop if the cell is already revealed
            return
        
        self.revealed = True  # mark this cell as revealed
        self.show_cell()   # show the number of mines around it

        if self.surrounded_cells_mines == 0:
            for cell in self.surrounded_cells:
                cell.reveal_zero_mines_around()   # recursion
    
    # returns the cell object based on the x and y coordinates
    def get_cell_by_axis(self,x,y):
        for cell in Cell.all:
            if cell.x == x and cell.y == y:
                return cell
    @property
    # returns a list of all the cells around the cell in a one cell radius
    def surrounded_cells(self):
        cells = [
            self.get_cell_by_axis(self.x - 1, self.y - 1), 
            self.get_cell_by_axis(self.x -1, self.y),
            self.get_cell_by_axis(self.x -1, self.y +1),
            self.get_cell_by_axis(self.x, self.y -1),
            self.get_cell_by_axis(self.x +1, self.y -1),
            self.get_cell_by_axis(self.x +1,self.y),
            self.get_cell_by_axis(self.x+1,self.y+1),
            self.get_cell_by_axis(self.x, self.y+1)
        ]

        cells = [cell for cell in cells if cell is not None]
        return cells       
    
    @property
    # returns the number of mines around the cell thorugh conter
    def surrounded_cells_mines(self):
        counter = 0
        for cell in self.surrounded_cells:
            if cell.is_mine:
                counter +=1
        return counter

    # shows the number of mines around the cell
    def show_cell(self):
        Cell.cell_count -=1
        self.cell_button_object.configure(text=self.surrounded_cells_mines)
        if Cell.cell_count_label_object:
            Cell.cell_count_label_object.configure(
                text=f"Cells Left:{Cell.cell_count}"
                )
            self.cell_button_object.configure(
                bg='SystemButtonFace'
            )
        self.is_opened = True 


    def show_mine(self):
        # change the color of the button to red if mine then end game
        self.cell_button_object.configure(bg = "red")
        ctypes.windll.user32.MessageBoxW(0, "You Lost", "Game Over", 0)
        sys.exit()

    # right click event
    def right_click(self, event):
        if not self.is_mine_candidate:
            self.cell_button_object.configure(
                bg = 'orange'
            )
            self.is_mine_candidate = True
        else:
            self.cell_button_object.configure(
                bg = 'SystemButtonFace'
            )
            self.is_mine_candidate = False

    # randomizes the mines in the game
    @staticmethod
    def randomize_mines():
        picked_cells = random.sample(Cell.all, settings.mines_count)
        for picked_cell in picked_cells:
            picked_cell.is_mine = True

    def __repr__(self):
        return f"Cell({self.x}, {self.y})"

    def restart_program():
        python = sys.executable
        os.execl(python, python, * sys.argv)

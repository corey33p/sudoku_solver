from sudoku_solver import Solver
from sudoku_display import Display
from tkinter import mainloop
import threading

class Parent:
    def __init__(self,board_path):
        self.solver = Solver(self,board_path)
        self.display = Display(self)
        go_thread = threading.Thread(target=self.solver.solve_sequence)
        go_thread.daemon = True
        go_thread.start()
        return mainloop()

if __name__ == '__main__':
    main_object=Parent("E:/Documents/sudoku/Sudoku 2/puzzle 6--evil.txt")

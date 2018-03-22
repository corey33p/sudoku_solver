import fileinput
import filecmp
import os.path
import numpy as np

class Solver:
    def __init__(self, board_path):
        self.loadboard(filename = board_path)
        self.printboard(self.board)
        self.starting_board = np.copy(self.board)
        self.possibilities = np.zeros((9,9,9))
        for i in range(1,10): self.possibilities[:,:,i-1] = i
        stretch_board = self.board.reshape(9,9,1).repeat(9,axis=2)
        self.possibilities[self.possibilities == stretch_board] += 1
        self.possibilities[self.possibilities == 10] = 1
    def manualboard(self):
        cell = 0
        print('Input puzzle manually...\n')
        while cell < 81:
            cell += 1
            row = ((cell - 1)//9 + 1)
            column = cell % 9
            if column == 0:
                column = 9
            self.board[row, column] = input('Value at row ' + str(row) + ', column ' + str(column) + ': ')
        return
    def printoptions(self):
        all = os.listdir()
        index = 0
        print('\n')
        while index < len(all):
            if os.path.isfile(all[index]):
                    print(all[index])
            index = index + 1
        print('\n')
        return
    def loadboard(self,filename = None):
        if not filename: filename = input('In which file is the sudoku data located? ')
        while (os.path.isfile(filename) == False):
            print('\nNot a valid filename. Press 1 to view files to choose from or 2 to enter a new filename:\n')
            choice = input('1 or 2? ')
            while (choice != '1') and (choice != '2'):
                choice = input("Choose '1' or '2': ")
            if choice == '1':
                printoptions()
                filename = input('In which file is the sudoku data located? ')
            elif choice == '2': filename = input('\nIn which file is the sudoku data located? ')
        self.board = np.loadtxt(filename,dtype=np.int32)
    def printboard(self,board=None):
        if board is None: board = self.board
        print('\n')
        for row in range(board.shape[0]):
            print(" ",end="")
            for column in range(board.shape[1]):
                if column == 8 and ((row + 1) % 3 == 0):
                    if board[row, column] == 0: print("_")
                    else: print(str(board[row, column]))
                    print('-----------------------------')
                elif column == 8:
                    if board[row, column] == 0: print("_\n")
                    else: print(str(board[row, column]) + '\n')
                elif (column + 1) % 3 == 0:
                    if board[row, column] == 0: print("_ | ", end = '')
                    else: print(str(board[row, column]) + ' | ', end = '')
                else:
                    if board[row, column] == 0: print("_  ", end='')
                    else: print(str(board[row, column]) + '  ', end = '')
        print('\n')
        return
    def exclude_possibilities(self):
        board_updated = False
        for row in range(9):
            for column in range(9):
                if self.board[row,column] == 0:
                    group_col_begin = 3 * (column // 3)
                    group_row_begin = 3 * (row // 3)
                    for i in range(1,10):
                        unique = np.unique(self.possibilities[row,column,:])
                        if unique.size > 1:
                            if unique[0] == i: unique_not_i = unique[1]
                            else: unique_not_i = unique[0]
                        if i in self.board[group_row_begin:group_row_begin+3,group_col_begin:group_col_begin+3]:
                            self.possibilities[row,column,:][self.possibilities[row,column,:] == i] = unique_not_i
                        elif i in self.board[row,:]:
                            self.possibilities[row,column,:][self.possibilities[row,column,:] == i] = unique_not_i
                        elif i in self.board[:,column]:
                            self.possibilities[row,column,:][self.possibilities[row,column,:] == i] = unique_not_i
        for row in range(self.board.shape[0]):
            for column in range(self.board.shape[1]):
                unique_possibilities = np.unique(self.possibilities[row,column,:])
                if len(unique_possibilities) == 1 and self.board[row,column] != unique_possibilities[0]:
                    self.board[row,column] = unique_possibilities[0]
                    self.possibilities[row,column,:] = unique_possibilities[0]
                    return True
        return board_updated
    def pp(self):
        for i in range(self.possibilities.shape[2]):
            print(str(self.possibilities[:,:,i]) + "\n")
    def best_guess(self):
        fewest_possibilities = 10
        for row in range(9):
            for column in range(9):
                current_possibilities = np.unique(self.possibilities[row,column,:])
                num_possibilities = current_possibilities.size
                if num_possibilities == 2:
                    return row, column, current_possibilities.astype(np.int32)
                if num_possibilities < fewest_possibilities:
                    fewest_possibilities = num_possibilities
                    best_possibilities = current_possibilities
                    best_row_column = [row, column]
        return best_row_column[0], best_row_column[1], best_possibilities.astype(np.int32)
    def solve_sequence(self):
        counter = 0
        while True:
            if (self.board != 0).sum() == 81: return True
            break_loop = False
            if counter % 2 == 0:
                while not break_loop:
                    print("exclude...")
                    break_loop = not self.exclude_possibilities()
                    if break_loop: counter += 1
                    print("break_loop: " + str(break_loop))
                    self.printboard()
                    input()
            else:
                print("guess...")
                board_save = np.copy(self.board)
                poss_save = np.copy(self.possibilities)
                row, column, guesses = self.best_guess()
                for guess in guesses:
                    print("row, column, guess: " + str(row), str(column), str(guess))
                    self.board[row,column] = guess
                    if self.solve_sequence(): break
                    self.board = np.copy(board_save)
                    self.possibilities = np.copy(poss_save)
                    board_save = np.copy(self.board)
                    poss_save = np.copy(self.possibilities)
                counter += 1

a=Solver("C:/Users/cpa01430/Documents/Python/sudoku/puzzle 2.txt")
a.solve_sequence()
a.printboard()

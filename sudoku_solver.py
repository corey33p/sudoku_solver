import fileinput
import filecmp
import os.path
import numpy as np

class Solver:
    def __init__(self, parent, board_path):
        self.parent = parent
        self.loadboard(filename = board_path)
        self.printboard(self.board)
        self.debug = False
        self.guess_depth = 0
        # self.starting_board = np.copy(self.board)
        self.possibilities = np.zeros((9,9,9),np.uint8)
        for i in range(1,10): self.possibilities[:,:,i-1] = i
        for row in range(9):
            for column in range(9):
                if self.board[row,column] != 0:
                    self.possibilities[row,column,:] = 0
                    self.possibilities[row,column,self.board[row,column]-1] = self.board[row,column]
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
    def note_maker(self,type):
        if type not in ('s','m','g'):
            return
        answer = ''
        for i in range(self.guess_depth): answer += '|--'
        answer += '>'
        if type == 's':   answer += ' Single number exclusion '
        elif type == 'm': answer += ' Multi number exclusion  '
        elif type == 'g': answer += ' Number guessed          '
        numbers_on_board = (self.board != 0).sum()
        answer += str(numbers_on_board)
        answer += '/81\n'
        return answer
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
        self.board = np.loadtxt(filename,dtype=np.uint8)
    def printboard(self,board=None,box=None):
        if board is None: board = self.board
        print('\n')
        the_str = "                            \n"
        for row in range(board.shape[0]):
            the_str += "  "
            for column in range(board.shape[1]):
                if column == 8 and ((row + 1) % 3 == 0):
                    if board[row, column] == 0: the_str += " \n"
                    else: the_str += (str(board[row, column]) + "\n")
                    the_str += '  ----------------------------\n'
                elif column == 8:
                    if board[row, column] == 0: the_str += "_\n                            \n"
                    else: the_str += (str(board[row, column]) + '\n                            \n')
                elif (column + 1) % 3 == 0:
                    if board[row, column] == 0: the_str += "_ | "
                    else: the_str += (str(board[row, column]) + ' | ')
                else:
                    if board[row, column] == 0: the_str += "_  "
                    else: the_str += str(board[row, column]) + '  '
        the_str += '\n'
        the_str = the_str.split("\n")
        if box:
            row = box[0] * 2 + 1
            col = (box[1] * 3 + 3) + ((box[1]) // 3)
            the_str[row-1] = the_str[row-1][:col-2] + "___" + the_str[row-1][col+1:]
            the_str[row+1] = the_str[row+1][:col-2] + "~~~" + the_str[row+1][col+1:]
            the_str[row] = the_str[row][:col-3] + "| " + the_str[row][col-1] + " |" + the_str[row][col+2:]
        for _ in the_str: print(_)
    def search(self):
        if self.debug: print("search...")
        # rule out possible numbers based on current numbers
        for row in range(9):
            for column in range(9):
                if self.board[row,column] == 0:
                    group_col_begin = 3 * (column // 3)
                    group_row_begin = 3 * (row // 3)
                    for i in range(1,10):
                        unique = np.unique(self.possibilities[row,column,:])
                        if i in self.board[group_row_begin:group_row_begin+3,group_col_begin:group_col_begin+3]:
                            self.possibilities[row,column,i-1] = 0
                        if i in self.board[row,:]:
                            self.possibilities[row,column,i-1] = 0
                        if i in self.board[:,column]:
                            self.possibilities[row,column,i-1] = 0
        # place number by exclusion of all other numbers for a single place
        for row in range(9):
            for column in range(9):
                unique = np.unique(self.possibilities[row,column,:])
                unique = unique[unique != 0]
                if self.debug: print("unique: " + str(unique))
                if unique.size == 1 and self.board[row,column] != unique[0]:
                    self.board[row,column] = unique[0]
                    self.possibilities[row,column,:] = 0
                    self.possibilities[row,column,unique[0]-1] = unique[0]
                    if self.debug: self.pp()
                    self.printboard(box=(row,column))
                    if self.debug: input("check1")
                    # note = self.note_maker('m')
                    # self.parent.display.textbox.write(note)
                    return True
        # place number by exclusion of same number in multiple places
        for g_row in range(3):
            for g_col in range(3):
                group_col_begin = 3 * g_col
                group_row_begin = 3 * g_row
                for i in range(1,10):
                    sub_possibilities = "green"
                    if i not in self.board[group_row_begin:group_row_begin+3,group_col_begin:group_col_begin+3]:
                        sub_possibilities = np.ones((3,3))==1
                        sub_possibilities[self.board[group_row_begin:group_row_begin+3,group_col_begin:group_col_begin+3]!=0]=False
                        for j in range(3):
                            if i in self.board[group_row_begin + j,:]:
                                sub_possibilities[j,:] = False
                            if i in self.board[:,group_col_begin + j]:
                                sub_possibilities[:,j] = False
                        if sub_possibilities.sum() == 1:
                            where = np.argwhere(sub_possibilities)[0]
                            where[0] = where[0] + group_row_begin
                            where[1] = where[1] + group_col_begin
                            self.board[where[0],where[1]] = i
                            self.possibilities[where[0],where[1],:] = 0
                            self.possibilities[where[0],where[1],i-1] = i
                            if self.debug: self.pp()
                            self.printboard(box=(row,column))
                            if self.debug: input("check1")
                            # note = self.note_maker('s')
                            # self.parent.display.textbox.write(note)
                            return True
        return False
    def pp(self):
        for i in range(self.possibilities.shape[2]):
            print(str(self.possibilities[:,:,i]) + "\n")
    def guesses(self,board,possibilities,possibility_count):
        for row in range(9):
            for column in range(9):
                if board[row,column] == 0:
                    current_possibilities = list(np.unique(possibilities[row,column,:]))
                    if 0 in current_possibilities: current_possibilities.pop(current_possibilities.index(0))
                    if len(current_possibilities) == possibility_count:
                        for possibility in current_possibilities:
                            if self.debug: self.pp()
                            if self.debug: print("row: " + str(row), end = ", ")
                            if self.debug: print("column: " + str(column), end = ", ")
                            if self.debug: print("possibility: " + str(possibility))
                            if self.debug: self.printboard(box=(row,column))
                            if self.debug: input("check7")
                            yield row, column, possibility
    def solved_check(self):
        if (self.board != 0).sum() == 81: return True
        else: return False
    def bad_board_check(self):
        if (self.possibilities.sum(2) == 0).any(): return True
        for row in range(9):
            for column in range(9):
                for i in range(1,10):
                    if len(np.argwhere(self.board[row,:] == i)) > 1: return True
                    if len(np.argwhere(self.board[:,column] == i)) > 1: return True
                    group_col_begin = 3 * (column // 3)
                    group_row_begin = 3 * (row // 3)
                    if len(np.argwhere(self.board[group_row_begin:group_row_begin+3,group_col_begin:group_col_begin+3] == i)) > 1: return True
        return False
    def solve_sequence(self,guess_depth=0,max_guess_depth=0,tentative=False,guessing_allowed=True):
        if (self.board != 0).sum() == 81: return True
        self.guess_depth = guess_depth
        if self.guess_depth > 0:
            note = self.note_maker('g')
            self.parent.display.textbox.write(note)
        counter = 0
        break_loop = False
        while not break_loop:
            break_loop = not self.search()
            counter += 1
            if self.bad_board_check(): 
                if tentative: return 0, None, None
                else: 
                    print("bad board")
                    return False
            if self.solved_check(): 
                if tentative: return 81, np.copy(self.board), np.copy(self.possibilities)
                else: return True
        if tentative: return counter, np.copy(self.board), np.copy(self.possibilities)
        elif guessing_allowed and guess_depth <= max_guess_depth:
            guess_results = []
            guesses_found = False
            out_of = 2
            while not guesses_found:
                for guess in self.guesses(np.copy(self.board),np.copy(self.possibilities),out_of):
                    guesses_found = True
                    board_bak = np.copy(self.board)
                    poss_bak = np.copy(self.possibilities)
                    row, column, guess = guess
                    self.board[row,column] = guess
                    guess_results.append(self.solve_sequence(guess_depth = guess_depth + 1,tentative=True))
                    current = len(guess_results) - 1
                    if guess_results[current][0] == 81:
                        self.board = guess_results[current][1]
                        self.possibilities = guess_results[current][2]
                        return True
                    self.board = board_bak
                    self.possibilities = poss_bak
                out_of += 1
                #
                board_bak = np.copy(self.board)
                poss_bak = np.copy(self.possibilities)
                guess_results = list(filter(lambda a: a[0] != 0, guess_results))
                guess_results.sort(key = lambda x: x[0],reverse = True)
                for guess in guess_results:
                    self.board = guess[1]
                    self.possibilities = guess[2]
                    if not self.solve_sequence(guess_depth = guess_depth + 1,guessing_allowed=False):
                        self.board = np.copy(board_bak)
                        self.possibilities = np.copy(poss_bak)
                    else: return True
                while True:
                    if guess_depth == 0: max_guess_depth += 1
                    '''
                    I smell overlapping sub-problems.
                    Can probably be fixed.
                    Next part is necessary to keep from going too deep
                    down a wrong path.'''
                    for guess in guess_results:
                        self.board = guess[1]
                        self.possibilities = guess[2]
                        if not self.solve_sequence(guess_depth = guess_depth + 1,
                                                   max_guess_depth=max_guess_depth,
                                                   guessing_allowed=True):
                            self.board = np.copy(board_bak)
                            self.possibilities = np.copy(poss_bak)
                        else: return True
                    if guess_depth != 0: break


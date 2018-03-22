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
    
def printboard(board=None,box=None):
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
        the_str[row+1] = the_str[row+1][:col-2] + "‾‾‾" + the_str[row+1][col+1:]
        the_str[row] = the_str[row][:col-3] + "| " + the_str[row][col-1] + " |" + the_str[row][col+2:]
    for _ in the_str: print(_)

a=np.array([[0,0,0,0,0,0,0,0,0],
[0,1,0,8,4,0,0,0,0],
[0,0,2,5,6,0,0,9,0],
[0,0,0,0,0,3,0,0,0],
[2,0,7,0,0,0,0,4,0],
[3,0,6,9,5,0,0,0,8],
[0,0,0,0,0,0,0,0,0],
[0,0,8,3,0,6,5,0,1],
[0,0,1,0,0,0,0,7,6]])
for r in range(9):
    for c in range(9):
        b=printboard(a,(r,c))
        input()


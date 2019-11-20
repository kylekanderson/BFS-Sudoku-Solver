# SWDV 610: Data Structures
# Final Assignment Submission
# Kyle Anderson

# At this point in time, you are familiar with all of the data boardWidths and data structures in Python and can implement them in a variety of ways.  For your final project, you must make a choice of which algorithms and data structures can best be utilized to solve a problem and implement them in a program.

# You must develop an algorithm and/or data structure and implement it to solve a problem of your choosing. For example, you may want to address the classic Knight's Tour (Links to an external site.) problem by implementing a graph utilizing a depth first search algorithm. In your program, you must also provide a test case for the algorithm. This is a fairly open-ended challenge but should showcase the skills and knowledge you have acquired over your coursework so far.

# You will be submitting your code as a .py file as well as a brief video of you explaining what your program should do and  so it functioning.  You may reference the rubric to further understand the parameters for grading.

############################################################################################################
# Requirements:
# [x] Program completes its set purpose
# [x] Clearly explains code and demonstrates its functionality
# [x] Code is readable and clearly commented and organized.
# [x] Problem choose for program to solve fits under the submission guidelines.
# [x] Data Structures are clearly referenced and articulated what they are and how they will be utilized.
############################################################################################################

# IMPORTS:
from queue import Queue
import copy
import os
import time

# CONSTANTS:
WIDTH = 80
APPLICATION_TITLE = 'Sudoku Solver\nSWDV 610: Data Structures\nFinal Assignment Submission\nKyle Anderson'
BORDER_CHARACTER = '*'


class Problem(object):
    '''A class representing the state of the problem'''

    def __init__(self, board):
        self.board = board

        # set 'boardWidth' equal to the board type (ex: 6x6, 9x9, etc.)
        self.boardWidth = len(board)

        # set 'quadrantHeight' equal to the quadrant height (2 for 6x6, 3 for 9x9)
        self.quadrantHeight = int(self.boardWidth/3)

    def filter_values(self, values, used):
        '''returns a list of valid numbers from values that do not appear in used'''
        validNumbers = []
        # iterate over the supplied values (list)
        for number in values:
            # if the current number does not exist in used (list), then add it to the validNumbers (list)
            if number not in used:
                validNumbers.append(number)
        return validNumbers

    def get_first_empty_spot(self, board, state):
        '''returns the first empty spot on the board (marked as 0)'''
        # iterate over rows and columns in the board and return (row, column) if they are empty (equal to 0)
        for row in range(board):
            for column in range(board):
                if state[row][column] == 0:
                    return row, column

    def actions(self, state):
        '''takes a state and yields numbers, rows, and columns representing valid moves'''
        # this function iteratively refines a List (options) to find available moves based on row, column, and quadrant and then yields those as output
        # define a set of valid numbers that can be placed on the board
        numberSet = range(1, self.boardWidth+1)
        # list of valid values in spot's column
        inColumn = []
        # list of valid values in spot's quadrant
        inBlock = []

        # use get_first_empty_spot to get the first empty spot on the board
        row, column = self.get_first_empty_spot(self.boardWidth, state)

        # create a list of numbers currently in the row
        inRow = []
        for number in state[row]:
            if number != 0:
                inRow.append(number)

        # find a list (options) of valid values based on the row
        options = self.filter_values(numberSet, inRow)

        # create a list of numbers currently in the column
        for columnIndex in range(self.boardWidth):
            if state[columnIndex][column] != 0:
                inColumn.append(state[columnIndex][column])

        # find a list (options) of valid values based on the column
        options = self.filter_values(options, inColumn)

        rowStart = int(row/self.quadrantHeight)*self.quadrantHeight
        columnStart = int(column/3)*3

        # create a list of numbers currently in the quadrant
        for quadrantRow in range(0, self.quadrantHeight):
            for quadrantColumn in range(0, 3):
                inBlock.append(state[rowStart + quadrantRow]
                               [columnStart + quadrantColumn])

        # find a list (options) of valid values based on the quadrant
        options = self.filter_values(options, inBlock)

        for number in options:
            yield number, row, column

    def result(self, state, action):
        '''returns an updated board after adding a new valid value'''

        # 'play' is the number being added to the board
        play = action[0]
        row = action[1]
        column = action[2]

        # Add new valid value to board
        newState = copy.deepcopy(state)
        newState[row][column] = play

        return newState

    def is_goal_state(self, state):
        '''use sums of each row, column, and quadrant to determine validity of state'''

        # in a sudoku board, if you take the length of a row/column/quadrant and add 1 to it...
        # then, add up each number below that number...
        # you'll get the expected sum for each row/column/quadrant
        total = sum(range(1, self.boardWidth+1))

        # perform 2 checks here:
        # 1st check that state is the same size as self
        # 2nd check that the sum of the state[row] is equal to total
        for row in range(self.boardWidth):
            if (len(state[row]) != self.boardWidth) or (sum(state[row]) != total):
                return False

            # now, check that all of the numbers in the column add up to the expected total
            columnTotal = 0
            for column in range(self.boardWidth):
                columnTotal += state[column][row]
            if (columnTotal != total):
                return False

        # check quadrants and return false if total is invalid
        # start at 0, stop at self.boardWidth, step by 3
        for column in range(0, self.boardWidth, 3):
            # start at 0, stop at self.boardWidth, step by self.quadrantHeight
            for row in range(0, self.boardWidth, self.quadrantHeight):
                quadrantTotal = 0
                for quadrantRow in range(0, self.quadrantHeight):
                    for quadrantColumn in range(0, 3):
                        quadrantTotal += state[row +
                                               quadrantRow][column + quadrantColumn]
                if (quadrantTotal != total):
                    return False
        return True


class Node:
    def __init__(self, state, action=None):
        self.state = state
        self.action = action

    def expand(self, Problem):
        '''use each action to create a new board state'''
        childNodeList = []
        # find all of the possible actions (number, row, column) on the current node's state
        # iterate over those and use them to create child nodes
        # and add them to the childNodeList
        for action in Problem.actions(self.state):
            childNodeList.append(self.child_node(Problem, action))
        return childNodeList

    def child_node(self, Problem, action):
        '''returns a node with a new board state'''
        # use the Problem.result method to get an updated board
        next = Problem.result(self.state, action)
        # create a Node object from the updated board and return it
        return Node(next, action)


class UserInterface:
    def __init__(self):
        self.width = WIDTH
        self.borderCharacter = BORDER_CHARACTER

    def drawBorder(self):
        '''print a simple border with the width and borderCharacter defined by CONSTANTS'''
        print(self.width * self.borderCharacter)

    def drawTitleScreen(self):
        '''print a formatted title screen out to the console'''
        self.clearTerminal()
        self.drawBorder()
        print('{0}'.format(APPLICATION_TITLE))
        self.drawBorder()

    def clearTerminal(self):
        '''clear the terminal
        # note: this checks the os name and sends the appropriate terminal command for the os'''
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')


def BFS(initialState):
    '''performs a breadth-first search on a Problem object and returns a Node object (child) representing the solution (if one exists)'''
    # create board node of Problem tree holding original board
    node = Node(initialState.board)
    # check if original board is correct and immediately return if valid
    if initialState.is_goal_state(node.state):
        return node

    # create a queue data structure and add the node to it
    fifo = Queue()
    fifo.put(node)

    # loop until all nodes are explored or solution found
    while not fifo.empty():
        # pull a node from the end of the queue
        node = fifo.get()
        # call the 'expand' method on the node, using the initialState as the base problem
        # the 'expand' function will return a list of nodes, so we need to iterate over those here
        for child in node.expand(initialState):
            # if the current child's state meets the goal state requirements, then return it (problem solved)
            # if not, then put it on the queue
            if initialState.is_goal_state(child.state):
                return child
            fifo.put(child)

    return None


def solve_bfs(board):
    '''takes a 2D array representing a sudoku puzzle and, using breadth-first-search, determines a solution to the puzzle and prints it to the screen'''
    startTime = time.time()

    print('\nSolving...')

    initialState = Problem(board)
    solution = BFS(initialState)

    if solution:
        print('Found a solution:')
        for row in solution.state:
            print(row)
    else:
        print('No possible solutions found')

    endTime = time.time()

    print('Time taken: {0:.3g} seconds'.format(endTime - startTime))


def main():
    ui = UserInterface()
    ui.drawTitleScreen()
    print('Testing a 6x6 board...')
    board = [[0, 0, 0, 0, 5, 6],
             [0, 0, 2, 0, 3, 0],
             [0, 0, 0, 0, 6, 1],
             [4, 1, 0, 0, 0, 0],
             [0, 3, 0, 6, 0, 0],
             [1, 6, 0, 0, 0, 0]]

    print('Starting Board:')
    for row in board:
        print(row)

    solve_bfs(board)

    print('\n\nTesting a 9x9 board...')
    board = [[0, 5, 0, 2, 0, 0, 0, 0, 0],
             [3, 0, 0, 0, 0, 5, 0, 8, 0],
             [9, 6, 0, 0, 7, 8, 2, 0, 0],
             [0, 0, 0, 0, 3, 0, 0, 2, 0],
             [7, 0, 8, 0, 0, 0, 1, 0, 3],
             [0, 4, 0, 0, 8, 0, 0, 0, 0],
             [0, 0, 1, 6, 4, 0, 0, 3, 2],
             [0, 7, 0, 5, 0, 0, 0, 0, 1],
             [0, 0, 0, 0, 0, 9, 0, 5, 0]]

    print('Starting Board:')
    for row in board:
        print(row)

    solve_bfs(board)

    print('\n\nTesting an invalid 9x9 board...')
    # notice that there are 2 5's in the middle quadrant (at [3][5] and [4][3])
    board = [[0, 0, 9, 0, 7, 0, 0, 0, 5],
             [0, 0, 2, 1, 0, 0, 9, 0, 0],
             [1, 0, 0, 0, 2, 8, 0, 0, 0],
             [0, 7, 0, 0, 0, 5, 0, 0, 1],
             [0, 0, 8, 5, 1, 0, 0, 0, 0],
             [0, 5, 0, 0, 0, 0, 3, 0, 0],
             [0, 0, 0, 0, 0, 3, 0, 0, 6],
             [8, 0, 0, 0, 0, 0, 0, 0, 0],
             [2, 1, 0, 0, 0, 0, 0, 8, 7]]

    print('Starting Board:')
    for row in board:
        print(row)

    solve_bfs(board)


if __name__ == '__main__':
    main()

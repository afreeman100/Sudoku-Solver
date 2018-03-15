import numpy as np


class Node:

    def __init__(self, toSolve):
        self.sudoku = toSolve


    def getChildren(self):
        sudoku = self.sudoku
        children = []

        # go through whole grid
        for i in range(9):
            for j in range(9):
                # find first empty square
                if sudoku[i][j] == 0:
                    # square could contain numbers from 1-9: create new grid for each possibility
                    for k in range(1, 10):
                        temp = np.copy(sudoku)
                        temp[i][j] = k
                        child = Node(temp)
                        # see which of the new grids are valid
                        if child.isValid():
                            children.append(child)

                    return children


    # split grid into rows, columns and 3x3 boxes and return list of results
    def splitGrid(self):
        sudoku = self.sudoku

        splits = []
        for i in range(9):
            splits.append(sudoku[i, :])

        for i in range(9):
            splits.append(sudoku[:, i])

        for i in range(0, 9, 3):
            for j in range(0, 9, 3):
                splits.append(sudoku[i:i + 3, j:j + 3])

        return splits


    # returns true if a grid does not have any duplicate values in any rows/columns/sections
    def isValid(self):
        splits = self.splitGrid()
        return all(self.validTest(s) for s in splits)


    def validTest(self, section):
        # count occurrences of each number -> more that 1 occurrence is invalid
        for i in range(1, 10):
            if np.count_nonzero(section == i) > 1:
                return False

        return True


    # each row, column and 3x3 must be correct for grid to be solution
    def isSolution(self):
        splits = self.splitGrid()
        return all(self.solutionTest(s) for s in splits)


    # returns true if section contains all numbers from 1-9
    def solutionTest(self, section):
        # reshape section into row form and sort it. Does it match [1,2...8,9] ?
        r = np.sort(np.reshape(section, 9))
        t = np.arange(1, 10)
        return np.all(np.equal(r, t))


def sudoku_solver(sudoku):
    current = Node(sudoku)
    frontier = [current]

    while len(frontier) > 0:
        # pop from top of list -> depth first search
        current = frontier.pop()
        children = current.getChildren()

        for child in children:
            if child.isSolution():
                return child.sudoku
            frontier.append(child)

    #return array of -1s if unsolvable
    unsolved = np.empty([9,9])
    unsolved.fill(-1)
    return unsolved



def main():

    # Load sudokus
    sudokus = np.load("data/sudokus.npy")
    print("Shape of sudokus array:", sudokus.shape, "; Type of array values:", sudokus.dtype)

    # Load solutions
    solutions = np.load("data/solutions.npy")
    print("Shape of solutions array:", solutions.shape, "; Type of array values:", solutions.dtype, "\n\n\n")

    #solve each and check the result matches the correct answer
    for i, e in enumerate(sudokus):

        solve = sudoku_solver(e)
        correct = np.all(np.equal(solve, solutions[i]))
        print("Sudoku ", i, ": ", correct)


main()

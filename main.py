def matrixStrToList(data: str):
    return list(map(lambda x: [char for char in x], filter(lambda x: len(x) != 0, data.split('\n'))))


def matrixListToStr(data: list):
    return '\n'.join(list(map(lambda x: ''.join(x), data)))


class Board:
    def __init__(self, data: str, targetData: str):
        self.board: list = matrixStrToList(data)
        self.targetBoard: list = matrixStrToList(targetData)
        self.steps = list()
        self.dimensions = (len(self.board), len(self.board[0]))

        # initialize positions map - used for detecting "correct" positions
        self._targetPositionsMap = {}
        for y in range(0, self.dimensions[0]):
            for x in range(0, self.dimensions[1]):
                self._targetPositionsMap[self.targetBoard[y][x]] = (y, x)


    def isSolved(self):
        return matrixListToStr(self.board) == matrixListToStr(self.targetBoard)


    def idealPosition(self, y, x):
        return self._targetPositionsMap[self.board[y][x]]


    def apply(self, action, quantity=1):
        """
        Apply an action to the board
        :param quantity: amount of times an action should be applied
        :param action: For example, "R0" or "U3" as in (row 0) shift right or (row 3) shift up.
        """

        # 0 of an action means do nothing
        if quantity <= 0:
            return

        self.steps.append(action)

        direction = action[0]
        subject = int(action[1])

        # horizontal shifts
        if direction == "L" or direction == "R":
            row = self.board[subject]
            if direction == "L":
                # left shift
                row.append(row.pop(0))
            else:
                # right shift
                row.insert(0, row.pop())
        # vertical shifts
        else:
            if direction == "D":
                # down shift
                spare = self.board[-1][subject]

                for i in range(0, len(self.board) - 1):
                    self.board[-i - 1][subject] = self.board[-i - 2][subject]

                self.board[0][subject] = spare
            else:
                # up shift
                spare = self.board[0][subject]

                for i in range(0, len(self.board) - 1):
                    self.board[i][subject] = self.board[i + 1][subject]

                self.board[-1][subject] = spare

        # quantity means repeat an action
        self.apply(action, quantity - 1)


def loopover(scrambledBoard, solvedBoard):
    board = Board(scrambledBoard, solvedBoard)

    for y in range(0, board.dimensions[0]):
        for x in range(0, board.dimensions[1]):
            idealPos = board.idealPosition(y, x)

            # skip pieces already in the correct location
            if idealPos == (y, x):
                continue

            # very first piece is easy
            if idealPos == (0, 0):
                board.apply(f"L{y}", x - idealPos[1])
                board.apply(f"U{x}", y - idealPos[0])


    print(scrambledBoard)
    print()
    print(matrixListToStr(board.board))
    print()
    print(board.steps)

    return board.steps

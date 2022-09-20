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


    def findPiece(self, piece):
        """
        Find the location of a piece in the board
        :param piece:
        :return:
        """

        for y in range(0, self.dimensions[0]):
            for x in range(0, self.dimensions[1]):
                if (self.board[y][x] == piece):
                    return (y, x)


    def idealPosition(self, piece):
        """
        Find the ideal location of a piece based on the target board.
        :param piece: The target piece to find the ideal position of. List is in targetBoard
        :return:
        """

        return self._targetPositionsMap[piece]
    

    def dragPiece(self, piece, movement):
        """
        Move the board by dragging a piece.
        :param piece:
        :param movement:
        :return:
        """

        return self.dragLocation(self.findPiece(piece), movement)


    def dragLocation(self, location, movement):
        """
        Move the board by dragging a particular location.
        :param movement: (y, x) tuple of motion. One of y or x must be zero. Only one dimension at a time.
        """
        
        # 0 motion means do nothing
        if movement == (0, 0):
            return

        # we can only move in one direction at a time
        if movement[0] != 0 and movement[1] != 0:
            raise "Only one direction of motion allowed at a time."

        direction = None
        target = None
        magnitude = None
        if movement[0] == 0:
            magnitude = movement[1]
            if magnitude < 0:
                direction = "L"
                target = location[0]
            else:
                direction = "R"
                target = location[0]
        else:
            magnitude = movement[0]
            if magnitude < 0:
                direction = "U"
                target = location[1]
            else:
                direction = "D"
                target = location[1]

        for i in range(abs(magnitude)):
            self.steps.append(direction + str(target))

            # horizontal shifts
            if direction == "L" or direction == "R":
                row = self.board[target]
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
                    spare = self.board[-1][target]

                    for i in range(0, len(self.board) - 1):
                        self.board[-i - 1][target] = self.board[-i - 2][target]

                    self.board[0][target] = spare
                else:
                    # up shift
                    spare = self.board[0][target]

                    for i in range(0, len(self.board) - 1):
                        self.board[i][target] = self.board[i + 1][target]

                    self.board[-1][target] = spare


    def print(self):
        print(matrixListToStr(self.board))
        print()


# noinspection SpellCheckingInspection
def loopover(scrambledBoard, solvedBoard):
    board = Board(scrambledBoard, solvedBoard)

    for row in board.targetBoard:
        for peice in row:
            board.print()
            idealPosition = board.idealPosition(peice)
            currentPosition = board.findPiece(peice)

            # this piece is supposed to be on the first layer
            if idealPosition[0] == 0:
                board.dragPiece(peice, (0, idealPosition[1] - currentPosition[1]))
                board.dragPiece(peice, (idealPosition[0] - currentPosition[0], 0))
                continue

            board.dragLocation((0, idealPosition[1]), (idealPosition[0] - currentPosition[0], 0))
            board.dragPiece(peice, (0, idealPosition[1] - currentPosition[1]))
            board.dragPiece(peice, (idealPosition[0] - currentPosition[0], 0))

    board.print()
    print(board.steps)
    
    return board.steps

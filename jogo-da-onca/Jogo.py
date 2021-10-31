# %%
import networkx as nx
import matplotlib.pyplot as plt

class JogoDaOnca:
    C_EMPTY = 0
    C_JAGUAR = 1
    C_DOG = 2

    C_WAIT_JAGUAR = "WAITING JAGUAR"
    C_WAIT_DOG = "WAITING DOG"
    C_NOT_INIT = "NOT_INITIALIZED"

    DOGS_INIT_POS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15]
    JAGUAR_INIT_POS = 13

    BOARD_ROUTES = [
        [1, [2, 6, 7], [0, 0]],
        [2, [1, 3, 7], [1, 0]],
        [3, [2, 4, 7, 8, 9], [2, 0]],
        [4, [3, 5, 9], [3, 0]],
        [5, [4, 9, 10], [4, 0]],

        [6, [1, 7, 11], [0, -1]],
        [7, [1, 2, 3, 6, 8, 11, 12, 13], [1, -1]],
        [8, [3, 7, 9, 13], [2, -1]],
        [9, [3, 4, 5, 8, 10, 13, 14, 15], [3, -1]],
        [10, [5, 9, 15], [4, -1]],

        [11, [6, 7, 12, 16, 17], [0, -2]],
        [12, [7, 11, 13, 17], [1, -2]],
        [13, [7, 8, 9, 12, 14, 17, 18, 19], [2, -2]],
        [14, [9, 13, 15, 19], [3, -2]],
        [15, [9, 10, 14, 19, 20], [4, -2]],

        [16, [11, 17, 21], [0, -3]],
        [17, [11, 12, 13, 16, 18, 21, 22, 23], [1, -3]],
        [18, [13, 17, 19, 23], [2, -3]],
        [19, [13, 14, 15, 18, 20, 23, 24, 25], [3, -3]],
        [20, [15, 19, 25], [4, -3]],

        [21, [16, 17, 22], [0, -4]],
        [22, [17, 21, 23], [1, -4]],
        [23, [17, 18, 19, 22, 24, 26, 27, 28], [2, -4]],
        [24, [19, 23, 25], [3, -4]],
        [25, [19, 20, 24], [4, -4]],

        [26, [23, 27, 29], [1, -5]],
        [27, [23, 26, 28, 30], [2, -5]],
        [28, [23, 27, 31], [3, -5]],

        [29, [26, 30], [0, -6]],
        [30, [27, 29, 31], [2, -6]],
        [31, [28, 30], [4, -6]]
    ]

    def __init__(self):
        self.board = []
        self.status = JogoDaOnca.C_NOT_INIT

    def displayBoard(self):
        G = nx.Graph()
        states = {
            0: ' ',
            1: 'O',
            2: 'C'
        }
        labeldict = {}

        for route in self.BOARD_ROUTES:
            stateNo = self.board[route[0] - 1][1]
            no = states[stateNo]
            labeldict[route[0]] = "{}:{}".format(no, route[0])

            G.add_node(route[0], pos=(route[2]))

            for connection in route[1]:
                G.add_edge(route[0], connection)

        position = nx.get_node_attributes(G, 'pos')
        plt.clf()
        nx.draw(G, position, labels=labeldict, node_size=500,
                node_color='cyan', with_labels=True, font_color='black')
        plt.show()

    def getBoard(self):
        self.displayBoard()

        return self.board

    def getBoardRoutes(self):
        return JogoDaOnca.BOARD_ROUTES

    def setPositionContent(self, position, content):
        for pos in self.board:
            if pos[0] == position:
                pos[1] = content

    def getPositionContent(self, position):
        for pos in self.board:
            if pos[0] == position:
                return pos[1]

    def getJaguarPosition(self):
        for pos in self.board:
            if pos[1] == JogoDaOnca.C_JAGUAR:
                return pos[0]

    def getDogsPositions(self):
        lst = []
        for pos in self.board:
            if pos[1] == JogoDaOnca.C_DOG:
                lst.append(pos[0])
        return lst

    def getDogsQuantity(self):
        return len(self.getDogsPositions())

    def getStatus(self):
        return self.status

    def newBoard(self):
        self.board = [[x, 0] for x in range(1, 32)]
        for pos in JogoDaOnca.DOGS_INIT_POS:
            self.setPositionContent(pos, JogoDaOnca.C_DOG)
        self.setPositionContent(JogoDaOnca.JAGUAR_INIT_POS, JogoDaOnca.C_JAGUAR)
        self.status = JogoDaOnca.C_WAIT_JAGUAR

    def getPossibleWalk(self, actualPos):
        for pos in JogoDaOnca.BOARD_ROUTES:
            if pos[0] == actualPos:
                return pos[1]

    def canWalk(self, actualPos, newPos):
        return newPos in self.getPossibleWalk(actualPos)

    def dogPlay(self, actualPos, newPos):
        if self.getPositionContent(actualPos) == JogoDaOnca.C_DOG and self.getPositionContent(newPos) == JogoDaOnca.C_EMPTY and self.canWalk(actualPos, newPos) and self.status == JogoDaOnca.C_WAIT_DOG:
            self.setPositionContent(actualPos, JogoDaOnca.C_EMPTY)
            self.setPositionContent(newPos, JogoDaOnca.C_DOG)
            self.status = JogoDaOnca.C_WAIT_JAGUAR
            return True
        else:
            return False

    def jaguarWalk(self, newPos):
        if self.getPositionContent(newPos) == JogoDaOnca.C_EMPTY and self.canWalk(self.getJaguarPosition(), newPos) and self.status == JogoDaOnca.C_WAIT_JAGUAR:
            self.setPositionContent(self.getJaguarPosition(), JogoDaOnca.C_EMPTY)
            self.setPositionContent(newPos, JogoDaOnca.C_JAGUAR)
            self.status = JogoDaOnca.C_WAIT_DOG
            return True
        else:
            return False
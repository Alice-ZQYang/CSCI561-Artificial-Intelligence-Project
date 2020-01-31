# -*- coding:utf-8 -*-

import time
import random

# =====================================
# Global variables
# =====================================

# Constant variables
INT_MAX = 2 ** 31 - 1
INT_MIN = -2 ** 31

# 8 directions of how to move
directions = [
    [0, 1],  # North
    [1, 0],  # East
    [-1, 0],  # West
    [0, -1],  # South
    [1, 1],  # Northeast
    [1, -1],  # Southeast
    [-1, -1],  # Southwest
    [-1, 1]  # Northwest
]

# which agent to play
agent1Action = True

# positions of camp
camp = {(0, 0): False, (0, 1): False, (0, 2): False, (0, 3): False, (0, 4): False,
        (1, 0): False, (1, 1): False, (1, 2): False, (1, 3): False, (1, 4): False,
        (2, 0): False, (2, 1): False, (2, 2): False, (2, 3): False,
        (3, 0): False, (3, 1): False, (3, 2): False,
        (4, 0): False, (4, 1): False}
enemyCamp = {
    (11, 14): False, (11, 15): False,
    (12, 13): False, (12, 14): False, (12, 15): False,
    (13, 12): False, (13, 13): False, (13, 14): False, (13, 15): False,
    (14, 11): False, (14, 12): False, (14, 13): False, (14, 14): False, (14, 15): False,
    (15, 11): False, (15, 12): False, (15, 13): False, (15, 14): False, (15, 15): False, }

# =====================================
# Class
# =====================================

class Node:
    def __init__(self, startPos, endPos):
        self.startPos = startPos
        self.endPos = endPos

    def __str__(self):
        return (str(self.startPos) + "" + str(self.endPos))


class ChessAgent:
    """Summary of class here.

    Chess agent to play the game

    """
    def __init__(self, filename):
        """Initilize class"""

        f = open(filename)
        self.mode = f.readline()
        self.color = (f.readline())[0]
        self.enemyColor = None
        self.playTime = float(f.readline())

        # recording the camp postion
        if self.color == "B":
            self.enemyColor = "W"
            self.camp = {(0, 0): False, (0, 1): False, (0, 2): False, (0, 3): False, (0, 4): False,
                         (1, 0): False, (1, 1): False, (1, 2): False, (1, 3): False, (1, 4): False,
                         (2, 0): False, (2, 1): False, (2, 2): False, (2, 3): False,
                         (3, 0): False, (3, 1): False, (3, 2): False,
                         (4, 0): False, (4, 1): False}
            self.enemyCamp = {
                (11, 14): False, (11, 15): False,
                (12, 13): False, (12, 14): False, (12, 15): False,
                (13, 12): False, (13, 13): False, (13, 14): False, (13, 15): False,
                (14, 11): False, (14, 12): False, (14, 13): False, (14, 14): False, (14, 15): False,
                (15, 11): False, (15, 12): False, (15, 13): False, (15, 14): False, (15, 15): False, }
        else:
            self.enemyColor = "B"
            self.camp = {
                (11, 14): False, (11, 15): False,
                (12, 13): False, (12, 14): False, (12, 15): False,
                (13, 12): False, (13, 13): False, (13, 14): False, (13, 15): False,
                (14, 11): False, (14, 12): False, (14, 13): False, (14, 14): False, (14, 15): False,
                (15, 11): False, (15, 12): False, (15, 13): False, (15, 14): False, (15, 15): False, }
            self.enemyCamp = {(0, 0): False, (0, 1): False, (0, 2): False, (0, 3): False, (0, 4): False,
                              (1, 0): False, (1, 1): False, (1, 2): False, (1, 3): False, (1, 4): False,
                              (2, 0): False, (2, 1): False, (2, 2): False, (2, 3): False,
                              (3, 0): False, (3, 1): False, (3, 2): False,
                              (4, 0): False, (4, 1): False}

        ## construct Chess Board
        self.chessBoard = []
        self.curPos = {}  # recording our chess position
        self.enemyCurPos = {}
        for i in range(16):
            line = f.readline()
            tmp = []
            for j in range(16):
                tmp.append(line[j])
                if line[j] == self.color:
                    if (i, j) in self.camp:
                        self.curPos[(i, j)] = True  # in the camp
                    else:
                        self.curPos[(i, j)] = False  # outside the camp
                if line[j] == self.enemyColor:
                    if (i, j) in self.enemyCamp:
                        self.enemyCurPos[(i, j)] = True  # enemy in the camp
                    else:
                        self.enemyCurPos[(i, j)] = False  # enemy outside the camp
            self.chessBoard.append(tmp)
    def run(self):
        if self.mode[0] == "S":
            self.SingleMove()
        else:
            self.Game()

    def SingleMove(self):
        """
        MODE: SINGLE
        return: the start position and the target position of single move
        """
        legalList = []
        corner = {"W": (0, 0), "B": (15, 15)}

        # chess in the camp
        for pos in self.curPos:
            if self.curPos[pos]:
                resList = self.newLegalMove(pos[0], pos[1])

                if not resList:  # current chess can not move
                    continue

                # If the current chess can move outside camp
                for res in resList:
                    if res not in self.camp: # can move outside the camp
                        self.PrintSingleMove(pos, res)
                        self.curPos.pop(pos)
                        self.curPos[(res[0], res[1])] = False
                        return
                    else:
                        if ManhattanDistance(corner[self.color], res) < ManhattanDistance(corner[self.color], pos): # can move further away
                            legalList.append([pos, res])


        try:
            # no target position outside the camp, choose randomly from the result Set
            [start, end] = legalList.pop()
            self.PrintSingleMove(start, end)
            return
        except:
            # all chess outside the camp || chess in the camp cannot move outside ==> We can move the chess outside the camp
            for pos in self.curPos:
                if not self.curPos[pos]:
                    resList = self.newLegalMove(pos[0], pos[1])
                    for res in resList:
                        # chess outside the camp cannot enter camp
                        if res not in self.camp and ManhattanDistance(corner[self.color], res) < ManhattanDistance(corner[self.color], pos):
                            self.PrintSingleMove(pos, res)
                            return

    def Game(self):
        """
        MODE: GAME
        return: the start position and the target position of single move
        """
        val, node = self.AlphaBeta(Node((0, 0), (0, 0)), depth=1, alpha=INT_MIN, beta=INT_MAX, maximizingPlayer=True)
        self.PrintSingleMove(node.startPos, node.endPos)
        print (val, node)
        return (node.startPos, node.endPos)

    def validPos(self, color):
        """
        :param color: "W"  or "B", which one to move
        :return: the positions of chess which can move according to the rules
        """
        validList = []
        dict = {}
        flag = True  # 可以走camp外面的棋

        ## 我方所有可以动的棋子
        if color == self.color:
            # 必须只走camp里面的棋
            for (x, y) in self.camp:
                if self.chessBoard[x][y] == color:
                    validList.append((x, y))
                    flag = False
                    # dict[(x, y)] = True

            # 可以走camp外面的棋了
            if flag:
                for i in range(16):
                    for j in range(16):
                        if self.chessBoard[i][j] == color:
                            validList.append((i, j))


        ## 敌方所有可以动的棋子
        else:
            # 必须只走camp里面的棋
            for (x, y) in self.enemyCamp:
                if self.chessBoard[x][y] == color:
                    validList.append((x, y))
                    flag = False
                    # dict[(x, y)] = True

            # 可以走camp外面的棋了
            if flag:
                for i in range(16):
                    for j in range(16):
                        if self.chessBoard[i][j] == color:
                            validList.append((i, j))


        # print (validList)
        return random.sample(validList, len(validList))

    def validMove(self, color):
        """
        （1）camp里面的棋子最后可以出来
        （2） 1不成立的情况下，camp里面的棋子出不来 但是可以更往外走
        （3） 2也不成立，可以动外面的棋子

        :param color: 当前move什么颜色的棋子
        :return: list
        [
        [startPos, endPos1, endPos2, ...],
        ...
        ]
        """
        validList = []
        corner = {"W": (0, 0), "B": (15, 15)}

        if color == self.color:
            camp = self.camp
            enemyCamp = self.enemyCamp
        else:
            camp = self.enemyCamp
            enemyCamp = self.camp

        # 情况（1）成立
        if self.campToOutside(camp, color):
            #print "case 1"
            for (i, j) in camp:
                if self.chessBoard[i][j] == color:# 在camp里面有棋子
                    resList = self.newLegalMove(i, j)
                    tmp = [(i, j)]
                    for res in resList:
                        if res not in camp:
                            tmp.append(res)
                    if len(tmp) > 1:
                        validList.append(tmp)

            return validList



        # 情况（1）不成立，情况（2）成立
        if self.campFurtherAway(camp, color):
            #print "case 2"
            for (i, j) in camp:
                if self.chessBoard[i][j] == color:# 在camp里面有棋子
                    resList = self.newLegalMove(i, j)
                    tmp = [(i, j)]
                    for res in resList:
                        if ManhattanDistance(res, corner[color]) < ManhattanDistance((i,j), corner[color]):
                            tmp.append(res)
                    if len(tmp) > 1:
                        validList.append(tmp)

            return validList

        # （1）和（2）都不成立，可以动外面的棋子
        for i in range(16):
            for j in range(16):
                if (i, j) not in camp and self.chessBoard[i][j] == color:
                    #print ("****")
                    #print(i, j)
                    resList = self.newLegalMove(i, j)
                    tmp = [(i, j)]
                    for res in resList:
                        # chess inside the enemy camp cannot move outside
                        if (i, j) in enemyCamp and res not in enemyCamp:
                            continue
                        # chess outside the camp cannot enter its camp && chess should move forward
                        if (res not in camp) and ManhattanDistance(res, corner[color]) <= ManhattanDistance((i,j), corner[color]):
                            tmp.append(res)

                    if len(tmp) > 1:
                        validList.append(tmp)

        return validList


    def campToOutside(self, camp, color):
        for (i, j) in camp:
            if self.chessBoard[i][j] == color: # 在camp里面有棋子
                resList = self.newLegalMove(i, j)
                for res in resList:
                    if res not in camp: # chess inside the camp can move outside the camp
                        return True
        return False

    def campFurtherAway(self, camp, color):
        corner = {"W":(0,0), "B":(15,15)}
        for (i, j) in camp:
            if self.chessBoard[i][j] == color: # 在camp里面有棋子
                resList = self.newLegalMove(i, j)
                for res in resList:
                    if (res in camp) and ManhattanDistance(res,corner[color]) < ManhattanDistance((i,j), corner[color]): # chess inside the camp cannot move outside the camp but can move furtheraway
                        return True
        return False

    def award(self, startPos, endPos, camp):
        if (startPos not in camp) and (endPos in camp):
            return 30 * ManhattanDistance(startPos, endPos)
        if (startPos not in camp) and (endPos not in camp):
            return 2 * ManhattanDistance(startPos, endPos)
        else:
            return ManhattanDistance(startPos, endPos)


    def AlphaBeta(self, node, depth, alpha, beta, maximizingPlayer):
        """
        Alpha-beta pruning algorithm
        """
        self.chessBoard[node.startPos[0]][node.startPos[1]], self.chessBoard[node.endPos[0]][node.endPos[1]] = \
        self.chessBoard[node.endPos[0]][node.endPos[1]], self.chessBoard[node.startPos[0]][node.startPos[1]]

        if depth == 0:
            value = self.heuristicValue()
            self.chessBoard[node.startPos[0]][node.startPos[1]], self.chessBoard[node.endPos[0]][node.endPos[1]] = \
                self.chessBoard[node.endPos[0]][node.endPos[1]], self.chessBoard[node.startPos[0]][node.startPos[1]]
            if maximizingPlayer:
                return value + self.award(node.startPos, node.endPos, self.enemyCamp), node
            else:
                return value + self.award(node.startPos, node.endPos, self.camp), node

        if maximizingPlayer:
            value = INT_MIN
            child = None
            allValidMoves = self.validMove(self.color)
            for validMove in allValidMoves:
                start = validMove[0]
                for i in range(1, len(validMove)):
                    end = validMove[i]
                    childNode = Node(start, end)
                    childVal, _ = self.AlphaBeta(childNode, depth - 1, alpha, beta, False)
                    if value < childVal:  # value = max(value, childVal)
                        value = childVal
                        child = childNode
                    alpha = max(alpha, value)


                    if alpha >= beta:  # beta cut-off
                        print("beta cut-off")
                        break
                if alpha >= beta:
                    break
            self.chessBoard[node.startPos[0]][node.startPos[1]], self.chessBoard[node.endPos[0]][node.endPos[1]] = \
                self.chessBoard[node.endPos[0]][node.endPos[1]], self.chessBoard[node.startPos[0]][node.startPos[1]]
            return value, child
        else:
            value = INT_MAX
            child = None

            allValidMoves = self.validMove(self.enemyColor)
            for validMove in allValidMoves:
                start = validMove[0]
                for i in range(1, len(validMove)):
                    end = validMove[i]
                    childNode = Node(start, end)
                    childVal, _ = self.AlphaBeta(childNode, depth - 1, alpha, beta, True)

                    if value > childVal:  # value = min(value, childVal)
                        value = childVal
                        child = childNode

                    beta = min(beta, value)


                    if alpha >= beta:  # alpha cut-off
                        print ("alpha cut-off")
                        break
                if alpha >= beta:
                    break
            self.chessBoard[node.startPos[0]][node.startPos[1]], self.chessBoard[node.endPos[0]][node.endPos[1]] = \
                self.chessBoard[node.endPos[0]][node.endPos[1]], self.chessBoard[node.startPos[0]][node.startPos[1]]
            return value, child

    def heuristicValue(self):
        """
        Heruistic function for the current state

        分数越小越好
        在敌人camp里面的棋得分0
        不在敌人camp里面的棋：得分是麦哈顿距离（当前棋 --> 离当前最近的敌人camp空着的位置）
        敌人的camp没有空（初始的时候）, 目标位置是（12，12）
        """
        heuristic = 0.0
        amount = 0
        blank = []
        for enemyPos in self.enemyCamp:
            if enemyPos not in self.enemyCurPos:  # 敌方空着的位置
                blank.append(enemyPos)

        ourChessPos = set()
        for i in range(16):
            for j in range(16):
                if self.chessBoard[i][j] == self.color:
                    ourChessPos.add((i, j))

        for pos in ourChessPos:
            if pos in self.enemyCamp:  # 已经到位的我方棋子
                continue
            else:  # 还没到位的我方棋子
                optDis = INT_MAX
                for blankPos in blank:
                    dis = ManhattanDistance(pos, blankPos)
                    if dis < optDis:
                        optDis = dis
                if (optDis == INT_MAX):
                    optDis = ManhattanDistance(pos, (12, 12))

                heuristic += optDis
                #amount += 1

        return - heuristic / 19


    def PrintSingleMove(self, pos, res):
        """
        Implemention to output result for SINGLE mode
        :param pos: current position
        :param res: target position
        :return:
        """

        ## Find the path
        path = {}
        moveDesc = self.FindPath(pos[0], pos[1], res[0], res[1], path)

        # print path
        pathList = []
        x = res[0]
        y = res[1]
        pathList.append((x, y))
        # print (path)
        while path[(x, y)] != (pos[0], pos[1]):
            (x, y) = path[(x, y)]
            pathList.append((x, y))
        pathList.append((pos[0], pos[1]))

        f = open("output.txt", "w")
        for i in range(len(pathList) - 1, 0, -1):
            #print (moveDesc, pathList[i], pathList[i - 1])
            f.write("%s %d,%d %d,%d\n"%(moveDesc, pathList[i][1], pathList[i][0], pathList[i-1][1], pathList[i-1][0]))


    def FindPath(self, x0, y0, x1, y1, path):
        """
        Operations for self.SingleMove()
        Given the final position, find the path from (x0, y0) to (x1, y1)
        """
        # Move to its neighbor
        for dir in directions:
            next_x = x0 + dir[0]
            next_y = y0 + dir[1]
            if (next_x < 0 or next_x > 15 or next_y < 0 or next_y > 15):
                continue
            if self.chessBoard[next_x][next_y] == "." and x1 == next_x and y1 == next_y:
                path[(x1, y1)] = (x0, y0)
                return "E"

        # Jump to the target
        for dir in directions:
            jump_x = x0 + 2 * dir[0]
            jump_y = y0 + 2 * dir[1]
            next_x = x0 + dir[0]
            next_y = y0 + dir[1]
            if (jump_x < 0 or jump_x > 15 or jump_y < 0 or jump_y > 15):
                continue
            if self.chessBoard[next_x][next_y] != "." and self.chessBoard[jump_x][jump_y] == ".":
                path[(jump_x, jump_y)] = (x0, y0)
                self.dfs(path, jump_x, jump_y, x1, y1)

        return "J"

    def dfs(self, path, x0, y0, x1, y1):
        """
        Operations for self.FindPath()
        """
        if (x0 == x1) and (y0 == y1):
            return

        self.chessBoard[x0][y0] = "T"

        for dir in directions:
            jump_x = x0 + 2 * dir[0]
            jump_y = y0 + 2 * dir[1]
            next_x = x0 + dir[0]
            next_y = y0 + dir[1]
            if (jump_x < 0 or jump_x > 15 or jump_y < 0 or jump_y > 15):
                continue
            if self.chessBoard[next_x][next_y] != "." and self.chessBoard[jump_x][jump_y] == ".":
                path[(jump_x, jump_y)] = (x0, y0)
                self.dfs(path, jump_x, jump_y, x1, y1)

        self.chessBoard[x0][y0] = "."


    def newLegalMove(self, x, y, show=False):
        """
        Find all the possible positions chess (x, y) can move to
        """
        resList = set()
        for dir in directions:
            next_x = x + dir[0]
            next_y = y + dir[1]
            if (next_x < 0 or next_x > 15 or next_y < 0 or next_y > 15):
                continue

            if self.chessBoard[next_x][next_y] == ".":
                resList.add((next_x, next_y))
            else:
                jump_x = next_x + dir[0]
                jump_y = next_y + dir[1]
                if (jump_x < 0 or jump_x > 15 or jump_y < 0 or jump_y > 15):
                    continue
                if self.chessBoard[jump_x][jump_y] == ".":
                    resList.add((jump_x, jump_y))
                    self.newJumpDFS(resList, jump_x, jump_y)

        if show:
            self.legalMoveVisulize(resList, x, y)


        return resList

    def newJumpDFS(self, resList, x, y):
        """
        Operations for self.newLegalMove()

        """
        self.chessBoard[x][y] = "T"

        for dir in directions:
            next_x = x + dir[0]
            next_y = y + dir[1]
            jump_x = next_x + dir[0]
            jump_y = next_y + dir[1]
            if (jump_x < 0 or jump_x > 15 or jump_y < 0 or jump_y > 15):
                continue

            if self.chessBoard[next_x][next_y] != "." and self.chessBoard[jump_x][jump_y] == ".":
                resList.add((jump_x, jump_y))
                self.newJumpDFS(resList, jump_x, jump_y)

        self.chessBoard[x][y] = "."



# =====================================
# Methods
# =====================================

def ManhattanDistance(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])




if __name__ == "__main__":
    #PlayGame("error2.txt", "error3.txt")
    ChessAgent("input.txt").run()

    #files = ["test1.txt", "test2.txt", "test3.txt"]
    #for file in files:
        #agent = ChessAgent(file)
        #agent.InitialVisualize()
        #print (agent.validMove("W"))
        #mainloop()
    #agent = ChessAgent("error3.txt")
    #print (agent.Game())
    #validList = agent.validMove(agent.color)
    #print (validList)
    #agent.Game()
    #for valid in validList:
        #if (valid[0] == (1,5)):
            #print valid





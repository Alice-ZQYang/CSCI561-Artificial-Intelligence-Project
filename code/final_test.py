# Homework 1 for CS570: Artifical Intelligence
# Author: Ziqi Yang
# Date: Sep 10th, 2019

import queue

# 8 directions of how to move
directions = [
    [0, 1], # North
    [1, 0], # East
    [-1, 0], # West
    [0, -1], # South
    [1, 1], # Northeast
    [1, -1], # Southeast
    [-1, -1], # Southwest
    [-1, 1] # Northwest
]

# Definition of pos Class
class pos:
    def __init__(self, x, y, val = 0):
        self.x = x
        self.y = y
        self.val = val
    def __lt__(self, other):
        return self.val <= other.val
    def __str__(self):
        return '(' + str(self.x)+", "+str(self.y) + ') :'+str(self.val)

class optimalPath:
    """
    The class is to find the optimal path from start point to target points
    Three algorithms included: BFS, A*, UCS
    """
    def __init__(self, alg, map, startPos, maxSteep, targetList):
        self.map = map
        self.startPos = startPos
        self.maxSteep = maxSteep
        self.targetList = targetList
        self.alg = alg

    def create_path(self, prev, target):
        a = []
        for line in prev:
            tmp = []
            for item in line:
                tmp.append(str(item.x)+','+str(item.y) + ':'+str(item.val))
            a.append(tmp)

        x = target.x
        y = target.y
        res = []
        while prev[x][y].x != -2:
            prev_x = prev[x][y].x
            prev_y = prev[x][y].y
            res.append(pos(prev_x, prev_y))

            x = prev_x
            y = prev_y
        return ( res[::-1] + [pos(target.x, target.y)])

    def createSinglePath(self, prev, target):
        res = []
        x = target.x
        y = target.y
        res.append(pos(x, y))

        while prev[(x, y)]:
            x, y = prev[(x, y)]
            res.append(pos(x, y))

        return res[::-1]


    def run_alg(self):
        if self.alg[0] == 'B':
            return self.BFS()

        if self.alg[0] == 'A':
            resList = []
            for i in range(len(self.targetList)):
                flag = True
                for j in range(0, i):
                    if self.targetList[i].x == self.targetList[j].x and self.targetList[i].y == self.targetList[j].y:
                        resList.append(resList[j])
                        flag = False
                        break
                if flag:
                    resList.append(self.AStar(self.targetList[i]))

            #for target in self.targetList:
                #resList.append(self.AStar(target))
            return resList

        if self.alg[0] == 'U':
            return self.UCS()

    def createPath(self, prev, targetRes):
        res = []
        for i in range(len(targetRes)):
            if not targetRes[i]:
                if self.targetList[i].x == self.startPos.x and self.targetList[i].y == self.startPos.y:
                    res.append([pos(self.startPos.x, self.startPos.y)])
                else:
                    res.append(False)
            else:
                tmp = []
                x = self.targetList[i].x
                y = self.targetList[i].y
                tmp.append(pos(x, y))

                while prev[(x, y)]:
                    x, y = prev[(x, y)]
                    tmp.append(pos(x, y))

                res.append(tmp[::-1])
        return res

    def BFS(self):
        searchQueue = queue.Queue() # Queue for BFS
        row = len(self.map) # Number of rows
        col = len(self.map[0]) # Number of columns
        prev = {} # Recording the position of previous point

        # The start point has been visited
        searchQueue.put(self.startPos)

        # Initialize the previous dictionary
        prev[(self.startPos.x, self.startPos.y)] = None

        # Recording the results when finding different targets
        cnt = len(self.targetList)
        targetRes = [False] * cnt

        while not searchQueue.empty():
            curPos = searchQueue.get()
            print (curPos.x, curPos.y)



            for dir in directions: # See all 8 directions
                x = curPos.x + dir[0]
                y = curPos.y + dir[1]

                if x < 0 or x >= row or y < 0 or y >= col: # Go out of the map -> see other directions
                    continue

                # There are two requirements for going to the next point
                # 1: the steep from current point to next point is satisfying maxSteep
                # 2: the next point is not visited
                if abs(self.map[x][y]-self.map[curPos.x][curPos.y]) <= self.maxSteep and ((x, y) not in prev):



                    # Record the previous pos of this target
                    prev[(x, y)] = (curPos.x, curPos.y)

                    # check if next point is target
                    # We can check here because the cost of the this point will not change if it is visited
                    for i in range(len(self.targetList)):
                        if curPos.x == self.targetList[i].x and curPos.y == self.targetList[i].y and (
                                not targetRes[i]):  # Find one of the targets
                            # the i-th item of target list is found
                            # targetRes[i] = True
                            cnt -= 1
                            # Find all the path -> Return the path according to prev
                            if cnt == 0:
                                print(prev)
                                return self.createPath(prev, targetRes)

                    searchQueue.put(pos(x, y)) # Adding to the queue

        return self.createPath(prev, targetRes)

    def UCS(self):
        frontier = queue.PriorityQueue() # Priority queue containing the possible frontier node with the path cost
        row = len(self.map)  # Number of rows
        col = len(self.map[0])  # Number of columns

        # initialize the visited map and prev map
        visited = set()
        prev = {}
        values = {}

        # Recording the results when finding different targets
        cnt = len(self.targetList)
        targetRes = [False] * cnt

        # The start point has been explored
        frontier.put(self.startPos)
        prev[(self.startPos.x, self.startPos.y)] = None
        visited.add((self.startPos.x, self.startPos.y))
        values[(self.startPos.x, self.startPos.y)] = 0

        while not frontier.empty():
            curPos = frontier.get()
            # print (curPos.x, curPos.y)
            # Check if this node the target point and optimal path
            for i in range(len(self.targetList)):
                if curPos.x == self.targetList[i].x and curPos.y == self.targetList[i].y and (not targetRes[
                    i]):  # Find one of the targets for the first time
                    # the i-th item of target list is found
                    # print ("Find Target ",i,", value = ", curPos.val)
                    targetRes[i] = True
                    cnt -= 1
                    # Find all the path -> Return the path according to prev
                    if cnt == 0:
                        # print(targetRes)
                        return self.createPath(prev, targetRes)

            # curPos is explored
            visited.add((curPos.x, curPos.y))

            # explore adjacent nodes for 8 directions
            for i in range(8):
                unitCost = 10 if i < 4 else 14 # unitCost differs according to the direction

                # (x, y): the position of adjacent node
                x = curPos.x + directions[i][0]
                y = curPos.y + directions[i][1]


                # Go out of the map -> see other directions
                if x < 0 or x >= row or y < 0 or y >= col:
                    continue

                # There are two requirements for adding the next point to the queue
                #    1: the steep from current point to next point is satisfying maxSteep
                #    2: the next point is not explored
                steep = abs(self.map[x][y] - self.map[curPos.x][curPos.y])
                if steep <= self.maxSteep and ((x, y) not in visited):
                    #
                    # print (x, y, steep, self.map[x][y])
                    value = curPos.val + unitCost

                    # Modify the the path and value of the node
                    if (x, y) not in prev: # has no father
                        prev[(x, y)] = (curPos.x, curPos.y)
                        values[(x, y)] = value
                    else: # once has a father, need to check whether to replace the value
                        if value < values[(x, y)]: # replace the father and value
                            prev[(x, y)] = (curPos.x, curPos.y)
                            values[(x, y)] = value
                        else:
                            continue # keep previous father and value

                    frontier.put(pos(x, y, val=value))  # Adding the next point to the priority queue

        return self.createPath(prev, targetRes)

    def AStar(self, target):
        frontier = queue.PriorityQueue()  # Priority queue containing the possible frontier node with the path cost
        row = len(self.map)  # Number of rows
        col = len(self.map[0])  # Number of columns

        # initialize the visited map and prev map
        visited = set()
        prev = {}
        values = {}


        # The start point has been explored
        self.startPos.val = self.heuristic_value(target, self.startPos)
        frontier.put(self.startPos)
        prev[(self.startPos.x, self.startPos.y)] = None

        while not frontier.empty():
            curPos = frontier.get()

            #print ("********************\n")
            #print ("curPos", curPos, '\n')

            # Find the target point and optimal path
            if curPos.x == target.x and curPos.y == target.y:
                # print ("Find Target (", target.x,",",target.y,") value = ", curPos.val)
                return self.createSinglePath(prev, target)  # Return the path according to previous map

            # no need to explore current node
            if (curPos.x, curPos.y) in visited:
                continue

            # Calculate/Get heuristic value from target to curPos
            cur_hval = self.heuristic_value(target, curPos)

            # Current node is explored
            visited.add((curPos.x, curPos.y))
            values[(curPos.x, curPos.y)] = curPos.val

            #print (values)
            # Explore adjacent nodes for 8 directions
            for i in range(8):
                unitCost = 10 if i < 4 else 14  # unitCost differs according to the direction

                # (x, y): the position of adjacent node
                x = curPos.x + directions[i][0]
                y = curPos.y + directions[i][1]

                # Go out of the map -> see other directions
                if x < 0 or x >= row or y < 0 or y >= col:
                    continue

                # There are two requirements for explore the next point
                # 1: the steep from current point to next point is satisfying maxSteep
                # 2: the next point is not explored
                steep = abs(self.map[x][y] - self.map[curPos.x][curPos.y])
                if steep <= self.maxSteep and ((x, y) not in visited):
                    # Calculate/Get heuristic value from target to curPos
                    g = curPos.val - cur_hval + (unitCost + steep)
                    h = self.heuristic_value(target, pos(x, y))
                    value = g + h

                    if (x, y) in values and values[(x, y)] <= value:
                        continue

                    #print ("Add: (", x, ", ", y, ") ---", g, ", ", h, ", ", value, '\n')
                    prev[(x, y)] = (curPos.x, curPos.y)
                    frontier.put(pos(x, y, val=value))
                    values[(x, y)] = value

        return False

    def heuristic_value(self, target, curNode):
        dif_x = abs(target.x - curNode.x)
        dif_y = abs(target.y - curNode.y)
        dif_z = abs(self.map[target.x][target.y] - self.map[curNode.x][curNode.y])
        return min(dif_x, dif_y) * 14 + (max(dif_x, dif_y) - min(dif_x, dif_y)) * 10 + dif_z


def main(name):
    ##############################################
    # step1: load data from "input.txt"
    f = open("input/" + name)
    #f=open(name)
    alg = f.readline()  # string     type of algorithm
    [w, h] = map(int, f.readline().split())  # int   w: column number, h: row number
    [y_start, x_start] = map(int, f.readline().split())  # int  (x_start, y_start) is the starting point
    startPos = pos(x_start, y_start)
    maxSteep = int(f.readline())  # int  maximum difference in elevation
    targetNum = int(f.readline())  # int     number of target positions
    targetList = []  # List of pos

    for _ in range(targetNum):
        [y_target, x_target] = map(int, f.readline().split())
        targetPos = pos(x_target, y_target)
        targetList.append(targetPos)

    Terrienmap = []
    for _ in range(h):
        Terrienmap.append(list(map(int, f.readline().split())))

    ##############################################
    # step2: run algorithm
    resList = optimalPath(alg, Terrienmap, startPos, maxSteep, targetList).run_alg()

    ##############################################
    # step3: write answers to "output.txt"
    #fout = open("output/out" + name[2:], 'w')
    fout = open("fuck.txt", 'w')

    for res in resList:
        if res:
            for item in res:
                fout.write(str(item.y) + "," + str(item.x) + " ")
            fout.write("\n")
        else:
            fout.write("FAIL\n")

if __name__ == '__main__':
    #import os
    import time
    main("input0-BFS.txt")
    exit()
    filelist = os.listdir("./input")
    for filename in filelist:
        main(filename)


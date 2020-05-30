import math

class robot:

    total_num=0
    communicate_range=0
    explore_range=0

    def __init__(self,pos):
        self.pos=pos
        robot.total_num += 1

    def setRange(self,communicate_range,explore_range):
        robot.communicate_range=communicate_range
        robot.explore_range=explore_range

    def getDistance(self,target):
        return abs(self.pos[0]-target[0])+abs(self.pos[1]-target[1])

    def canCommunicate(self,r:robot)->bool:
        return math.sqrt((self.pos[0]-r.pos[0])**2+(self.pos[1]-r.pos[1])**2)<=robot.communicate_range

    def explore(self):
        '''update map by BFS'''

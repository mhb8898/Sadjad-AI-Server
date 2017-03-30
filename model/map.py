
from enum import Enum
from random import randint
import json

N=10

class ObjectType(Enum):
    red=1
    blue=2
    yellow=3
    black=4
    green=5
    # pig=7
    # giant_pig=8
    rock=9
    wood=10
    glass=11
    empty=12


class rock(Enum):
    rock=9
    wood=10
    glass=11

class ColorEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj,ObjectType):
            return {"type": obj.name}
        return json.JSONEncoder.default(self, obj)


def check(t,i,j,map):
    if 0<=i<N and 0<=j<N and map[i][j] is t:
        return True
    else:
        return False

def dfs(i,j,map,seen=None):
    if seen is None:
        seen=set()
    seen.add((i,j))
    [dfs(i+x,j+y,map,seen) for x,y in [(1,0),(0,1),(-1,0),(0,-1)] if (i+x,j+y) not in seen and check(map[i][j],i+x,j+y,map)]
    return seen

def p(map):
    for i in map.map:
        print i

class Map:
    def __init__(self,map=None):
        if map is None:
            map = [[ObjectType.empty]*N for _ in range(N)]
        self.map=map
        self.rand()
        self.set_wall()
    def rand(self):
        self.gravity()
        i=N-1
        for j in range(N):
            if self.map[i][j] is ObjectType.empty:
                for x,y in dfs(i, j, self.map):
                    self.map[x][y]=ObjectType(randint(1, 5))
    def set_wall(self):
        self.map[5][5]=ObjectType.glass
        self.map[4][5]=ObjectType.glass
        self.map[4][4]=ObjectType.glass
        self.map[5][4]=ObjectType.glass

    def touch(self,i,j):
        # print i,j
        if self.map[i][j] is ObjectType.glass:
            return False
        group_bird=dfs(i,j,self.map)
        if len(group_bird)>1:
            for i,j in group_bird:
                self.map[i][j]=ObjectType.empty
            self.rand()
            return True
        else:
            return False

    # def shift(self,i,j,c):
    #     print i,j,c
    #     for f in range(i,N-c):
    #         self.map[f][j],self.map[f+c][j]=self.map[f+c][j],self.map[f][j]
    #
    # def gravity(self):
    #     for j in range(N):
    #         start=0
    #         for i in range(N):
    #             if self.map[i][j] is None:
    #                 start+=1
    #             elif self.map[i][j] is ObjectType.glass:
    #                 start=0
    #             if not i>=N-1 and self.map[i+1][j] is ObjectType.glass:
    #                 self.shift(i-start, j, start)
    #             if i==N-1 and start:
    #                 self.shift(i-start, j, start)


    def shift(self,i,j,k):
        print i,j,k
        for it in range(i, k):
            if self.map[it][j] is ObjectType.empty:
                for ite in range(it+1, k+1):
                    if self.map[ite][j] is not ObjectType.empty:
                        self.map[it][j],self.map[ite][j]=self.map[ite][j],self.map[it][j]
                        break

    def gravity(self):
        for j in range(N):
            start=0
            for i in range(N):
                if self.map[i][j] is ObjectType.glass:
                    if not start >= i-1:
                        self.shift(start, j, i-1)
                    start=i+1
                if i==N-1:
                    self.shift(start, j, i)




    def to_json(self):
        return json.dumps(self.map,cls=ColorEncoder)

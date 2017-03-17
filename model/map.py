
from enum import Enum
from random import choice
import json

N=10

class color(Enum):
    red=1
    blue=2
    yellow=3
    black=4
    green=5
    # pig=7
    # giant_pig=8
    # rock=9
    # wood=10
    # glass=11


class rock(Enum):
    rock=9
    wood=10
    glass=11

class ColorEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj,color):
            return {"color": obj.name}
        return json.JSONEncoder.default(self, obj)


def check(t,i,j,map):
    if 0<=i<N and 0<=j<N and map[i][j] is t:
        print i,j,t,map[i][j]
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
            map = [[None]*N for _ in range(N)]
        self.map=map
        self.rand()
    def rand(self):
        self.gravity()
        for i in range(N):
            for j in range(N):
                if self.map[i][j] is None:
                    self.map[i][j]=choice(list(color))
    def touch(self,i,j):
        group_bird=dfs(i,j,self.map)
        if len(group_bird)>1:
            for i,j in group_bird:
                self.map[i][j]=None
            return True
        else:
            return False

    def shift(self,i,j,c):
        for f in range(i,N-c):
            self.map[f][j],self.map[f+c][j]=self.map[f+c][j],self.map[f][j]

    def gravity(self):
        for j in range(N):
            for i in range(N):
                start=0
                while i+start<N and self.map[i+start][j] is None:
                    start+=1
                self.shift(i,j,start)
    def to_json(self):
        return json.dumps(self.map,cls=ColorEncoder)

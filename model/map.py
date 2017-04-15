
from enum import Enum
from random import randint
import json
import time

N=10

class ObjectType(Enum):
    empty=0
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
    rocket=12
    bomb=13
    laser=14

    def __init__(self,number,color=None):
        if 1<=number<=5:
            self.life_time = 1
        elif number == 9:
            self.life_time=3
        elif number == 10:
            self.life_time=2
        elif number == 11:
            self.life_time=1
        elif number==12:
            self.dir=randint(0, 1)
        else:
            self.life_time=0
        if color:
            self.color=color


walls=[ObjectType.rock,ObjectType.wood,ObjectType.glass]
powers=[ObjectType.rocket,ObjectType.bomb,ObjectType.laser]

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
        self.turn_number=0
    def rand(self):
        self.gravity()
        i=N-1
        for j in range(N):
            if self.map[i][j] is ObjectType.empty:
                for x,y in dfs(i, j, self.map):
                    self.map[x][y]=ObjectType(randint(1, 5))
    def set_wall(self):
        self.map[5][5]=ObjectType.glass
        self.map[4][5]=ObjectType.rock
        self.map[4][4]=ObjectType.glass
        self.map[5][4]=ObjectType.rock

    def action(self,i,j):
        if (i,j) in self.checked:
            return
        else:
            self.checked.add((i,j))
        if self.map[i][j] is ObjectType.rocket:
            # print "rocket"
            direction=self.map[i][j].dir
            self.map[i][j]=ObjectType.empty
            if direction==self.turn_number%2:
                for x in range(N):
                    if any([power is self.map[x][j] for power in powers]):
                        self.action(x, j)
                    self.map[x][j]=ObjectType.empty
            else:
                for y in range(N):
                    if any([power is self.map[i][y] for power in powers]):
                        self.action(i, y)
                    self.map[i][y]=ObjectType.empty
        elif self.map[i][j] is ObjectType.bomb:
            # print "bomb"
            l=[(i,j) for i in range(-2,3) for j in range(-2,3) if abs(i)+abs(j)<=2 and (i or j) ]
            self.map[i][j]=ObjectType.empty
            for x,y in l:
                x,y=x+i,y+j
                if 0<=x<N and 0<=y<N:
                    if any([self.map[x][y] is power for power in powers]):
                        self.action(x, y)
                    self.map[x][y]=ObjectType.empty

        elif self.map[i][j] is ObjectType.laser:
            # print "laser"
            self.map[i][j] = ObjectType.empty


    def touch(self,i,j):
        # print i,j
        # raw_input()
        time.sleep(0.35)
        self.checked=set()
        self.turn_number+=1
        # print i,j
        if any(self.map[i][j] is x for x in walls):
        # if self.map[i][j] is ObjectType.glass:
            return False
        self.action(i, j)
        group_bird=dfs(i,j,self.map)
        if len(group_bird)>1:
            around = set()
            for i,j in group_bird:
                [around.add((i+x,j+y)) for x,y in [(1,0),(0,1),(-1,0),(0,-1)] if 0<=i+x<N and 0<=j+y<N]
                self.map[i][j]=ObjectType.empty
            # print around
            if len(group_bird)>5:
                self.map[i][j]=ObjectType.rocket
            if len(group_bird)>6:
                self.map[i][j]=ObjectType.bomb
            if len(group_bird)>8:
                self.map[i][j]=ObjectType.laser
            [self.bomb(x,y) for x,y in around]
            self.rand()
            return True
        else:
            return False

    def bomb(self,i,j):
        if not any(self.map[i][j] is x for x in walls):
        # if self.map[i][j] is not ObjectType.glass:
            return False
        # print self.map[i][j]
        if self.map[i][j].life_time>1:
            self.map[i][j].life_time-=1
        else:
            self.map[i][j]=ObjectType.empty

    def shift(self,i,j,k):
        # print i,j,k
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
                if any(self.map[i][j] is x for x in walls):
                # if self.map[i][j] is ObjectType.glass:
                    if not start >= i-1:
                        self.shift(start, j, i-1)
                    start=i+1
                if i==N-1:
                    self.shift(start, j, i)


    def to_json(self):
        return json.dumps(self.map,cls=ColorEncoder)

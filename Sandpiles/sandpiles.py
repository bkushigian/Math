#!/usr/bin/python

from random import randrange

class Sandpile(object):
    def __init__(self, start_config = None, width = 17, height =17, 
                save_history = True, topple_func = None, catastrophe_point = 4,
                topology = 'table'):

        self.width      = width
        self.height     = height
        self.pile       = start_config
        self.cpoint     = catastrophe_point
        self.topology   = topology
        if start_config == None:
            def f(x,y):
                return self.cpoint - 1
        elif isinstance(start_config, int):
            self._start_number = start_config  # Store it for later
            def f(x,y):
                return self._start_number
        elif callable(start_config):
            f = start_config

        elif isinstance(start_config, str):
            if start_config == 'random':
                def f(x,y):
                    return randrange(4)
                        
        self.start_config = f

        self.setup()
        
        if topple_func == None:
            if topology == 'sandbox':
                def func():
                    stacks = [[0]*self.width]*self.height
                    pile = self.pile
                    for i in range(self.height):
                        for j in range(self.width):
                            if pile[i][j]   >= self.cpoint:
                                if (i - 1) >= 0:
                                    stacks[i-1][j] += 1
                                    pile[i][j] -= 1
                                if (i + 1) < self.height:
                                    stacks[i+1][j] += 1
                                    pile[i][j] -= 1
                                if (j - 1) >= 0:
                                    stacks[i][j-1] += 1
                                    pile[i][j] -= 1
                                if (j + 1) < self.width:
                                    stacks[i][j+1] += 1
                                    pile[i][j] -= 1

                    for i in range(self.height):
                        for j in range(self.width):
                            pile[i][j] += stacks[i][j]

            elif topology == 'torus':    # Should be Working...
                def func():
                    pile = self.pile
                    for i in range(self.height):
                        for j in range(self.width):
                            if pile[i][j]   >= self.cpoint:
                                pile[i-1][j] += 1
                                pile[(i+1) % self.height][j] += 1
                                pile[i][j-1] += 1
                                pile[i][(j+1) % self.width] += 1
                                pile[i][j] -= 4

            elif topology == 'table':   # Should be working...
                def func():
                    pile = self.pile
                    updated = True
                    while updated:
                        updated = False
                        for i in range(self.height):
                            for j in range(self.width):
                                if pile[i][j]   >= self.cpoint:
                                    updated = True
                                    if i > 0:
                                        pile[i-1][j] += 1
                                    if i + 1 < self.height:
                                        pile[(i+1) % self.height][j] += 1
                                    if j > 0:
                                        pile[i][j-1] += 1
                                    if j + 1 < self.width:
                                        pile[i][(j+1) % self.width] += 1
                                    pile[i][j] -= 4
                
            elif topology == 'projective-plane':
                def func():
                    raise NotImplementedError("projective plane topple")
                    pile = self.pile
                    for i in range(self.height):
                        for j in range(self.width):
                            if pile[i][j]   >= self.cpoint:
                                pile[i-1][j] += 1
                                pile[(i+1) % self.height][j] += 1
                                pile[i][j-1] += 1
                                pile[i][(j+1) % self.width] += 1
                                pile[i][j] -= 4
            self.topple = func
        else:
            self.topple = topple_func

    def setup(self):
        self.pile = []
        for i in range(self.height):
            self.pile.append([0] * self.width)

        for i in range(self.height):
            for j in range(self.width):
                self.pile[i][j] = self.start_config(i,j)
        

    def add(self, sp, x0 = 0, y0 = 0):
        for i in range(len(sp)):
            for j in range(len(sp[0])):
                if i < self.height and j < self.width:
                    self.pile[i][j] += sp[i][j]
    def run(self, pile_gen = None, iters = 10):
        if pile_gen == None:
            def f():
                width = self.width
                height = self.heigt

                while True:
                    yield
    
    def add_random(self, n = 1):
        for i in range(n):
            x,y = randrange(self.height), randrange( self.width)
            self.pile[x][y] += 1
        
    def __str__(self):
        return '\n'.join([' '.join(map(str, x)) for x in self.pile])

    def __repr__(self):
        return '\n'.join([' '.join(map(str, x)) for x in self.pile])

    def __add__(self, other):
        # FIXME: This should not update self...
        if isinstance(other, int):
            for i in range(self.height):
                for j in range(self.width):
                    self.pile[i][j] += other

        elif isinstance(other, Sandpile):
            for i in range(self.height):
                for j in range(self.width):
                    self.pile[i][j] += other.pile[i][j]
        self.topple()
        return self

    def __iadd__(self, other):
        if isinstance(other, int):
            for i in range(self.height):
                for j in range(self.width):
                    self.pile[i][j] += other

        elif isinstance(other, Sandpile):
            for i in range(self.height):
                for j in range(self.width):
                    self.pile[i][j] += other.pile[i][j]
        self.topple()
        return self
        
    def __getitem__(self, key):
        return self.pile[key]

    def __eq__(self, other):
        if isinstance(other, int):
            for i in range(self.height):
                for j in range(self.width):
                    self.pile[i][j] = other

        elif isinstance(other, Sandpile):
            for i in range(self.height):
                for j in range(self.width):
                    self.pile[i][j] = other[i][j]

    def __setitem__(self,key,value):
        raise NotImplementedError("Sandpile.__setitem__() should never be called!")


    

s   = Sandpile()
s1  = Sandpile(1)
s2  = Sandpile(2)
s3  = Sandpile(3)
sr1 = Sandpile('random')
sr2 = Sandpile('random')

s1center = Sandpile(0)
s1center[s1center.height/2][s1center.width/2] = 1


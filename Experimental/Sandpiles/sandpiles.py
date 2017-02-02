#!/usr/bin/python

from random import randrange
DEFAULT_WIDTH  = 33
DEFAULT_HEIGHT = 33

class Sandpile(object):
    _default_topology = 'table'
    _topologies = ('table', 'torus', 'plane', 'projective-plane', 'mobius-band')
    _characters = (' ', '-', '*', '#')
    print_intermediate = False
    def __init__(self, start_config = None, width = 17, height = 17, save_history = False, 
                 catastrophe_point = 4, topology = None, 
                 print_intermediate = None, pretty_print = False):
        self.width      = width              # Number of cols
        self.height     = height             # Number of rows
        if height == None:
            self.height     = width          # Height of cells (same as width)
        self.pile       = start_config       # How does this pile start off?
        self.cpoint     = catastrophe_point  # Max num before toppling - 4
        self.topology   = topology           # Topology we are working on
        if self.topology == None or self.topology not in self._topologies:
            self.topology = self._default_topology
        if print_intermediate in (True, False):
            Sandpile.print_intermediate = print_intermediate
        self._repr_char = ''                 # Not a char, a string. Seperates for printing
        self.pretty_print = pretty_print     # Print nice chars or just ints?

        # Create function to reinitialize
        if start_config == None:
            def f(x,y):
                return self.cpoint - 1
            self.start_config = f        

        elif isinstance(start_config, int):
            self._start_number = start_config  # Store it for later
            def f(x,y):
                return self._start_number
            self.start_config = f        

        elif callable(start_config):
            f = start_config

        elif isinstance(start_config, str):
            if start_config == 'random':
                def f(x,y):
                    return randrange(4)
                self.start_config = f        
            elif start_config == 'center':
                def f(x,y):
                    if (x == self.height) / 2 and (y == self.width / 2):
                        return 1
                    return 0
                self.start_config = f        
            elif start_config.startswith('center'):
                try:
                    n = int(start_config[6:])
                except Exception as e:
                    raise RuntimeError("start_config '{}' starts with 'center' and ends with non-integer '{}'".format(start_config, start_config[6:]))
                def f(x,y):
                    if x == (self.height / 2) and y == (self.width / 2):
                        return n
                    return 0
                self.start_config = f        

        # ... and set this as our start function
        self.setup()  # This calls what we just did!
        
        # How do we topple? The user can define this, but probably wants to just
        # do something we already did!
        # TODO: Change this to a map of pre-defined functions?
        if self.topology == 'sandbox':
            # 'sandbox' refers to walls that prevent sand from escaping.
            # This is equivalent to always subtracting the lowest value'd
            # pile from all piles after each topple. 
            raise NotImplementedError("sandbox is broken. Yeah, yeah, I'm an asshole. Tell someone who cares")
            def func():
                # FIXME: This doesn't work. At all. BLAH
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

                # TODO: Move into the original loop
                for i in range(self.height):
                    for j in range(self.width):
                        pile[i][j] += stacks[i][j]
            self.topple = func

        elif self.topology == 'torus':    # Should be Working...
            def func():
                if Sandpile.print_intermediate:
                    print "Starting Topple"
                    print self
                pile = self.pile
                updated = True
                while updated:
                    updated = False
                    for i in range(self.height):
                        for j in range(self.width):
                            if pile[i][j]   >= self.cpoint:
                                updated = True
                                pile[i-1][j] += 1
                                pile[(i+1) % self.height][j] += 1
                                pile[i][j-1] += 1
                                pile[i][(j+1) % self.width] += 1
                                pile[i][j] -= 4
                    if Sandpile.print_intermediate and updated:
                        print self
            self.topple = func

        elif self.topology == 'table':   # Should be working...
            print_inter = Sandpile.print_intermediate

            def func():
                if print_inter == True:
                    print "Starting Topple"
                    print self
                    print '-' * self.width
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
                    if print_inter == True:
                        print self 
                        print ('-' * self.width)
            self.topple = func
            
        elif self.topology == 'projective-plane':
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
            raise RuntimeError("Invalid topology: '{}'!".format(self.topology))

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

    def shift_up(self, n, filler_value = 0):
        result = Sandpile(filler_value, topology = self.topology, width = self.width,
                          height = self.height, catastrophe_point = self.cpoint)
        for i in range(n, self.height):
            for j in range(self.width):
                result[i - n][j] = self[i][j]
        return result

    def shift_down(self, n, filler_value = 0):
        result = Sandpile(filler_value, topology = self.topology, width = self.width,
                          height = self.height, catastrophe_point = self.cpoint)
        for i in range(n, self.height):
            for j in range(self.width):
                result[i][j] = self[i - n][j]
        return result

    def shift_left(self, n, filler_value = 0):
        result = Sandpile(filler_value, topology = self.topology, width = self.width,
                          height = self.height, catastrophe_point = self.cpoint)
        for i in range(n, self.height):
            for j in range(self.width):
                result[i][j - n] = self[i][j]
        return result

    def shift_right(self, n, filler_value = 0):
        result = Sandpile(filler_value, topology = self.topology, width = self.width,
                          height = self.height, catastrophe_point = self.cpoint)
        for i in range(n, self.height):
            for j in range(self.width):
                result[i][j] = self[i][j - n]
        return result

    def __str__(self):
        if self.pretty_print:
            #return '\n'.join([ str(map(lambda a : self._characters[a], x)) for x in self.pile])
            return '\n'.join([self._repr_char.join(map(lambda a : self._characters[a], x)) for x in self.pile])
        return '\n'.join([self._repr_char.join(map(str, x)) for x in self.pile])

    def __repr__(self):
        return str(self)

    def __add__(self, other):
        '''Add two sandpiles together. Must be the same size. 'Constant'
        Sandpile can be denoted as an integer (i.e., Sandpile + 3 is the same as
        adding a sandpile with 3's everywhere. '''
        # FIXME: This should not update self...
        if isinstance(other, int):
            result = Sandpile(0, width = self.width, height = self.height, topology = self.topology)
            for i in range(self.height):
                for j in range(self.width):
                    result[i][j] = self[i][j] + other

        elif isinstance(other, Sandpile):
            assert self.width == other.width and self.height == other.height
            assert self.topology == other.topology # Add plane to torus? NO!
            result = Sandpile(0, width = self.width, height = self.height, topology = self.topology)
            for i in range(self.height):
                for j in range(self.width):
                    result[i][j] = self[i][j] + other[i][j]
        else:
            raise RuntimeError("Unrecognized value {} in sandpile.__add__".format(other))
        result.topple()
        return result

    def __iadd__(self, other):
        if isinstance(other, int):
            for i in range(self.height):
                for j in range(self.width):
                    self[i][j] += other

        elif isinstance(other, Sandpile):
            assert self.width == other.width and self.height == other.height
            for i in range(self.height):
                for j in range(self.width):
                    self[i][j] += other[i][j]
        else:
            raise RuntimeError("Unrecognized value {} in sandpile.__iadd__".format(other))
        self.topple()
        return self
        
    def __imul__(self, other):
        if isinstance(other, int):
            for i in range(self.height):
                for j in range(self.width):
                    self[i][j] *= other

        else:
            raise RuntimeError("Unrecognized value {} in sandpile.__imul__".format(other))
        self.topple()
        return self

    
    def __mul__(self, other):
        if isinstance(other, int):
            result = Sandpile(0, height = self.height, width = self.width,
            topology = self.topology)
            for i in range(self.height):
                for j in range(self.width):
                    self[i][j] *= other

        else:
            raise RuntimeError("Unrecognized value {} in sandpile.__imul__".format(other))
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


    


def main():
    # These can be changed for testing
    width  = 73
    height = 35
    topology = 'table'

    #Sandpile.print_intermediate = True

    start_pile = Sandpile(start_config  = 3,         topology = topology, width = width, height = height)
    center     = Sandpile(start_config = 'center1',  topology = topology, width = width, height = height, pretty_print = True)
    # s2 = s + center

    # s2.pretty_print = True

    n = 11
    l = [center.shift_left(n * i) + center.shift_right(n * i) + 
         center.shift_up(n * i) + center.shift_down(n * i) for i in range(0, width / n)]
    s3 = center + 0
    for pile in l:
        s3 += pile

    final = start_pile + s3
    final.pretty_print = True
    print final

if __name__ == '__main__':
    main()

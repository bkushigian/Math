#!/usr/bin/python

from random import randrange
from time import time
from nonblockingconsole import NonBlockingConsole as NBC

DEFAULT_WIDTH  = 33
DEFAULT_HEIGHT = 33

class Sandpile(object):
    _default_topology = 'table'
    _topologies = ('table', 'torus', 'plane', 'projective-plane', 'mobius-band')
    _characters = ' -*^%$#'
    print_intermediate = False
    _pretty_print      = False
    _print_sleep_time  = 0.04    # Smooth printing when printing quickly!
    _nbc               = NBC()   # Non-blocking console, for interrupting printing
    def __init__(self, start_config = None, width = 17, height = 17, save_history = False, 
                 catastrophe_point = 4, topology = None, sink_config = None,
                 print_intermediate = None, pretty_print = None):
        self.width      = width              # Number of cols
        self.height     = height             # Number of rows
        if height == None:
            self.height     = width          # Height of cells (same as width)
        self.pile       = None               # How does this pile start off?
        self.sink       = None
        self.cpoint     = catastrophe_point  # Max num before toppling - 4
        self.topology   = topology           # Topology we are working on
        if self.topology == None or self.topology not in self._topologies:
            self.topology = self._default_topology
        if print_intermediate in (True, False):
            Sandpile.print_intermediate = print_intermediate
        self._repr_char = ' '                 # Not a char, a string. Seperates for printing
        if pretty_print in (True, False):
            Sandpile._pretty_print = pretty_print     # Print nice chars or just ints?
        self.pretty_print = Sandpile._pretty_print


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
            elif start_config.startswith('tower'):
                config_str = start_config[5:]
                configs = config_str.split(',')
                assert len(configs) == 3

                X,Y,TOWER_HEIGHT = map(int,configs)

                def f(x,y):
                    if x == X and y == Y:
                        return TOWER_HEIGHT
                    return 0
                    
                self.start_config = f        

        # Check your sinks
        if sink_config == None:
            def func(x,y):
                return 0
            self.sink_config = func

        elif callable(sink_config):
            self.sink_config = sink_config

        elif isinstance(sink_config, list):   # This will be a list of tuples
            mySet = set([])
            for tup in sink_config:
                assert isinstance(tup, tuple) or isinstance(tup, list)
                mySet.add( (x,y) )
            def func(x,y):
                return (x,y) in mySet

            self.sink_config = func           # This will be updated in setup
            
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
                update = False    # The result
                pile = self.pile
                for i in range(self.height):
                    for j in range(self.width):
                        if pile[i][j]   >= self.cpoint:
                            updated = True
                            if (i - 1) >= 0:
                                pile[i-1][j] += 1
                                pile[i][j] -= 1
                            if (i + 1) < self.height:
                                pile[i+1][j] += 1
                                pile[i][j] -= 1
                            if (j - 1) >= 0:
                                pile[i][j-1] += 1
                                pile[i][j] -= 1
                            if (j + 1) < self.width:
                                pile[i][j+1] += 1
                                pile[i][j] -= 1
                return updated

            self.topple_single = func

        elif self.topology == 'torus':    # Should be Working...
            def func():
                updated = False
                pile = self.pile
                for i in range(self.height):
                    for j in range(self.width):
                        if pile[i][j]   >= self.cpoint:
                            updated = True
                            pile[i-1][j] += 1
                            pile[(i+1) % self.height][j] += 1
                            pile[i][j-1] += 1
                            pile[i][(j+1) % self.width] += 1
                            pile[i][j] -= 4
                return updated

            self.topple_single = func

        elif self.topology == 'table':   # Should be working...
            def func():
                pile = self.pile
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
                return updated

            self.topple_single = func
            
        elif self.topology == 'projective-plane':
            def func():
                raise NotImplementedError("projective plane topple")
                updated = False
                pile = self.pile
                for i in range(self.height):
                    for j in range(self.width):
                        if pile[i][j]   >= self.cpoint:
                            updated = True
                            pile[i-1][j] += 1
                            pile[(i+1) % self.height][j] += 1
                            pile[i][j-1] += 1
                            pile[i][(j+1) % self.width] += 1
                            pile[i][j] -= 4
                return updated

            self.topple = func
        else:
            raise RuntimeError("Invalid topology: '{}'!".format(self.topology))

    def topple(self):
        if Sandpile.print_intermediate:
            print self
            print '\n' + ('='*80) + '\n'
            nbc = NBC()
        while self.topple_single():
            if Sandpile.print_intermediate:
                t0 = time()
                print self
                print '\n' + ('='*80) + '\nEnter to continue'
                while time() - self._print_sleep_time < t0:
                    if nbc.get_data():
                        return
                
    def setup(self):
        self.pile = []
        self.sink = []
        for i in range(self.height):
            self.pile.append([0] * self.width)
            self.sink.append([0] * self.width)

        for i in range(self.height):
            for j in range(self.width):
                self.pile[i][j] = self.start_config(i,j)
                self.sink[i][j] = self.sink_config(i,j)
        

    def add(self, other):
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

        return result

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
        self.topple()
        return self   # For chaining 

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
        for i in range(self.height):
            for j in range(n, self.width):
                result[i][j - n] = self[i][j]
        return result

    def shift_right(self, n, filler_value = 0):
        result = Sandpile(filler_value, topology = self.topology, width = self.width,
                          height = self.height, catastrophe_point = self.cpoint)
        for i in range(self.height):
            for j in range(n, self.width):
                result[i][j] = self[i][j - n]
        return result

    def _get_character(self,n):
        if n >= 0 and n < len(self._characters):
            return self._characters[n]
        return '!'
    def __str__(self):
        if Sandpile._pretty_print:
            #return '\n'.join([ str(map(lambda a : self._characters[a], x)) for x in self.pile])
            return '\n'.join([self._repr_char.join(map(lambda a : self._get_character(a), x)) for x in self.pile])
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
    # Note that these width/height values drastically increase time to test.
    # Also, they change the thing being created (since this is the size of the
    # table!)

    width      = 81
    height     = 81
    topology   = 'table'
    n = 2       # This varies the dispersal for the shifting operations
    sleep_time = 2.0

    start_pile = Sandpile(start_config  = 3,         topology = topology, width = width, height = height)
    center     = Sandpile(start_config = 'center1',  topology = topology, width = width, height = height, pretty_print = True)
    # s2 = s + center

    # s2.pretty_print = True
    def test1():
        print "BEGINNING TEST 1"
        l = []
        factor = (width/2) / n
        for i in range(0, factor):
            temp = center.shift_left(n * i) + center.shift_right(n * i) + center.shift_up(n * i) + center.shift_down(n * i)
            l.append(temp)

        s3 = center + 0
        for pile in l:
            s3 += pile
        final = start_pile + s3
        final.pretty_print = True

        print start_pile
        print 
        print (' ' * (width/2)) + '+'
        print 
        print s3
        print 
        print (' ' * (width/2)) + '='
        print 
        print final

    def test2():
        print "BEGINNING TEST 2"
        s = (start_pile + 0)
        print s
        print
        print '=' * width
        print
        generating = True
        with NBC() as nbc:
            while True:
                x = nbc.get_data()
                if x == 'p':   # Pause/ Unpause
                    generating = not generating
                elif x:
                    break

                if generating:
                    ctime = time()
                    print s.add_random(100)
                    print
                    print '=' * width
                    print
                    while (time() < ctime + sleep_time):
                        continue

    def test3():
        print "BEGINNING TEST 3"
        s = Sandpile(start_config = 'center4000', topology = topology, width = width, height = height)
        Sandpile.print_intermediate = True
        s.topple()
        print s


    def test4():
        print "BEGINNING TEST 4"
        Sandpile.print_intermediate = True
        s1 = Sandpile(start_config = 'tower{},{},4700'.format(7*height/16, 7*width/16), topology = topology, width = width, height = height)
        s2 = Sandpile(start_config = 'tower{},{},4700'.format(7*height/16, 9*width/16), topology = topology, width = width, height = height)
        s3 = Sandpile(start_config = 'tower{},{},4700'.format(9*height/16, 7*width/16), topology = topology, width = width, height = height)
        s4 = Sandpile(start_config = 'tower{},{},4700'.format(9*height/16, 9*width/16), topology = topology, width = width, height = height)
        s = s1.add(s2).add(s3).add( s4)
        s.topple()
        print s
    
    def test5():
        print "BEGINNING TEST 4"
        Sandpile.print_intermediate = True
        s1 = Sandpile(start_config = 'tower{},{},4700'.format(height/2, 15*width/32), topology = topology, width = width, height = height)
        s2 = Sandpile(start_config = 'tower{},{},4700'.format(height/2, 17*width/32), topology = topology, width = width, height = height)
        s = s1.add(s2)
        s.topple()
        print s

    def test6():
        print "BEGINNING TEST 4"
        Sandpile.print_intermediate = True
        s1 = Sandpile(start_config = 'tower{},{},4700'.format(15*height/32, 14*width/32), topology = topology, width = width, height = height)
        s2 = Sandpile(start_config = 'tower{},{},4700'.format(17*height/32, 18*width/32), topology = topology, width = width, height = height)
        s = s1.add(s2)
        s.topple()
        print s
    test3()
    test4()
    test5()
    test6()

if __name__ == '__main__':
    main()

#!/usr/bin/python3
from utils import ffs

class CollatzFunction:
    '''
    An instance of CollatzFunction computes the next number in a CollatzFunction
    sequence given a starting value. This can be accessed as follows:

        c = Collatz()    # Collatz is short for CollatzFunction and is defined
                         # near EOF
        c(4)   # returns 2
        c(5)   # returns 16
        c[5]   # returns [5, 16, 8, 4, 2, 1]

    Additionally this includes a method sequence that generates the _infinite_
    sequence:

        sequence = c.sequence(32):
        for i in sequence:
            print(i)
        # Prints 32, 16, 8, 4, 2, 1, 4, 2, 1, 4, 2, 1, ...

    Finally, there is a orbit method that is exactly the same as sequence() but
    terminates at 1.
    '''

    def __init__(self, mult = 3, add = 1, parity = 2):
        self.mult   = mult
        self.add    = add
        self.parity = parity

    
    def __call__(self, ns):
        '''Returns the next collatz number after n'''
        try:
            return [self._call(k) for k in ns]
        except:
            return self._call(ns)

    def _call(self, n):
        if n % self.parity == 0:
            return n // self.parity
        return self.mult * n + self.add
        

    def orbit(self, ns):
        try:
            return [self._orbit(k) for k in ns]
        except:
            return self._orbit(ns)

    def _orbit(self, n):
        yield n
        while n != 1:
            n = self(n)
            yield n

    def sequence(self, ns):
        try:
            return [self._sequence(k) for k in ns]
        except:
            return self._sequence(ns)

    def _sequence(self, n):
        yield n
        while True:
            n = self(n)
            yield n

    def length(self, ns):
        '''return the number of elements in the orbit'''
        try:
            return [self._length(k) for k in ns]
        except:
            return self._length(ns)

    def _length(self, n):
        l = 1
        while n > 1:
            l += 1
            n = self(n)
        return l
    
    def lengths(self, lower = 1, upper = 128):
        # XXX: This has been deprecated. Please use length(range(100))
        print("[!] WARNING: lengths is deprecated")
        lower = max(1, lower)
        upper = max(lower + 1, upper)
        return [self.length(i) for i in range(lower, upper)]

    def evens(self, n):
        '''evens returns a list of the length of consecutive cascading even
        divisions. For input n = 7 we have:

            7 -> 22     []
            22 -> 11    [1]
            11 -> 34
            34 -> 17    [1,1]
            17 -> 52
            52 -> 26    
            26 -> 13    [1,1,2]
            26 -> 40   
            40 -> 20
            20 -> 10
            10 -> 5     [1,1,2,3]
            5  -> 16
            16 -> 8
            8  -> 4
            4  -> 2
            2  -> 1     [1,1,2,3,4] 

        and we return [1,1,2,3,4]
        '''
        assert self.parity == 2  # This ONLY makes sense with parity of 2
        result = []
        if n % 2 == 1:
            n = self(n)
        while n > 1:
            trailing_zeros = ffs(n)
            result.append(trailing_zeros)
            n >>= trailing_zeros
            if n > 1:
                n = self.mult * n + self.add
        return result
        
    def __getitem__(self, key):
        return self.orbit(key)

Collatz = CollatzFunction       # A shortcut

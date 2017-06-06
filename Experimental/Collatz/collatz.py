#!/usr/bin/python3

class CollatzFunction:
    '''
    An instance of CollatzFunction computes the next number in a CollatzFunction
    sequence given a starting value. This can be accessed as follows:

        c = CollatzFunction()
        c(4)   # returns 2
        c(5)   # returns 16

    Additionally this includes a method get_orbit that generates the _infinite_
    orbit:

        orbit = c.orbit(32):
        for i in orbit:
            print(i)
        # Prints 32, 16, 8, 4, 2, 1, 4, 2, 1, 4, 2, 1, ...

    Finally, there is a sequence method that is exactly the same as orbit() but
    terminates at 1.
    '''

    def __init__(self, mult = 3, add = 1, parity = 2):
        self.mult   = mult
        self.add    = add
        self.parity = parity

    
    def __call__(self, n):
        '''Returns the next collatz number after n'''
        if n % self.parity == 0:
            return n // self.parity
        return self.mult * n + self.add

    def sequence(self, n):
        yield n
        while n != 1:
            n = self.__call__(n)
            yield n

    def orbit(self, n):
        yield n
        while True:
            n = self.__call__(n)
            yield n

    def length(self, n):
        '''return length of the sequence before reaching 1'''
        l = 0
        while n > 1:
            l += 1
            n = self(n)
        return l


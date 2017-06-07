#!/usr/bin/python3
import argparse # For parsing arguments to dictate program flow
try:
    import matplotlib as mpl
    import matplotlib.pyplot as plt
except:
    print("Couldn't import matplotlib")

from collatz import Collatz # Short for CollatzFunction

if __name__ == '__main__':
    op = 5
    if op == 1:
        c = Collatz()
        data = c.lengths(1, 10000)
        plt.plot(data, 'r.')
        plt.ylabel('termination time')
        plt.xlabel('start value')
        plt.show()

    elif op == 2:
        c = Collatz()
        # seed = 11239012322
        seed = 2**32 - 1
        data = list(c[seed])
        plt.plot(data, 'r.')
        plt.ylabel('value at current iteration')
        plt.xlabel('ith iteration of collatz on seed value {}'.format(seed))
        plt.yscale('log')
        plt.show()

    elif op == 3:
        c = Collatz()
        seed = 12345678
        data = list(c.evens(seed))
        plt.plot(data, 'r.')
        plt.ylabel('number of iterations on ith cascade')
        plt.xlabel('ith cascade for seed value {}'.format(seed))
        #plt.yscale('log')
        plt.show()

    elif op == 4:
        c = Collatz()
        # seed = 11239012322
        seed = 2**32 - 1
        data = list(c[seed])
        plt.plot(data, 'r.')
        plt.ylabel('value at current iteration')
        plt.xlabel('ith iteration of collatz on seed value {}'.format(seed))
        #plt.yscale('log')
        plt.show()
    elif op == 5:
        c = Collatz()
        seeds = [3**k - 1 for k in range(800)]
        data = c.length(seeds)
        plt.plot(data, 'r.')
        plt.show()

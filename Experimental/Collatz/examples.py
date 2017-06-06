from collatz import CollatzFunction as Collatz
from utils import ffs

C = Collatz()
def print_sequence(n):
    for k in C.sequence(n):
        print(k)
    
def print_ffs_after_increase(n):
    assert n > 0
    i = 1       # Count which iteration we're on
    print("1: {}".format(n))
    while n > 1:
        i += 1
        m = C(n)
        if m > n:   # We increased w/ m = 3n + 1
            print("{}: {} {}".format(i, m, ffs(m)))
        else:
            print("{}: {}".format(i, m))
        n = m


if __name__ == '__main__':
    while True:
        selection = input(
'''(1) print sequence
(2) print sequence with trailing zeros info
''')
        try:
            selection = int(selection)
            if selection in (1,2):
                break
        except:
            continue
    while True:
        starting_number = input('''Enter number to start at''')
        try:
            starting_number = int(starting_number)
            if starting_number > 0:
                break
        except:
            continue
    if selection == 1:
        print_sequence(starting_number)
    else:
        print_ffs_after_increase(starting_number)


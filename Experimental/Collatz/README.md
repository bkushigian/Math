# Collatz Stuff

## Installing
Well, this is part of a larger git repo so if you want to install this you can
download the zip, pull out this folder and delete everything else. Otherwise you
can run a `git clone ...` (this will let you keep up to date with any updates I
issue).

# Running
Assuming that this directory is named `Collatz/` (so that the project looks like

    Collatz/
        collatz.py
        examples.py
        README.md
        utils.py

then you can issue a `cd path/to/Collatz` and that will bring your terminal
here. Then you can run `python3` which will open up an interpreter. Then run

    >>> from collatz import CollatzFunction
    >>> C = CollatzFunction()
    >>> C(1)
    4
    >>> C(4)
    2
    >>> C(2)
    1
    >>> C.length(1)
    >>> D = CollatzFunction(add = 101)
    >>> D(1)
    104
    >>> D(104)
    52
    >>> seq = C[5]
    >>> list(seq)
    [5, 16, 8, 4, 2, 1]

## Basics
This is a tiny module to play with the Collatz conjecture. Basicall there is a
class `CollatzFunction` defined in `collatz.py` that allows the user to define
different functions similiar to the Collatz conjecture. For example, we can open
a terminal in the `Collatz/` directory and enter the following

    from collatz import CollatzFunction
    C = CollatzFunction()    # This is just the normal Collatz function
    C(3)    # => 10
    C(10)   # => 5
    C(5)    # => 16

    # The following creates a collatz-like function that operates as follows:
    # if n is a multiple of 3 then D(n) = n / 3
    # otherwise D(n) = 5*n + 1

    D = CollatzFunction(mult = 5, add = 1, parity = 3)
    D(2)     # => 11
    D(11)    # => 56
    D(56)    # => 281
    D(281)   # => 1406

We can see in this last example that this will never terminate (since we have
the fixed point `2 = 5 * 2 + 1 (mod 3)`). This prompts the methods
`CollatzFunction.orbit()` and `CollatzFunction.sequence()` which returns an
__generator__ rather than a list. Why?  Because this gives us the option to
evaluate _lazily_ and not have to compute the entire contents of a sequence
ahead of time. Thus we can run the following code:

    for x in C.sequence(5):
        print(x)

which outputs:
    
    5 
    16 
    8 
    4 
    2 
    1

We also have a shortcut for the `sequence` function, which is just syntactic
sugar. We can access `C.sequence(5)` with `C[5]`.


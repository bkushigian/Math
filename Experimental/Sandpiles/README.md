# Sandpiles

Sandpiles are cool. They are piles of sand! I'm from Cape Cod, so I like sand.
That is why I wrote piles of it. Sand is cool. You're cool. I'm cool. We should
all be cool and play with cool things like sand!

## But really, sand piles...
Sandpiles (also known as *Abelian Sandpiles*) are a mathematical abstraction on
literal piles of sand. You should check out [this page by people smarter than
me](https://en.wikipedia.org/wiki/Abelian_sandpile_model "Wikipedia") to find
out more.

## sandpiles.py
This is where the magic happens. Actually, it's not magic. It's sand. This is
really a reference implementation to check out some different ideas. Currently
the `topple` function is really inefficient and can be improved by a factor of
two very easily using the *Abelian property of sandpiles*, which is a big fancy
five-dollar way of saying *the order of toppeling does not matter*. Neat! I
didn't know about this when I built it. I should change this.

Also, this was quickly written after over 24 hours of no sleep. So bugs. YUM!
But also, I should write this in C if I feel like actually working with this.

## TODO, and TODON'T's
There are no TODON'T's. You are allowed TODO whatever you want TODO. But as I
mentioned, I would like to

  * Improve the topple functions (there are a few, since there are different
    topologies)
  * *Verify* the various topologies topple functions
  * Write this in C for better performance (and perhaps wrap in Python?)
  * Better visualizing methods (ie, not just text! Use a GUI. Yuck! I know,
    right? But not all GUIs are disgusting. There are good GUIs too. Maybe when
    you're older...)
  * Ooooh ooooh ooooooooh!!! Write it in HASKELL with Lazy Evaluation!!!! Dude!
    Then we can write it on an infinite plane!!!! Come ON, that is fucking
    awesome!

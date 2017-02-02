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
five-dollar way of saying *the order of toppeling does not matter*.

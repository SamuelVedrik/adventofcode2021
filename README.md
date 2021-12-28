# Sam's Advent of Code 2021. 

Completed up to day 25! 
Written in python.


### Things I learned in this AOC:

- **defaultdict**
    `from collections import defaultdict`
    I have been using these extensively, and allows for way cleaner code. It removes the need for 
    `if key in dict: dict[key] = foo`

- **Getting idx from a 2d boolean array**.

    Assuming that `arr` is a 2d array of booleans, then we can do:

    `ids = np.transpose(np.nonzero(arr))`

    Where `ids[0, :]` is the `(i, j)` index of the first `True` in `arr`.
    We can then use `origin[ids[:, 0], ids[:, 1]]` as equivalent to `origin[arr]`, assuming that `origin` is the 2d array that arr originates from.

    This is useful when we want to manipulate the indexes in some fashion. Look at day 25 for an example.

- **NetworkX**

    A useful library that can make graphs. Useful for getting shortest paths, etc.

- **heapq**
    
    Heapifies a list. I used these a lot for Uniform-Cost search (A Djikstra alternative)






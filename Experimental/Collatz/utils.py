def ffs(n):
    '''find first set or count trailing zeros'''
    assert isinstance(n, int) or isinstance(n, long)
    count = 0
    while not n & 1:
        n = n >> 1
        count += 1
    return count

#depricate, replace by numpy array

def length(a:tuple):
    return sum([i**2 for i in a])**0.5
def unit(a:tuple):
    len_a = length(a)
    return tuple([i/len_a for i in a])

def dist(a:tuple, b:tuple):
    return length([ai-bi for ai, bi in zip(a,b)])

def div(a:tuple, b:tuple):
    return tuple([ai-bi for ai, bi in zip(a,b)])

def mly(a:int, b:tuple):
    return tuple([a*bi for bi in b])
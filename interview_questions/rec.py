"""Subset question etc etc..."""

def subsets(st):
    ret = []
    if len(st) <= 1:
        return [st]
    ret.append(st[-1])
    for a in subsets(st[:-1]):
        ret.append(a+st[-1])
        ret.append(a)
    return ret

print subsets('a')
print subsets('ab')
print subsets('abc')

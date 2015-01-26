def upper(x):
    for i in range(1, 32):
        if x & (1<<i) == 0 and x & (1<<i-1) > 0:
            x = x ^ (1<<i)
            x = x ^ (1<<i-1)
            return x
    return None 

def lower(x):
    for i in range(0, 31):
        if x & (1<<i) == 0 and x & (1<<i+1) > 0:
            x = x ^ (1<<i)
            x = x ^ (1<<i+1)
            return x
    return None

def mbin(x):
    if x is None:
        return x
    return bin(x)

if __name__ == '__main__':
    for i in range(16):
        print i, mbin(i), mbin(upper(i)), mbin(lower(i))
         

"""The 'right' way to do this..."""

def longest_string(strings):
    return max(*strings, key=len)

if __name__ == '__main__':
    strings = 'This is a test of the longest string function'
    print longest_string(strings.split())

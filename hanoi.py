import sys

#data = sys.stdin.readlines()

n,k = sys.stdin.readline().split(' ')
start = sys.stdin.readline().split(' ')
end = sys.stdin.readline().split(' ')

n = int(n)
k = int(k)
start = [int(x) for x in start]

end = [int(x) for x in end]
nmoves = 0

def moveDisks(n,origin,destination,buffer):
    if (n<=0) : return
    
    moveDisks(n-1,origin, buffer, destination)
    
    start[n-1]=destination
    print n,destination
    
    moveDisks(n-1,buffer,destination,origin) 
    
moveDisks(n,1,3,2)


import sys
# tower of hanoi solver

# input line 1 number of disks, number of pegs
# input line 2 initial configuration 
#(ie 1 1 1, all on peg 1, or 1 2 3 all on separate pegs with largest on 3)
# input line 3 final configuration 

n,k = sys.stdin.readline().split(' ')
start = sys.stdin.readline().split(' ')
end = sys.stdin.readline().split(' ')

n = int(n)
k = int(k)
start = tuple([int(x) for x in start])
end = tuple([int(x) for x in end])

solutions = {}

class Solution:
    def __init__(self,configuration,parent=None):
        self.configuration = configuration
        self.colour = 0
        self.dist = -1
        self.predecesor = None
        if parent != None:
            self.links = [parent]
        else:
            self.links = []

    def Moves(self):
        buried = [] # keep track of pegs that have smaller disks on top
        for disk,origin in enumerate(self.configuration):
            if origin not in buried: # this disk is on top
                buried.append(origin)
                for dest in range(k):
                    if dest not in buried: # destination is valid
                        newConfiguration = list(self.configuration) # create copy
                        newConfiguration[disk] = dest
                        newConfiguration = tuple(newConfiguration) #hmm
                        if newConfiguration not in solutions.keys():
                            newSolution = Solution(newConfiguration,self)
                            solutions[newConfiguration] = newSolution
                            self.links.append(newSolution)
                            newSolution.Moves() # will hit recursion limit on large trees
                        else :
                            if solutions[newConfiguration] not in self.links:
                                solutions[newConfiguration].links.append(self)
                                self.links.append(solutions[newConfiguration])


s = Solution(start)
s.Moves()

s.colour = 1 # grey
s.dist = 0
s.predecesor = None

queue = [s]

while queue != []:
    a = queue.pop(0) # this isn't very efficient way to implement a queue
    for link in a.links:
        if link.colour == 0: # white
            link.colour = 1 # grey
            link.dist = a.dist+1
            link.predecesor = a
            queue.append(link)
    a.colour = 2
    
e = solutions[end]

print e.dist
moves = [e]

while e != s:
    e = e.predecesor
    moves.append(e)
    
for move in moves:
    print move.configuration


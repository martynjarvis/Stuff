import random
nrounds = 10 
pseudogames = 500000
nwins = 0
deck = range(1,14)+range(1,14)+range(1,14)+range(1,14)
results = [0 for i in deck]
cumulative =[0 for i in deck]
for i in range(pseudogames):
	if i%10000 ==0:print i,pseudogames
	random.shuffle(deck)
	nrun = -1
        currentcard = -1
	guess = 0
	previouscards = []
	for card in deck:
	    #print "Card is ",card 
	    if (card > currentcard and guess < 0) or (card < currentcard and guess > 0) :
		#print "FAIL"
		break 
	    else : 
		currentcard = card
	        previouscards.append(card)
	        nrun = nrun+1     
	        #make guess		
	        nhigher = (13-card)*4
	        nlower = (card-1)*4
	        for prevcard in previouscards:
	            if prevcard>card : nhigher = nhigher-1
	            elif prevcard<card : nlower = nlower-1
	        if nlower>nhigher:guess=-1
	        elif nhigher>nlower: guess = +1
	        else : guess = random.choice([-1,+1])
		#if 7 keep current guess
	    #print "Guess is ",guess
	#print nrun
	#results.append(nrun)
	if nrun>=nrounds: nwins=nwins+1
	results[nrun] = results[nrun]+1
	for f in range(nrun+1): cumulative[f] = cumulative[f]+1

print results
print cumulative

print nwins
print "Probability of winning = ", float(nwins)/float(pseudogames)
print "n cards","Probability"
for i,result in enumerate(cumulative) : 
	print i, float(result)/float(pseudogames)
#Results
#n rounds  --  prob winning
#0	1.0
#1	0.7827
#2	0.59371
#3	0.447655
#4	0.33783
#5	0.255506
#6	0.193344
#7	0.145128
#8	0.110728
#9	0.084394
#10

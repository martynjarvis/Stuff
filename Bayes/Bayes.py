#!/usr/bin/python

import sys
import Bayes_Classes

guesser = Bayes_Classes.myBayes()
guesser.load('my_guesser.bay')

# This should probably be changed back
# The idea should be that the program returns a keyword that describes what to do next
# i.e. "greeting" -> return a greeting
# it should be aware of some sort of history in a conversation, ie subject and order of statements
# i.e. if the program asks hello, the program shouldn't the react to the users response

# Definitions:
# If the program returns the definition keyword, each word should then be checked indiviually
# Word with the lowest match to the definition, becomes the subject of the definition


if len(guesser.poolNames())<1 :
  guesser.newPool("greeting")
  guesser.newPool("exit")
  guesser.newPool("time")
  guesser.newPool("day")
  guesser.newPool("date")
  guesser.newPool("no")
  guesser.newPool("yes")

print guesser.poolNames()

while True :
  text = raw_input("Make a statement or ask a question:\n")
  output = guesser.guess(text)
  temp = output
  if len(output)>0 :
    #eventually this should pick a response and give that, or if two responses are close, ask what the user meant
    for i, response in enumerate(output) :
      print i, response
    num = raw_input("Pick correct response and program will learn:\n")  
    if int(num)<len(output) : 
      guess = output[int(num)]
      guesser.train(guess[0], text)
      if output[0][0] == "exit" : break    
    else : 
      print "Unknown, ignoring."           
  else :
    print "Unknown Statement."
    for i, response in enumerate(guesser.poolNames()) :
      print i, response
    num = raw_input("Pick correct response and program will learn:\n")
    if int(num)<len(guesser.poolNames()) : 
      guesser.train(guesser.poolNames()[int(num)], text)
    else : 
      print "Unknown, ignoring."


guesser.save('my_guesser.bay')


import datetime
today = datetime.date.today()
str = str(today)
guesser.save('my_guesser'+str+'.bay')
#save back up


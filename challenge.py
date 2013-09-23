#!/usr/bin/env python
# -*- coding: utf-8 -*-
# print out the hex bytes of a jpeg file, find end of header, image size, and extract any text comment
# (JPEG = Joint Photographic Experts Group)
# tested with Python24    vegaseat    21sep2005

try:
    # the sample jpeg file is an "all blue 80x80 200dpi image, saved at a quality of 90"
    # with the quoted comment added
    imageFile = 'channel.jpg'
    data = open(imageFile, "rb").read()
except IOError:
    print "Image file %s not found" % imageFile
    raise SystemExit

# initialize empty list
hexList = []
for ch in data:
    # make a hex byte
    byt = "%02X" % ord(ch)
    hexList.append(byt)

#print hexList  # test

print

print "hex dump of a 80x80 200dpi all blue jpeg file:"
print "(the first two bytes FF and D8 mark a jpeg file)"
print "(index 6,7,8,9 spells out the subtype JFIF)"
k = 0
for byt in hexList:
    # add spacer every 8 bytes
    if k % 8 == 0:
        print "  ",
    # new line every 16 bytes
    if k % 16 == 0:
        print
    print byt,
    k += 1
    
print
print "-"*50

# the header goes from FF D8 to the first FF C4 marker
for k in range(len(hexList)-1):
    if hexList[k] == 'FF' and hexList[k+1] == 'C4':
        print "end of header at index %d (%s)" % (k, hex(k))
        break

# find pixel width and height of image
# located at offset 5,6 (highbyte,lowbyte) and 7,8 after FF C0 or FF C2 marker
for k in range(len(hexList)-1):
    if hexList[k] == 'FF' and (hexList[k+1] == 'C0' or hexList[k+1] == 'C2'):
        #print k, hex(k)  # test
        height = int(hexList[k+5],16)*256 + int(hexList[k+6],16)
        width  = int(hexList[k+7],16)*256 + int(hexList[k+8],16)
        print "width = %d  height = %d pixels" % (width, height)

# find any comment inserted into the jpeg file
# marker is FF FE followed by the highbyte/lowbyte of comment length, then comment text
comment = ""
for k in range(len(hexList)-1):
    if hexList[k] == 'FF' and hexList[k+1] == 'FE':
        #print k, hex(k)  # test
        length = int(hexList[k+2],16)*256 + int(hexList[k+3],16)
        #print length  # test
        for m in range(length-3):
            comment = comment + chr(int(hexList[k + m + 4],16))
            #print chr(int(hexList[k + m + 4],16)),  # test
            #print hexList[k + m + 4],  # test
            
if len(comment) > 0:
    print comment
else:
    print "No comment"

#import pickle
#reader = pickle.load(open('banner.p', 'rb'))
#for line in reader :
  #output = ""
  #for group in line :
    #output = output + group[0]*group[1]
  #print output
##print reader#.readline()


#import urllib
#import re

#data = re.compile('\d{3,5}')

#opener = urllib.FancyURLopener({})

#url = "http://www.pythonchallenge.com/pc/def/linkedlist.php?nothing="
#param = "46059"

#while True :
  #f = opener.open(url+param)
  #string = f.read()
  #print param,string
  #number = data.findall(string)
  #if len(number)>0:
    #param=number[len(number)-1]
  #else :
    #break
  
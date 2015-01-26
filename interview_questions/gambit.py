import urllib2
import re
import cookielib

cj = cookielib.CookieJar()

opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj), urllib2.HTTPSHandler(debuglevel=1))

url ="http://quiz.gambitresearch.com/"
r = opener.open(url).read()

regex1 = re.compile("[0-9]+\s\S\s[0-9]+\s\S\s[0-9]+")
s = regex1.findall(r)

regex2 = re.compile("[0-9]{3}")
t = regex2.findall(r)
b = int(t[0])

s = s[0].split(' ')
s[0] = str((int(s[0])+b)%1000)
s[2] = str((int(s[2])+b)%1000)
s[4] = str((int(s[4])+b)%1000)
s = ' '.join(s)
print s
a = eval(s)

url ="http://quiz.gambitresearch.com/job/%s" % a
print url
r = opener.open(url)

print r.read()

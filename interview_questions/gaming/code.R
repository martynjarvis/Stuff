exient = read.csv("C:/Users/Martyn/Projects/exient/ExientDataSet.csv",as.is=TRUE)

# lets looks at the data before we start
head(exient)
summary(exient)

# convert timestamp string to datetime object
exient$Timestamp <- strptime(exient$Timestamp, "%b %d, %Y %I:%M %p")
hist(exient$Timestamp,breaks = 100) # gaps in data... intersting 

# 1. Using the “dim” command (or alternatively, “nrow” and “ncol”), write down the number of rows and columns in the data set.
dim(exient)

# 2. What dates does the data set span? (Note: the data is in chronological order.)
head(exient$Timestamp)
tail(exient$Timestamp)

# 3. As shown on the first line of the data, the player with UserID 908844CB-6B9C-4499-B9F2-87CCB43042CD is using an Apple iPad Mini. 
# What device is the player with UserID AAF9C549-6970-4536-9B67-03D2775F1A01 using? 
exient[exient$UserID=='AAF9C549-6970-4536-9B67-03D2775F1A01','Device']

# 4. How many times was level ‘00-00-Fruit-00’ played? (The answer is a two-digit number ending in ‘5’.) 
# What proportion of these races had the outcome ‘beatLevel’?
a4 <- exient[exient$Level=='00-00-Fruit-00','Outcome']
length(a4)
table(a4)

# 5. What command(s) could you use to check that the lowest and highest times to finish a race are 
# approximately are 1.02 and 5970 seconds?
max(exient$RaceTime)
min(exient$RaceTime)

# 6. The ‘TotalRaces’ column is in the range of 1 to 506. 
# Some integers within this range do not appear in the dataset (e.g. 450, 470, 501). 
# In fact, there are 26 such integers between 1 and 506. What is the sum of these 26 integers?
a6a <- as.data.frame(tabulate(exient$TotalRaces))
a6b <- which(a6a[1]==0)
a6b
length(a6b)
sum(a6b)

# 7. Write code to identify the set of races that the player with UID AAF9C549-6970-4536-9B67-03D2775F1A01 
# played in ‘Challenge’ mode (28 entries),
#  and calculate the mean time they took to complete a race within this subset of data.
a7.selection <- exient$UserID=='AAF9C549-6970-4536-9B67-03D2775F1A01' & exient$RaceType=='Challenge' 
a7.a <- exient[a7.selection,c('Outcome','RaceTime')]
nrow(a7.a)
summary(a7.a$RaceTime)
mean(a7.a$RaceTime)

# 8. Generate a histogram of the time taken to complete a race, and comment on the plot. 
# Determine the value T such that 95% of race times are less than T.
% NOTE TODO what defines a completed race?
hist(exient$RaceTime)
summary(exient$RaceTime)
a8.selection <- exient$RaceTime < 150 # remove outliers
hist(exient$RaceTime[a8.selection], main="", sub="",xlab="Time taken to complete race (s)", ylab="Frequency")
quantile(exient$RaceTime,  probs = c(0.95))

# 9. The histogram in Figure 1 has been generated from the dataset and provides information 
# on an important metric in mobile games. 
# Its axes have been hidden. What does the plot represent? Write R code to reproduce the plot.
hist(exient$TimeSinceInstall,breaks=1000,xlim = c(0,300000),main="", sub="",xlab="Time since install (s)", ylab="Frequency")

# 10. For which version of the game were most races logged (approximately 69% of the entries in the full data set)?
table(exient$Version)

# 11.In the version identified in the question above, 
# how many entries were made by players who had spent more than 10 hours playing the game?
# (The answer is a 3-digit number ending in ‘8’).
a11.selection <- exient$Version==183806 & exient$TimeInGame>(60*60*10) 
length(exient$Timestamp[a11.selection])

# For questions 12 and 13 below, please focus attention on the subset of data obtained in question 11 above.

# 12.How many players were there in this subset of the data? 
# Which two players might we wish to discard, and why? 
# Can you investigate further and suggest why each of these oddities has arisen?
table(exient$UserID[a11.selection])

# Lets investigate further.
# First, order by TimeInGame rather than log timestamp
exient2 <- exient [with(exient , order(TimeInGame)), ]
head(exient2)

# now we can look at playing habits chronologically

exient2[exient2$UserID=='0FDABD6B-C5E0-487D-87D8-255EC2ED307B',c('Version','TimeInGame','Timestamp')] 
# jumps from 92k to 150k?

exient2[exient2$UserID=='3C0CE2B2-72D4-4B43-98C7-B04747E95F32',c('Version','TimeInGame','Timestamp')] 
# jumps from 23k to 65k?

exient2[exient2$UserID=='46FC3345-5D33-4FD6-9444-EFECE98AC32C',c('Version','TimeInGame','Timestamp')]
# different versions? check device id
# jumps from 17k to 56k

exient2[exient2$UserID=='7E964A54-996B-4F25-82AA-0B6D20438C02',c('Version','TimeInGame','Timestamp')]
# different versions

exient2[exient2$UserID=='908844CB-6B9C-4499-B9F2-87CCB43042CD',c('Version','TimeInGame','Timestamp')]
# jumps from 5k to 62k 
# then 80k to 137k

exient2[exient2$UserID=='AE140C77-2E9A-4ABE-B298-44D223FBB0CA',c('Version','TimeInGame','Timestamp')]
# jumps 24k to 65k
# then 65k to 85k 

exient2[exient2$UserID=='B8E90A1D-6DA6-43B4-A035-8363D05F4495',c('Version','TimeInGame','Timestamp')]
# jumps 16k to 73k
# then 95k to 152k

exient2[exient2$UserID=='C327894B-3A7A-4469-AF77-FB60921C56A2',c('Version','TimeInGame','Timestamp')]
#jumps 24k to 82k

# Jumps can be explained by missing data.
# Different versions and overlapping data could be different installations

# 13.Identify the strongest and weakest players based on the proportion of races in which 
# they had an outcome of ‘beatLevel’. 
# How confident are you in this assessment? Explain your answer briefly.
beat.level <- exient$Version==183806 & exient$TimeInGame>60*60*10 & exient$Outcome == "beatLevel"
win.ratio = table(exient$UserID[beat.level])/ table(exient$UserID[a11.selection])
win.ratio

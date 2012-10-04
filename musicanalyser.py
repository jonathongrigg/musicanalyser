# Copyright (c) Jonathon Grigg 2012
#
# Simple Python program that scrapes the top 100 songs of the US iTunes chart
# and saves the resulting information (songs and beginning character frequency)
# in a dated text file that the user can then later see what has changed
#
# A lot more could potentially be done with this information, but for my
# purpose of discovering what was the most common song start letter, it will do

import collections
import datetime
import string
import urllib2

def getChartSource():
	itunesChartUrl = 'https://www.apple.com/itunes/charts/songs/'
	site = urllib2.urlopen(itunesChartUrl)
	pageSource = site.read()
	site.close()
	chartSourceBegin = pageSource.find('<div id="grid">')
	chartSourceEnd = pageSource.find('</div>', chartSourceBegin)
	return pageSource[chartSourceBegin:chartSourceEnd]

def findSongTitle(source, position):
	beginString = '<strong>' + str(position) + '.</strong>'
	endString = '<strong>' + str(position + 1) + '.</strong>'
	positionString = source[source.find(beginString):source.find(endString)]
	titleEnd = positionString[:positionString.find('</a></h3><h4>')]
	return titleEnd[titleEnd.rfind('">') + 2:]

chartSource = getChartSource()
characterFrequency = collections.defaultdict(int)
top100 = dict.fromkeys(range(1, 101))
time = datetime.datetime.now().strftime('%Y-%m-%d')

for i in range(1, 101):
	title = findSongTitle(chartSource, i)
	top100[i] = title
	characterFrequency[title.lower()[0]] += 1

# Let's save this information to a dated file for future reference
saveFile = open('results-%s' % (time), "w")

saveFile.write('Top 100 Songs for %s:\n' % (time))
for position in top100:
	print '%i: %s' % (position, top100[position])
	saveFile.write('%i: %s \n' % (position, top100[position]))

saveFile.write('\nCharacter frequency:\n')
for character in string.ascii_lowercase:
	print '%s: %i' % (character, characterFrequency[character])
	saveFile.write('%s: %i \n' % (character, characterFrequency[character]))

saveFile.close()
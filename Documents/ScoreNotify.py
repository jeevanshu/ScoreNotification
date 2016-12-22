from bs4 import BeautifulSoup
import os
import sys
import time
import requests
import subprocess as SE

cricinfoRss='http://static.cricinfo.com/rss/livescores.xml'

def getURLtext(url):
	retryCount=5
	r=requests.get(url)
	while r.status_code is not 200:
		if retryCount ==0:
			print 'Check your internet connection'
			sys.exit(1)
		retrycount=-1
		print 'Request failed,trying to connect...'
		time.sleep(3)
		r=requests.get(url)
	data=r.text
	soup=BeautifulSoup(data,'lxml')
	return soup

def findMatches():
	global allMatches
	liveMatches= getURLtext(cricinfoRss)
	allMatches=liveMatches.find_all('description')

	if len(allMatches)>1:
		askUser()

def askUser():
	global choice
	for index,game in enumerate(allMatches[1:],1):
		print '%d.'%index ,str(game.string)

	choice=int(input('Choose preferred match:\n'))

	while True:
		if choice in range(1,index+1):
			break
		choice=int(input('Invalid Choice.Enter your choice:'))


def guiNotify(message):
	if os.path.isfile('/etc/lsb-release'):
		SE.Popen(['notify-send',message])

def getScore():
	scoreURL=str(allMatches[choice].find_next_sibling().string)
	mainPage=getURLtext(scoreURL)
	score=str(mainPage.title.string).split('|')[0]
	inningsReq= mainPage.find('div',{'class':'innings-requirement'}).string.strip()
	message=score+inningsReq
	guiNotify(message)
	print message

try:
	findMatches()
	getScore()
	notify=raw_input('Would you like to get notification?\n Enter(y|n)\n')
	if notify =='y':
		min=int(input('After how many minutes would you like to be notified\n Enter minutes:'))
		while True:
			time.sleep(min*60)
			getScore()
except KeyboardInterrupt:
	print 'Ending the task:keyboard interrupted'
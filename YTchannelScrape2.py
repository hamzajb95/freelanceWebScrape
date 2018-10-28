#This code has a throughput 1.72 times the original
import bs4 as bs
import http
import re
import sys
import urllib.request
from urllib.request import Request
import unicodecsv as csv
import time
import threading
from queue import Queue
import math

testurl = 'https://www.channelcrawler.com/eng/results/136614/page:1'
q = Queue()
soupLock = threading.Lock()
combDataLock = threading.Lock()
threadList = []

def main():
  print('Program Started')
  startTime = time.time()
  urls = getPages(make_soup(testurl))
  for u in urls:
    print(u)
    t = threading.Thread(target= threader,args=(u,))
    #t.daemon = True
    t.start()
    threadList.append(t)

  for b in threadList:
    b.join()

  print('Runtime is: '+str(time.time()-startTime))

def getPages(soup):
  PageList = []
  body=soup.body
  for h3 in body.findAll('h3',{"class":"results-title"}):
    if h3 is not None:
      channels = h3.text.strip()
      channels = channels.replace(',','')
      match = (re.search(r'\d+',channels))
      channelsInt = int(match.group())
  NumPages = math.floor(channelsInt/20)
  for i in range(NumPages):
    PageList.append('https://www.channelcrawler.com/eng/results/136614/page:'+str(i+1))
  return PageList

def threader(url):
  #with soupLock:
  mySoup = make_soup(url)
  #getNumPages(mySoup)
  #for inst in range(20):
  theList = combineData(getTitle(mySoup),getData(mySoup))
  writeRecords(theList)
     
     
def make_soup(theUrl):
  try:
    wp = urllib.request.urlopen(theUrl).read()
    mySoup = bs.BeautifulSoup(wp,'html5lib')
    print('soup created')
    return mySoup
  except (http.client.IncompleteRead) as e:
    wp = e.partial
    print('partial throw')
  except:
    mySoup = make_soup(testurl)
    return mySoup

def getTitle(soup):
  listTitle = []
  listId = []
  body = soup.body
  for div in body.findAll('div',{"class": "channel col-xs-12 col-sm-4 col-lg-3"}):
    if div is not None:
      for h4 in div.findAll('h4'):
        if h4 is not None:
          for a in h4.findAll('a'):
            if a is not None:
              link = a.get('href') 
              listId.append(link)             
              title = a.get('title')
              listTitle.append(title)
  return (listTitle,listId)            
              

def getData(soup):
    listSubs = []
    listVids = []
    listDates = []

    body = soup.body
    for div in body.findAll('div',{"class": "channel col-xs-12 col-sm-4 col-lg-3"}):
      if div is not None:
        for p in div.findAll('p'):
          if p is not None:
            for small in p.findAll('small'):              
              rawText = small.text
              
              subMatch = re.search(r'([\d,]+)\sSubscribers',rawText)
              if subMatch:
                  subs = subMatch.group(1)
                  listSubs.append(subs)
                  
              
              vidMatch = re.search(r'(\d+)\sVideos',rawText)
              if vidMatch:
                  vids = vidMatch.group(1)                  
                  listVids.append(vids)
                  

              
              dateMatch = re.search(r'Join\sDate:\s(\d+.\d+.\d+)',rawText)
              if dateMatch:
                  date = dateMatch.group(1)
                  listDates.append(date)
    
    return (listSubs,listVids,listDates)

def combineData(tuple1,tuple2):
  cList = []              
  titleList = tuple1[0]
  idList = tuple1[1]
  subsList = tuple2[0]
  vidList = tuple2[1]
  dateList = tuple2[2]
  for i in range(20):
    record = []
    try:
      record.append(titleList[i].encode("utf-8"))
      record.append(subsList[i].encode("utf-8"))
      record.append(vidList[i].encode("utf-8"))
      record.append(dateList[i].encode("utf-8"))
      record.append(idList[i].encode("utf-8"))
    except(IndexError):
      print("Index Errors occurs whilst combining record")
    cList.append(record)
  return cList   

def getNextPage(soup):
  body = soup.body
  for li in body.findAll('li',{"class": "next"}):
    if li is not None:
      for a in li.findAll('a'):
        nextLink = 'https://www.channelcrawler.com'+a.get('href')
        return nextLink

def writeRecords(cList):
  
  with open('ChannelList.csv','ab') as fw:
    file = csv.writer(fw,delimiter=',')
    file.writerows(cList)
  
if __name__ == '__main__':
  main()



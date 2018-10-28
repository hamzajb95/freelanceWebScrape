import bs4 as bs
import http
import re
import sys
import urllib.request
from urllib.request import Request
import unicodecsv as csv

testurl = 'https://www.channelcrawler.com/eng/results/136614/page:1'

def main():
    x = 'https://www.channelcrawler.com/eng/results/136614/page:1'
    for i in range(10):
      mySoup = make_soup(x)
      theList = combineData(getTitle(mySoup),getData(mySoup))
      writeRecords(theList)
      x = getNextPage(mySoup)
    input()
    

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
    
    record.append(titleList[i])
    
    record.append(subsList[i])
    record.append(vidList[i])
    record.append(dateList[i])
    record.append(idList[i])
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


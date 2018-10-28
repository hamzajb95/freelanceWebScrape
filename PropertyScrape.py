import bs4 as bs
import http
import re
import sys
import urllib.request
from urllib.request import Request
import csv

testurl = 'https://condo.singaporeexpats.com/1/singapore-property-all/rent'
counterX = 0

def main():
  url = 'https://condo.singaporeexpats.com/1/singapore-property-all/rent'
  while url is not None:
    mySoup = make_soup(url)
    theData = combineData(getTitle(mySoup),getSize(mySoup),getPrice(mySoup),getNum(mySoup),getLink(mySoup))
    writeRecords(theData)
    url = getNextPage(mySoup)
    print(url)
  print('scraping complete')
  input("Press enter to exit ;)")


def make_soup(theUrl):
  try:
    wp = urllib.request.urlopen(theUrl).read()
    mySoup = bs.BeautifulSoup(wp,'lxml')
    print('soup created')
    return mySoup
  except (http.client.IncompleteRead) as e:
    wp = e.partial
    print('partial throw')
  except:
    mySoup = make_soup(testurl)
    return mySoup 

def getTitle(soup):
  titleList = []
  body = soup.body
  for div in body.findAll('div',{"class": "smtitle"}):
    data = div.text
    titleList.append(data)
  return titleList

def getSize(soup):
  sizeList = []
  body = soup.body
  for div in body.findAll('div',{"class":"smcol1"}):
    if div is not None:
      data = div.text
      matchSize = re.search(r'\d+\s\w+\s\/\s\d+.\d+',data) 
      if matchSize:
        size = matchSize.group()
      else:
        size = 'no match'
      sizeList.append(size)
  return sizeList

def getPrice(soup):
  priceList =[]
  body = soup.body
  for div in body.findAll('div',{"class":"smprice"}):
    data = div.text
    priceList.append(data)
  return priceList

def getNum(soup): 
  numList =[]
  body = soup.body
  for div in body.findAll('div',{"class":"smcol1"}):
    if div is not None:
      data = div.text
      matchNum = re.search(r'\+\d+\s\d+',data)
      if matchNum:
        number = matchNum.group()
      else:
        number = 'no match'
    numList.append(number)
  return numList

def getLink(soup):
  linkList = []
  body = soup.body
  for div in body.findAll('div',{"class": "smtitle"}):
    for a in div.findAll('a'):
        thisUrl = a.get('href')
        linkList.append(thisUrl)
  return linkList

def combineData(title,size,price,num,link):
  cList = []
  for i in range(30):
    record = []
    record.append(title[i])
    record.append(size[i])
    record.append(price[i])
    record.append(num[i])
    record.append(link[i])
    cList.append(record)
  return cList


def writeRecords(cList):
  
  with open('CondoProperties.csv','a',newline='') as fw:
    file = csv.writer(fw,delimiter=',')
    data = cList
    file.writerows(data)
    global counterX
    counterX +=1
    print('INFO: '+counterX + 'pages have been scraped!!!!!')

def getNextPage(soup):
  body = soup.body
  for li in body.findAll('li',{'class':'next'}):
    if li is not None:
      for a in li.findAll('a'):
        if a is not None:
          html = 'https://condo.singaporeexpats.com' + a.get('href')
          return html
        else: return 'zzz'  
    else: return 'zzz'


if __name__ == '__main__':
  main()
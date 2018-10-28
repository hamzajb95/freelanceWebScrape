import bs4 as bs
import urllib.request
from urllib.request import Request
import re
import unicodecsv as csv
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException
import threading
import concurrent.futures as cf


isModal = True

def scripter(driver,urlPath,destPath,isModal):  
  path = r'C:\\Users\Hamza JB\Documents\Python\Camping Sites for Max'+urlPath
  urlx = file_read(path)
  number = 0
  for url in urlx:
    #url = urlx[0]
    print(url)
    records,urls,recordx = [],[],[]
    #soup = make_soup(url)
    urls.append(url)
    try:
      profhtml = selSoup(driver,url,"ctl00_ctl00_cphMain_main_btn_TabPro")
      conhtml = selSoup(driver,url,"ctl00_ctl00_cphMain_main_btn_TabCon")
      title = getTitle(profhtml)
      website = getWebsite(profhtml)
      contacts = getContacts(conhtml)
      location = getLocation(conhtml)
      sD = shortDescription(profhtml)
      rat = getRating(profhtml)
      pTb1 = getTableData(profhtml,"jq-campsite-profile","d336 list21")
      TB1 = sortPTb1(pTb1)
      #print(TB1)
      pTb2 = getTableData(profhtml,"jq-campsite-profile","d336 list22")
      TB2 = sortPtb2(pTb2)
      prices = getPrices(profhtml)
      #print(prices)
      infra = getInfra(profhtml)
      records = urls + title + website + contacts + location + sD + rat + TB1 + TB2 + prices + infra
      print((number))
      print(len(records))
      number += 1
      recordx.append(records)
      writeRecords(recordx,destPath)
    except(TimeoutException):
      pass
        
def getTitle(soup):
  tit=[]
  body = soup.body
  for div in body.findAll('div',class_='d200'):
    for h1 in div.findAll('h1',class_='d20'):
      name = h1.text.strip()
      tit.append(name)
      return tit

def getWebsite(soup):  
  sit=[]
  website = ''
  body = soup.body
  for a in body.findAll('a',id='ctl00_ctl00_cphMain_main_ucActionLinkBlock_hlHomepageLeft'):      
    website = a.get('href')           
  #website = checkWebsite(website)
  sit.append(website)
  return sit  
  
def checkWebsite(website):
  if type(website) == type(None):
    return 'no information'
  else: return website

def shortDescription(soup):
  sDl =[]
  body = soup.body
  for div in body.findAll('div',class_="d23"):
    sD = div.text.strip()
  if sD is not "":
    sDl.append(sD)
  else:
    sDl.append('no information')
  return sDl

def getRating(soup):
  rtng = ''
  rt = []
  body = soup.body
  for span in body.findAll('span', class_="rating rating-stars-green large"):
    rtng = span.text.strip()  
  rtng = checkWebsite(rtng)   
  rt.append(rtng)
  return rt

def getLocation(soup):
  body = soup.body  
  locLst=[]
  for span in body.findAll('span',itemprop = 'streetAddress'):
    locLst.append(span.text.strip())
  if len(locLst) == 0:
    locLst.append('no information')
    
  for span in body.findAll('span',itemprop = 'addressLocality'):
    locLst.append(span.text.strip())
  if len(locLst) == 1:
    locLst.append('no information')
    
  for span in body.findAll('span',itemprop = 'addressCountry'):
    locLst.append(span.text.strip())
  if len(locLst) == 2:
    locLst.append('no information')
  return locLst

def getContacts(soup):
  body = soup.body  
  conLst=[]

  for span in body.findAll('span',class_ = 'd3843'):
    conLst.append(span.text.strip())
  if len(conLst) == 0:
    conLst.append('no info')  
  for span in body.findAll('span',class_= 'd3844'):
    conLst.append(span.text.strip())
  if len(conLst) == 1:
    conLst.append('no info')
  return conLst

def getPrices(soup):
  priceList = []
  body = soup.body
  for p in body.findAll('p',class_='d339'):
    for span in p.findAll('span'):
      priceList.append(span.text.strip())
      break
  for p in body.findAll('p',class_='d340'):
    for span in p.findAll('span'):
      priceList.append(span.text.strip())
      break
  return priceList

def getTableData(soup,divID,ulClass):
  x=''
  body = soup.body
  for div in body.findAll('div',id=divID):
    for ul in div.findAll('ul', class_=ulClass):
      for li in ul.findAll('li'):     
        for span in li.findAll('span'):
          if span is not None:
            x = x + span.text.strip()+'\n'
        x = x+'------next LI------'+'\n'    
      spanText = cleanString(x)
      #for i in spanText: print(i)   
      return spanText
    
def sortPTb1(data):
  temp = []
  dogCount = 0
  counter = 0
  x = []
  weGood = True
  for text in data:
    if counter == 0 and weGood:
      opMatch = re.search(r'(\d+.\d+.\s-\s\d+.\d+.)',text)
      if opMatch:
        x.append(opMatch.group(1))
        try:
          x.append(opMatch.group(2))
        except (IndexError):
          x.append('NA/-') 
      else:
        x.append('N/A-')
        x.append('N/A-')         
      counter += 1
      weGood = False
    elif counter == 1 and weGood:      
      temp.append(text)
      dogCount += 1      
      if dogCount == 15:
        x.append(temp[0])
        x.append(temp[2])
        x.append(temp[5])        
        counter +=1
        weGood = False
    elif counter == 2 and weGood:
      x.append(text)
      counter +=1
      weGood = False
    elif counter == 3 and weGood:      
      x.append(text)
      counter +=1
      weGood = False
    elif counter == 4 and weGood:      
      x.append(text)
      counter +=1
      weGood = False
    elif counter == 5 and weGood:      
      x.append(text)
      counter +=1
      weGood = False
    elif counter == 6 and weGood:
      x.append(text)
      counter +=1
      weGood = False
    elif counter == 7 and weGood:
      x.append(text)      
      counter +=1
      weGood = False
    elif counter == 8 and weGood:
      x.append(text)
      counter +=1
      weGood = False 
    if text == '------next LI------':
      weGood = True
  
  return x
  
def sortPtb2(data):
  tbList=[]
  counter = 0
  weGood = True
  for text in data:
    if counter == 0 and weGood:
      tbList.append(text)
      counter+=1
      weGood = False
    elif counter == 1 and weGood:
      tbList.append(text)
      counter+=1
      weGood = False
    elif counter == 2 and weGood:
      tbList.append(text)
      counter+=1
      weGood = False
    elif counter == 3 and weGood:
      tbList.append(text)
      counter+=1
      weGood = False
    elif counter == 4 and weGood:
      tbList.append(text)      
      counter+=1
      weGood = False
    elif counter == 5 and weGood:
      tbList.append(text)
      counter+=1
      weGood = False
    elif counter == 6 and weGood:
      tbList.append(text)
      counter+=1
      weGood = False
    elif counter == 7 and weGood:
      tbList.append(text)
      counter+=1
      weGood = False
    if text == '------next LI------':
      weGood = True
  #print(numPitches+' , '+tourPitches+' , '+dtPitches+' , '+sPitchYP+' , '+carFree+
  #    ' , ' +carPermit+' , '+mHSpace+' , '+osoCaravan)
  return tbList

def cleanString(text):  
  words = text.split("\n")
  for word in words: word.strip()
  words = list(filter(None,words))
  return words

def getInfra2(data, liID):
  body = data.body
  for li in body.findAll('li',id= liID):
    info = ''
    x = li.get('class')
    check = str(x)
    if check == "['yes']":
      info = 'yes'
    elif check == "['no']":
      info = 'no'
    else:
      info = 'no information' 
  return info
    
def getInfra(data):
  infraList = []
  power = getInfra2(data,'liStrom')
  infraList.append(power)      
  water = getInfra2(data,'liWaterConnectionAtPitch')
  infraList.append(water)  
  waste = getInfra2(data,'liSewageHookUpAtPitch')
  infraList.append(waste)  
  gas = getInfra2(data,'liGasConnectionAtPitch')
  infraList.append(gas)  
  tv = getInfra2(data,'liTVConnectionAtPitch')
  infraList.append(tv)    
  gasExch = getInfra2(data,'liGasBottleExchange')
  infraList.append(gasExch)  
  wifi = getInfra2(data,'liWlan')
  infraList.append(wifi)
  intTerminal = getInfra2(data,'liInetTerm')
  infraList.append(intTerminal)  
  safety = getInfra2(data,'liLockers')
  infraList.append(safety)  
  lounge = getInfra2(data,'liLounge')
  infraList.append(lounge)  
  dryingRoom = getInfra2(data,'liDryingRoom')
  infraList.append(dryingRoom)  
  cookingRoom = getInfra2(data,'liCookingFacilities')
  infraList.append(cookingRoom)  
  dogShower = getInfra2(data,'liDogShowers')
  infraList.append(dogShower)  
  dogLawn = getInfra2(data,'liDogMeadow')
  infraList.append(dogLawn)  
  dogBath = getInfra2(data,'liDogBathing')
  infraList.append(dogBath)  
  wasteCar = getInfra2(data,'liVerEntMob')
  infraList.append(wasteCar)  
  food = getInfra2(data,'liLebensm')
  infraList.append(food)  
  Bread = getInfra2(data,'liBreadAtCampsite')
  infraList.append(Bread)  
  snacks = getInfra2(data,'liImbiss')
  infraList.append(snacks)  
  restrnt = getInfra2(data,'liRestaurant')
  infraList.append(restrnt)
  whelChr = getInfra2(data,'liWheelchairRamps')
  infraList.append(whelChr)  
  pathPaved = getInfra2(data,'liMostWaysPaved')
  infraList.append(pathPaved)  
  bonfire = getInfra2(data,'liCentralBonfireArea')
  infraList.append(bonfire)  
  campfire = getInfra2(data,'liCampfireAtPitchAllowed')
  infraList.append(campfire)  
  firewood = getInfra2(data,'liFirewood')
  infraList.append(firewood)    
  grill = getInfra2(data,'liCharcoalGrillAllowed')
  infraList.append(grill)  
  tables = getInfra2(data,'liTablesAndBenches')
  infraList.append(tables)
  babyChange = getInfra2(data,'liBabyChange')
  infraList.append(babyChange)
  WC = getInfra2(data,'liWashingCabins')
  infraList.append(WC)
  rentBR = getInfra2(data,'liRentableBathroomCount')
  infraList.append(rentBR) 
  handicapWC = getInfra2(data,'liSaniHandi')
  infraList.append(handicapWC)
  washingMch = getInfra2(data,'liWashingMachines')
  infraList.append(washingMch)
  tDryer = getInfra2(data,'liLaundryDriers')
  infraList.append(tDryer)
  playGrd = getInfra2(data,'liPlaygrd')
  infraList.append(playGrd)
  indrPlay = getInfra2(data,'liIndoorGamingPossibilities')
  infraList.append(indrPlay)
  petZoo = getInfra2(data,'liPettingZoo')
  infraList.append(petZoo)
  childEnt = getInfra2(data,'liKidsAnim')
  infraList.append(childEnt)
  swim = getInfra2(data,'liSwimNat')
  infraList.append(swim)
  beach = getInfra2(data,'liSandBeach')
  infraList.append(beach)
  handicapWtr = getInfra2(data,'liHandicappedAccessibleWaterEntrance')
  infraList.append(handicapWtr)
  nudist = getInfra2(data,'liNudistBeach')
  infraList.append(nudist)
  poolOut = getInfra2(data,'liPoolOut')
  infraList.append(poolOut)
  wtrSlide = getInfra2(data,'liWaterSlide')
  infraList.append(wtrSlide)
  poolIn = getInfra2(data,'liPoolIn')
  infraList.append(poolIn)
  hotBath = getInfra2(data,'liThermalbad')
  infraList.append(hotBath)
  sauna = getInfra2(data,'liSauna')
  infraList.append(sauna)
  tennis = getInfra2(data,'liTennis')
  infraList.append(tennis)
  tT = getInfra2(data,'liTableTennis')
  infraList.append(tT)
  vBall = getInfra2(data,'liVolleyball')
  infraList.append(vBall)
  miniGolf = getInfra2(data,'liMiniGolf')
  infraList.append(miniGolf)
  golf = getInfra2(data,'liGolf')
  infraList.append(golf)
  sailSurf = getInfra2(data,'liSailSurf')
  infraList.append(sailSurf)
  boatHire = getInfra2(data,'liBoatHire')
  infraList.append(boatHire)
  slipWay = getInfra2(data,'liSlipway')
  infraList.append(slipWay)
  bikeRent = getInfra2(data,'liBikeRent')
  infraList.append(bikeRent)
  riding = getInfra2(data,'liHorsebackRiding')
  infraList.append(riding)
  fishing = getInfra2(data,'liFishing')
  infraList.append(fishing)
  divingSt = getInfra2(data,'liDivingStation')
  infraList.append(divingSt)
  skiLift = getInfra2(data,'liSkilift')
  infraList.append(skiLift)
  skiing = getInfra2(data,'liCrossCountrySkiing')
  infraList.append(skiing)
  tents = getInfra2(data,'liTents')
  infraList.append(tents)
  rentCab = getInfra2(data,'liRentCabins')
  infraList.append(rentCab)
  caravans = getInfra2(data,'liCaravan')
  infraList.append(caravans)
  mobHome = getInfra2(data,'liMobileBungalows')
  infraList.append(mobHome)
  apparts = getInfra2(data,'liApartments')
  infraList.append(apparts)
  dAIRA = getInfra2(data,'liDogsAllowedInRentedAccomodation')
  infraList.append(dAIRA)

  return infraList

def file_read(fname):
    with open(fname) as f:
    #Content_list is the list that contains the read lines.     
      content_list = f.readlines()
    return content_list

def selSoup(driver,theUrl,btnID):
  try:
    driver.get(theUrl)
  except(Exception):
    driver.get(theUrl)
  element = WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.ID, btnID)))
  driver.execute_script("arguments[0].click();", element)
  global isModal
  if isModal: 
    try:
      modal = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "mc-closeModal")))
      driver.execute_script("arguments[0].click();", modal)
      isModal = False
    except(Exception): print('modal not found')      
  html = driver.execute_script("return document.documentElement.outerHTML")
  mySoup = bs.BeautifulSoup(html,"lxml")
  
  return mySoup

def writeRecords(cList,destPath):
  
  with open(r'C:\\Users\Hamza JB\Documents\Python\Camping Sites for Max'+destPath,'ab') as fw:
    file = csv.writer(fw,delimiter=',')
    file.writerows(cList)
    



import bs4 as bs
import urllib.request
from urllib.request import Request
import re
from random import randint
import time
import unicodecsv as csv
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile

isModal = True

def main():  
  path = r'C:\Users\Hamza JB\Anaconda3\envs\env_scrape\CampingScrape\errorList2.txt'
  urlx = file_read(path)
  driver = webdriver.Firefox()
  number = 1
  for url in urlx:
    records,urls,recordx = [],[],[]
    if url is not '\n':      
      urls.append(url)
      try:
        conhtml = selSoup(driver,url,"ctl00_ctl00_cphMain_main_btn_TabCon")
        contacts = getContacts(conhtml)
        location = getLocation(conhtml)
        records = urls + contacts + location
        print("recN:"+ str(number))
        print("The length is"+ str(len(records)))
        number += 1
        recordx.append(records)
        print(recordx)
      except(TimeoutException):
        pass
    else:
      records.append('This is a break')
      recordx.append(records)
      print("empty line")
    writeRecords(recordx)  
    print()  
    
         
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

  #survey = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "_hj-f5b2a1eb-9b07_transition")))
  #driver.execute_script("arguments[0].click();", survey)
  time.sleep(randint(3,4))
  html = driver.execute_script("return document.documentElement.outerHTML")
  mySoup = bs.BeautifulSoup(html,"lxml")

  return mySoup

def writeRecords(cList):  
  with open(r'C:\Users\Hamza JB\Anaconda3\envs\env_scrape\CampingScrape\CampsitesError.csv','ab') as fw:
    file = csv.writer(fw,delimiter=',')
    file.writerows(cList)

def writeFile(data):
  path = r'C:\\Users\Hamza JB\Documents\Python\Camping Sites for Max\soupList.txt'
  file = open(path,'w')
  file.write(data)
  file.close()




if __name__ == "__main__":
    main()


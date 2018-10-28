import bs4 as bs
import http
import re
import sys
import urllib.request
from urllib.request import Request
import requests
import csv
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

def main():
  LinkList = []
  testurl = 'https://en.camping.info/campsites'
  mySoup= make_soup(testurl)
  #z = getLinks(s)
  #for link in z:
  #  LinkList.append(link)
  driver = webdriver.Firefox()
  driver.get(testurl)
  x = driver.find_element_by_class_name('mc-closeModal')
  x.click()
  for i in range(1899):
    z = getLinks(mySoup)
    for link in z:
      LinkList.append(link)
    writeRecords(z)
    driver.implicitly_wait(10)
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "ctl00_ctl00_cphMain_main_ucSearchResult_btn_NextPage")))
    driver.execute_script("arguments[0].click();", element)
    html = driver.execute_script("return document.documentElement.outerHTML")
    mySoup = bs.BeautifulSoup(html,"html.parser")
    
  
  print(len(LinkList))
  print(LinkList[11])
  print(LinkList[119])
  
  

  
  


def make_soup(theUrl):
  wp = requests.get(theUrl)
  mySoup = bs.BeautifulSoup(wp.content,'lxml')
  print('soup created')
  return mySoup
    

def getLinks(soup):
  list = []  
  for a in soup.findAll('a',class_ = 'fn org item'):
    x = 'https://en.camping.info'+a.get('href')
    list.append(x)
  return list

def writeRecords(cList):  
  with open(r'C:\\Users\Hamza JB\Documents\Python\Camping Sites for Max\your_file.txt', 'a') as f:
    for item in cList:
        f.write("%s\n" % item)
    
    

if __name__ == '__main__':
    main()
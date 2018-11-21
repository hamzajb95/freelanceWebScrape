import bs4 as bs
import urllib.request
from urllib.request import Request
import json
import unicodecsv as csv
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
import time

#global variable
match = ''

def main():
  for i in range(5):  
  #    x='https://ae.pricena.com/livesearch.html'
    y= 'https://ae.pricena.com/en/search/recent?limit=50'
    chrome_options = Options()  
    chrome_options.add_argument("--headless")    
    driver = webdriver.Chrome('C:/Users/Hamza JB/Anaconda3/envs/env_scrape/scrapy/chromedriver.exe',chrome_options=chrome_options )
    

    soupy = selSoup(driver,y)
    file1 = json_loader(soupy,match)    
    writeRecords(file1)
    print(match)
    time.sleep(15)


def json_loader(souptxt,matchy): #use json module to access json file 
  dat_block = []
  
  data = json.loads(souptxt)
  for search in data:
    unit=[]
    word = search['keyword']
    
    if word == matchy:
      break
    else:
      print(search['country']+' --- '+search['keyword']+' --- '+search['url'])
      unit.append(str(search['country']))
      unit.append(str(search['keyword']))
      unit.append(str(search['url']))
      dat_block.append(unit) 

  global match  
  try:
    match = dat_block[0][1]
  except(IndexError):pass
  print("Match is "+match)
  return dat_block
  

def writeRecords(cList):      #Takes list of lists as argument and writes them to csv file given as path
    with open('Test1UAE.csv','ab') as fw:
      file = csv.writer(fw,delimiter=',')
      data = cList
      file.writerows(data)
      print('File created!')

def selSoup(driver,theUrl):
  try:
    driver.get(theUrl)
  except(Exception): 
    driver.get(theUrl)   
  soup = bs.BeautifulSoup(driver.page_source, 'html.parser')
  x = []
  for data in soup.find_all('pre'):
    x = data.get_text()
  return x
  #return mySoup


  

if __name__ == "__main__":
    main()
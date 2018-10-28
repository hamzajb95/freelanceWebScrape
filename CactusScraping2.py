import sys
import urllib.request
from urllib.request import Request
import re
import bs4 as bs
from selenium import webdriver
import os
from urllib.parse import urlparse

def main():
  #url ='http://www.cactus-art.biz/gallery/Photo_gallery_abc_cactus.htm'
  testurl = 'http://www.cactus-art.biz/schede/ACANTHOCALYCIUM/Acanthocalycium_glaucum/Acanthocalycium_glaucum/Acanthocalycium_glaucum.htm'
#  driver = webdriver.Firefox()
#  driver.get(url)
#  table = driver.find_element_by_xpath('//table[@id="AutoNumber4"]')
  #table.find_element_by_xpath()
#  print(table.text)

  #MAKE THE SOUP
  #soup = make_soup(testurl)
  #mainLinks(soup)
  #print(getName(testurl))
  testurl = 'http://www.cactus-art.biz/schede/ACANTHOCALYCIUM/Acanthocalycium_griseum/Acanthocalycium_griseum_810.jpg'
  download_img('asfad',testurl)

def make_soup(theUrl):
  urlReq = Request(theUrl, headers={'User-Agent': 'Chrome/68.0.3440.106'})
  authinfo = urllib.request.HTTPBasicAuthHandler()
  proxy_support = urllib.request.ProxyHandler({"http" : "http://47.52.64.149:80"})
  opener = urllib.request.build_opener(proxy_support, authinfo, urllib.request.CacheFTPHandler)
  #INSTALLING PROXY
  urllib.request.install_opener(opener)
  #Opening file
  wp = urllib.request.urlopen(urlReq).read()
  mySoup = bs.BeautifulSoup(wp,'lxml')
  return mySoup

#def getName(soup,url):
#  for i in soup.findAll('i'):
#    if i is not None:
#      rawName = i.text
#      Name = rawName.strip()
#      return Name

def getName(url):
  a = urlparse(url)
  aPath = a.path
  filename = os.path.basename(aPath)
  return filename

def download_img(imgName,imgPath):  
  full_path = 'CactusImages/'+imgName+'.jpg'
  urllib.request.urlretrieve(imgPath,full_path)

        




if __name__ == '__main__':
  main()
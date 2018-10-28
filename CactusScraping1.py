import sys
import urllib.request
from urllib.request import Request
import re
import bs4 as bs
import http
import os
from urllib.parse import urlparse
import urllib

testurl ='http://www.cactus-art.biz/schede/ACANTHOCALYCIUM/Acanthocalycium_thionanthum/Acanthocalycium_thionanthum_copiapoides/Acanthocalycium_thionanthum_copiapoides.htm'

def main():
  url ='http://www.cactus-art.biz/gallery/Photo_gallery_abc_cactus.htm'
  count = 0
  soup = make_soup(url)
  m_Links = mainLinks(soup)
  for mlink in m_Links:
    if(count >= 50):
      s_Links = subLinks(mlink)
      for imgLinks in s_Links:      
        print('getting next file')
        #CREATE THE NEW SOUPS
        thisSoup = make_soup(imgLinks)
        filename = getName(imgLinks)
        dlPath = getImgPath(thisSoup,imgLinks)
        download_img(filename,dlPath)
      count += 1
      print('A total of '+str(count)+" links downloaded")
    else:
      count += 1
      print('A total of '+str(count)+" links downloaded")
        
  
  
  
  
  
def make_soup(theUrl):
  
  urlReq = Request(theUrl, headers={'User-Agent': 'Chrome/68.0.3440.106'})
  authinfo = urllib.request.HTTPBasicAuthHandler()
  proxy_support = urllib.request.ProxyHandler({"http" : "http://40.81.124.138:3128"})
  opener = urllib.request.build_opener(proxy_support, authinfo, urllib.request.CacheFTPHandler)
  #INSTALLING PROXY
  urllib.request.install_opener(opener)
  #Opening file
  try:
    wp = urllib.request.urlopen(urlReq).read()
    mySoup = bs.BeautifulSoup(wp,'lxml')
    print('soup created')
    return mySoup
  except (http.client.IncompleteRead) as e:
    wp = e.partial
    print('partial throw')
  except:
    mySoup = make_soup(testurl)
    return mySoup 
    

def mainLinks(soupy):
  linkList = []  
  for table in soupy.findAll('table'):
    if table is not None:
      mytable = table.get('id')
      if mytable == 'AutoNumber4':
        for tr in table.findAll('td'):
          td = tr.get('colspan')
          if td is not None:
            if int(td) == 3:                
              for link in tr.findAll('a'):
                temp = link.get('href')
                linkInst = 'http://www.cactus-art.biz'+ temp[2:]
                linkList.append(linkInst)
  print('Main Links collected sucessfully')
  return linkList

def subLinks(link):
  links =[]
  soup = make_soup(link)
  for table in soup.findAll('table'):
    if table is not None:  
      mytable = table.get('cellpadding')
      if mytable == '5':
        for subtable in table.findAll('table'):
          checkTable = subtable.get('cellpadding')
          if checkTable == '3':
            for anchors in subtable.findAll('a'):
              temp = CactusType(link)+ '/' + anchors.get('href')
              links.append(temp)
  print('Sub links fetched sucessfully')          
  return links
    
def CactusType(url):
  match = re.search(r'\w+:[\/][\/]\w+.\w+-\w+.\w+[\/]\w+[\/]\w+',url).group()
  return match

def getImgPath(soup,url):    
  try:
    for img in soup.findAll('img'):
      x = img.get('width')
      if x is not None:
        if int(x) >= 800:            ##Assuming that there is only one img with width > 800
          filename = img.get('src')
          match = re.search(r'.+/', url)
          path = match.group() + filename
          print(path)
          return path 
  except:
    mySoup = make_soup(testurl)
    return getImgPath(mySoup,testurl)
    
def getName(url):
  a = urlparse(url)
  aPath = a.path
  filename = os.path.basename(aPath)
  return filename

#def download_img(imgName,imgPath):  
#  imagefile = open('CactusImages/'+imgName+'.jpeg','wb')
#  try:
#    imagefile.write(urllib.request.urlopen(imgPath).read())
#  except (http.client.IncompleteRead) as e:
#    imagefile = e.partial
#  #imagefile.close()
#  print(imgName+" file created.")

def download_img(imgName,imgPath):  
  full_path = 'CactusImages/'+imgName+'.jpg'
  if not os.path.exists(full_path):
    try:
      urllib.request.urlretrieve(imgPath,full_path)
    except (TypeError):
      print ("Shit went down")  
    except(Exception):
      print ("Shit went down")

  


if __name__ == '__main__':
  main()

def main():
  path = r'C:\Users\Hamza JB\Anaconda3\envs\env_scrape\CampingScrape\list4.txt'
  path1 = r'C:\Users\Hamza JB\Anaconda3\envs\env_scrape\CampingScrape\list3.txt'
  url2 = file_read(path)
  url3 = file_read(path1)
  x = list(set(url3) - set(url2))
  writeFile(x)



def fixList(urlx):
  listprep=[]
  for url in urlx:
    if len(url) > 2:
        url = url.replace('\"','')
        print(url)
        listprep.append(url)
  print(len(listprep))
  writeFile(listprep)
    

def file_read(fname):
    with open(fname) as f:
    #Content_list is the list that contains the read lines.     
      content_list = f.readlines()
    return content_list

def writeFile(data):
  path = r'C:\Users\Hamza JB\Anaconda3\envs\env_scrape\CampingScrape\List5.txt'
  file = open(path,'w')
  for d in data:
    file.write(d)
  file.close()

if __name__ == "__main__":
  main() 
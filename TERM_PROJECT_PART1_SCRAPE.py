####### LING78100 TERM PROJECT
####### PART 1: SPEECH SCRAPING

####### __author__ = 'yimizhao'
####### original code: https://github.com/yimihua2013/Mining-the-Web_Python/blob/master/ObamaSpeech.py
####### edited by Winnie Yan 


import os
import requests
from bs4 import BeautifulSoup 


####### TOP 50 George W. Bush SPEECHES FROM AMERICAN RHETORIC WEBSITE 
website = "https://www.americanrhetoric.com/gwbushspeeches.htm"
r = requests.get(website)
page = BeautifulSoup(r.content, features="lxml")


### PART I: grab the urls###
# get the urls
def filter_link(link):
    href = link.get('href')
    if href:
        return href.startswith("speeches") and (href.endswith(".html") or href.endswith(".htm")) 

links = page.find_all('a')
urls = filter(filter_link, links)
urls = [url.get('href') for url in urls]
print(len(urls)) 

# display the urls
def get_url(link):
    pre = "http://www.americanrhetoric.com/"
    return pre+link

full_urls = []
for url in urls:
    full_urls.append(get_url(url))


### PART II: fetch the speech content###
# get the speech content
def get_g_data(url):
    re = requests.get(url)
    page_data = BeautifulSoup(re.content, features="lxml")
    g_data = page_data.find_all("font", {"face": "Verdana"})
    return g_data

directory = "Bush/" 

try:
    os.mkdir(directory)
except OSError:
    print ("Creation of the directory %s failed" % directory)
else:
    print ("Successfully created the directory %s " % directory)

# write into .txt files
def write_speech(url):
    name = url.split('/')[-1].split('.')[0]
    print('{}'.format(name))
    with open(directory + name + '.txt', 'w', encoding="utf-16") as f:
        resultset = get_g_data(url)
        for line in resultset:
            f.write(str(line.text))
      
count = 0
for i in range(0,50):
    write_speech(full_urls[i])
    count+=1
print(count)    





####### TOP 50 Barack Obama SPEECHES FROM AMERICAN RHETORIC WEBSITE 
website = "https://www.americanrhetoric.com/barackobamaspeeches.htm"
r = requests.get(website)
page = BeautifulSoup(r.content, features="lxml")


### PART I: grab the urls###
# get the urls
def filter_link(link):
    href = link.get('href')
    if href:
        return href.startswith("speeches") and (href.endswith(".html") or href.endswith(".htm")) 

links = page.find_all('a')
urls = filter(filter_link, links)
urls = [url.get('href') for url in urls]
print(len(urls)) 

# display the urls
def get_url(link):
    pre = "http://www.americanrhetoric.com/"
    return pre+link

full_urls = []
for url in urls:
    full_urls.append(get_url(url))


### PART II: fetch the speech content###
# get the speech content
def get_g_data(url):
    re = requests.get(url)
    page_data = BeautifulSoup(re.content, features="lxml")
    g_data = page_data.find_all("font", {"face": "Verdana"})
    return g_data

directory = 'BarryO/'

try:
    os.mkdir(directory)
except OSError:
    print ("Creation of the directory %s failed" % directory)
else:
    print ("Successfully created the directory %s " % directory)

# write into .txt files
def write_speech(url):
    name = url.split('/')[-1].split('.')[0]
    print('{}'.format(name))
    with open(directory + name + '.txt', 'w', encoding="utf-16") as f:
        resultset = get_g_data(url)
        for line in resultset:
            f.write(str(line.text))
         
count = 0
for i in range(0,50):
    write_speech(full_urls[i])
    count+=1
print(count)

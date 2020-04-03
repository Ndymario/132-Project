import urllib2
import requests
from bs4 import BeautifulSoup
import pprint

url = 'https://www.barcodelookup.com/'
barcode = raw_input(" enter a barcode ")
page = requests.get(url + barcode
                    )
soup = BeautifulSoup(page.content, 'lxml')

item_name = soup.find('h4')

name = item_name.text.strip()
print name


##url = 'https://www.barcodelookup.com/028400070560'
##
####barcode = raw_input(" enter a barcode ")
##
####page = urllib2.urlopen(url)
##page = requests.get(url)
##
###print page.content  # looks like it worked but froze the program
##
####pprint.pprint(page.content)
##
####soup = BeautifulSoup(page.content, 'html.praser')
##soup = BeautifulSoup(page.content, 'lxml')
##
##item_name = soup.find('h4')
##
##name = item_name.text.strip()
##print name
##
####r = requests.get("http://" + url +"/" +barcode)
####
####data = r.text
####
####soup = BeautifulSoup(data)
####
####for link in soup.find_all('a'):
####    print(link.get('href'))


## important ####
# python -m " all the files below"
# install beautifulsoup, lxml , and requests

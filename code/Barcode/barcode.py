## important ####
# python -m " all the files below"
# install beautifulsoup, lxml , and requests


import requests
from bs4 import BeautifulSoup
#import pprint





def lookupname(barcode):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    url = 'https://www.barcodelookup.com/'
    barcode = barcode
    page = requests.get(url + barcode, headers=headers)
    soup = BeautifulSoup(page.content, 'lxml')
    item_name = soup.find('h4')
    bcheck = item_name.text.strip()
    
    if ("API" in bcheck):
        name = "Item not in DataBase!"
        

    else:
        name = namecheck(bcheck)
    return name

def namecheck(name):
    name = name
    check =raw_input( "Is this corect: {}? \nY/N  ".format(name))
    check = check.lower()
    if (check == "y" or check == "yes"):
        return name
    else:
        name = raw_input("Type corect name")
        return name
    
    
barcode = raw_input(" enter a barcode ")
name = lookupname(barcode)
print name


##url = 'https://www.barcodelookup.com/'
##barcode = raw_input(" enter a barcode ")
##page = requests.get(url + barcode)
##soup = BeautifulSoup(page.content, 'lxml')
##
##item_name = soup.find('h4')
##
##name = item_name.text.strip()
##print name


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




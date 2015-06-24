import urllib2
import requests

from bs4 import BeautifulSoup

page = requests.get('https://contrataciondelestado.es/wps/portal/plataforma', verify=False)

soup = BeautifulSoup(page.text)
links = soup('div')
#print links[0]
#print
#print links[2]

print '-----------FIN----------------'
for link in links:
    try:
      link['class']
      #print link
    except KeyError:
        continue
    if link['class'] == ['paddingLeft1']:
        print link
        for child in link.children:
	  print(child)
	  
for cuki in page.cookies
    print cuki
import urllib2
from bs4 import BeautifulSoup

page = urllib2.urlopen("https://contrataciondelestado.es/wps/portal/plataforma")
soup = BeautifulSoup(page)
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
#from BeautifulSoup import BeautifulSoup
from bs4 import BeautifulSoup
import requests

url = 'http://stefan.sofa-rockers.org/'
payload = {
    'q': 'Python',
}
r = requests.get(url )

soup = BeautifulSoup(r.text)
titles = [h1.text for h1 in soup.findAll('h1')]

for t in titles:
    print(t)

#print(soup.prettify())
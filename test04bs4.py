import urllib2
from bs4 import BeautifulSoup

page = urllib2.urlopen("https://icc-ccs.org/piracy-reporting-centre/live-piracy-report")
soup = BeautifulSoup(page)
L = soup('td')
print L[0]
print
print L[2]

print '-----------OTRO----------------'

for incident in L:
    try:
        incident['class']
        print incident['class']
    except KeyError:
        continue
    if incident['class'] == ['jos_fabrik_icc_ccs_piracymap2012___narrations', 'fabrik_element']:
        where, linebreak, what = incident.contents[:3]
        print where.strip()
        print what.strip()
        print
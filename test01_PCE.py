
import httplib

#thisurl = "https://contrataciondelestado.es:443/wps/portal/!ut/p/b1/04_Sj9Q1MzWyNDYzsjTUj9CPykssy0xPLMnMz0vMAfGjzOJNXP2dnd08jAwMXH2NDYw8zN0tXI2dDQwCTIEKIoEKDHAARwNC-sP1o8BKTI2dTcK8wgLMgj3dDQw8PdxcfEINTQ3cjcygCvBY4eeRn5uqnxuVY-mp66gIAPyNS4w!/dl4/d5/L2dJQSEvUUt3QS80SmtFL1o2XzRFT0NDRkgyMDhTM0QwMkxEVVU2SEgyMEc1/"
thisurl = "contrataciondelestado.es"


c = httplib.HTTPSConnection(thisurl)
c.request("GET", "/wps/portal/plataforma")
response = c.getresponse()
print response.status, response.reason
data = response.read()
print data
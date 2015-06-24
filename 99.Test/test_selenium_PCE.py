# coding=utf-8
from selenium import webdriver
from bs4 import BeautifulSoup


expedientes =[]
# No puede ser headless con driver Firefox
driver = webdriver.Firefox()

#Carga página
driver.get("https://contrataciondelestado.es")

#Clica en búsqueda avanzada
driver.find_element_by_link_text('Búsqueda avanzada de licitaciones').click()

#Selecciona AGE
el = driver.find_element_by_id('viewns_Z7_AVEQAI930OBRD02JPMTPG21004_:form1:comboTipoAdminMAQ')
for option in el.find_elements_by_tag_name('option'):
    if (option.text).encode('utf-8') == 'Administración General del Estado':
        option.click() # select() in earlier versions of webdriver
        break

#Selecciona MSSSI
nomAdmin = driver.find_element_by_id('viewns_Z7_AVEQAI930OBRD02JPMTPG21004_:form1:comboadmins')      
for option in nomAdmin.find_elements_by_tag_name('option'):
    if (option.text).encode('utf-8') == 'Ministerio de Sanidad, Servicios Sociales e Igualdad':
        option.click() # select() in earlier versions of webdriver
        break
      
#Fecha publicacion entre 01/12/2014      
fDesde = driver.find_element_by_id('viewns_Z7_AVEQAI930OBRD02JPMTPG21004_:form1:textMinFecAnuncioMAQ2')
fDesde.send_keys("01-12-2014")

# y 31/12/2014
fHasta = driver.find_element_by_id('viewns_Z7_AVEQAI930OBRD02JPMTPG21004_:form1:textMaxFecAnuncioMAQ')
fHasta.send_keys("31-12-2014")

# pulsa el bot´on de buscar
driver.find_element_by_id('viewns_Z7_AVEQAI930OBRD02JPMTPG21004_:form1:button1').click()

# En linea saca los expedientes
html_page = driver.page_source

soup = BeautifulSoup(html_page)

expedientes_pag = [c.text for c in soup.findAll('td', {'class':'tdExpediente'})]

expedientes.extend(expedientes_pag)

# Pulsa enlace siguiente
driver.find_element_by_id('viewns_Z7_AVEQAI930OBRD02JPMTPG21004_:form1:footerSiguiente').click()

# En linea saca los expedientes
html_page = driver.page_source

soup = BeautifulSoup(html_page)

expedientes_pag = [c.text for c in soup.findAll('td', {'class':'tdExpediente'})]

expedientes.extend(expedientes_pag)

# Cierra el driver
driver.quit()
#for t in titles:
#    print(t)

for exp in expedientes:
    print(exp)


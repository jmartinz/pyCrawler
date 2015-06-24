# coding=utf-8

# -*- coding: utf-8 -*-
#from __future__ import print_function
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup



def extraeContratos(table):
#https://adesquared.wordpress.com/2013/06/16/using-python-beautifulsoup-to-scrape-a-wikipedia-table/  
    f = open('output.csv', 'a')
    
    expediente = ""
    tipoContrato = ""
    estado = ""
    importe = ""
    fechas = ""
    organo = ""

    for row in table.findAll("tr"):
#      print (row)
	    cells = row.findAll("td")
	    #print len(cells)
	    #For each "tr", assign each "td" to a variable.
	    if len(cells) == 6:
		expediente = cells[0].find(text=True)
	      #print(expediente)  
		tipoContrato = cells[1].find(text=True)
		estado = cells[2].find(text=True)
		importe = cells[3].find(text=True)
		fechas = cells[4].find(text=True)
		organo = cells[5].find(text=True)
#		   
		write_to_file = expediente + "," + tipoContrato + "," + estado + "," + importe + "," + fechas+ "," + organo + "\n"
		#print write_to_file
		f.write(write_to_file.encode("UTF-8"))

	    #district can be a list of lists, so we want to iterate through the top level lists first...
#	    for x in range(len(district)):
		    #For each list, split the string
		    #postcode_list = district[x].split(",")
		    #For each item in the split list...
		    #for i in range(len(postcode_list)):
			    #Check it's a postcode and not other text
			    #if (len(postcode_list[i]) > 2) and (len(postcode_list[i]) <= 5):
				    #Strip out the "\n" that seems to be at the start of some postcodes


    f.close()



expedientes =[]
# No puede ser headless con driver Firefox
driver = webdriver.Firefox()

#Carga página
driver.get("https://contrataciondelestado.es")

#Clica en búsqueda avanzada
#driver.find_element_by_link_text('Búsqueda avanzada de licitaciones').click()
driver.find_element_by_css_selector("div.paddingLeft1  a").click()

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
fDesde.send_keys("01-01-2014")

# y 31/12/2014
fHasta = driver.find_element_by_id('viewns_Z7_AVEQAI930OBRD02JPMTPG21004_:form1:textMaxFecAnuncioMAQ')
fHasta.send_keys("31-12-2014")

# pulsa el bot´on de buscar
driver.find_element_by_id('viewns_Z7_AVEQAI930OBRD02JPMTPG21004_:form1:button1').click()

#Imprime el número de elementos
print (driver.find_element_by_id('viewns_Z7_AVEQAI930OBRD02JPMTPG21004_:form1:textfooterTotalTotalMAQ').text)

nPagTotal = driver.find_element_by_id('viewns_Z7_AVEQAI930OBRD02JPMTPG21004_:form1:textfooterInfoTotalPaginaMAQ').text
#print ("Páginas totales: "+ nPagTotal)
print (nPagTotal)

# Recorre todas las páginas de resultados
while True: # Se ejecuta siempre hasta que no exista el enlace "siguiente"
    
    nPag = driver.find_element_by_id('viewns_Z7_AVEQAI930OBRD02JPMTPG21004_:form1:textfooterInfoNumPagMAQ').text
    #print ("Página : "+ nPag)
    print (nPag)

  # En linea saca los expedientes
    html_page = driver.page_source

    soup = BeautifulSoup(html_page)
    
    tableExp = soup.find("table", { "id" : "myTablaBusquedaCustom" })
    
    extraeContratos(tableExp)

    expedientes_pag = [c.text for c in soup.findAll('td', {'class':'tdExpediente'})]

    expedientes.extend(expedientes_pag)

    # Pulsa enlace siguiente, si no lo encuentra se sale del bucle
    try:      
      enlaceSiguiente= driver.find_element_by_id('viewns_Z7_AVEQAI930OBRD02JPMTPG21004_:form1:footerSiguiente')
      enlaceSiguiente.click()
    except NoSuchElementException:
      break
    
# En linea saca los expedientes
#html_page = driver.page_source

#soup = BeautifulSoup(html_page)

#expedientes_pag = [c.text for c in soup.findAll('td', {'class':'tdExpediente'})]

#expedientes.extend(expedientes_pag)

# Cierra el driver
driver.quit()
#for t in titles:
#    print(t)

# abre fichero
f = open('workfile', 'w')

for exp in expedientes:
    f.write(exp.encode("UTF-8")+ "\n")
     
#     print(exp.encode("UTF-8"), file=f)
#    print(exp)
#  print(exp.encode("UTF-8"))

f.close()



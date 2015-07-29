# coding=utf-8

# -*- coding: utf-8 -*-
#from __future__ import print_function
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup


# voy a volcar a fichero el texto en crudo de la tabla para testear como extraer la información con bs4
def extraeContratos(table):
    f = open('tablaContratos.txt', 'a')
    for row in table.findAll("tr"):
      f.write(row.encode("UTF-8")+ "\n")
    f.close()
    
expedientes =[]
# No puede ser headless con driver Firefox
driver = webdriver.Firefox()

#Carga página
driver.get("https://contrataciondelestado.es/wps/portal/!ut/p/b1/lZDLDoIwEEU_aaYParssrwLxAVZQujEsjMH42Bi_30rcGCPq7CZz7pzkgoOWKC6kYBPYgDt3t37fXfvLuTs-die2PFlEUZpRlJbFSKdxXYvMrybwQOsB_DAah3xopdQh0YislqhFVUXK_0HFnvmARbwpmlLY3CDmWRpPaxKgoeI3_4jgxW_sjPhzwkRAkRhLn_mPAvqn_13wJb8GNyBjDQzAWMXjEgrz7HLaQeuxyVY3SaVzxXARLj1WlLNVaShB5LCCNoGTO6Z-VH7g3R2UoLEz/dl4/d5/L2dBISEvZ0FBIS9nQSEh/pw/Z7_AVEQAI930OBRD02JPMTPG21004/act/id=0/p=javax.servlet.include.path_info=QCPjspQCPbusquedaQCPBusquedaVIS_UOE.jsp/299420689304/-/")

#Clica en búsqueda avanzada
#driver.find_element_by_link_text('Búsqueda avanzada de licitaciones').click()
#driver.find_element_by_css_selector("div.paddingLeft1  a").click()

#Selecciona AGE
#el = driver.find_element_by_id('viewns_Z7_AVEQAI930OBRD02JPMTPG21004_:form1:comboTipoAdminMAQ')
#for option in el.find_elements_by_tag_name('option'):
#    if (option.text).encode('utf-8') == 'Administración General del Estado':
#        option.click() # select() in earlier versions of webdriver
#        break

#Selecciona MSSSI
driver.find_element_by_id('viewns_Z7_AVEQAI930OBRD02JPMTPG21004_:form1:idSeleccionarOCLink').click()      # Organización contratante -> seleccionar
driver.find_elements_by_class_name('tafelTreeopenable')[1].click()                                                                       # Selecciona AGE
driver.find_element_by_id('tafelTree_maceoArbol_id_17').click()                                                                            # Selecciona Sanidad
driver.find_element_by_id('viewns_Z7_AVEQAI930OBRD02JPMTPG21004_:form1:botonAnadirMostrarPopUpArbolEO').click()     
#nomAdmin = 
#for option in nomAdmin.find_elements_by_tag_name('option'):
#    if (option.text).encode('utf-8') == 'Ministerio de Sanidad, Servicios Sociales e Igualdad':
#        option.click() # select() in earlier versions of webdriver
#        break
      
#Fecha publicacion entre 01/12/2014      
fDesde = driver.find_element_by_id('viewns_Z7_AVEQAI930OBRD02JPMTPG21004_:form1:textMinFecAnuncioMAQ2')
fDesde.send_keys("01-01-2014")

# y 31/12/2014
fHasta = driver.find_element_by_id('viewns_Z7_AVEQAI930OBRD02JPMTPG21004_:form1:textMaxFecAnuncioMAQ')
fHasta.send_keys("24-06-2015")

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
    


# Cierra el driver
driver.quit()



def main():
  
    # Lee la bbdd ¿con qué criterios?
    listaContratos=[]
    exp_data = open('tablaContratos.txt','r').read()

    soup = BeautifulSoup(exp_data)
     
    # Envia sólo las líneas que son de contratos 
    for row in soup.findAll("tr",  {'class': ['rowClass1', 'rowClass2']}):
        #pickle.dump(Contrato(row),  open('save.p', 'ab')) 
        listaContratos.append(Contrato(row))
        #print(row.prettify())
        
    for contrato in listaContratos:
        contrato.grabarBD()
        
    
    
if __name__ == "__main__":
    sys.exit(main())

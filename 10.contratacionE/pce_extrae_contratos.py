# coding=utf-8

# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import sys

phantonPath = "/home/jmartinz/00.py/phantomjs/phantomjs"
contratacionPage="https://contrataciondelestado.es/wps/portal/!ut/p/b1/lZDLDoIwEEU_aaYParssrwLxAVZQujEsjMH42Bi_30rcGCPq7CZz7pzkgoOWKC6kYBPYgDt3t37fXfvLuTs-die2PFlEUZpRlJbFSKdxXYvMrybwQOsB_DAah3xopdQh0YislqhFVUXK_0HFnvmARbwpmlLY3CDmWRpPaxKgoeI3_4jgxW_sjPhzwkRAkRhLn_mPAvqn_13wJb8GNyBjDQzAWMXjEgrz7HLaQeuxyVY3SaVzxXARLj1WlLNVaShB5LCCNoGTO6Z-VH7g3R2UoLEz/dl4/d5/L2dBISEvZ0FBIS9nQSEh/pw/Z7_AVEQAI930OBRD02JPMTPG21004/act/id=0/p=javax.servlet.include.path_info=QCPjspQCPbusquedaQCPBusquedaVIS_UOE.jsp/299420689304/-/"
#contratacionPage="https://contrataciondelestado.es"

#Clase que devuelve los contratos de n ministerio entre unas fechas usando el dirver que se indique 
class Contratos():

    driver = webdriver.PhantomJS(phantonPath, service_args=['--ignore-ssl-errors=true'])
    expedientes =[]
    ministerio = 'tafelTree_maceoArbol_id_'
    fIni= '01-01-2015'
    fFin='10-01-2015'
    
    nContratos = 0
    nPagTotal = 0
    
    def __init__(self, driverType=1, ministry='17', fini='01-01-2015',ffin='10-01-2015'):
        if driverType==1:
            self.driver  = webdriver.Firefox()
        else:   
            self.driver = webdriver.PhantomJS(phantonPath, service_args=['--ignore-ssl-errors=true'])
            self.driver.set_window_size(1120, 550)
        
        self.ministerio = self.ministerio + ministry
        self.fIni = fini
        self.fFin = ffin
#        self.debugPhanton()
        self.extraecontratos()
        
    def debugPhanton(self):
        #Carga página
        self.driver.get(contratacionPage)
        # check phantomjs
        print(self.driver.page_source)
        
    def extraecontratos(self):
        #Carga página
        driver.implicitly_wait(10) 
        driver.set_page_load_timeout(10) 
        try:   
            self.driver.get(contratacionPage)
        except TimeoutException as e:     #Handle y  
            #Handle your exception here     
            print(e)
        

        #Selecciona ministerio
        self.driver.find_element_by_id('viewns_Z7_AVEQAI930OBRD02JPMTPG21004_:form1:idSeleccionarOCLink').click()      # Organización contratante -> seleccionar
        self.driver.find_elements_by_class_name('tafelTreeopenable')[1].click()                                                                       # Selecciona AGE
        self.driver.find_element_by_id(self.ministerio).click()                                                                                                                  # Selecciona el Ministerio pasado por parámetros
        self.driver.find_element_by_id('viewns_Z7_AVEQAI930OBRD02JPMTPG21004_:form1:botonAnadirMostrarPopUpArbolEO').click()     
        
        #Fecha publicacion entre fIni      
        fDesde = self.driver.find_element_by_id('viewns_Z7_AVEQAI930OBRD02JPMTPG21004_:form1:textMinFecAnuncioMAQ2')
        fDesde.send_keys(self.fIni)
        
        # y fFin
        fHasta = self.driver.find_element_by_id('viewns_Z7_AVEQAI930OBRD02JPMTPG21004_:form1:textMaxFecAnuncioMAQ')
        fHasta.send_keys(self.fFin)
        
        # pulsa el botón de buscar
        self.driver.find_element_by_id('viewns_Z7_AVEQAI930OBRD02JPMTPG21004_:form1:button1').click()
        
        #Obtine el número de elementos
        self.nContratos=self.driver.find_element_by_id('viewns_Z7_AVEQAI930OBRD02JPMTPG21004_:form1:textfooterTotalTotalMAQ').text
        # y de páginas totales
        self.nPagTotal = self.driver.find_element_by_id('viewns_Z7_AVEQAI930OBRD02JPMTPG21004_:form1:textfooterInfoTotalPaginaMAQ').text

        
        # Recorre todas las páginas de resultados
        while True: # Se ejecuta siempre hasta que no exista el enlace "siguiente"
        
            nPag = self.driver.find_element_by_id('viewns_Z7_AVEQAI930OBRD02JPMTPG21004_:form1:textfooterInfoNumPagMAQ').text
    
            
            # En linea saca los expedientes de la página
            html_page = self.driver.page_source
            
            soup = BeautifulSoup(html_page)
            
            tableExp = soup.find("table", { "id" : "myTablaBusquedaCustom" })
       
            expedientes_pag = [c.text for c in soup.findAll('td', {'class':'tdExpediente'})]
            
            # Los añade a los expedientes totales
            self.expedientes.extend(expedientes_pag)
            
            # Pulsa enlace siguiente, si no lo encuentra se sale del bucle
            try:      
              enlaceSiguiente= self.driver.find_element_by_id('viewns_Z7_AVEQAI930OBRD02JPMTPG21004_:form1:footerSiguiente')
              enlaceSiguiente.click()
            except NoSuchElementException:
              break
        
        
        
        # Cierra el driver
        self.driver.quit()
        
        
# Sólo para probar que funcina        
def main():
  
    # Lee la bbdd ¿con qué criterios?
    contratosMSSSI=Contratos(driverType=2)
    print(contratosMSSSI.nContratos)
    print(contratosMSSSI.nPagTotal)

 
    
    
if __name__ == "__main__":
    sys.exit(main())        
        

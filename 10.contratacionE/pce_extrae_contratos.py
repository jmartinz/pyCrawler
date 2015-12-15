# coding=utf-8

# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException,  TimeoutException
from bs4 import BeautifulSoup
import sys

#phantonPath = "/home/jmartinz/00.py/phantomjs/phantomjs"
phantonPath = "../phantomjs/phantomjs"
contratacionPage = "https://contrataciondelestado.es/wps/portal/!ut/p/b1/lZDLDoIwEEU_aaYParssrwLxAVZQujEsjMH42Bi_30rcGCPq7CZz7pzkgoOWKC6kYBPYgDt3t37fXfvLuTs-die2PFlEUZpRlJbFSKdxXYvMrybwQOsB_DAah3xopdQh0YislqhFVUXK_0HFnvmARbwpmlLY3CDmWRpPaxKgoeI3_4jgxW_sjPhzwkRAkRhLn_mPAvqn_13wJb8GNyBjDQzAWMXjEgrz7HLaQeuxyVY3SaVzxXARLj1WlLNVaShB5LCCNoGTO6Z-VH7g3R2UoLEz/dl4/d5/L2dBISEvZ0FBIS9nQSEh/pw/Z7_AVEQAI930OBRD02JPMTPG21004/act/id=0/p=javax.servlet.include.path_info=QCPjspQCPbusquedaQCPBusquedaVIS_UOE.jsp/299420689304/-/"
#contratacionPage="https://contrataciondelestado.es"
""" Móudlo para extraer datos de la página de contatación
        del estado
"""


class Contratos():
    """ Clase que devuelve los contratos de un ministerio entre unas fechas usando el dirver que se indique
            driverType=1 (Firefox, online) / 2(phantomjs)
            ministry:
                6: MAGRAMA
                7: MAExCoop
                8. MDEfensa
                9: MINECO
                10:MEDCD
                11:MESS
                12:MFOM
                13:MINHAP
                14:MINET
                15:MINJUS      
                16:MINPRES
                17:MSSSI
                18:MinTraInm
                19:MinInt
                20: Presidencia Gobierno
            fini: dd-mm-aaaa
            ffin: dd-mm-aaaa
    """
    driver = "" #webdriver.PhantomJS(phantonPath, service_args=['--ignore-ssl-errors=true'])
    driverType=1
    expedientes =[]
    ministerio = 'tafelTree_maceoArbol_id_'
    ministry=0
    fIni= '01-01-2015'
    fFin='10-01-2015'
    
    nContratos = 0
    nPagTotal = 0
    
    def __init__(self, driverType=1, ministry='17', fini='01-01-2015',ffin='10-01-2015'):
        self.driverType=driverType
        self.ministry = ministry
        if driverType==1:
            self.driver  = webdriver.Firefox()
        elif driverType==2:   
            self.driver = webdriver.PhantomJS(phantonPath, service_args=['--ignore-ssl-errors=true'])
            self.driver.set_window_size(1120, 550)
        
        self.ministerio = self.ministerio + ministry
        self.fIni = fini
        self.fFin = ffin
#        self.debugPhanton()
        self.extraecontratos()
        
    def cargaPagina(self):
        #Carga página
        if self.driverType==2:
            self.driver.implicitly_wait(10) 
            self.driver.set_page_load_timeout(10) 
        try:   
            self.driver.get(contratacionPage)
        except TimeoutException as e:     #Handle y  
            #Handle your exception here     
            print(e)        
        
    def debugPhanton(self):
        self.cargaPagina()
        # check phantomjs
        print(self.driver.page_source)
        
    def extraecontratos(self):
        
        self.cargaPagina()       

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
            
            soup = BeautifulSoup(html_page, "html5lib")
            
#            tableExp = soup.find("table", { "id" : "myTablaBusquedaCustom" })
#       
#            expedientes_pag = [c.text for c in soup.findAll('td', {'class':'tdExpediente'})]
            expedientes_pag = []
            # Añade sólo las líneas que son de contratos 
            for row in soup.findAll("tr",  {'class': ['rowClass1', 'rowClass2']}):
                expedientes_pag.append(row)
            
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
  

    contratosMSSSI=Contratos(driverType=2)
    print(contratosMSSSI.nContratos)
    print(contratosMSSSI.nPagTotal)

    # abre fichero
    f = open('workfile', 'w')
    
    for exp in contratosMSSSI.expedientes:
        f.write(exp.encode("UTF-8")+ "\n")
         
    f.close()

 
    
    
if __name__ == "__main__":
    sys.exit(main())        
        

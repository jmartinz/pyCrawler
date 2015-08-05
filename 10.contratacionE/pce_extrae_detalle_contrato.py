# coding=utf-8

# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException,  TimeoutException
from bs4 import BeautifulSoup
import sys

#phantonPath = "/home/jmartinz/00.py/phantomjs/phantomjs"
phantonPath = "../phantomjs/phantomjs"
contratacionPage="https://contrataciondelestado.es/wps/portal/!ut/p/b1/lZDLDoIwEEU_aaYParssrwLxAVZQujEsjMH42Bi_30rcGCPq7CZz7pzkgoOWKC6kYBPYgDt3t37fXfvLuTs-die2PFlEUZpRlJbFSKdxXYvMrybwQOsB_DAah3xopdQh0YislqhFVUXK_0HFnvmARbwpmlLY3CDmWRpPaxKgoeI3_4jgxW_sjPhzwkRAkRhLn_mPAvqn_13wJb8GNyBjDQzAWMXjEgrz7HLaQeuxyVY3SaVzxXARLj1WlLNVaShB5LCCNoGTO6Z-VH7g3R2UoLEz/dl4/d5/L2dBISEvZ0FBIS9nQSEh/pw/Z7_AVEQAI930OBRD02JPMTPG21004/act/id=0/p=javax.servlet.include.path_info=QCPjspQCPbusquedaQCPBusquedaVIS_UOE.jsp/299420689304/-/"
#contratacionPage="https://contrataciondelestado.es"

""" Clase que devuelve los detalles de un contrato por nº expediente y Órgano de contratación 
        numExpediente
        OrgContratacion
        driverType=1 (Firefox, online) / 2(phantomjs)
""" 
class detalleContrato():

    driver = "" #webdriver.PhantomJS(phantonPath, service_args=['--ignore-ssl-errors=true'])
    driverType=1
    estadoLic = ""
    procedimiento = ""
    enlacelic = ''
    codigocpv = ''
    resultado = ''
    adjudicatario =''
    numlicitadores = ''
    impadjudicacion = ''
    
    def __init__(self, numExpediente, OrgContratacion, driverType=1):
        self.driverType=driverType
        self.numExpediente = numExpediente
        self.OrgContratacion = OrgContratacion
        if driverType==1:
            self.driver  = webdriver.Firefox()
        elif driverType==2:   
            self.driver = webdriver.PhantomJS(phantonPath, service_args=['--ignore-ssl-errors=true'])
            self.driver.set_window_size(1120, 550)        

        self.extraeDetalles()
        
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
        
    def extraeDetalles(self):
        
        self.cargaPagina()       

        #Introduce contrato
        contrato = self.driver.find_element_by_id('viewns_Z7_AVEQAI930OBRD02JPMTPG21004_:form1:text71ExpMAQ')
        contrato.send_keys(self.numExpediente)
        
        #Introduce ´organo contrataci´on     
        orgcont = self.driver.find_element_by_id('viewns_Z7_AVEQAI930OBRD02JPMTPG21004_:form1:texoorganoMAQ')
        orgcont.send_keys(self.OrgContratacion)
        
      
        # pulsa el botón de buscar
        self.driver.find_element_by_id('viewns_Z7_AVEQAI930OBRD02JPMTPG21004_:form1:button1').click()
        

        #Obtener enlace
        self.driver.find_element_by_id('viewns_Z7_AVEQAI930OBRD02JPMTPG21004_:form1:enlaceExpediente_0').click() #sólo sirve para el primer expediente... como es este caso.
        
        # Obtiene los datos 
        self.estadoLic = self.driver.find_element_by_id('viewns_Z7_AVEQAI930OBRD02JPMTPG21006_:form1:text_Estado').text
        self.procedimiento = self.driver.find_element_by_id('viewns_Z7_AVEQAI930OBRD02JPMTPG21006_:form1:text_Procedimiento').text
        self.enlacelic = self.driver.find_element_by_id('viewns_Z7_AVEQAI930OBRD02JPMTPG21006_:form1:text_EnlaceLicPLACE').text
        self.codigocpv = self.driver.find_element_by_id('viewns_Z7_AVEQAI930OBRD02JPMTPG21006_:form1:text_CPV').text
        
        #Dependiendo del estado los siguientes elementos pueden existir o no
        try:      
            self.resultado = self.driver.find_element_by_id('viewns_Z7_AVEQAI930OBRD02JPMTPG21006_:form1:text_Resultado').text
            self.adjudicatario = self.driver.find_element_by_id('viewns_Z7_AVEQAI930OBRD02JPMTPG21006_:form1:text_Adjudicatario').text
            self.numlicitadores = self.driver.find_element_by_id('viewns_Z7_AVEQAI930OBRD02JPMTPG21006_:form1:text_NumeroLicitadores').text
            self.impadjudicacion = self.driver.find_element_by_id(' viewns_Z7_AVEQAI930OBRD02JPMTPG21006_:form1:text_ImporteAdjudicacion').text
        except NoSuchElementException:
            resultado = ''
            adjudicatario =''
            numlicitadores = ''
            impadjudicacion = ''
        
        # Cierra el driver
        self.driver.quit()
        
        
# Sólo para probar que funcina        
def main():
  

    detalles=detalleContrato(numExpediente = u'2015/213/00008', OrgContratacion=u'Secretaría General de la Agencia Española de Medicamentos y Productos Sanitarios', driverType=1)
    print(detalles.estadoLic)
    print(detalles.procediminto)

   
    
if __name__ == "__main__":
    sys.exit(main())        
        

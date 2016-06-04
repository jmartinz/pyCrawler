# coding=utf-8

# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException,  TimeoutException
from bs4 import BeautifulSoup
from datetime import datetime
from decimal import *
import sys

#phantonPath = "/home/jmartinz/00.py/phantomjs/phantomjs"
phantonPath = "../phantomjs/phantomjs"
contratacionPage = "https://contrataciondelestado.es/wps/portal/!ut/p/b1/lZDLDoIwEEU_aaYParssrwLxAVZQujEsjMH42Bi_30rcGCPq7CZz7pzkgoOWKC6kYBPYgDt3t37fXfvLuTs-die2PFlEUZpRlJbFSKdxXYvMrybwQOsB_DAah3xopdQh0YislqhFVUXK_0HFnvmARbwpmlLY3CDmWRpPaxKgoeI3_4jgxW_sjPhzwkRAkRhLn_mPAvqn_13wJb8GNyBjDQzAWMXjEgrz7HLaQeuxyVY3SaVzxXARLj1WlLNVaShB5LCCNoGTO6Z-VH7g3R2UoLEz/dl4/d5/L2dBISEvZ0FBIS9nQSEh/pw/Z7_AVEQAI930OBRD02JPMTPG21004/act/id=0/p=javax.servlet.include.path_info=QCPjspQCPbusquedaQCPBusquedaVIS_UOE.jsp/299420689304/-/"
#contratacionPage="https://contrataciondelestado.es"


class detalleContrato():
    """ Clase que devuelve los detalles de un contrato por nº expediente y Órgano de contratación
            numExpediente
            OrgContratacion
            driverType=1 (Firefox, online) / 2(phantomjs)
    """
    driver = ""
    driverType = 1
    estadoLic = ""
    procedimiento = ""
    enlacelic = ''
    codigocpv = ''
    resultado = ''
    adjudicatario =''
    numlicitadores = 0
    impadjudicacion = ''

    def __init__(self, numExpediente, OrgContratacion, driverType=1):
        self.driverType = driverType
        self.numExpediente = numExpediente
        self.OrgContratacion = OrgContratacion
        if driverType == 1:
            self.driver  = webdriver.Firefox()
        elif driverType == 2:
            self.driver = webdriver.PhantomJS(phantonPath, service_args=['--ignore-ssl-errors=true'])
            self.driver.set_window_size(1120, 550)

        self.extraeDetalles()

    def cargaPagina(self):
        #Carga página
        if self.driverType == 2:
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
            importe_text = self.driver.find_element_by_id('viewns_Z7_AVEQAI930OBRD02JPMTPG21006_:form1:text_ImporteAdjudicacion').text.replace(".","").replace(",",".")
            try:
                self.impadjudicacion = Decimal(importe_text.strip(' "'))
            except (ValueError, TypeError, DecimalException) as e:
                self.impadjudicacion = 0
            numlicitadores_text = self.driver.find_element_by_id('viewns_Z7_AVEQAI930OBRD02JPMTPG21006_:form1:text_NumeroLicitadores').text
            try:
                self.numlicitadores = int(numlicitadores_text)
            except ValueError:
                self.numlicitadores =0
            print("numlic= ",self.numlicitadores)
        except NoSuchElementException:
            resultado = ''
            adjudicatario =''
            numlicitadores = 0
            impadjudicacion = ''

        # En linea saca los documentos de la página
        html_page = self.driver.page_source

        soup = BeautifulSoup(html_page, "html5lib")

        self.Documento={}
        
        for row in soup.findAll("tr",  {'class': ['rowClass1', 'rowClass2']}):
            try:
                fechadoc=datetime.strptime(row.find("td", {'class': 'fechaPubLeft'}).text, '%d/%m/%Y %H:%M:%S') 
                tipodoc=row.find("td", {'class': 'tipoDocumento'}).text
                docs = row.find("td", {'class': 'documentosPub'}).findAll('div')
                enlacedoc = docs[0].find('a', href=True)['href']
                self.Documento[tipodoc]=[fechadoc,enlacedoc]
            except:    # documentos adicionales
                try:
                    fechadoc = datetime.strptime(row.find(id='viewns_Z7_AVEQAI930OBRD02JPMTPG21006_:form1:TableEx1_Aux:0:textSfecha1PadreGen').text, '%d/%m/%Y %H:%M:%S') 
                    tipodoc = row.find(id='viewns_Z7_AVEQAI930OBRD02JPMTPG21006_:form1:TableEx1_Aux:0:textStipo1PadreGen').text
                    enlace =row.find(id='viewns_Z7_AVEQAI930OBRD02JPMTPG21006_:form1:TableEx1_Aux:0:linkVerDocPadreGen')['href']
                    self.Documento[tipodoc]=[fechadoc,enlacedoc]                
                except:
                    pass
                    

        # Cierra el driver
        self.driver.quit()


# Sólo para probar que funcina
def main(nExp,orgCon):


#    detalles=detalleContrato(numExpediente = u'2015/213/00008', OrgContratacion=u'Secretaría General de la Agencia Española de Medicamentos y Productos Sanitarios', driverType=2)
#    detalles=detalleContrato(numExpediente = u'CR0228/2012', OrgContratacion=u'Secretaría General del Instituto de Salud Carlos III', driverType=2)
    detalles=detalleContrato(numExpediente = nExp, OrgContratacion=orgCon, driverType=2)

    print(detalles.estadoLic)
    print(detalles.procedimiento)
    print(detalles.enlacelic)
    print(detalles.codigocpv)
    print(detalles.resultado)
    print(detalles.adjudicatario)
    print(detalles.numlicitadores)
    print(detalles.impadjudicacion)
    for docs in detalles.Documento.keys():
        print(docs,"-",detalles.Documento[docs][0],detalles.Documento[docs][1])



if __name__ == "__main__":
    if not len(sys.argv) == 3:
        print ('Usage: pce_extrae_detalle_contrato.py  numExpediente orgContratacion')
        sys.exit(1)

    sys.exit(main(sys.argv[1], # TODO comprobar 1 ó 2
                    sys.argv[2],        # TODO comprobar entre 6 y 20
 ))


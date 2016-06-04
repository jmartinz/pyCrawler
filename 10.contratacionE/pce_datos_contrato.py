# coding=utf-8

# -*- coding: utf-8 -*-
import re
from bs4 import BeautifulSoup
import sys

import peewee     #  object-relational mapper
from pce_db  import PceOrgano,  PceExpediente, PceFecha

from datetime import datetime
from decimal import *

""" Clase que de cada linea de la tabla extraida de contratos
obtiene los datos de cada contrato"""
class Contrato:

    ministry=0
    def __init__(self, row, ministry):

        self.ministry=ministry

        # Check that row has the correct class
        if row.get("class")[0] in ['rowClass1','rowClass2']:

            # Buscamos los datos del expediente por la clase de columna tdExpediente
            expediente = row.find("td", {'class': 'tdExpediente'}).findAll('div')
            self.num_expediente = expediente[0].text
            self.desc_expediente = expediente[1].text

            #Buscamos id_licitacion
            enlace = expediente[0].find('a', href=True)
            pattern = re.compile("'(\w+)':'(.*?)'")                 #http://stackoverflow.com/questions/25111752/extracting-text-using-beautifulsoup-in-python
            fields = dict(re.findall(pattern, enlace['onclick']))
            self.id_licitacion=int(fields['idLicitacion'])


            # Buscamos los datos del contrato por la clase de columna tdTipoContrato
            self.tiposContrato=[]
            for tipoContrato in row.find("td", {'class': 'tdTipoContrato'}).findAll('div'):
                self.tiposContrato.append(tipoContrato.text)

            # Buscamos el estado del expediente por la clase de columna tdEstado
            self.estado = row.find("td", {'class': 'tdEstado'}).text

            # Buscamos el importe del expediente por la clase de columna tdImporte
            importe_text= row.find("td", {'class': 'tdImporte'}).text.replace(".","").replace(",",".")
            self.importe = Decimal(importe_text.strip(' "'))
            
            # Buscamos el organo de contratación por la clase de columna tdOrganoContratacion
            datosOrganoC = row.find("td", {'class': 'tdOrganoContratacion'})
            self.organo = datosOrganoC.text
            self.organoURL=datosOrganoC.find('a').get('href')

            # Buscamos las fechas por la clase de columna tdFecha
            self.Fecha={}
            diaFecha=""

            for fecha in row.find("td", {'class': 'tdFecha'}).findAll('div'):
                tFecha =fecha.find('span', {'class':'anchoTipoFecha'}).text
                tipoFecha=u""
                # Eliminamos signos de puntuación y espacios (no acentos)
                for e in tFecha:
                    if e.isalnum():
                        tipoFecha += e

                # Busca la fecha
                diaFecha= fecha.find('span', {'class':'textAlignLeft'})
                if diaFecha is None:
                    diaFecha=""
                    date_fecha=""
                    # si está vacia la fecha no se añade el "tipo"
                else:
                    diaFecha=diaFecha.text
                    date_fecha = datetime.strptime(diaFecha, '%d/%m/%Y')
                    self.Fecha[tipoFecha]=date_fecha
    #        print(fechas.prettify())

    def grabarBD(self):
        # comprueba si existe el órgano. Si es así lee el Id, si no... lo crea
        try:
            idOrgano= PceOrgano.get(PceOrgano.descripcion==self.organo).id_organo
        except PceOrgano.DoesNotExist:
            organo = PceOrgano.create(descripcion = self.organo,
                                                      url = self.organoURL
                                                      )
            idOrgano= organo.id_organo

 # Se comprueba si existe ya una licitación con el id, si no se crea
        try:
            descLicitacion = PceExpediente.get(PceExpediente.id_licitacion ==self.id_licitacion).desc_expediente#
#            print("licitacion ",self.id_licitacion,"-",self.num_expediente ,"ya existe con descripcion: ",descLicitacion)
 #           print("La nueva descripcion seria: ",self.desc_expediente)
            return "Licitacion "+str(self.id_licitacion)+"-"+str(self.num_expediente) +" ya existe"
        except PceExpediente.DoesNotExist:
            expedienteBD= PceExpediente.create(desc_expediente = self.desc_expediente,
                                    num_expediente = self.num_expediente, 
                                    estado = self.estado,
                                    id_organo = idOrgano,
                                    importe_base = self.importe,
                                    tipo_contrato_1 = self.tiposContrato[0],
                                    tipo_contrato_2 = self.tiposContrato[1],
                                    id_ministerio = self.ministry,
                                    id_licitacion=self.id_licitacion
                                    )
#        nexp = expedienteBD.save()
        
        # recorre las fechas y las graba en la tabla de fechas
#		ATENCION, se leen fechas solo para las nuevas ---> MAL, tiene que haber nuevas fehcas!!!
#            for tipoFecha in self.Fecha.iterkeys():
            for tipoFecha in self.Fecha.keys():
                fechaBD = PceFecha.create(fecha = self.Fecha[tipoFecha],
                                    id_licitacion = self.id_licitacion,
                                    tipo_fecha = tipoFecha
                                    )
#            	print(self.id_licitacion,":",tipoFecha,"-", self.Fecha[tipoFecha])
        
#        return nexp
        return ""
        
 # Sólo para probar que funcina
def main():

    # Lee el fichero con el html previamente guardado
    listaContratos=[]
    exp_data = open('./Datos/tablaContratos_v2.txt','r').read()
    
    soup = BeautifulSoup(exp_data, "html5lib")

    
    # Envia sólo las líneas que son de contratos
    for row in soup.findAll("tr",  {'class': ['rowClass1', 'rowClass2']}):
        #pickle.dump(Contrato(row),  open('save.p', 'ab'))
        #print(row.prettify())
        print(row)
        listaContratos.append(Contrato(row, 6))
        
    for contrato in listaContratos:
        contrato.grabarBD()



if __name__ == "__main__":
    sys.exit(main())

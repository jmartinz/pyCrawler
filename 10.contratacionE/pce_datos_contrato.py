# coding=utf-8

# -*- coding: utf-8 -*-
import re
from bs4 import BeautifulSoup
import sys

import peewee     #  object-relational mapper
from pce_db  import PceOrgano,  PceExpediente

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
            self.importe = row.find("td", {'class': 'tdImporte'}).text

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
                else:
                    diaFecha=diaFecha.text


                self.Fecha[tipoFecha]=diaFecha
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

 # ATENCION MAL LAS FECHAS (Formato texto, no Fecha)
        expedienteBD= PceExpediente(desc_expediente = self.desc_expediente,
                                                           num_expediente = self.num_expediente,
                                                           estado = self.estado,
                                                           id_organo = idOrgano,
                                                          importe = self.importe,
                                                          tipo_contrato_1 = self.tiposContrato[0],
                                                          tipo_contrato_2 = self.tiposContrato[1],

# Se selecciona correctametne del diccionario. Si no se encuentra la clave, se devuelve cadna vacia (seria mejor none??)
#                                                          fec_adj_prov = self.Fecha[u'AdjProvisional'],
#                                                          fec_adj_definitiva = self.Fecha[u'AdjDefinitiva'],
#                                                          fec_adjudicacion = self.Fecha[u'FAdjudicación'],
#                                                          fec_formalizacion = self.Fecha[u'FFormalización'],
#                                                          fec_presentacion = self.Fecha[u'Presentación'],

                                                          fec_adj_prov = self.Fecha.get(u'AdjProvisional',''),
                                                          fec_adj_definitiva = self.Fecha.get(u'AdjDefinitiva',''),
                                                          fec_adjudicacion = self.Fecha.get(u'FAdjudicación',''),
                                                          fec_formalizacion = self.Fecha.get(u'FFormalización',''),
                                                          fec_presentacion = self.Fecha(u'Presentación',''),

                                                          id_ministerio = self.ministry,
                                                          id_licitacion=self.id_licitacion
                                                          )
        nexp = expedienteBD.save()
        return nexp

 # Sólo para probar que funcina
def main():

    # Lee el fichero con el html previamente guardado
    listaContratos=[]
    exp_data = open('./Datos/tablaContratos_2.txt','r').read()

    soup = BeautifulSoup(exp_data)

    # Envia sólo las líneas que son de contratos
    for row in soup.findAll("tr",  {'class': ['rowClass1', 'rowClass2']}):
        #pickle.dump(Contrato(row),  open('save.p', 'ab'))
        listaContratos.append(Contrato(row, 6))
        #print(row.prettify())

    for contrato in listaContratos:
        contrato.grabarBD()



if __name__ == "__main__":
    sys.exit(main())

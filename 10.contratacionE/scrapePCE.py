# coding=utf-8

# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import sys

""" Clase que de cada linea de la tabla extraida de contratos
obtiene los datos de cada contrato"""
class Contrato:

    
#    num_expediente = ""
#    desc_expediente =""
#    tipoContrato = []
#    estado = ""
#    importe = ""
#    fechas = [] 
#    organo = []

    def __init__(self, row):

        cells = row.findAll("td")
	    #print len(cells)
	    #For each "tr", assign each "td" to a variable.
        if len(cells) == 6:
            expediente = cells[0].findAll(text=True)
            self.num_expediente = expediente[0]
            self.desc_expediente = expediente[1]
	      #print(expediente)  
            self.tipoContrato = cells[1].findAll(text=True)
            self.estado = cells[2].find(text=True)
            self.importe = cells[3].find(text=True)
            #self.fechas = cells[4].findAll(text=True)
            self.organo = cells[5].findAll(text=True)
        
        # Buscamos las fechas por la clase de columna
        self.Fecha={}
        fechas = row.find("td", {'class': 'tdFecha'})
        diaFecha=""
        for fecha in fechas.findAll('div'):
            tipoFecha =fecha.find('span', {'class':'anchoTipoFecha'}).string
            
            # Busca la fecha
            diaFecha= fecha.find('span', {'class':'textAlignLeft'})
            if diaFecha is None:
                diaFecha=""
            else:
                diaFecha=diaFecha.string

            
            self.Fecha[tipoFecha]=diaFecha
#        print(fechas.prettify())
    
    
    
    
def main():
  
    # Lee el fichero con el html previamente guardado
    listaContratos=[]
    exp_data = open('tablaContratos_2.txt','r').read()

    soup = BeautifulSoup(exp_data)
      
    for row in soup.findAll("tr",  {'class': ['rowClass1', 'rowClass2']}):
        listaContratos.append(Contrato(row))
        #print(row.prettify())
    
    
if __name__ == "__main__":
    sys.exit(main())
    

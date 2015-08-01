# coding=utf-8

# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import sys
from pce_datos_contrato import Contrato
from pce_extrae_contratos import Contratos
  
    

def main():
    
    if not len(sys.argv) == 5:
        print ('usage: pce_Principal.py  driverType(1=Firefox, online / 2=phantomjs) ministry(6..20) fini(dd-mm-aaaa) ffin (dd-mm-aaaa)')
        sys.exit(1)

    pDT= int(sys.argv[1]) # TODO comprobar 1 ó 2
    pMin=sys.argv[2]        # TODO comprobar entre 6 y 20
    pFIni=sys.argv[3]        # TODO comprobar bien formada
    pFFin=sys.argv[4]        # TODO comprobar bien formada  y mayor que PFIni
 
  
    # Extrae las líneas de contratos de la página web
    contratos=Contratos(driverType=pDT, ministry=pMin, fini=pFIni,ffin=pFFin)
    listaContratos=[]

    # Envia  las líneas  de contratos para obtener los datos
    for row in contratos.expedientes:
        listaContratos.append(Contrato(row, contratos.ministry))
    
    #Graba cada uno de los contratos en BBDD    
    for contrato in listaContratos:
        contrato.grabarBD()
        
    
    
if __name__ == "__main__":
    sys.exit(main())
    

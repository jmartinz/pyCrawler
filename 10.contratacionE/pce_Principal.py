# coding=utf-8

# -*- coding: utf-8 -*-

import sys
import  datetime
import time 
from bs4 import BeautifulSoup
from pce_datos_contrato import Contrato
from pce_extrae_contratos import Contratos

log_file = "Principal.log"

def log2file(log_str):

    str2w = str(datetime.datetime.now()).split('.')[0] + " - " + log_str +"\n"
    f = open(log_file, 'a')
#    print(str2w,file=f)
    f.write(str2w)

    f.close()          

def main():
    
    nreggrabados=0
    
    if not len(sys.argv) == 5:
        print ('usage: pce_Principal.py  driverType(1=Firefox, online / 2=phantomjs) ministry(6..20) fini(dd-mm-aaaa) ffin (dd-mm-aaaa)')
        sys.exit(1)

    pDT= int(sys.argv[1]) # TODO comprobar 1 ó 2
    pMin=sys.argv[2]        # TODO comprobar entre 6 y 20
    pFIni=sys.argv[3]        # TODO comprobar bien formada
    pFFin=sys.argv[4]        # TODO comprobar bien formada  y mayor que PFIni
 
    # Inicia contador de tiempo
    inicio = time.time()
    regUpdated=0
    regRead=0

    # Extrae las líneas de contratos de la página web
    contratos=Contratos(driverType=pDT, ministry=pMin, fini=pFIni,ffin=pFFin)
    
    #Escribe el número de contratos seleccionados en la página
    log2file('Se han seleccionado '+ str(contratos.nContratos) +' contratos  en la PCE.')            
    
    listaContratos=[]
    # Envia  las líneas  de contratos para obtener los datos
    for row in contratos.expedientes:
        listaContratos.append(Contrato(row, contratos.ministry))
    
    #Graba cada uno de los contratos en BBDD    
    for contrato in listaContratos:
        nreggrabados += contrato.grabarBD()
        
    #Escribe el número de contratos grabados en BD
    log2file('Se han grabado '+ str(nreggrabados) +' contratos  en la BD.')         

        
    # Escribe el tiempo tardado    
    fin = time.time()
    tiempo_total = fin - inicio
    log2file('El proceso tardó :'+ str(tiempo_total) +' s')        
    
if __name__ == "__main__":
    sys.exit(main())
    

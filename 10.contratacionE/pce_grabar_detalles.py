# coding=utf-8

# -*- coding: utf-8 -*-


import sys
# piece os code from https://pythonadventures.wordpress.com/tag/ascii/
# in order to avoid error of type UnicodeEncodeError: 'ascii' codec can't encode character u'\xf3' in position 70: ordinal not in range(128)
reload(sys)
sys.setdefaultencoding("utf-8")
# end piece of code
import  datetime
import time 
import peewee     #  object-relational mapper 
from pce_db  import PceOrgano,  PceExpediente,  PceEstado,  PceTipoProcedimiento
from pce_datos_contrato import Contrato
from pce_extrae_detalle_contrato import detalleContrato
import traceback


log_file = "GrabarDetalles.log"

def log2file(log_str):

    str2w = str(datetime.datetime.now()).split('.')[0] + " - " + log_str +"\n"
    f = open(log_file, 'a')
#    print(str2w,file=f)
    f.write(str2w)

    f.close()      

def grabarDetalleBD(datos_contrato, detalles):    

    # comprueba si existe el estado de licitación. Si es así lee el Id, si no... lo crea
    try:
        id_estado = PceEstado.get(PceEstado.descripcion==detalles.estadoLic).id_estado
    except PceEstado.DoesNotExist:
        estado = PceEstado.create(descripcion = detalles.estadoLic)
        id_estado= estado.id_estado
        
    # comprueba si existe el procedimiento de licitación. Si es así lee el Id, si no... lo crea
    try:
        id_tipo_procedimiento = PceTipoProcedimiento.get(PceTipoProcedimiento.descripcion==detalles.procedimiento).id_tipo_procedimiento
    except PceTipoProcedimiento.DoesNotExist:
        procedimiento = PceTipoProcedimiento.create(descripcion = detalles.procedimiento)
        id_tipo_procedimiento= procedimiento.id_tipo_procedimiento
     
    # actualiza registro 
    q = PceExpediente.update(id_estado=id_estado,id_tipo_procedimiento=id_tipo_procedimiento).where(PceExpediente.id_expediente == datos_contrato.id_expediente)
    n = q.execute()
    
    return n

def main():
    
#    if not len(sys.argv) == 1:
#        print ('usage: pce_grabar_detalles.py ')
#        sys.exit(1)

    # Inicia contador de tiempo
    inicio = time.time()
    regUpdated=0
    regRead=0
    
    log2file('Inicio grabar detalles.' )
    
    #Escribe el número de registros leidos
    nunContSinDet = PceExpediente.select(PceExpediente.id_licitacion, PceExpediente.num_expediente, PceOrgano.descripcion).where(PceExpediente.id_estado >> None).count()
    log2file('Hay '+ str(nunContSinDet) +' contratos sin detalles.') 
    
    # Lee de la BD contratos sin detalles
    contSinDet = (PceExpediente
             .select(PceExpediente.id_licitacion, PceExpediente.num_expediente, PceOrgano.descripcion)
             .where(PceExpediente.id_estado >> None)
             .join(PceOrgano)
             .naive())
    

    
    # Para cada uno de ellos se leen los detalles y se graban en BD    
    for contrato in contSinDet:
        try:
            detalles=detalleContrato(numExpediente = contrato.num_expediente, OrgContratacion=contrato.descripcion, driverType=2)

            regRead += 1
        
            nreg = grabarDetalleBD(contrato, detalles)
            regUpdated += nreg
            log2file('Procesado expediente  '+ contrato.num_expediente + ' id: '+str(contrato.id_expediente))
        except:
            log2file('Error en expediente  '+ contrato.num_expediente + ' id: '+str(contrato.id_expediente))
            var = traceback.format_exc()
            log2file("Error inesperado"+ var)
  
    #Escribe el número de registros leidos
    log2file('Se han leido '+ str(regRead) +' registros de la BD.')
            
    #Escribe el número de registros actualizados
    log2file('Se han actualizado '+ str(regUpdated) +' registros de la BD.')       

    # Escribe el tiempo tardado    
    fin = time.time()
    tiempo_total = fin - inicio
    log2file('El proceso tardó :'+ str(tiempo_total) +' s')    
    
if __name__ == "__main__":
    sys.exit(main())
    

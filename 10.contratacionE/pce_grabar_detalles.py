# coding=utf-8

# -*- coding: utf-8 -*-


import sys
import peewee     #  object-relational mapper 
from pce_db  import PceOrgano,  PceExpediente,  PceEstado,  PceTipoProcedimiento
from pce_datos_contrato import Contrato
from pce_extrae_detalle_contrato import detalleContrato

  
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
    q.execute()

def main():
    
#    if not len(sys.argv) == 1:
#        print ('usage: pce_grabar_detalles.py ')
#        sys.exit(1)

    # Lee de la BD contratos sin detalles
    contSinDet = (PceExpediente
             .select(PceExpediente.id_expediente, PceExpediente.num_expediente, PceOrgano.descripcion)
             .where(PceExpediente.id_estado >> None)
             .join(PceOrgano)
             .naive())
    
    # Para cada uno de ellos se leen los detalles y se graban en BD    
    for contrato in contSinDet:
        detalles=detalleContrato(numExpediente = contrato.num_expediente, OrgContratacion=contrato.descripcion, driverType=2)

        grabarDetalleBD(contrato, detalles)
        
    
    
if __name__ == "__main__":
    sys.exit(main())
    

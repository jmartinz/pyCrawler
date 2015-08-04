import peewee     #  object-relational mapper 
from pce_db  import PceOrgano,  PceExpediente

query = (PceExpediente
         .select(PceExpediente.id_expediente, PceExpediente.num_expediente, PceOrgano.descripcion)
         .where(PceExpediente.id_estado >> None)
         .join(PceOrgano)
         .naive())
         
for line in query:
    print line.id_expediente,  line.num_expediente, line.descripcion

import peewee     #  object-relational mapper 
from pce_db  import PceOrgano,  PceExpediente

query = (PceExpediente
         .select(PceExpediente.id_expediente, PceExpediente.num_expediente, PceOrgano.descripcion)
         .join(PceOrgano)
         .naive())
         
for line in query:
    print line.id_expediente,  line.num_expediente, line.descripcion

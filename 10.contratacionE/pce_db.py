from peewee import *

database = MySQLDatabase('pce', **{'host': '127.0.0.1', 'password': 'reptiliano', 'user': 'pce'})

class UnknownField(object):
    pass

class BaseModel(Model):
    class Meta:
        database = database

class PceOrgano(BaseModel):
    descripcion = CharField(null=True)
    id_organo = PrimaryKeyField()
    url = CharField(null=True)

    class Meta:
        db_table = 'pce_organo'

class PceExpediente(BaseModel):
    desc_expediente = CharField(null=True)
    estado = CharField(null=True)
    fec_adj_prov = CharField(null=True)
    fec_adj_provisional = CharField(null=True)
    fec_adjudicacion = CharField(null=True)
    fec_formalizacion = CharField(null=True)
    fec_presentacion = CharField(null=True)
    id_expediente = PrimaryKeyField()
    id_organo = ForeignKeyField(db_column='id_organo', null=True, rel_model=PceOrgano, to_field='id_organo')
    importe = CharField(null=True)
    pce_expedientecol = CharField(null=True)
    tipo_contrato_1 = CharField(null=True)
    tipo_contrato_2 = CharField(null=True)

    class Meta:
        db_table = 'pce_expediente'

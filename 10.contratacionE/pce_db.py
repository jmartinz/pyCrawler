from peewee import *

database = MySQLDatabase('pce', **{'host': '127.0.0.1', 'password': 'pce', 'user': 'pce'})

class UnknownField(object):
    pass

class BaseModel(Model):
    class Meta:
        database = database

class PceMinisterio(BaseModel):
    Nombre = CharField(null=True)
    id_ministerio = PrimaryKeyField()
    Nombre_corto = CharField(null=True)

    class Meta:
        db_table = 'pce_ministerio'


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
    fec_adj_definitiva = CharField(null=True)
    fec_adjudicacion = CharField(null=True)
    fec_formalizacion = CharField(null=True)
    fec_presentacion = CharField(null=True)
    id_expediente = PrimaryKeyField()
    id_organo = ForeignKeyField(db_column='id_organo', null=True, rel_model=PceOrgano, to_field='id_organo')
    importe = CharField(null=True)
    num_expediente = CharField(null=True)
    tipo_contrato_1 = CharField(null=True)
    tipo_contrato_2 = CharField(null=True)
    id_ministerio = ForeignKeyField(db_column='id_ministerio', null=True, rel_model=PceMinisterio, to_field='id_ministerio')

    class Meta:
        db_table = 'pce_expediente'

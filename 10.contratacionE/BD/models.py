from peewee import *

database = MySQLDatabase('pce', **{'user': 'pce', 'password': 'pce'})

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

class PceMinisterio(BaseModel):
    nombre = CharField(db_column='Nombre', null=True)
    nombre_corto = CharField(db_column='Nombre_corto', null=True)
    id_ministerio = PrimaryKeyField()

    class Meta:
        db_table = 'pce_ministerio'

class PceEstado(BaseModel):
    descripcion = CharField(null=True)
    id_estado = PrimaryKeyField()

    class Meta:
        db_table = 'pce_estado'

class PceTipoProcedimiento(BaseModel):
    descripcion = CharField(null=True)
    id_tipo_procedimiento = PrimaryKeyField()

    class Meta:
        db_table = 'pce_tipo_procedimiento'

class PceExpediente(BaseModel):
    adjudicatario = CharField(null=True)
    codigocpv = CharField(null=True)
    desc_expediente = CharField(null=True)
    enlacelic = CharField(null=True)
    estado = CharField(null=True)
    id_estado = ForeignKeyField(db_column='id_estado', null=True, rel_model=PceEstado, to_field='id_estado')
    id_licitacion = PrimaryKeyField()
    id_ministerio = ForeignKeyField(db_column='id_ministerio', null=True, rel_model=PceMinisterio, to_field='id_ministerio')
    id_organo = ForeignKeyField(db_column='id_organo', null=True, rel_model=PceOrgano, to_field='id_organo')
    id_tipo_procedimiento = ForeignKeyField(db_column='id_tipo_procedimiento', null=True, rel_model=PceTipoProcedimiento, to_field='id_tipo_procedimiento')
    importe_adj = DecimalField(null=True)
    importe_base = DecimalField(null=True)
    num_expediente = CharField(null=True)
    numlicitadores = IntegerField(null=True)
    resultado = CharField(null=True)
    tipo_contrato_1 = CharField(null=True)
    tipo_contrato_2 = CharField(null=True)

    class Meta:
        db_table = 'pce_expediente'

class PceDocumento(BaseModel):
    documento = CharField(null=True)
    fecha = DateTimeField(null=True)
    id_licitacion = ForeignKeyField(db_column='id_licitacion', rel_model=PceExpediente, to_field='id_licitacion')
    tipo_documento = CharField()

    class Meta:
        db_table = 'pce_documento'
        primary_key = CompositeKey('id_licitacion', 'tipo_documento')

class PceFecha(BaseModel):
    fecha = DateField(null=True)
    id_licitacion = ForeignKeyField(db_column='id_licitacion', rel_model=PceExpediente, to_field='id_licitacion')
    tipo_fecha = CharField()

    class Meta:
        db_table = 'pce_fecha'
        primary_key = CompositeKey('id_licitacion', 'tipo_fecha')


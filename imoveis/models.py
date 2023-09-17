from base.models import BaseModel
from django.db import models
from base.custom_fields import CodigoField


class Imovel(BaseModel):

    SIM_NAO_CHOICES = (
        (True, 'Sim'),
        (False, 'Não'),
    )

    codigo_imovel = CodigoField(prefix='IMO-', primary_key=True, editable=False)
    limite_hospedes = models.IntegerField(default=1)
    quantidade_banheiros = models.IntegerField(default=0)
    aceita_animal_estimacao = models.BooleanField(default=False)
    valor_limpeza = models.FloatField(default=0)
    data_ativacao = models.DateField()

    def __str__(self):
        return self.codigo_imovel

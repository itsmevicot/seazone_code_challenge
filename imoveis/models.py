from base.models import BaseModel
from django.db import models
from base.custom_fields import CodigoField


class Imovel(BaseModel):
    codigo_imovel = CodigoField(prefix='IMO-', editable=False, unique=True)
    limite_hospedes = models.PositiveIntegerField(default=1)
    quantidade_banheiros = models.PositiveIntegerField(default=0)
    aceita_animal_estimacao = models.BooleanField(default=False)
    valor_limpeza = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    data_ativacao = models.DateField()

    def __str__(self):
        return self.codigo_imovel

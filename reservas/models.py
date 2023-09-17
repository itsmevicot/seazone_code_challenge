from base.models import BaseModel
from django.db import models
from base.custom_fields import CodigoField


class Reserva(BaseModel):
    codigo_reserva = CodigoField(prefix='RES-', primary_key=True, editable=False)
    anuncio = models.ForeignKey('anuncios.Anuncio', on_delete=models.PROTECT, related_name='reservas')
    data_checkin = models.DateTimeField()
    data_checkout = models.DateTimeField()
    preco_total = models.FloatField()
    comentario = models.CharField(max_length=500, blank=True)
    numero_hospedes = models.IntegerField()

    def __str__(self):
        return self.codigo_reserva

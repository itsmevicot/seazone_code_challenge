from base.models import BaseModel
from django.db import models
from base.custom_fields import CodigoField


class Reserva(BaseModel):
    codigo_reserva = CodigoField(prefix='RES-', editable=False, unique=True)
    anuncio = models.ForeignKey('anuncios.Anuncio', on_delete=models.PROTECT, related_name='reservas')
    data_checkin = models.DateField()
    data_checkout = models.DateField()
    preco_total = models.DecimalField(decimal_places=2, max_digits=10)
    comentario = models.CharField(max_length=255)
    numero_hospedes = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.codigo_reserva

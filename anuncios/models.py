from base.models import BaseModel
from django.db import models


class Anuncio(BaseModel):
    imovel = models.ForeignKey('imoveis.Imovel', on_delete=models.PROTECT, related_name='anuncios')
    nome_plataforma = models.CharField(max_length=50)
    taxa_plataforma = models.FloatField(default=0)

    def __str__(self):
        return self.nome_plataforma

from base.models import BaseModel
from django.db import models


class Anuncio(BaseModel):
    imovel = models.ForeignKey('imoveis.Imovel', on_delete=models.PROTECT, related_name='anuncios')
    nome_plataforma = models.CharField(max_length=50)
    taxa_plataforma = models.FloatField(default=0)

    @property
    def descricao(self):
        return f"{self.imovel.codigo_imovel} - {self.nome_plataforma}"

    def __str__(self):
        return self.descricao

    class Meta:
        unique_together = ('imovel', 'nome_plataforma')

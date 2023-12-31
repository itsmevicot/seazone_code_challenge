from base.models import BaseModel
from django.db import models


class Anuncio(BaseModel):
    imovel = models.ForeignKey('imoveis.Imovel', on_delete=models.PROTECT, related_name='anuncios')
    nome_plataforma = models.CharField(max_length=50)
    taxa_plataforma = models.DecimalField(decimal_places=2, max_digits=10, default=0)

    @property
    def descricao(self):
        return f"{self.nome_plataforma} - {self.imovel.codigo_imovel}"

    def __str__(self):
        return self.descricao

    class Meta:
        unique_together = ('imovel', 'nome_plataforma')

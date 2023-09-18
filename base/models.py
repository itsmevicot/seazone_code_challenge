from django.db import models
from base.manager import AtivoManager


class BaseModel(models.Model):
    objects = AtivoManager()

    criado_em = models.DateTimeField(auto_now_add=True, editable=False)
    atualizado_em = models.DateTimeField(auto_now=True, editable=False)
    ativo = models.BooleanField(default=True, editable=False)

    class Meta:
        abstract = True

    def delete(self):
        self.ativo = False
        self.save()

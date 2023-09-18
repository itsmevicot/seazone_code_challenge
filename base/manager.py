from django.db import models


class AtivoManager(models.Manager):
    def ativos(self):
        return self.model.objects.filter(ativo=True)

    def inativos(self):
        return self.model.objects.filter(ativo=False)

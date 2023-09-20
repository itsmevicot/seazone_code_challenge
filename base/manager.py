from django.db import models


class AtivoManager(models.Manager):
    def ativos(self, **kwargs):
        if kwargs.get('ativo'):
            raise ValueError('Não é possível sobrescrever o valor de ativo.')
        return self.model.objects.filter(ativo=True, **kwargs)

    def inativos(self, **kwargs):
        if kwargs.get('ativo'):
            raise ValueError('Não é possível sobrescrever o valor de ativo.')
        return self.model.objects.filter(ativo=False, **kwargs)


import random
import string
from django.db import models


class CodigoField(models.CharField):
    def __init__(self, prefix='', *args, **kwargs):
        self.prefix = prefix
        kwargs['max_length'] = len(prefix) + 12
        super().__init__(*args, **kwargs)

    def gerar_codigo(self):
        """

        Gera um código alfanumérico de 12 dígitos precedido de um prefixo.

        """
        return self.prefix + ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))

    def deconstruct(self):
        """
        Desconstrói o campo personalizado para as migrações do Django.

        Este método é necessário para que as migrações do Django saibam como lidar
        com campos personalizados.

        A principal personalização aqui é para excluir o argumento 'max_length' (que é
        computado com base no prefixo) e adicionar o 'prefix' ao dicionário kwargs.

        """
        name, path, args, kwargs = super().deconstruct()
        if 'max_length' in kwargs:
            del kwargs['max_length']
        kwargs['prefix'] = self.prefix
        return name, path, args, kwargs

    def pre_save(self, model_instance, add):
        """
        Realiza o pré-save para evitar códigos iguais e verifica a instância correta da model que utiliza a função
        para gerar o código.

        """
        valor = getattr(model_instance, self.attname)
        if not valor:
            while True:
                codigo = self.gerar_codigo()
                if not model_instance.__class__.objects.filter(**{self.attname: codigo}).exists():
                    break
            valor = codigo
            setattr(model_instance, self.attname, valor)
        return valor

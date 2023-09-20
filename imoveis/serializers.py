from rest_framework import serializers
from imoveis.models import Imovel


class ImovelSerializer(serializers.ModelSerializer):
    limite_hospedes = serializers.IntegerField(
        min_value=1,
        required=False,
        error_messages={
            'min_value': 'O limite de hóspedes deve ser maior ou igual a 1.'
        }
    )
    quantidade_banheiros = serializers.IntegerField(
        min_value=0,
        required=False,
        error_messages={
            'min_value': 'A quantidade de banheiros deve ser maior ou igual a 0.'
        }
    )
    aceita_animal_estimacao = serializers.BooleanField(required=False, default=None, allow_null=True)

    valor_limpeza = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=0,
        required=False,
        error_messages={
            'min_value': 'O valor da limpeza deve ser maior ou igual a 0.'
        }
    )
    data_ativacao = serializers.DateField(input_formats=['%d/%m/%Y'], required=False)

    class Meta:
        model = Imovel
        fields = '__all__'

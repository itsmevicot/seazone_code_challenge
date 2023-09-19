from rest_framework import serializers
from imoveis.models import Imovel


class SimNaoSerializer(serializers.BooleanField):
    def to_representation(self, value):
        return 'Sim' if value else 'Não'

    def to_internal_value(self, data):
        if data == 'Sim':
            return True
        elif data == 'Não':
            return False
        else:
            return super(SimNaoSerializer, self).to_internal_value(data)


class ImovelSerializer(serializers.ModelSerializer):
    aceita_animal_estimacao = SimNaoSerializer()

    class Meta:
        model = Imovel
        fields = '__all__'


class ImovelQuerySerializer(serializers.Serializer):
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
    aceita_animal_estimacao = serializers.CharField(required=False, default=None)
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

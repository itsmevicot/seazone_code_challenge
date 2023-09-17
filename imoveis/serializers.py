from rest_framework import serializers
from imoveis.models import Imovel


class SimNaoChoices(serializers.BooleanField):
    def to_representation(self, value):
        return 'Sim' if value else 'Não'

    def to_internal_value(self, data):
        if data == 'Sim':
            return True
        elif data == 'Não':
            return False
        else:
            return super(SimNaoChoices, self).to_internal_value(data)

class ImovelSerializer(serializers.ModelSerializer):
    aceita_animal_estimacao = SimNaoChoices()

    class Meta:
        model = Imovel
        fields = '__all__'

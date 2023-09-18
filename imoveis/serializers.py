import decimal
from datetime import date
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

    def validate_limite_hospedes(self, limite_hospedes: int):
        if limite_hospedes < 1:
            raise serializers.ValidationError({
                'limite_hospedes': 'O limite de hóspedes deve ser maior ou igual a 1.'})
        return limite_hospedes

    def validate_valor_limpeza(self, valor_limpeza: decimal):
        if valor_limpeza < 0:
            raise serializers.ValidationError({
                'valor_limpeza': 'O valor de limpeza deve ser maior ou igual a 0.'})
        return valor_limpeza

    def validate_data_ativacao(self, data_ativacao: date):
        if data_ativacao < date.today():
            raise serializers.ValidationError({
                'data_ativacao': 'A data de ativação deve ser maior ou igual a data atual.'
            })
        return data_ativacao

    class Meta:
        model = Imovel
        fields = '__all__'

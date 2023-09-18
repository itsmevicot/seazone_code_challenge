import decimal
from rest_framework import serializers
from anuncios.models import Anuncio
from reservas.models import Reserva


class ReservaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reserva
        fields = '__all__'

    def validate(self, data):
        data_checkin = data['data_checkin']
        data_checkout = data['data_checkout']

        if data_checkin == data_checkout:
            raise serializers.ValidationError({
                'data_checkin': 'A data de check-in e check-out não podem ser iguais.',
                'data_checkout': 'A data de check-in e check-out não podem ser iguais.'
            })

        if data_checkin > data_checkout:
            raise serializers.ValidationError({
                'data_checkin': 'A data de check-in não pode ser posterior à data de check-out.'
            })

        reservas_sobrepostas = Reserva.objects.filter(
            anuncio=data['anuncio'],
            ativo=True,
            data_checkout__gt=data_checkin,
            data_checkin__lt=data_checkout
        )

        if reservas_sobrepostas.exists():
            raise serializers.ValidationError({
                'data_checkin': 'As datas selecionadas se sobrepõem a uma reserva existente.',
                'data_checkout': 'As datas selecionadas se sobrepõem a uma reserva existente.'
            })

        return data

    def validate_numero_hospedes(self, numero_hospedes: int):
        anuncio = Anuncio.objects.get(
            pk=self.initial_data['anuncio'])

        if numero_hospedes < 1:
            raise serializers.ValidationError({
                'numero_hospedes': 'O número de hóspedes deve ser maior ou igual a 1.'
            })
        elif numero_hospedes > anuncio.imovel.limite_hospedes:
            raise serializers.ValidationError({
                'numero_hospedes': f'O número de hóspedes não pode exceder o limite do imóvel: {anuncio.imovel.limite_hospedes}'
            })
        return numero_hospedes

    def validate_preco_total(self, preco_total: decimal):
        if preco_total < 0:
            raise serializers.ValidationError({
                'preco_total': 'O preço total deve ser maior ou igual a 0.'
            })
        return preco_total

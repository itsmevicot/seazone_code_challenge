import decimal
from rest_framework import serializers
from anuncios.models import Anuncio
from reservas.models import Reserva


class ReservaSerializer(serializers.ModelSerializer):
    def validate(self, data):
        data_checkin = data['data_checkin']
        data_checkout = data['data_checkout']

        if data_checkin >= data_checkout:
            raise serializers.ValidationError('A data de Check-in não pode ser maior ou igual a data de Check-out.')

        reservas_sobrepostas = Reserva.objects.filter(
            anuncio=data['anuncio'],
            ativo=True,
            data_checkout__gt=data_checkin,
            data_checkin__lt=data_checkout
        )

        if reservas_sobrepostas.exists():
            raise serializers.ValidationError({
               'data_checkin/data_checkout': 'Já existe uma reserva para essas datas neste imóvel.'
            })

        return data

    class Meta:
        model = Reserva
        fields = '__all__'


class ReservaQuerySerializer(serializers.Serializer):
    anuncio = serializers.PrimaryKeyRelatedField(queryset=Anuncio.objects.ativos(), required=False)
    imovel = serializers.CharField(required=False)
    data_checkin = serializers.DateField(input_formats=['%d/%m/%Y'], required=False)
    data_checkout = serializers.DateField(input_formats=['%d/%m/%Y'], required=False)
    preco_total = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=0,
        required=False,
        error_messages={
            'min_value': 'O preço total deve ser maior ou igual a 0.'
        }
    )
    comentario = serializers.CharField(required=False)
    numero_hospedes = serializers.IntegerField(
        min_value=1,
        required=False,
        error_messages={
            'min_value': 'O número de hóspedes deve ser maior ou igual a 1.'
        }
    )

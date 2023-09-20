from rest_framework import serializers
from anuncios.models import Anuncio
from reservas.models import Reserva


class ReservaSerializer(serializers.ModelSerializer):
    anuncio = serializers.PrimaryKeyRelatedField(queryset=Anuncio.objects.ativos())
    data_checkin = serializers.DateField(input_formats=['%d/%m/%Y'])
    data_checkout = serializers.DateField(input_formats=['%d/%m/%Y'])
    preco_total = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=0,
        error_messages={'min_value': 'O preço total deve ser maior ou igual a 0.'}
    )
    comentario = serializers.CharField()
    numero_hospedes = serializers.IntegerField(
        min_value=1,
        error_messages={'min_value': 'O número de hóspedes deve ser maior ou igual a 1.'}
    )

    def validate(self, data):
        data_checkin = data.get('data_checkin')
        data_checkout = data.get('data_checkout')
        numero_hospedes = data.get('numero_hospedes')
        anuncio = data.get('anuncio')
        imovel = data.get('anuncio').imovel

        if data_checkin >= data_checkout:
            raise serializers.ValidationError({
                'data_checkin': 'A data de Check-in não pode ser maior ou igual a data de Check-out.',
                'data_checkout': 'A data de Check-out não pode ser menor ou igual a data de Check-in.'
            })

        if numero_hospedes > imovel.limite_hospedes:
            raise serializers.ValidationError({
                'numero_hospedes': f'O número de hóspedes excede o limite de hóspedes: {imovel.limite_hospedes}'
            })

        reservas_sobrepostas = Reserva.objects.ativos(
            anuncio=anuncio.pk,
            data_checkout__gt=data_checkin,
            data_checkin__lt=data_checkout
        )

        if reservas_sobrepostas.exists():
            raise serializers.ValidationError({
                'data_checkin': 'Já existe uma reserva para essas datas neste imóvel.',
                'data_checkout': 'Já existe uma reserva para essas datas neste imóvel.'
            })

        return data

    class Meta:
        model = Reserva
        fields = '__all__'


class ReservaQuerySerializer(serializers.Serializer):
    codigo_reserva = serializers.CharField(required=False)
    anuncio = serializers.PrimaryKeyRelatedField(queryset=Anuncio.objects.ativos(), required=False)
    imovel = serializers.CharField(required=False)
    data_checkin = serializers.DateField(input_formats=['%d/%m/%Y'], required=False)
    data_checkout = serializers.DateField(input_formats=['%d/%m/%Y'], required=False)
    preco_total = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=0,
        required=False,
        error_messages={'min_value': 'O preço total deve ser maior ou igual a 0.'}
    )
    comentario = serializers.CharField(required=False)
    numero_hospedes = serializers.IntegerField(
        min_value=1,
        required=False,
        error_messages={'min_value': 'O número de hóspedes deve ser maior ou igual a 1.'}
    )

    def validate(self, data):
        data_checkin = data.get('data_checkin')
        data_checkout = data.get('data_checkout')

        if data_checkin and data_checkout and data_checkin >= data_checkout:
            raise serializers.ValidationError('A data de Check-in não pode ser maior ou igual a data de Check-out.')

        return data

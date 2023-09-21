from rest_framework import serializers
from anuncios.models import Anuncio
from reservas.exceptions import CheckinLaterThanCheckoutException, ExceedGuestLimitException, OverlappingBookingException
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
            raise CheckinLaterThanCheckoutException()

        if numero_hospedes > imovel.limite_hospedes:
            raise ExceedGuestLimitException(imovel.limite_hospedes)

        reservas_sobrepostas = Reserva.objects.ativos(
            anuncio=anuncio.pk,
            data_checkout__gt=data_checkin,
            data_checkin__lt=data_checkout
        )

        if reservas_sobrepostas.exists():
            raise OverlappingBookingException()

        return data

    class Meta:
        model = Reserva
        fields = '__all__'


class ReservaQuerySerializer(serializers.Serializer):
    codigo_reserva = serializers.CharField(required=False)
    anuncio = serializers.PrimaryKeyRelatedField(queryset=Anuncio.objects.ativos(), required=False)
    codigo_imovel = serializers.CharField(required=False)
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
            raise CheckinLaterThanCheckoutException()

        return data

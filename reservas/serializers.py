from rest_framework import serializers
from reservas.models import Reserva


class ReservaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reserva
        fields = '__all__'

    def validate(self, data):
        if data['data_checkin'] > data['data_checkout']:
            raise serializers.ValidationError({
                'data_checkin': 'A data de check-in não pode ser posterior à data de check-out.'
            })
        return data

from rest_framework import serializers
from anuncios.models import Anuncio


class AnuncioSerializer(serializers.ModelSerializer):
    taxa_plataforma = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=0,
        error_messages={
            'min_value': 'A taxa da plataforma não pode ser negativa.'
        }
    )

    class Meta:
        model = Anuncio
        fields = '__all__'


class AnuncioQuerySerializer(serializers.Serializer):
    imovel = serializers.CharField(
        required=False,
    )

    nome_plataforma = serializers.CharField(
        required=False,
    )

    taxa_plataforma = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=0,
        required=False,
        error_messages={
            'min_value': 'A taxa da plataforma não pode ser negativa.'
        }
    )

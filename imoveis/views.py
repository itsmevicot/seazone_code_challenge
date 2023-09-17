from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from .models import Imovel
from .serializers import ImovelSerializer
from datetime import datetime


class ImovelList(generics.ListCreateAPIView):
    model = Imovel
    serializer_class = ImovelSerializer

    def get_queryset(self):
        queryset = Imovel.objects.all()

        limite_hospedes = self.request.query_params.get('limite_hospedes')
        quantidade_banheiros = self.request.query_params.get('quantidade_banheiros')
        aceita_animal_estimacao = self.request.query_params.get('aceita_animal_estimacao')
        valor_limpeza = self.request.query_params.get('valor_limpeza')
        data_ativacao = self.request.query_params.get('data_ativacao')

        if limite_hospedes:
            queryset = queryset.filter(limite_hospedes__gte=limite_hospedes)

        if quantidade_banheiros:
            queryset = queryset.filter(quantidade_banheiros__gte=quantidade_banheiros)

        if aceita_animal_estimacao:
            queryset = queryset.filter(aceita_animal_estimacao=aceita_animal_estimacao.lower() in ['true', '1'])

        if valor_limpeza:
            queryset = queryset.filter(valor_limpeza__lte=valor_limpeza)

        if data_ativacao:
            try:
                data_formatada = datetime.strptime(data_ativacao, '%d/%m/%Y').date()
                queryset = queryset.filter(data_ativacao=data_formatada)
            except ValueError:
                raise ValidationError('Data de Ativação inválida. O formato deve ser DD/MM/YYYY (ex: 12/03/2023)')

        return queryset

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('limite_hospedes', openapi.IN_QUERY,
                              description="Limite de hóspedes. Filtra por valores maiores ou iguais ao informado.",
                              type=openapi.TYPE_INTEGER,
                              required=False),
            openapi.Parameter('quantidade_banheiros', openapi.IN_QUERY,
                              description="Quantidade de banheiros. Filtra por valores maiores ou iguais ao informado.",
                              type=openapi.TYPE_INTEGER,
                              required=False),
            openapi.Parameter('aceita_animal_estimacao', openapi.IN_QUERY,
                              description="Aceita animais de estimação",
                              type=openapi.TYPE_BOOLEAN,
                              required=False),
            openapi.Parameter('valor_limpeza', openapi.IN_QUERY,
                              description="Valor da limpeza. Filtra por valores menores ou iguais ao informado.",
                              type=openapi.TYPE_NUMBER,
                              format=openapi.FORMAT_FLOAT,
                              required=False,
                              example=55.38),
            openapi.Parameter('data_ativacao', openapi.IN_QUERY,
                              description="Data de ativação do imóvel (formato DD/MM/YYYY).",
                              type=openapi.TYPE_STRING,
                              required=False,
                              example="15/06/2023"),
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class ImovelDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Imovel.objects.all()
    serializer_class = ImovelSerializer

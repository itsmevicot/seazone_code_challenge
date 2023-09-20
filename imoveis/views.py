from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from .models import Imovel
from .serializers import ImovelSerializer


class ImovelList(generics.ListCreateAPIView):
    """
    Endpoint para listar e criar imóveis.
    """
    model = Imovel
    serializer_class = ImovelSerializer

    def get_queryset(self):
        queryset = Imovel.objects.ativos()
        query_serializer = ImovelSerializer(data=self.request.query_params)
        query_serializer.is_valid(raise_exception=True)
        validated_data = query_serializer.validated_data

        if validated_data.get('limite_hospedes'):
            queryset = queryset.filter(limite_hospedes__gte=validated_data['limite_hospedes']).order_by('limite_hospedes')

        if validated_data.get('quantidade_banheiros'):
            queryset = queryset.filter(quantidade_banheiros__gte=validated_data['quantidade_banheiros']).order_by('quantidade_banheiros')

        if validated_data.get('aceita_animal_estimacao') is not None:
            queryset = queryset.filter(aceita_animal_estimacao=validated_data['aceita_animal_estimacao']).order_by('aceita_animal_estimacao')

        if validated_data.get('valor_limpeza'):
            queryset = queryset.filter(valor_limpeza__lte=validated_data['valor_limpeza']).order_by('valor_limpeza')

        if validated_data.get('data_ativacao'):
            queryset = queryset.filter(data_ativacao=validated_data['data_ativacao']).order_by('data_ativacao')

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
        response = super(ImovelList, self).list(request, *args, **kwargs)
        return response


class ImovelDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Endpoint para recuperar, atualizar e deletar imóveis.
    """
    queryset = Imovel.objects.ativos()
    serializer_class = ImovelSerializer

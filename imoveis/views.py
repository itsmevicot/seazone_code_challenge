from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from .models import Imovel
from .serializers import ImovelSerializer, ImovelQuerySerializer


class ImovelList(generics.ListCreateAPIView):
    """
    Endpoint para listar e criar imóveis.
    """
    model = Imovel
    serializer_class = ImovelSerializer

    def get_queryset(self):
        queryset = Imovel.objects.ativos()

        query_serializer = ImovelQuerySerializer(data=self.request.query_params)
        query_serializer.is_valid(raise_exception=True)
        validated_data = query_serializer.validated_data

        if 'limite_hospedes' in validated_data:
            queryset = queryset.filter(limite_hospedes__gte=validated_data['limite_hospedes']).order_by('limite_hospedes')

        if 'quantidade_banheiros' in validated_data:
            queryset = queryset.filter(quantidade_banheiros__gte=validated_data['quantidade_banheiros']).order_by('quantidade_banheiros')

        aceita_animal = validated_data.get('aceita_animal_estimacao')
        if aceita_animal:
            if aceita_animal.lower() in ['true', '1']:
                queryset = queryset.filter(aceita_animal_estimacao=True)
            elif aceita_animal.lower() in ['false', '0']:
                queryset = queryset.filter(aceita_animal_estimacao=False)

        if 'valor_limpeza' in validated_data:
            queryset = queryset.filter(valor_limpeza__lte=validated_data['valor_limpeza']).order_by('valor_limpeza')

        if 'data_ativacao' in validated_data:
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

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from anuncios.models import Anuncio
from anuncios.serializers import AnuncioSerializer, AnuncioQuerySerializer


class AnuncioList(generics.ListCreateAPIView):
    """
    Endpoint para listar e criar anúncios.
    """
    model = Anuncio
    serializer_class = AnuncioSerializer

    def get_queryset(self):
        queryset = Anuncio.objects.ativos()

        query_serializer = AnuncioQuerySerializer(data=self.request.query_params)
        query_serializer.is_valid(raise_exception=True)
        validated_data = query_serializer.validated_data


        if 'codigo_imovel' in validated_data:
            queryset = queryset.filter(imovel__codigo_imovel=validated_data['codigo_imovel'])
        if 'nome_plataforma' in validated_data:
            queryset = queryset.filter(nome_plataforma__icontains=validated_data['nome_plataforma'])
        if 'taxa_plataforma' in validated_data:
            queryset = queryset.filter(taxa_plataforma__lte=validated_data['taxa_plataforma'])

        return queryset

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('codigo_imovel', openapi.IN_QUERY,
                                description="Código do imóvel.",
                                type=openapi.TYPE_STRING,
                                required=False,
                                example='IMO-000000000001'),
            openapi.Parameter('nome_plataforma', openapi.IN_QUERY,
                                description="Nome da plataforma.",
                                type=openapi.TYPE_STRING,
                                required=False,
                                example='Airbnb'),
            openapi.Parameter('taxa_plataforma', openapi.IN_QUERY,
                                description="Taxa da plataforma. Filtra por valores menores ou iguais ao informado.",
                                type=openapi.TYPE_NUMBER,
                                required=False,
                                example=0.3),
        ]
    )
    def get(self, request, *args, **kwargs):
        response = super(AnuncioList, self).list(request, *args, **kwargs)
        return response


class AnuncioDetail(generics.RetrieveUpdateAPIView):
    """
    Endpoint para recuperar e atualizar anúncios.
    """
    queryset = Anuncio.objects.ativos()
    serializer_class = AnuncioSerializer

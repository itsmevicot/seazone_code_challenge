from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.response import Response
from anuncios.models import Anuncio
from anuncios.serializers import AnuncioSerializer


class AnuncioList(generics.ListCreateAPIView):
    """
    Endpoint para listar e criar anúncios.
    """
    model = Anuncio
    serializer_class = AnuncioSerializer

    def get_queryset(self):
        queryset = Anuncio.objects.ativos()

        codigo_imovel = self.request.query_params.get('codigo_imovel')
        nome_plataforma = self.request.query_params.get('nome_plataforma')
        taxa_plataforma = self.request.query_params.get('taxa_plataforma')

        if codigo_imovel:
            queryset = queryset.filter(imovel__codigo_imovel=codigo_imovel)
        if nome_plataforma:
            queryset = queryset.filter(nome_plataforma__icontains=nome_plataforma)
        if taxa_plataforma:
            queryset = queryset.filter(taxa_plataforma__lte=taxa_plataforma)

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
        if not response.data:
            return Response(status=status.HTTP_204_NO_CONTENT)
        return response


class AnuncioDetail(generics.RetrieveUpdateAPIView):
    """
    Endpoint para recuperar e atualizar anúncios.
    """
    queryset = Anuncio.objects.ativos()
    serializer_class = AnuncioSerializer

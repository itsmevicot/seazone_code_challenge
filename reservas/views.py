from django.db.models import Q
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from reservas.models import Reserva
from reservas.serializers import ReservaSerializer, ReservaQuerySerializer


reserva_request_body = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'data_checkin': openapi.Schema(type=openapi.TYPE_STRING, example="21/01/2024", format="date"),
        'data_checkout': openapi.Schema(type=openapi.TYPE_STRING, example="03/02/2024", format="date"),
        'preco_total': openapi.Schema(type=openapi.TYPE_NUMBER, example=0, format=openapi.FORMAT_DECIMAL),
        'comentario': openapi.Schema(type=openapi.TYPE_STRING, example="Acomodação excelente!"),
        'numero_hospedes': openapi.Schema(type=openapi.TYPE_INTEGER, example=2),
        'anuncio': openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
    }
)


class ReservaList(generics.ListCreateAPIView):
    """
    Endpoint para listar e criar reservas.
    """
    model = Reserva
    serializer_class = ReservaSerializer

    def get_queryset(self):
        queryset = Reserva.objects.ativos()

        query_serializer = ReservaQuerySerializer(data=self.request.query_params)
        query_serializer.is_valid(raise_exception=True)
        validated_data = query_serializer.validated_data

        if validated_data.get('imovel'):
            queryset = queryset.filter(anuncio__imovel__codigo_imovel=validated_data['imovel'])

        if validated_data.get('anuncio'):
            queryset = queryset.filter(anuncio=validated_data['anuncio'])

        if validated_data.get('data_checkin') and validated_data.get('data_checkout'):
            data_checkin = validated_data['data_checkin']
            data_checkout = validated_data['data_checkout']

            if data_checkin >= data_checkout:
                raise ValidationError('A data de Check-in não pode ser maior ou igual a data de Check-out.')

            queryset = queryset.filter(
                Q(data_checkin__range=(data_checkin, data_checkout)) |
                Q(data_checkout__range=(data_checkin, data_checkout)) |
                Q(data_checkin__lte=data_checkin, data_checkout__gte=data_checkout)
            )

        elif validated_data.get('data_checkin'):
            queryset = queryset.filter(data_checkin=validated_data['data_checkin'])

        elif validated_data.get('data_checkout'):
            queryset = queryset.filter(data_checkout=validated_data['data_checkout'])

        if validated_data.get('preco_total'):
            queryset = queryset.filter(preco_total__lte=validated_data['preco_total'])

        if validated_data.get('comentario'):
            queryset = queryset.filter(comentario__icontains=validated_data['comentario'])

        if validated_data.get('numero_hospedes'):
            queryset = queryset.filter(numero_hospedes__lte=validated_data['numero_hospedes'])

        if validated_data.get('codigo_reserva'):
            queryset = queryset.filter(codigo_reserva=validated_data['codigo_reserva'])

        return queryset

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('codigo_reserva', openapi.IN_QUERY,
                              description="Filtro pelo código da reserva.",
                              type=openapi.TYPE_STRING,
                              required=False,
                              example='RES-8EQOO73ROF1'),
            openapi.Parameter('imovel', openapi.IN_QUERY,
                              description="Filtro pelo código do imóvel.",
                              type=openapi.TYPE_STRING,
                              required=False,
                              example='IMO-O8EQOO73ROF1'),
            openapi.Parameter('anuncio', openapi.IN_QUERY,
                              description="Filtro pelo código do anúncio.",
                              type=openapi.TYPE_STRING,
                              required=False),
            openapi.Parameter('data_checkin', openapi.IN_QUERY,
                              description="Filtro pela data exata de check-in ou início de um intervalo no formato DD/MM/YYYY. Usado em combinação com 'data_checkout' para intervalos.",
                              type=openapi.TYPE_STRING,
                              required=False,
                              example='01/10/2023'),
            openapi.Parameter('data_checkout', openapi.IN_QUERY,
                              description="Filtro pela data exata de check-out ou fim de um intervalo no formato DD/MM/YYYY. Usado em combinação com 'data_checkin' para intervalos.",
                              type=openapi.TYPE_STRING,
                              required=False,
                              example='10/10/2023'),
            openapi.Parameter('preco_total', openapi.IN_QUERY,
                              description="Filtro pelo preço total (até o valor indicado).",
                              type=openapi.TYPE_NUMBER,
                              format=openapi.FORMAT_FLOAT,
                              required=False,
                              example='1500.00'),
            openapi.Parameter('comentario', openapi.IN_QUERY,
                              description="Busca parcial no campo de comentários.",
                              type=openapi.TYPE_STRING,
                              required=False,
                              example='Acomodação excelente!'),
            openapi.Parameter('numero_hospedes', openapi.IN_QUERY,
                              description="Filtro pelo número de hóspedes (até o valor indicado).",
                              type=openapi.TYPE_INTEGER,
                              required=False,
                              example=3),
        ]
    )
    def get(self, request, *args, **kwargs):
        response = super(ReservaList, self).list(request, *args, **kwargs)
        return response

    @swagger_auto_schema(
        request_body=reserva_request_body,
    )
    def post(self, request, *args, **kwargs):
        response = super(ReservaList, self).create(request, *args, **kwargs)
        return response


class ReservaDetail(generics.RetrieveDestroyAPIView):
    """
    Endpoint para recuperar e deletar reservas.
    """
    queryset = Reserva.objects.ativos()
    serializer_class = ReservaSerializer

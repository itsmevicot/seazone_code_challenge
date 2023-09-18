from django.db.models import Q
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from reservas.models import Reserva
from reservas.serializers import ReservaSerializer
from datetime import datetime


class ReservaList(generics.ListCreateAPIView):
    """
    Endpoint para listar e criar reservas.
    """
    model = Reserva
    serializer_class = ReservaSerializer

    def get_queryset(self):
        queryset = Reserva.objects.ativos()

        anuncio = self.request.query_params.get('anuncio')
        data_checkin = self.request.query_params.get('data_checkin')
        data_checkout = self.request.query_params.get('data_checkout')
        preco_total = self.request.query_params.get('preco_total')
        comentario = self.request.query_params.get('comentario')
        numero_hospedes = self.request.query_params.get('numero_hospedes')

        if anuncio:
            queryset = queryset.filter(anuncio__pk=anuncio)

        data_formatada_checkin = None
        data_formatada_checkout = None

        if data_checkin:
            try:
                data_formatada_checkin = datetime.strptime(data_checkin, '%d/%m/%Y').date()
            except ValueError:
                raise ValidationError('Data de Check-in inválida. O formato deve ser DD/MM/YYYY (ex: 01/10/2023)')

        if data_checkout:
            try:
                data_formatada_checkout = datetime.strptime(data_checkout, '%d/%m/%Y').date()
            except ValueError:
                raise ValidationError('Data de Check-out inválida. O formato deve ser DD/MM/YYYY (ex: 10/10/2023)')

        if data_formatada_checkin and data_formatada_checkout:
            if data_formatada_checkin > data_formatada_checkout:
                raise ValidationError('A data de Check-in não pode ser maior que a data de Check-out.')
            queryset = queryset.filter(
                Q(data_checkin__range=(data_formatada_checkin, data_formatada_checkout)) |
                Q(data_checkout__range=(data_formatada_checkin, data_formatada_checkout)) |
                Q(data_checkin__lte=data_formatada_checkin, data_checkout__gte=data_formatada_checkout)
            )
        elif data_formatada_checkin:
            queryset = queryset.filter(data_checkin=data_formatada_checkin)
        elif data_formatada_checkout:
            queryset = queryset.filter(data_checkout=data_formatada_checkout)

        if preco_total:
            queryset = queryset.filter(preco_total__lte=preco_total)
        if comentario:
            queryset = queryset.filter(comentario__icontains=comentario)
        if numero_hospedes:
            queryset = queryset.filter(numero_hospedes__lte=numero_hospedes)

        return queryset

    @swagger_auto_schema(
        manual_parameters=[
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
        if not response.data:
            return Response(status=status.HTTP_204_NO_CONTENT)
        return response


class ReservaDetail(generics.RetrieveDestroyAPIView):
    """
    Endpoint para recuperar e deletar reservas.
    """
    queryset = Reserva.objects.ativos()
    serializer_class = ReservaSerializer

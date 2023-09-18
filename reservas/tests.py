from rest_framework.test import APITestCase
from imoveis.models import Imovel
from reservas.models import Reserva
from anuncios.models import Anuncio
from reservas.serializers import ReservaSerializer
from rest_framework import status
from django.urls import reverse
from datetime import date, timedelta


class ReservaViewTestCase(APITestCase):
    def setUp(self):
        self.imovel = Imovel.objects.create(
            limite_hospedes=4,
            quantidade_banheiros=2,
            aceita_animal_estimacao=True,
            valor_limpeza=100.0,
            data_ativacao=date.today()
        )
        self.anuncio = Anuncio.objects.create(
            imovel=self.imovel,
            nome_plataforma="Airbnb",
            taxa_plataforma=0.1)

        self.reserva = Reserva.objects.create(
            anuncio=self.anuncio,
            data_checkin=date.today(),
            data_checkout=date.today() + timedelta(days=5),
            preco_total=500.0,
            comentario="Bom, bonito e barato!",
            numero_hospedes=3
        )

        self.valid_payload = {
            'anuncio': self.anuncio.pk,
            'data_checkin': (date.today() + timedelta(days=6)).strftime('%Y-%m-%d'),
            'data_checkout': (date.today() + timedelta(days=10)).strftime('%Y-%m-%d'),
            'preco_total': 600.0,
            'comentario': "Espaçoso, aconchegante e bem localizado. Nota 10, recomendo!",
            'numero_hospedes': 4
        }

    def teste_criar_reserva(self):
        response = self.client.post(reverse('reservas:reservas-list'), data=self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Reserva.objects.count(), 2)

    def teste_listar_reservas(self):
        response = self.client.get(reverse('reservas:reservas-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def teste_pegar_reserva_pelo_id(self):
        response = self.client.get(reverse('reservas:reservas-detail', args=[self.reserva.codigo_reserva]))
        reserva = Reserva.objects.get(pk=self.reserva.codigo_reserva)
        serializer = ReservaSerializer(reserva)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def teste_deletar_reserva(self):
        response = self.client.delete(reverse('reservas:reservas-detail', args=[self.reserva.codigo_reserva]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def teste_filtrar_reserva_pelo_intervalo_de_datas(self):
        response = self.client.get(reverse('reservas:reservas-list'), data={
            'data_checkin': self.reserva.data_checkin.strftime('%d/%m/%Y'),
            'data_checkout': self.reserva.data_checkout.strftime('%d/%m/%Y')
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def teste_tentativa_atualizacao_metodo_nao_permitido(self):
        update_payload = {
            'comentario': "Atualizando o comentário da reserva."
        }
        response = self.client.patch(reverse('reservas:reservas-detail', args=[self.reserva.codigo_reserva]),
                                     data=update_payload)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

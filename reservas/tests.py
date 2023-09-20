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
            data_checkin=date(2023, 9, 10),
            data_checkout=date(2023, 9, 15),
            preco_total=500.0,
            comentario="Bom, bonito e barato!",
            numero_hospedes=3
        )

        self.valid_payload = {
            'anuncio': self.anuncio.pk,
            'data_checkin': "10/01/2024",
            'data_checkout': "20/01/2024",
            'preco_total': 2105.37,
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
        self.assertEqual(response.data['count'], 1)

    def teste_pegar_reserva_pelo_id(self):
        response = self.client.get(reverse('reservas:reservas-detail', args=[self.reserva.pk]))
        reserva = Reserva.objects.get(pk=self.reserva.pk)
        serializer = ReservaSerializer(reserva)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def teste_deletar_reserva(self):
        response = self.client.delete(reverse('reservas:reservas-detail', args=[self.reserva.pk]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def teste_filtrar_reserva_pelo_intervalo_de_datas(self):
        response = self.client.get(reverse('reservas:reservas-list'), data={
            'data_checkin': self.reserva.data_checkin.strftime('%d/%m/%Y'),
            'data_checkout': self.reserva.data_checkout.strftime('%d/%m/%Y')
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def teste_tentativa_atualizacao_metodo_nao_permitido(self):
        update_payload = {
            'comentario': "Atualizando o comentário da reserva."
        }
        response = self.client.patch(reverse('reservas:reservas-detail', args=[self.reserva.pk]),
                                     data=update_payload)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def teste_reserva_sobreposta(self):
        reserva_data = {
            "anuncio": self.anuncio.id,
            "data_checkin": "18/09/2023",
            "data_checkout": "25/09/2023",
            "preco_total": "300.00",
            "comentario": "Barato!",
            "numero_hospedes": 1,
        }
        response = self.client.post(reverse('reservas:reservas-list'), reserva_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        reserva_sobreposta_data = {
            "anuncio": self.anuncio.id,
            "data_checkin": "20/09/2023",
            "data_checkout": "22/09/2023",
            "preco_total": "200.00",
            "comentario": "Incrível!",
            "numero_hospedes": 1,
        }
        response_sobreposta = self.client.post(reverse('reservas:reservas-list'), reserva_sobreposta_data, format='json')

        self.assertEqual(response_sobreposta.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('data_checkin', response_sobreposta.data)
        self.assertIn('data_checkout', response_sobreposta.data)

    def teste_data_checkin_igual_data_checkout(self):
        payload = self.valid_payload.copy()
        payload['data_checkin'] = "10/10/2023"
        payload['data_checkout'] = "10/10/2023"
        response = self.client.post(reverse('reservas:reservas-list'), data=payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('data_checkin', response.data)
        self.assertIn('data_checkout', response.data)

    def teste_data_checkin_posterior_data_checkout(self):
        payload = self.valid_payload.copy()
        payload['data_checkin'] = "15/10/2023"
        payload['data_checkout'] = "08/10/2023"
        response = self.client.post(reverse('reservas:reservas-list'), data=payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('data_checkin', response.data)

    def teste_numero_hospedes_invalido(self):
        payload = self.valid_payload.copy()
        payload['numero_hospedes'] = 0
        response = self.client.post(reverse('reservas:reservas-list'), data=payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('numero_hospedes', response.data)

        payload['numero_hospedes'] = self.imovel.limite_hospedes + 1
        response = self.client.post(reverse('reservas:reservas-list'), data=payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('numero_hospedes', response.data)

    def teste_preco_total_invalido(self):
        payload = self.valid_payload.copy()
        payload['preco_total'] = -10.0
        response = self.client.post(reverse('reservas:reservas-list'), data=payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('preco_total', response.data)

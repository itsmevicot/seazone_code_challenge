from rest_framework.test import APITestCase
from anuncios.models import Anuncio
from anuncios.serializers import AnuncioSerializer
from imoveis.models import Imovel
from rest_framework import status
from django.urls import reverse
from datetime import date


class AnuncioViewTestCase(APITestCase):
    def setUp(self):
        self.imovel = Imovel.objects.create(
            limite_hospedes=8,
            quantidade_banheiros=7,
            aceita_animal_estimacao=True,
            valor_limpeza=320,
            data_ativacao=date.today()
        )
        self.anuncio = Anuncio.objects.create(
            imovel=self.imovel,
            nome_plataforma="Airbnb",
            taxa_plataforma=0.1
        )

        self.valid_payload = {
            'imovel': self.imovel.pk,
            'nome_plataforma': 'Booking',
            'taxa_plataforma': 0.15
        }

    def teste_criar_anuncio(self):
        response = self.client.post(reverse('anuncios:anuncios-list'), data=self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Anuncio.objects.count(), 2)

    def teste_listagem_com_filtro_anuncios(self):
        response = self.client.get(reverse('anuncios:anuncios-list'), data={'nome_plataforma': 'Airbnb'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def teste_pegar_anuncio_pelo_id(self):
        response = self.client.get(reverse('anuncios:anuncios-detail', args=[self.anuncio.id]))
        anuncio = Anuncio.objects.get(pk=self.anuncio.id)
        serializer = AnuncioSerializer(anuncio)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def teste_atualizar_anuncio(self):
        response = self.client.put(reverse('anuncios:anuncios-detail', args=[self.anuncio.id]),
                                   data=self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def teste_deletar_anuncio(self):
        response = self.client.delete(reverse('anuncios:anuncios-detail', args=[self.anuncio.id]))
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

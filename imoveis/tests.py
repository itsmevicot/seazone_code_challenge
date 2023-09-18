from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from datetime import date
from .models import Imovel
from .serializers import ImovelSerializer


class ImovelViewTestCase(APITestCase):
    def setUp(self):
        self.imovel = Imovel.objects.create(
            limite_hospedes=5,
            quantidade_banheiros=2,
            aceita_animal_estimacao=True,
            valor_limpeza=50.0,
            data_ativacao=date.today()
        )

        self.valid_payload = {
            'limite_hospedes': 3,
            'quantidade_banheiros': 1,
            'aceita_animal_estimacao': False,
            'valor_limpeza': 25.0,
            'data_ativacao': '2023-12-01'
        }

    def teste_criar_imovel(self):
        response = self.client.post(reverse('imoveis:imoveis-list'), data=self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Imovel.objects.count(), 2)

    def teste_litagem_com_filtro_imoveis(self):
        response = self.client.get(reverse('imoveis:imoveis-list'), data={'limite_hospedes': 5})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        response_with_invalid_date = self.client.get(reverse('imoveis:imoveis-list'), data={'data_ativacao': 'invalid_date'})
        self.assertEqual(response_with_invalid_date.status_code, status.HTTP_400_BAD_REQUEST)

    def teste_pegar_imovel_pelo_id(self):
        response = self.client.get(reverse('imoveis:imoveis-detail', args=[self.imovel.codigo_imovel]))
        imovel = Imovel.objects.get(pk=self.imovel.codigo_imovel)
        serializer = ImovelSerializer(imovel)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def teste_atualizar_imovel(self):
        response = self.client.put(reverse('imoveis:imoveis-detail', args=[self.imovel.codigo_imovel]),
                                   data=self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def teste_deletar_imovel(self):
        response = self.client.delete(reverse('imoveis:imoveis-detail', args=[self.imovel.codigo_imovel]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

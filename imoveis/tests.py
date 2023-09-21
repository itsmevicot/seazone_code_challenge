from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from datetime import date, timedelta
from .models import Imovel
from .serializers import ImovelQuerySerializer


class ImovelViewTestCase(APITestCase):
    def setUp(self):
        self.imovel = Imovel.objects.create(
            limite_hospedes=5,
            quantidade_banheiros=2,
            aceita_animal_estimacao=True,
            valor_limpeza=50.0,
            data_ativacao=date.today()
        )

        self.payload_valido = {
            'limite_hospedes': 3,
            'quantidade_banheiros': 1,
            'aceita_animal_estimacao': False,
            'valor_limpeza': 25.0,
            'data_ativacao': '01/12/2023'
        }

    def teste_criar_imovel(self):
        response = self.client.post(reverse('imoveis:imoveis-list'), data=self.payload_valido)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Imovel.objects.count(), 2)

    def teste_listagem_imoveis_com_filtro(self):
        response = self.client.get(reverse('imoveis:imoveis-list'), data={'limite_hospedes': 5})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

        response_with_invalid_date = self.client.get(reverse('imoveis:imoveis-list'), data={'data_ativacao': 'data_invalida'})
        self.assertEqual(response_with_invalid_date.status_code, status.HTTP_400_BAD_REQUEST)

    def teste_pegar_imovel_pelo_id(self):
        response = self.client.get(reverse('imoveis:imoveis-detail', args=[self.imovel.pk]))
        imovel = Imovel.objects.get(pk=self.imovel.pk)
        serializer = ImovelQuerySerializer(imovel)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def teste_atualizar_imovel(self):
        response = self.client.put(reverse('imoveis:imoveis-detail', args=[self.imovel.pk]),
                                   data=self.payload_valido)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def teste_deletar_imovel(self):
        response = self.client.delete(reverse('imoveis:imoveis-detail', args=[self.imovel.pk]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def teste_validacao_limite_hospedes_menor_que_um(self):
        payload_invalido = self.payload_valido.copy()
        payload_invalido['limite_hospedes'] = 0
        response = self.client.post(reverse('imoveis:imoveis-list'), data=payload_invalido)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('limite_hospedes', response.data)

    def teste_validacao_valor_limpeza_menor_que_0(self):
        payload_invalido = self.payload_valido.copy()
        payload_invalido['valor_limpeza'] = -10.0
        response = self.client.post(reverse('imoveis:imoveis-list'), data=payload_invalido)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('valor_limpeza', response.data)

    def teste_validacao_data_ativacao_anterior_ao_dia_atual(self):
        payload_invalido = self.payload_valido.copy()
        payload_invalido['data_ativacao'] = (date.today() - timedelta(days=1)).strftime('%Y-%m-%d')
        response = self.client.post(reverse('imoveis:imoveis-list'), data=payload_invalido)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('data_ativacao', response.data)

    def teste_validacao_aceita_animal_estimacao_entrada_invalida(self):
        payload_invalido = self.payload_valido.copy()
        payload_invalido['aceita_animal_estimacao'] = 'Invalido'
        response = self.client.post(reverse('imoveis:imoveis-list'), data=payload_invalido)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('aceita_animal_estimacao', response.data)

        payload_valido = self.payload_valido.copy()
        payload_valido['aceita_animal_estimacao'] = False
        response = self.client.post(reverse('imoveis:imoveis-list'), data=payload_valido)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

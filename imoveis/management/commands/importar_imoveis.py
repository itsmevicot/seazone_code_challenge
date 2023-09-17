from django.core.management.base import BaseCommand
import csv
from django.db import transaction
from imoveis.models import Imovel

class Command(BaseCommand):
    help = 'Importa ou atualiza dados de imóveis de um arquivo CSV'

    def handle(self, *args, **kwargs):
        csv_file_path = 'imoveis/fixtures/imoveis.csv'
        with transaction.atomic():
            print("Importando ou atualizando imóveis...")
            with open(csv_file_path, mode='r', encoding='utf-8') as file:
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    defaults = {
                        'limite_hospedes': int(row['limite_hospedes']),
                        'quantidade_banheiros': int(row['quantidade_banheiros']),
                        'aceita_animal_estimacao': row['aceita_animal_estimacao'].lower() == 'true',
                        'valor_limpeza': float(row['valor_limpeza']),
                        'data_ativacao': row['data_ativacao']
                    }
                    Imovel.objects.update_or_create(
                        codigo_imovel=row['codigo_imovel'],
                        defaults=defaults
                    )
            print("OK!")

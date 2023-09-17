from django.core.management.base import BaseCommand
import csv
from django.db import transaction
from anuncios.models import Anuncio
from imoveis.models import Imovel

class Command(BaseCommand):
    help = 'Importa ou atualiza dados de anúncios de um arquivo CSV'

    def handle(self, *args, **kwargs):
        csv_file_path = 'anuncios/fixtures/anuncios.csv'
        with transaction.atomic():
            print("Importando ou atualizando anúncios...")
            with open(csv_file_path, mode='r', encoding='utf-8') as file:
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    imovel = Imovel.objects.get(pk=row['imovel_id'])
                    defaults = {
                        'imovel': imovel,
                        'nome_plataforma': row['nome_plataforma'],
                        'taxa_plataforma': float(row['taxa_plataforma']),
                    }
                    Anuncio.objects.update_or_create(
                        id=row['id'],
                        defaults=defaults
                    )
            print("OK!")

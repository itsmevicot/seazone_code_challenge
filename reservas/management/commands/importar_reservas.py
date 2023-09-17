from django.core.management.base import BaseCommand
import csv
from django.db import transaction
from anuncios.models import Anuncio
from reservas.models import Reserva


class Command(BaseCommand):
    help = 'Importa ou atualiza dados de reservas de um arquivo CSV'

    def handle(self, *args, **kwargs):
        csv_file_path = 'reservas/fixtures/reservas.csv'
        with transaction.atomic():
            print("Importando ou atualizando reservas...")
            with open(csv_file_path, mode='r', encoding='utf-8') as file:
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    anuncio = Anuncio.objects.get(pk=row['anuncio_id'])
                    defaults = {
                        'anuncio': anuncio,
                        'data_checkin': row['data_checkin'],
                        'data_checkout': row['data_checkout'],
                        'preco_total': float(row['preco_total']),
                        'comentario': row['comentario'],
                        'numero_hospedes': int(row['numero_hospedes']),
                    }
                    Reserva.objects.update_or_create(
                        codigo_reserva=row['codigo_reserva'],
                        defaults=defaults
                    )
            print("OK!")

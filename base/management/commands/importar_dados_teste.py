from django.core.management import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Comando para importação dos dados de teste das fixtures de Imóveis, Anúncios e Reservas.'

    def handle(self, *args, **kwargs):
        fixtures = ['imoveis.json', 'anuncios.json', 'reservas.json']

        for fixture in fixtures:
            call_command('loaddata', fixture)
        print("Dados de teste importados com sucesso!")

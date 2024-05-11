from django.core.management.base import BaseCommand
from ClientData.models import COVID_DATA_ML

class Command(BaseCommand):
    help = 'Clear all data from the COVID_DATA_ML table'

    def handle(self, *args, **kwargs):
        COVID_DATA_ML.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('All data cleared successfully!'))

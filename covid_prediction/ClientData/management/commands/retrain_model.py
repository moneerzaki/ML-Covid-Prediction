# from django.core.management.base import BaseCommand
# from covid_prediction.models import COVID_DATA_ML
# from covid_prediction.utils import retrain_model_function

# class Command(BaseCommand):
#     help = 'Retrain the model'
#     def handle(self, *args, **kwargs):
#         # Retrieve all data entries
#         all_entries = COVID_DATA_ML.objects.all()
#         # Retrain the model using the retrieved data
#         retrain_model_function(all_entries)

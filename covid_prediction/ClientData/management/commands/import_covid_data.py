# import os
# from datetime import datetime
# from django.core.management.base import BaseCommand
# from tablib import Dataset
# from ClientData.models import COVID_DATA_ML
# from ClientData.resources import COVIDDataResource

# class Command(BaseCommand):
#     help = 'Import COVID data from CSV'

#     def handle(self, *args, **kwargs):
#         print("Importing COVID data from CSV...")

#         file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '..', '..', 'fixtures', 'Covid.csv')
#         print("1.")
#         dataset = Dataset().load(open(file_path))
#         print("2.")
#         resource = COVIDDataResource()
#         print("3.")
#         result = resource.import_data(dataset, dry_run=False)
#         print("4.")
#         successful_count = 0  # Counter for successful uploads

#         if result.has_errors():
#             for error in result.rows_errors():
#                 self.stdout.write(f"Error: {error}")
#                 print("error")
#         else:
#             # Loop through each row and count successful uploads
#             for index, row in enumerate(dataset, start=1):
#                 if not row.errors:
#                     successful_count += 1
#                     timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#                     self.stdout.write(f"Uploading row {index} at {timestamp}")
#                     print("successful_count", file=self.stdout)

#             self.stdout.write(f"Data imported successfully! Total instances: {successful_count}")


import csv
import os
from django.core.management.base import BaseCommand
from datetime import datetime
from ClientData.models import COVID_DATA_ML
from ClientData.resources import COVIDDataResource

class Command(BaseCommand):
    help = 'Import COVID data from CSV'

    def handle(self, *args, **kwargs):
        print("Importing COVID data from CSV...")

        file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '..', '..', 'fixtures', 'Covid.csv')
        successful_count = 0  # Counter for successful uploads

        with open(file_path, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            next(csvreader)  # Skip header row if exists
            
            for index, row in enumerate(csvreader, start=1):
                # Process each row
                try:
                    # Assuming the CSV columns match the model fields
                    covid_data = COVID_DATA_ML.objects.create(
                        usmer=row[0],
                        sex=row[1],
                        patient_type=row[2],
                        dead=row[3],
                        pneumonia=row[4],
                        age=int(row[5]),
                        pregnant=row[6],
                        diabetes=row[7],
                        copd=row[8],
                        asthma=row[9],
                        inmsupr=row[10],
                        hipertension=row[11],
                        other_disease=row[12],
                        cardiovascular=row[13],
                        obesity=row[14],
                        renal_chronic=row[15],
                        tobacco=row[16],
                        medical_unit_1=row[17],
                        medical_unit_2=row[18],
                        medical_unit_3=row[19],
                        medical_unit_4=row[20],
                        medical_unit_5=row[21],
                        medical_unit_6=row[22],
                        medical_unit_7=row[23],
                        medical_unit_8=row[24],
                        medical_unit_9=row[25],
                        medical_unit_10=row[26],
                        medical_unit_11=row[27],
                        medical_unit_12=row[28],
                        medical_unit_13=row[29],
                        # Add more fields as needed
                        classification_final=row[-1]  # Assuming last column is classification_final
                    )
                    successful_count += 1
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    print(f"Successfully uploaded row {index} at {timestamp}")
                except Exception as e:
                    print(f"Error uploading row {index}: {str(e)}")

        print(f"Data imported successfully! Total instances: {successful_count}")

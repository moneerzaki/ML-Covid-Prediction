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

        file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '..', '..', 'fixtures', 'Final_Dataset.csv')
        successful_count = 0  # Counter for successful uploads

        with open(file_path, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            next(csvreader)  # Skip header row if exists
            
            for index, row in enumerate(csvreader, start=1):
                # Process each row
                try:
                    # Assuming the CSV columns match the model fields
                    # covid_data = 
                    # print("HEHEEEEE:  ", type(row[5]), row[5])

                    COVID_DATA_ML.objects.create(
                        USMER=row[0],
                        SEX=row[1],
                        PATIENT_TYPE=row[2],
                        # dead=row[3],
                        PNEUMONIA=row[3],
                        AGE=int(row[4]) if row[4] else 0,
                        PREGNANT=row[5],
                        DIABETES=row[6],
                        COPD=row[7],
                        ASTHMA=row[8],
                        INMSUPR=row[9],
                        HIPERTENSION=row[10],
                        OTHER_DISEASE=row[11],
                        CARDIOVASCULAR=row[12],
                        OBESITY=row[13],
                        RENAL_CHRONIC=row[14],
                        TOBACO=row[15],
                        MEDICAL_UNIT_1=row[16],
                        MEDICAL_UNIT_2=row[17],
                        MEDICAL_UNIT_3=row[18],
                        MEDICAL_UNIT_4=row[19],
                        MEDICAL_UNIT_5=row[20],
                        MEDICAL_UNIT_6=row[21],
                        MEDICAL_UNIT_7=row[22],
                        MEDICAL_UNIT_8=row[23],
                        MEDICAL_UNIT_9=row[24],
                        MEDICAL_UNIT_10=row[25],
                        MEDICAL_UNIT_11=row[26],
                        MEDICAL_UNIT_12=row[27],
                        MEDICAL_UNIT_13=row[28],
                        # Add more fields as needed
                        CLASSIFICATION_FINAL=row[-1]  # Assuming last column is classification_final
                    )
                    successful_count += 1
                    # timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    # print(f"Successfully uploaded row {index} at {timestamp}")
                    print({index})
                except Exception as e:
                    print(f"Error uploading row {index}: {str(e)}")

        print(f"Data imported successfully! Total instances: {successful_count}")

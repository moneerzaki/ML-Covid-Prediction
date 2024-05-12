from import_export import resources
from .models import COVID_DATA_ML

class COVIDDataResource(resources.ModelResource):
    class Meta:
        model = COVID_DATA_ML
        # fields = (
        #     'usmer',
        #     'sex',
        #     'patient_type',
        #     'dead',
        #     'pneumonia',
        #     'age',
        #     'pregnant',
        #     'diabetes',
        #     'copd',
        #     'asthma',
        #     'inmsupr',
        #     'hipertension',
        #     'other_disease',
        #     'cardiovascular',
        #     'obesity',
        #     'renal_chronic',
        #     'tobacco',
        #     'medical_unit_1',
        #     'medical_unit_2',
        #     'medical_unit_3',
        #     'medical_unit_4',
        #     'medical_unit_5',
        #     'medical_unit_6',
        #     'medical_unit_7',
        #     'medical_unit_8',
        #     'medical_unit_9',
        #     'medical_unit_10',
        #     'medical_unit_11',
        #     'medical_unit_12',
        #     'medical_unit_13',
        #     'classification_final',
        # )

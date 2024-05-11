from django import forms
from .models import COVID_DATA_ML

class COVIDDataForm(forms.ModelForm):
    class Meta:
        model = COVID_DATA_ML
        fields = '__all__'
    # Define choices for medical units
    MEDICAL_UNIT_CHOICES = [(i, f"Medical Unit {i}") for i in range(1, 14)]
    
    # Create ChoiceField for medical units
    medical_unit_choice = forms.ChoiceField(choices=MEDICAL_UNIT_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))
        # widgets = {
        #     'SEX': forms.CheckboxInput(choices=[('Male', 'Male'), ('Female', 'Female')]),
        # }
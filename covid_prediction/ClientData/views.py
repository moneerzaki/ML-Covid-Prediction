from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import COVIDDataForm
from .models import COVID_DATA_ML
from django.contrib import messages
from keras.models import model_from_json
from tensorflow.keras.models import load_model
import os
import zipfile
import numpy as np


# @staff_member_required
def retrain_model(request):
    if request.method == 'POST':
        form = RetrainForm(request.POST)
        if form.is_valid():
            # Load the dataset saved from user data
            dataset = load_dataset()
            # Preprocess the dataset
            X_train, y_train = preprocess_data(dataset)
            # Train the model
            new_model = train_model(X_train, y_train)
            # Save the updated model
            new_model.save('path/to/updated_model')
            return render(request, 'retrain_success.html')
    else:
        form = RetrainForm()
    return render(request, 'retrain_form.html', {'form': form})


def load_model_from_files(model_path):
    # Load model architecture from JSON file
    with open(os.path.join(model_path, 'config.json'), 'r') as json_file:
        model_json = json_file.read()
        model = model_from_json(model_json)

    # Load model weights
    model.load_weights(os.path.join(model_path, 'model.weights.h5'))
    return model



def make_prediction(form_data):
    model_path = './AI_models/model_6'

    model = load_model_from_files(model_path)
    sample = np.array([form_data])
    prediction = model.predict(sample)
    print ("------------------>>>>>>>",prediction)
    if(prediction[0] >=0.47):
        ans = True
    else: ans = False
    # prediction = True
    
    return ans





def ClientDataEntry(request):
    if request.method == 'POST':
        form = COVIDDataForm(request.POST)
        if form.is_valid():
            # Print form values to console
            # print("Form data before saving:", form.cleaned_data)

            # Get selected medical unit
            medical_unit = int(form.cleaned_data['medical_unit_choice'])
            medicalchoice = f"MEDICAL_UNIT_{medical_unit}"
            row = {
                'USMER' :0 if form.cleaned_data['USMER'] == False else 1,
                'SEX' :0 if form.cleaned_data['SEX'] == False else 1,
                'PATIENT_TYPE' :0 if form.cleaned_data['PATIENT_TYPE'] == False else 1,
                # 'DEAD' :0 if form.cleaned_data['DEAD'] == False else 1,
                'PNEUMONIA' :0 if form.cleaned_data['PNEUMONIA'] == False else 1,
                'AGE' :form.cleaned_data['AGE'],
                'PREGNANT' :0 if form.cleaned_data['PREGNANT'] == False else 1,
                'DIABETES' :0 if form.cleaned_data['DIABETES'] == False else 1,
                'COPD' :0 if form.cleaned_data['COPD'] == False else 1,
                'ASTHMA' :0 if form.cleaned_data['ASTHMA'] == False else 1,
                'INMSUPR' :0 if form.cleaned_data['INMSUPR'] == False else 1,
                'HIPERTENSION' :0 if form.cleaned_data['HIPERTENSION'] == False else 1,
                'OTHER_DISEASE' :0 if form.cleaned_data['OTHER_DISEASE'] == False else 1,
                'CARDIOVASCULAR' :0 if form.cleaned_data['CARDIOVASCULAR'] == False else 1,
                'OBESITY' :0 if form.cleaned_data['OBESITY'] == False else 1,
                'RENAL_CHRONIC' :0 if form.cleaned_data['RENAL_CHRONIC'] == False else 1,
                'TOBACO' :0 if form.cleaned_data['TOBACO'] == False else 1,
                'MEDICAL_UNIT_1' :0 if form.cleaned_data['MEDICAL_UNIT_1'] == False else 1,
                'MEDICAL_UNIT_2' :0 if form.cleaned_data['MEDICAL_UNIT_2'] == False else 1,
                'MEDICAL_UNIT_3' :0 if form.cleaned_data['MEDICAL_UNIT_3'] == False else 1,
                'MEDICAL_UNIT_4' :0 if form.cleaned_data['MEDICAL_UNIT_4'] == False else 1,
                'MEDICAL_UNIT_5' :0 if form.cleaned_data['MEDICAL_UNIT_5'] == False else 1,
                'MEDICAL_UNIT_6' :0 if form.cleaned_data['MEDICAL_UNIT_6'] == False else 1,
                'MEDICAL_UNIT_7' :0 if form.cleaned_data['MEDICAL_UNIT_7'] == False else 1,
                'MEDICAL_UNIT_8' :0 if form.cleaned_data['MEDICAL_UNIT_8'] == False else 1,
                'MEDICAL_UNIT_9' :0 if form.cleaned_data['MEDICAL_UNIT_9'] == False else 1,
                'MEDICAL_UNIT_10' :0 if form.cleaned_data['MEDICAL_UNIT_10'] == False else 1,
                'MEDICAL_UNIT_11' :0 if form.cleaned_data['MEDICAL_UNIT_11'] == False else 1,
                'MEDICAL_UNIT_12' :0 if form.cleaned_data['MEDICAL_UNIT_12'] == False else 1,
                'MEDICAL_UNIT_13' :0 if form.cleaned_data['MEDICAL_UNIT_13'] == False else 1,
                medicalchoice:1,

            }
            
            print ("&&&&&&&&&&&&&-----&&&&&&&&&&&&&&&")
            print ("row: ", row)
            input_values = [
                row['USMER'], 
                row['SEX'], 
                row['PATIENT_TYPE'], 
                # 0,                  # will be removed for the dead part. 
                row['PNEUMONIA'], 
                row['AGE'], 
                row['PREGNANT'], 
                row['DIABETES'], 
                row['COPD'], 
                row['ASTHMA'], 
                row['INMSUPR'], 
                row['HIPERTENSION'], 
                row['OTHER_DISEASE'], 
                row['CARDIOVASCULAR'], 
                row['OBESITY'], 
                row['RENAL_CHRONIC'], 
                row['TOBACO'], 
                row['MEDICAL_UNIT_1'], 
                row['MEDICAL_UNIT_2'], 
                row['MEDICAL_UNIT_3'], 
                row['MEDICAL_UNIT_4'], 
                row['MEDICAL_UNIT_5'], 
                row['MEDICAL_UNIT_6'], 
                row['MEDICAL_UNIT_7'], 
                row['MEDICAL_UNIT_8'], 
                row['MEDICAL_UNIT_9'], 
                row['MEDICAL_UNIT_10'], 
                row['MEDICAL_UNIT_11'], 
                row['MEDICAL_UNIT_12'], 
                row['MEDICAL_UNIT_13'],
                # row[medical_unit_choice],
            ]
            

            # making predictoin 
            prediction = make_prediction(input_values)
            print ()
            print("*************########*****************")
            print ("prediction: ", prediction)
            # Create an instance of COVID_DATA_ML
            covid_data = form.save(commit=False)
            # Get selected medical unit
            medical_unit = int(form.cleaned_data['medical_unit_choice'])
            # Set corresponding MEDICAL_UNIT to True and others to False
            # medicalchoice = f"MEDICAL_UNIT_{medical_unit}"
            setattr(covid_data, medicalchoice, True)
            # for i in range(1, 14):
            #     field_name = f"MEDICAL_UNIT_{i}"
            #     if i == medical_unit:
            #         setattr(covid_data, field_name, True)
            #     else:
            #         setattr(covid_data, field_name, False)
            # Save the object
            covid_data.save()
            return redirect('Results', prediction=prediction)  # redirect to success page 
        else:
            # Print form errors to console
            print(form.errors)
            # Add a message for the user
            messages.error(request, 'Form is invalid. Please correct the errors below.')
    else:
        form = COVIDDataForm()
    return render(request, 'ClientDataForm.html', {'form': form})



def homepage(request):
    print("homepage.html file")
    # return HttpResponse("homepage.html should be here")
    return render(request, "homepage.html", {})
# def ClientDataEntry(request):
#     return HttpResponse("Welcome to my Django project!")



def Results(request, prediction):
    predict_result = prediction
    ground_truth_result = None 
    # print("ground_truth_result", ground_truth_result)
    if request.method == 'POST':
        # print("POST data:", request.POST)  # Print entire POST data
        ground_truth_result = request.POST.get('ground_truth_result')
        print("*****************ground_truth_result**********************")
        print("---->",ground_truth_result)
        # if ground_truth_result:
        all_entries = COVID_DATA_ML.objects.all()
        if all_entries.exists():
            last_entry = all_entries.last()
            # print("*&*&*&**& entries exits -----------")
            if ground_truth_result is "None":
                last_entry.delete()
                print(" ---------- your entry was deleted from our dataset ----------")
            elif ground_truth_result == "True":
                last_entry.CLASSIFICATION_FINAL = True
                last_entry.save()
                print(" ---------- GROUND TRUTH UPDATED. ----------")
                print( "--->",last_entry.CLASSIFICATION_FINAL)
            else: 
                # last_entry.GROUND_TRUTH = True
                # last_entry.save()
                print(" ---------- No covid. ----------")
                print( "--->",last_entry.CLASSIFICATION_FINAL)

        return render(request, "homepage.html", {})
        
                    
    return render(request, "Results.html", {'predict_result': predict_result, "ground_truth_result": ground_truth_result})


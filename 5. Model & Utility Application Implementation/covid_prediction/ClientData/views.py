from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import COVIDDataForm
from .models import COVID_DATA_ML
from django.contrib import messages
from keras.models import model_from_json
from django.core.management.base import BaseCommand
from datetime import datetime
# from tensorflow.keras.models import load_model
import os
import zipfile
import numpy as np
import schedule
import time

def preprocess_row2(row):
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
    return input_values
def preprocess_row1(data): 
    
    row = {
            'USMER' :0 if data['USMER'] == False else 1,
            'SEX' :0 if data['SEX'] == False else 1,
            'PATIENT_TYPE' :0 if data['PATIENT_TYPE'] == False else 1,
            # 'DEAD' :0 if data['DEAD'] == False else 1,
            'PNEUMONIA' :0 if data['PNEUMONIA'] == False else 1,
            'AGE' :data['AGE'],
            'PREGNANT' :0 if data['PREGNANT'] == False else 1,
            'DIABETES' :0 if data['DIABETES'] == False else 1,
            'COPD' :0 if data['COPD'] == False else 1,
            'ASTHMA' :0 if data['ASTHMA'] == False else 1,
            'INMSUPR' :0 if data['INMSUPR'] == False else 1,
            'HIPERTENSION' :0 if data['HIPERTENSION'] == False else 1,
            'OTHER_DISEASE' :0 if data['OTHER_DISEASE'] == False else 1,
            'CARDIOVASCULAR' :0 if data['CARDIOVASCULAR'] == False else 1,
            'OBESITY' :0 if data['OBESITY'] == False else 1,
            'RENAL_CHRONIC' :0 if data['RENAL_CHRONIC'] == False else 1,
            'TOBACO' :0 if data['TOBACO'] == False else 1,
            'MEDICAL_UNIT_1' :0 if data['MEDICAL_UNIT_1'] == False else 1,
            'MEDICAL_UNIT_2' :0 if data['MEDICAL_UNIT_2'] == False else 1,
            'MEDICAL_UNIT_3' :0 if data['MEDICAL_UNIT_3'] == False else 1,
            'MEDICAL_UNIT_4' :0 if data['MEDICAL_UNIT_4'] == False else 1,
            'MEDICAL_UNIT_5' :0 if data['MEDICAL_UNIT_5'] == False else 1,
            'MEDICAL_UNIT_6' :0 if data['MEDICAL_UNIT_6'] == False else 1,
            'MEDICAL_UNIT_7' :0 if data['MEDICAL_UNIT_7'] == False else 1,
            'MEDICAL_UNIT_8' :0 if data['MEDICAL_UNIT_8'] == False else 1,
            'MEDICAL_UNIT_9' :0 if data['MEDICAL_UNIT_9'] == False else 1,
            'MEDICAL_UNIT_10' :0 if data['MEDICAL_UNIT_10'] == False else 1,
            'MEDICAL_UNIT_11' :0 if data['MEDICAL_UNIT_11'] == False else 1,
            'MEDICAL_UNIT_12' :0 if data['MEDICAL_UNIT_12'] == False else 1,
            'MEDICAL_UNIT_13' :0 if data['MEDICAL_UNIT_13'] == False else 1,
            # medicalchoice:1,
        }
            
    # print ("&&&&&&&&&&&&&-----&&&&&&&&&&&&&&&")
    # print ("row: ", row)
    # input_values = preprocess_row2(row)
    return row


def prepreprocess(data):
    row = {
        'USMER' : 0 if data.USMER == False else 1,
        'SEX' : 0 if data.SEX == False else 1,
        'PATIENT_TYPE' : 0 if data.PATIENT_TYPE == False else 1,
        # 'DEAD' :0 if data['DEAD'] == False else 1,
        'PNEUMONIA' : 0 if data.PNEUMONIA == False else 1,
        'AGE' : data.AGE,
        'PREGNANT' : 0 if data.PREGNANT == False else 1,
        'DIABETES' : 0 if data.DIABETES == False else 1,
        'COPD' : 0 if data.COPD == False else 1,
        'ASTHMA' : 0 if data.ASTHMA == False else 1,
        'INMSUPR' : 0 if data.INMSUPR == False else 1,
        'HIPERTENSION' : 0 if data.HIPERTENSION == False else 1,
        'OTHER_DISEASE' : 0 if data.OTHER_DISEASE == False else 1,
        'CARDIOVASCULAR' : 0 if data.CARDIOVASCULAR == False else 1,
        'OBESITY' : 0 if data.OBESITY == False else 1,
        'RENAL_CHRONIC' : 0 if data.RENAL_CHRONIC == False else 1,
        'TOBACO' : 0 if data.TOBACO == False else 1,
        'MEDICAL_UNIT_1' : 0 if data.MEDICAL_UNIT_1 == False else 1,
        'MEDICAL_UNIT_2' : 0 if data.MEDICAL_UNIT_2 == False else 1,
        'MEDICAL_UNIT_3' : 0 if data.MEDICAL_UNIT_3 == False else 1,
        'MEDICAL_UNIT_4' : 0 if data.MEDICAL_UNIT_4 == False else 1,
        'MEDICAL_UNIT_5' : 0 if data.MEDICAL_UNIT_5 == False else 1,
        'MEDICAL_UNIT_6' : 0 if data.MEDICAL_UNIT_6 == False else 1,
        'MEDICAL_UNIT_7' : 0 if data.MEDICAL_UNIT_7 == False else 1,
        'MEDICAL_UNIT_8' : 0 if data.MEDICAL_UNIT_8 == False else 1,
        'MEDICAL_UNIT_9' : 0 if data.MEDICAL_UNIT_9 == False else 1,
        'MEDICAL_UNIT_10' : 0 if data.MEDICAL_UNIT_10 == False else 1,
        'MEDICAL_UNIT_11' : 0 if data.MEDICAL_UNIT_11 == False else 1,
        'MEDICAL_UNIT_12' : 0 if data.MEDICAL_UNIT_12 == False else 1,
        'MEDICAL_UNIT_13' : 0 if data.MEDICAL_UNIT_13 == False else 1,
        # medicalchoice:1,
    }
    return preprocess_row2(row)

def retrain_at_midnight(data):
    print("In retraining")
    model_path = './AI_models/FinalModel'
    model = load_model_from_files(model_path)
    print(type(data))
    print(type(data[0]))
    x_train = [row[:-1] for row in data]  
    y_train = [row[-1] for row in data]   
    x_train = np.array(x_train)
    y_train = np.array(y_train).reshape(-1, 1)
    model.fit(x_train, y_train)
    model.save("Model.keras") #to save the model params
    print("New model saved")


def schedule_retraining():
    min_entires = 2048  # Adjust this value as needed
    num_entries = COVID_DATA_ML.objects.count()
    all_entries = COVID_DATA_ML.objects.all()
    print("-------------_________--------------")
    data_to_train = []
    current_time = datetime.now().time()
        # Check if it's the desired time (e.g., 12:00 AM)
    if current_time.hour == 8:
        print("It is going to retraiiiin")
        for i in range(num_entries):
            entry = all_entries[i]
            row = prepreprocess(entry)
            row.append(entry.CLASSIFICATION_FINAL)
            data_to_train.append(row)

        print("Done adding")
        # schedule.every().day.at("00:00").do(retrain_at_midnight(data_to_train))
        retrain_at_midnight(data_to_train)

    # for entry in all_entries:
    #     # print(entry.USMER)
    #     # print(type(entry))
    #     # print(type(entry.USMER))
    #     # data1 = prepreprocess(entry)
    #     data_to_train.append(prepreprocess(entry))

    # print(type(all_entries[0]))
    # if num_entries > min_entires:
    #     # print("Number of entries exceeds the maximum.")
    #     x=0
    # else:
    #     x=0
    #     # print("Number of entries is within the limit.")
    #     # Perform actions if the number of entries is within the limit

    # schedule.every().day.at("00:00").do(retrain_at_midnight)

    # Run the scheduler loop
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)  # Sleep for 1 second to prevent high CPU usage

# Call the scheduling function when your Django server starts
# schedule_retraining()






# def retrain() :
#     all_entries = COVID_DATA_ML.objects.all()
# # @staff_member_required
# def retrain_model(request):
#     if request.method == 'POST':
#         form = RetrainForm(request.POST)
#         if form.is_valid():
#             # Load the dataset saved from user data
#             dataset = load_dataset()
#             # Preprocess the dataset
#             X_train, y_train = preprocess_data(dataset)
#             # Train the model
#             new_model = train_model(X_train, y_train)
#             # Save the updated model
#             new_model.save('path/to/updated_model')
#             return render(request, 'retrain_success.html')
#     else:
#         form = RetrainForm()
#     return render(request, 'retrain_form.html', {'form': form})


def load_model_from_files(model_path):
    # Load model architecture from JSON file
    with open(os.path.join(model_path, 'config.json'), 'r') as json_file:
        model_json = json_file.read()
        model = model_from_json(model_json)

    # Load model weights
    model.load_weights(os.path.join(model_path, 'model.weights.h5'))
    return model



def make_prediction(form_data):
    model_path = './AI_models/FinalModel'

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
            input_values = preprocess_row1(form.cleaned_data)
            input_values["MEDICAL_UNIT_{medical_unit}"]=1
            input_values = preprocess_row2(input_values)
            # input_values = {}
            
            # medical_unit = int(data['medical_unit_choice'])
            # medicalchoice = f"MEDICAL_UNIT_{medical_unit}"

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
            # ground_truth_result = None
            # predict_result = prediction
            # return render(request, "Results.html", {'predict_result': predict_result, "ground_truth_result": ground_truth_result})
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
    print("in homepage")
    schedule_retraining()
    # print("homepage.html file")
    # return HttpResponse("homepage.html should be here")
    return render(request, "homepage.html", {})
# def ClientDataEntry(request):
#     return HttpResponse("Welcome to my Django project!")



def Results(request, prediction):
    # predict_result = prediction
    ground_truth_result = "None" 
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
            
            if ground_truth_result == "None":
                all_entries.last().delete()
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

        return redirect('homepage')
    msg = 'hehe'    
    if prediction == 'True':
        msg = 'Unfortunately with a high probability you are a covid suspect.'
        prediction = True
    else:
        msg = 'fortunately you are not a covid holder'
        prediction = False                   
    return render(request, "Results.html", {'msg': msg, "ground_truth_result": ground_truth_result, 'prediction':prediction})


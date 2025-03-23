import ast
import numpy as np
import pandas as pd
from .file_utils import read_file
import pickle as pkl
import warnings
warnings.filterwarnings("ignore")

department_dict = read_file("api/data/departments.json")
diseases_list = read_file("api/data/diseases_list.json")
symptom_dict = read_file("api/data/symptom_dict.json")
# print(diseases_list)

precaution = pd.read_csv("api/data/precautions_df.csv")
description = pd.read_csv("api/data/description.csv")
medication = pd.read_csv('api/data/medications.csv')
workout = pd.read_csv("api/data/workout_df.csv")
diets = pd.read_csv('api/data/diets.csv')

with open("api/models/knn-tunned.pkl", "rb") as file:
    model = pkl.load(file)


def get_info(disease):
    descr = description[description['Disease'] == disease]['Description']
    descr = " ".join({w for w in descr})

    pre = precaution[precaution['Disease'] == disease][['Precaution_1', 'Precaution_2', 'Precaution_3', 'Precaution_4']]
    pre = pre.values.tolist()[0]

    die = diets[diets['Disease'] == disease]['Diet']
    die = ast.literal_eval(die.values.tolist()[0])

    work = workout[workout['disease'] == disease]['workout']
    work = work.values.tolist()

    med = medication[medication['Disease'] == disease]['Medication']
    med = ast.literal_eval(med.values.tolist()[0])

    department = department_dict[disease]

    return {
        'disease' : disease,
        "department" : department,
        "description": descr,
        "precaution": pre,
        "medication": med,
        "workout": work,
        "diets": die,
    }

def get_predicted_value(patient_symptoms):
    input_vector = np.zeros(len(symptom_dict))

    if len(patient_symptoms) <= 4:
        return {
            "error" : "please select more than four symptoms for correct predicction"
        }    
    for item in patient_symptoms:
        input_vector[symptom_dict[item]] = 1

    disease = diseases_list[str(model.predict([input_vector])[0])]
    # print("\n", disease)

    result = get_info(disease)
    # print(result)
    return result

def remove_nan(data):
    if isinstance(data, list):
        return [item for item in data if item is not None]  # Removing None values
    elif isinstance(data, dict):
        return {key: remove_nan(value) for key, value in data.items()}
    else:
        return data


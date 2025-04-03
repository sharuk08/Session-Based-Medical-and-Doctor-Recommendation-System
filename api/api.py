from .utils.predict import get_predicted_value, symptom_dict
from .utils.disease_predict import classify_using_bytes
from flask_restx import Api, reqparse, Resource, Namespace
from werkzeug.datastructures import FileStorage
from flask import request
import pandas as pd
import warnings

data = pd.read_csv("api/data/Doctors.csv")
warnings.filterwarnings("ignore")

api = Api(
    title="Disease Diagnosis",
    description="Get the solution for your disease",
    version="1.0",
    validate=True,
    doc="/api/v1",
    contact="Visit Doctors", 
    contact_url="http://localhost:5000/doctors"
)


def specialization_filter(Specialization):
    data = pd.read_csv("api/data/Doctors.csv")
    return (data['Specialization'] == Specialization)

def city_filter(city):
    data = pd.read_csv("api/data/Doctors.csv")
    return (data['City'] == city)

def state_filter(state):
    data = pd.read_csv("api/data/Doctors.csv")
    return (data['State'] == state)

disease_args = reqparse.RequestParser()
disease_args.add_argument(name="file", type=FileStorage, location="files", required=True)

predict_args = reqparse.RequestParser()
predict_args.add_argument(name="symptoms", type=str, location="json", required=True)

disease_predict_args = reqparse.RequestParser()
disease_predict_args.add_argument(name="file", type=FileStorage, location="files", required=True)
disease_predict_args.add_argument(
    name="disease_type", 
    type=str, 
    location="form",
    help="select the type of disease which you want to use for classification",
    required=True, 
    choices=[
        "skin_disease", 
        "oral_disease", 
        "lung_disease",
        "bone_class",
        "brain_tumor"
    ]
)

predict_namespace = Namespace(name="predict controller", path="/predict")
disease_namespace = Namespace(name="Disease controller", path="/disease")

@predict_namespace.route("/symptoms")
class Symptoms(Resource):
    def get(self):
        all_symptoms = {key: None for key in symptom_dict}
        return all_symptoms

@predict_namespace.route("/symptoms-list")
class Predict2(Resource):
    @predict_namespace.expect(predict_args)
    def post(self):
        symptoms = predict_args.parse_args()['symptoms']
        queries = [symptom.strip() for symptom in symptoms.split(',')]

        return get_predicted_value(queries)

@predict_namespace.route("/")
class Predict(Resource):
    def post(self):
        symptoms = request.json['symptoms']
        queries = list()
        for s in symptoms:
            queries.append(s['tag'])
            
        if len(queries) <= 3:
            return {
                "error" : "please select more than 4 symptoms for better result"
            }

        return get_predicted_value(queries)
    
@disease_namespace.route("/")
class DiseaseResource(Resource):
    @disease_namespace.expect(disease_predict_args)
    def post(self):
        file_bytes = disease_predict_args.parse_args()['file'].read()
        disease_type = disease_predict_args.parse_args()['disease_type']
         
        return classify_using_bytes(file_bytes, disease_type, 224)


api.add_namespace(predict_namespace)
api.add_namespace(disease_namespace)

from .utils.predict import get_predicted_value, symptom_dict
from flask_restx import Api, reqparse, Resource, Namespace
from werkzeug.datastructures import FileStorage
from flask import request
import pandas as pd
import warnings

data = pd.read_csv(r"api\data\Doctors.csv")
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
    data = pd.read_csv(r"api\data\Doctors.csv")
    return (data['Specialization'] == Specialization)

def city_filter(city):
    data = pd.read_csv(r"api\data\Doctors.csv")
    return (data['City'] == city)

def state_filter(state):
    data = pd.read_csv(r"api\data\Doctors.csv")
    return (data['State'] == state)

disease_args = reqparse.RequestParser()
disease_args.add_argument(name="file", type=FileStorage, location="files", required=True)

predict_args = reqparse.RequestParser()
predict_args.add_argument(name="symptoms", type=str, location="json", required=True)

predict_namespace = Namespace(name="predict controller", path="/predict")

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

        return get_predicted_value(queries)
    

api.add_namespace(predict_namespace)



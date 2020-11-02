import pandas as pd
import pickle
from ford_care.utils  import *


def import_model(path):
    return pickle.load(open(path, 'rb'))

def calculate_desgaste(cars):
    piece_dict = {'motor':200000, 'transmissão':125000, 'filtro-óleo':12500, 'filtro-combustível':12500}
    
    car_km = cars['ODOMETER'].astype(int)
    
    car = pd.DataFrame()
    
    car['motor(%)'] = 100 - porcentagem(car_km,piece_dict['motor'])
    car['transmissao(%)'] = 100 - porcentagem(car_km,piece_dict['transmissão'])
    car['filtro-oleo(%)'] = 100 - porcentagem(car_km,piece_dict['filtro-óleo'])
    car['filtro-combustivel(%)'] = 100 - porcentagem(car_km,piece_dict['filtro-combustível'])
    
    return car

def use_guesser(model_directory,df):
    ford_guesser = import_model(model_directory)
    
    x = df[['CAR_YEAR', 'AIR_INTAKE_TEMP',
           'ENGINE_COOLANT_TEMP', 'ENGINE_LOAD', 'ENGINE_POWER', 'ENGINE_RPM',
           'INTAKE_MANIFOLD_PRESSURE', 'SPEED', 'THROTTLE_POS']]
                           
    return ford_guesser.predict(x)

def use_classifier(model_directory,df):
    ford_classifier = import_model(model_directory)
    
    x = df[['CAR_YEAR', 'AIR_INTAKE_TEMP',
           'ENGINE_COOLANT_TEMP', 'ENGINE_LOAD', 'ENGINE_POWER', 'ENGINE_RPM',
           'INTAKE_MANIFOLD_PRESSURE', 'SPEED', 'THROTTLE_POS']]
    
    return ford_classifier.predict(x)

def apply_analysis(df, guesser_path, classifier_path):
    guesser_results = use_guesser(guesser_path,df)
    guesser_results = pd.DataFrame(guesser_results,columns=['PREDICTED_ALERT'])
    df = df.join(guesser_results)
    
    classifier_results = use_classifier(classifier_path,df)
    classifier_results = pd.DataFrame(guesser_results,columns=['ALERT_CLASSIFIER'])
    df = df.join(classifier_results)    
    df['ALERT_CLASSIFIER'].fillna('No Alarm', inplace=True)
    
    df = df.join(calculate_desgaste(df))
    
    return df

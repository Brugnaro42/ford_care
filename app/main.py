from ford_care.utils import *
from ford_care.MongoTools import *
from ford_care.analysis import *

if __name__ == '__main__':
    log('LENDO DADOS')
    log('--car_data')
    db = connect_to_mongo()
    df_car_data = mongo_to_pandas(db,'car_datas')
    log('--cars')
    df_cars = mongo_to_pandas(db,'cars')
    print('\n')
    log('Cruzando informações')
    df_cars.rename(mapper={'_id':'CAR','year':'CAR_YEAR'}, axis=1, inplace=True)
    df_car_data = df_cars[['CAR','CAR_YEAR','model']].merge(df_car_data, on='CAR')
    df_car_data = get_last_data(df_car_data).reset_index(drop=True)
    df_car_data.rename(mapper={'model':'MODEL','updatedate':'TIME'}, axis=1, inplace=True)
    df_car_data['MARK'] = 'Ford'
    df_car_data = apply_analysis(df_car_data, 'ford_care/ford_guesser.sav', 'ford_care/ford_classifier.sav')
    results = df_car_data[['CAR','PREDICTED_ALERT', 'ALERT_CLASSIFIER', 'motor(%)','transmissao(%)', 
                           'filtro-oleo(%)', 'filtro-combustivel(%)']]
    upload_to_mongo(results)
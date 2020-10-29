import pandas as pd
import numpy as np
import seaborn as sns
from datetime import datetime
import plotly.express as xp
import plotly.graph_objects as go
import matplotlib

# configurando pandas
pd.set_option('display.max_columns',None)

lista_colunas = ['AIR_INTAKE_TEMP', 'AMBIENT_AIR_TEMP', 'AUTOMATIC','BAROMETRIC_PRESSURE', 'CAR_YEAR', 
                 'DAYS_OF_WEEK', 'DTC_NUMBER','ENGINE_COOLANT_TEMP', 'ENGINE_LOAD', 'ENGINE_POWER', 'ENGINE_RPM',
                 'ENGINE_RUNTIME', 'EQUIV_RATIO','FUEL_LEVEL','FUEL_TYPE', 'HOURS', 'INTAKE_MANIFOLD_PRESSURE',
                 'LONG TERM FUEL TRIM BANK 2', 'MAF', 'MARK','MIN', 'MODEL', 'MONTHS',
                 'SHORT TERM FUEL TRIM BANK 1','SHORT TERM FUEL TRIM BANK 2', 'SPEED','THROTTLE_POS', 'TIME', 
                 'TIMING_ADVANCE', 'TROUBLE_CODES','VEHICLE_ID', 'YEAR']
def log(mes):
    print(datetime.now().strftime("[%d/%m/%Y %H:%M:%S] - "), mes)

def porcentagem(parte,total):
    perc = parte/total*100
    return str(perc)+'%'
    
def dict_odb2():
    # Leitura das bases
    df_codes = pd.read_csv("../data/odb2_codes.csv", sep=';')
    df_codes.drop(index = df_codes[(df_codes["problems"]=="ISO/SAE Reserved___") | 
                                  ((df_codes["problems"]=="___"))].index,inplace=True, axis=0)
    df_codes = df_codes[["code","problems"]]

    return df_codes.problems.str.replace('_','; ').str.replace(' ;','')

def get_experimental_dataset():
        #Leitura dos dados experimentais
    df_exp1 = pd.read_excel("../data/exp1_14drivers_14cars_dailyRoutes.xlsx")
    df_exp1.rename({"TIMESTAMP":"TIME","BAROMETRIC_PRESSURE(KPA)":"BAROMETRIC_PRESSURE"},inplace=True,
                   axis="columns")

    df_exp2 = pd.read_excel("../data/exp2_19drivers_1car_1route.xlsx")
    #, 'Short Term Fuel Trim Bank 1'
    df_exp2.rename({'Short Term Fuel Trim Bank 2':'SHORT TERM FUEL TRIM BANK 2',
                    'Short Term Fuel Trim Bank 1':'SHORT TERM FUEL TRIM BANK 1',
                    'Long Term Fuel Trim Bank 2':'LONG TERM FUEL TRIM BANK 2'},inplace=True,axis="columns")

    df_exp2.ENGINE_RPM = df_exp2.ENGINE_RPM.str.replace("RPM","").notna().astype(int)

    df_exp3 = pd.read_excel("../data/exp3_4drivers_1car_1route.xlsx")
    
    return pd.concat([df_exp1,df_exp2,df_exp3],sort=True).reset_index()

def get_problems(df):
    df["PROBLEM_1"] = df['TROUBLE_CODES'].str.slice(0,5)
    df["PROBLEM_2"] = df['TROUBLE_CODES'].str.slice(5,10)
    df["PROBLEM_3"] = df['TROUBLE_CODES'].str.slice(10,15)
    
    return df

def decode_trouble_code(df_exp):
    df_problems_final = pd.DataFrame()
    for i in df_exp.index:
        tmp2 = df_exp[df_exp.index==i]
        if str(tmp2.iloc[0]["TROUBLE_CODES"]) != 'nan':
            #print("Processando carro com problema")
            df_problems = tmp2[['PROBLEM_1','PROBLEM_2','PROBLEM_3']].T.reset_index(drop=True).reset_index()
            df_problems.columns = ['index','ERROR CODE']
            df_problems = df_problems.merge(pd.concat([tmp2,tmp2,tmp2]).reset_index(drop=True).reset_index(),on='index').drop(columns=['index','PROBLEM_1','PROBLEM_2','PROBLEM_3', 'TROUBLE_CODES'], axis=1)
            df_problems_final = pd.concat([df_problems_final, df_problems])
            log(porcentagem(i, df_exp.shape[0])+'% Concluído')
            os.system('cls')
    
    df_problems_final.reset_index(drop=True,inplace=True)
    return df_problems_final

def get_colunas_viaveis(df_exp):
    
    lista_colunas = []

    for c in df_exp.columns:
        perc = df_exp[c].isna().sum()/df_exp.shape[0]*100
        if perc < 60:
            lista_colunas.append(c)
            
    lista_colunas.append('ERROR CODE')
    return lista_colunas

def there_is_a_error(code):
    if 'P' in code :
        return True
    else:
        return False

def export_for_guesser(df_ext):
    df_ford_guesser = df_ext.copy()
    df_ford_guesser['ALERT'] = df_ford_guesser['ERROR CODE'].apply(there_is_a_error)
    df_ford_guesser['ERROR CODE'] = df_ford_guesser['ERROR CODE'].fillna('No Error Code')
    df_ford_guesser.reset_index(drop=True).to_csv('../data/ford_guesser_fuel.csv')
    
    
def export_for_classifier(df_ext):
    df_ford_classifier = df_ext[~df_ext['ERROR CODE'].isna()].reset_index(drop=True).copy()
    df_codes.columns = ['ERROR CODE', 'problems']
    df_codes['ERROR CODE'] = df_codes['ERROR CODE'].str[:5]
    df_ford_classifier = df_ford_classifier.merge(df_codes, on='ERROR CODE')
    df_ford_classifier.reset_index(drop=True).to_csv('../data/ford_classifier_fuel.csv')
    
def export_for_tear(df_ext):
    df_desgaste = df.copy()
    df.reset_index(drop=True).to_csv('../data/historico_experimentos.csv')
    

if __name__ == "__main__":
    df_codes = dict_odb2()
    df_exp = get_experimental_dataset()[lista_colunas]
    log('Dados Carregados')
    df = get_problems(df_exp)
    log('Decodificando códigos')
    df = decode_trouble_code(df)
    df = df[get_colunas_viaveis(df)]
    export_for_guesser(df)
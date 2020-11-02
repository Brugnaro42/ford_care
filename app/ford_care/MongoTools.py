import pymongo
from pymongo import MongoClient
from ford_care.utils import *
import pandas as pd
from urllib.parse import quote_plus

def connect_to_mongo():
    """ Connects to MongoDB database to get data

    Returns:
        The ford_care database.
    """
    log('Conectando ao banco de dados')

    Mongo_url = quote_plus('@@1234qwer')
    client = MongoClient('mongodb+srv://admin:'+Mongo_url+'@cluster0.lvveh.gcp.mongodb.net/ford_care?retryWrites=true&w=majority')
    log('Conexão efetuada com sucesso')
    
    log('Carregando banco de dados')
    db = client['ford_care']
    log('Dados carregados com sucesso')
    return db

def mongo_to_pandas(db, collection, query=None):
    """ Read a collection and stores it in Pandas Dataframe
    Args:
        db [Database] : the result of the function connect_to_mongo()
        collection [str] : the name of the desired collection
    Returns:
        Pandas Dataframe with collection data
        
    """
    
    # Make a query to the specific DB and Collection
    cursor = db[collection].find(query)

    # Expand the cursor and construct the DataFrame
    log('Passando coleção para o dataframe')
    df =  pd.DataFrame(list(cursor))
    log('Coleção carregada com sucesso')
    
    return df    

def get_last_data(df):
    log('Lendo últimos registros')
    tmp_max = df.groupby('CAR',as_index=False)['updatedate'].max()
    df['key'] = df['CAR'].astype(str) + df['updatedate'].astype(str)
    tmp_max['key'] = tmp_max['CAR'].astype(str) + tmp_max['updatedate'].astype(str)
    df = df[df['key'].isin(tmp_max.key)]
    df = df.drop_duplicates(subset='key')
    log('Filtro realizado com sucesso')
    return df

def upload_to_mongo(results):
    log('[!] Upload de resultados - Conectando ao banco')
    db = connect_to_mongo()
    doc_resultados = db['model_datas']

    log('[!] Upload de resultados - Banco de dados Conectado')
    for i in results.index:
        tmp_insert = results[results.index==i]
        result_dict = tmp_insert.to_dict("records")
        doc_resultados.insert_one({"index":"CAR","data":result_dict})
        
    log('[!] Upload de resultados - Resultados Inseridos')
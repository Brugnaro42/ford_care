from datetime import datetime
import pandas as pd


def pega_erro(cod, decod=df_codes):
    cod_meaning = df_codes[df_codes["code"].str.contains(cod)].head(1).problems

    if cod_meaning.shape[0] == 0:
        cod_meaning = "Unknown Error"

    return cod_meaning


def formata_timestamp(timestamp):
    time = datetime.fromtimestamp(timestamp / 1000)
    return time


def timeround10min(dt):
    a, b = divmod(round(dt.minute, -1), 60)
    return '%i:%02i' % ((dt.hour + a) % 24, b)


def log(mes):
    print(datetime.now().strftime("[%d/%m/%Y %H:%M:%S] - "), mes)
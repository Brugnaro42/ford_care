from datetime import datetime

def log(mes):
    print(datetime.now().strftime("[%d/%m/%Y %H:%M:%S] - "), mes)

def porcentagem(parte,total):
    perc = parte/total*100
    return perc
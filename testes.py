from iqoptionapi.stable_api import IQ_Option
from iqoptionapi.api import Logout
import time
import userdata
import os
from colorama import init, Fore, Back, Style

''' Config Colorama '''
init(convert=True, autoreset=True)

user = userdata.mainUser
api = IQ_Option(user["username"], user["password"])

def conexao():
    global api, user
    print("\n     iniciando aplicativo")
    print(Fore.LIGHTYELLOW_EX + " ... estabelecendo conexão com o servidor")
    api.connect()
   
    while True:
        if api.check_connect() == False:
            print(Fore.LIGHTYELLOW_EX + "\n ... tentativa de reconexão")
            api.connect()
        else:
            print(Fore.LIGHTGREEN_EX + "\n     conectado com sucesso!")
            break
conexao()

api.change_balance('PRACTICE') # PRACTICE / REAL
optionCod = 'EURUSD'


timeframe = 2
perCurto = 10
perLongo = 40
tempoGrafReal = 60

indicators = api.get_technical_indicators(optionCod)

sr = {}

for dados in indicators:
   if dados['candle_size'] == (int(tempoGrafReal)) and 'Classic' in dados['name']:
      sr.update({dados['name'].replace('Classic ', ''): dados['value']})

print(sr)

Logout(api)
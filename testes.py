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

velasCurto = api.get_candles(optionCod, (int(timeframe) * 60), perCurto,  time.time())
priCurto = round(velasCurto[1]['close'], 4)
ultCurto = round(velasCurto[perCurto-1]['close'], 4)
percCurto = abs(round(((ultCurto - priCurto) / priCurto) * 1000, 3))

velasLongo = api.get_candles(optionCod, (int(timeframe) * 60), perLongo,  time.time())
priLongo = round(velasLongo[1]['close'], 4)
ultLongo = round(velasLongo[perLongo-1]['close'], 4)
percLongo = abs(round(((ultLongo - priLongo) / priLongo) * 100, 3))

print('\nFechamento da última vela = {} e da vela {} = {}'.format(ultLongo, perLongo, priLongo))
print('Longo em', str(percLongo) + "%\n")
if ultLongo > priLongo:
   if percLongo > 0.2:
      print('Forte tendencia de alta')
   else:
      if ultCurto < priCurto:
         if percCurto > 0.2:
            print('Tendencia de alta com possível reversão')
         else:
            print('Tendencia de alta, na correção')
      else:
         print('Tendencia de alta')
      print('Curto em', str(percCurto) + "%")
else:
   if percLongo > 0.2:
      print('Forte tendencia de baixa')
   else:
      if ultCurto < priCurto:
         if percCurto > 0.2:
            print('Tendencia de baixa com possível reversão')
         else:
            print('Tendencia de baixa, na correção')
      else:
         print('Tendencia de baixa')
      print('Curto em', str(percCurto) + "%\n")

Logout(api)
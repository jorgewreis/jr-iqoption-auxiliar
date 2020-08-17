''' Importações de bibliotecas '''
import userdata
import iqoptionapi.country_id as Paises
import time
import json
import os
import collections
import logging
from colorama import init, Fore, Back, Style
from iqoptionapi.stable_api import IQ_Option
from datetime import datetime
from dateutil import tz

''' Config Colorama '''
init(convert=True, autoreset=True)

''' Definições iniciais '''
modoOperacao = ""   ''' PRACTICE/REAL'''
caixaInicial = 0

def descProgram():
    version = "1.0.01"
    appname = "IQ Option Auxiliar - Jorge Reis "
    os.system('cls')
    print("APP " + appname + "   Versão: " + version + "\n")

def menuPrincipal():
    global menuOp
    menuOp = 1
    while menuOp > 0:
        descProgram()
        print(' MENU PRINCIPAL:')
        print(' [1] - TRADER')
        print(' [2] - CONFIGURAÇÕES')
        print(Fore.LIGHTRED_EX + '\n [0] - SAIR')

        menuOp = int(input('\n Digite o número da opção escolhida: '))

        if menuOp == 1:
            print(Fore.LIGHTYELLOW_EX + '\n ... abrindo opção selecionada')
            print(Fore.RED + " Erro! Opção não configurada")
            time.sleep(2)
        elif menuOp == 2:
            print(Fore.LIGHTYELLOW_EX + '\n ... abrindo opção selecionada')
            print(Fore.RED + " Erro! Opção não configurada")
            time.sleep(2)
        else:
            print(Fore.YELLOW + "\n ... encerrando aplicativo")
            time.sleep(3)
            os.system('cls')
            break

def avisos():
    global modoOperacao
    if modoOperacao == "":
        modoOperacao = "PRACTICE"
        print(Fore.LIGHTYELLOW_EX + "Definindo modo de operação para Treinamento")

def alteraModo():
    global modoOperacao
    if modoOperacao == "PRACTICE":
        print(Fore.GREEN + "Alterando modo de operação para Uso real")
        modoOperacao = "REAL"
    else:
        print(Fore.LIGHTYELLOW_EX + "Alterando modo de operação para Treinamento")
        modoOperacao = "PRACTICE"
    print(Fore.RED + '\n ... voltando para menu anterior')
    time.sleep(2)

def perfil():
    global api
    perfil = json.loads(json.dumps(api.get_profile_ansyc()))
	
    return perfil

def conexao():
    global api, user
    user = userdata.mainUser
    api = IQ_Option(user["username"], user["password"])
    check, reason = api.connect()

    print(Fore.LIGHTYELLOW_EX + "\n ... estabelecendo conexão com o servidor")
    time.sleep(2)
    caixaInicial = api.get_balance


def time_converter(x): # Função para converter timestamp
	hora = datetime.strptime(datetime.utcfromtimestamp(x).strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
	hora = hora.replace(tzinfo=tz.gettz('GMT'))
	
	return str(hora)[:-6]

''' Definições finais antes de iniciar '''




''' Início do programa '''
conexao()
menuPrincipal()
avisos()
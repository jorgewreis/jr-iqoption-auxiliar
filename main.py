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
    global op
    menuOp = 1
    while menuOp > 0:
        descProgram()
        print(' MENU PRINCIPAL:')
        print(' [1] - TRADER')
        print(' [2] - CONFIGURAÇÕES')
        print(Fore.LIGHTRED_EX + '\n [0] - SAIR')

        menuOp = int(input('\n Digite o número da opção escolhida: '))
        if menuOp == 1:
            print("Opção não configurada")
        elif menuOp == 2:
            print("Opção não configurada")
        else:
            break

def avisos():
    global modoOperacao
    if modoOperacao == "":
        modoOperacao = "PRACTICE"
        print(Fore.YELLOW + "Definindo modo de operação para Treinamento")

def alteraModo():
    global modoOperacao
    if modoOperacao == "PRACTICE":
        print(Fore.GREEN + "Alterando modo de operação para Uso real")
        modoOperacao = "REAL"
    else:
        print(Fore.YELLOW + "Alterando modo de operação para Treinamento")
        modoOperacao = "PRACTICE"

def conexao():
    global api, user
    user = userdata.mainUser
    api = IQ_Option(user["username"], user["password"])
    check, reason = api.connect()

    print(Fore.YELLOW + "... estabelecendo conexão com o servidor")
    caixaInicial = api.get_profile_ansyc()


''' Definições finais antes de iniciar '''




''' Início do programa '''
conexao()
menuPrincipal()
avisos()
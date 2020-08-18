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
caixaInicial = 0
valordeEntrada = 1
optionCod = "EURUSD"
optionType = "BINARY"

def descProgram():
    version = "1.0.02"
    appname = "IQ Option Auxiliar - Jorge Reis "
    os.system('cls')
    print("APP " + appname + "   Versão: " + version)

def descPainel():
    global modoOperacao, caixaInicial, optionCod, optionType
    
    if modoOperacao == "REAL":
        modoOperacaoPainel = "REAL"
    else:
        modoOperacaoPainel = "TREINAMENTO"

    print("Modo: ", Fore.GREEN + modoOperacaoPainel, "    Caixa: ", Fore.GREEN + "R$ " + str(caixaInicial), "    Opção: ", Fore.GREEN + str(optionType), "/", Fore.GREEN + str(optionCod) + "\n")

def menuPrincipal():
    global menuOp
    menuOp = 1
    while menuOp > 0:
        descProgram()
        print('\n MENU PRINCIPAL:')
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
            menuConfig()
            time.sleep(2)
        else:
            print(Fore.YELLOW + "\n ... encerrando aplicativo")
            time.sleep(3)
            os.system('cls')
            break

def menuConfig():
    global modoOperacao, menuOp
    confOp = 1

    while confOp != 0:
        descProgram()
        descPainel()

        if modoOperacao == "REAL":
            modoRun = "TREINAMENTO"
        else:
            modoRun = "REAL"

        print(' 2. CONFIGURAÇÕES:')
        print('    [1] - Alterar modo de operação para', Fore.LIGHTYELLOW_EX + modoRun)
        print('    [2] - Alterar opção')
        '''print('    [3] - ALTERAR IDS (COPY TRADER)')
        print('    [4] - BUSCAR MELHORES OPÇÕES, por PAYOUT', Fore.LIGHTGREEN_EX + verPayout)
        print('    [5] - BUSCAR MELHORES OPÇÕES, por USER TOP', Fore.LIGHTGREEN_EX + verRanking)
        print('    [6] - BUSCAR ID DE USUÁRIO PELO NOME')
        print('    [7] - BUSCAR INFO DE USUÁRIO PELO ID')'''
        print('    [8] - FAST BUY')
        print(Fore.LIGHTRED_EX + '\n    [0] - VOLTAR AO MENU PRINCIPAL')

        confOp = int(input("\n Digite o número da opção escolhida: "))

        if confOp == 1:
            alteraModo()
        elif confOp == 2:
            alteraOption()
        elif confOp == 8:
            runConfTeste()
        menuOp = 1


def avisos():
    global modoOperacao
    if modoOperacao == "":
        modoOperacao = "PRACTICE"
        print(Fore.LIGHTYELLOW_EX + " ... definindo modo de operação para Treinamento")

def alteraModo():
    global modoOperacao
    if modoOperacao == "PRACTICE":
        print(Fore.GREEN + " ... alterando modo de operação para Uso real")
        modoOperacao = "REAL"
    else:
        print(Fore.LIGHTYELLOW_EX + " ... alterando modo de operação para Treinamento")
        modoOperacao = "PRACTICE"
    print(Fore.RED + '\n ... voltando para menu anterior')
    time.sleep(2)

def alteraOption():
    global optionCod

    optionCod = str.upper(input('\n Informe uma opção para operar: '))

    if optionCod == "":
        print(' Nenhuma opção foi definida')
    else:
        print(' Opção padrão alterada com sucesso para', Fore.GREEN + optionCod)

    print(Fore.RED + '\n ... voltando para o menu anterior')
    time.sleep(2)

def perfil():
    global api
    perfil = json.loads(json.dumps(api.get_profile_ansyc()))
	
    return perfil

def conexao():
    global api, user, caixaInicial, modoOperacao
    user = userdata.mainUser
    api = IQ_Option(user["username"], user["password"])
    check, reason = api.connect()

    print(Fore.LIGHTYELLOW_EX + "\n ... estabelecendo conexão com o servidor")
    time.sleep(2)
    modoOperacao = api.get_balance_mode()
    caixaInicial = api.get_balance()


def time_converter(x): # Função para converter timestamp
	hora = datetime.strptime(datetime.utcfromtimestamp(x).strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
	hora = hora.replace(tzinfo=tz.gettz('GMT'))
	
	return str(hora)[:-6]

def runConfTeste():
    global api, optionCod

    op = str(input("Informe a operação: [1] Compra  |  [2] Venda ? "))
    if op == 1:
        direction = "call"
        dir = "Compra"
    else:
        direction = "put"
        dir = "Venda"

    entrada = int(input("Informe o valor da entrada: "))
    api.buy(entrada, optionCod, direction, 1)
    print("\n", Fore.GREEN + dir, "de", optionCod, "no valor de R$", round(entrada, 2))
    time.sleep(3)

''' Definições finais antes de iniciar '''




''' Início do programa '''
conexao()
menuPrincipal()
avisos()
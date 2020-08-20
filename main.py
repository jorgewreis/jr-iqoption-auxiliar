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

user = userdata.mainUser
api = IQ_Option(user["username"], user["password"])

''' Config Colorama '''
init(convert=True, autoreset=True)

''' Definições iniciais '''
valordeEntrada = 1
tempoGrafReal = 5
tempoGrafInfo = "5 segundos"
optionCod = "EURUSD"
optionType = "BINARY"


def descProgram():
    version = "1.02"
    appname = "IQ Option Auxiliar - Jorge Reis "
    os.system('cls')
    print("APP " + appname + "   Versão: " + version)

def descPainel():
    global modoOperacao, caixaInicial, optionCod, optionType
    
    if modoOperacao == "REAL":
        modoOperacaoPainel = "REAL"
    else:
        modoOperacaoPainel = "TREINAMENTO"

    print("Modo: ", Fore.GREEN + modoOperacaoPainel, "    Caixa: ", Fore.GREEN + "R$ " + str(caixaInicial), "    Opção: ", Fore.GREEN + str(optionType), "/", Fore.GREEN + str(optionCod) + "    Tempo do gráfico:", tempoGrafInfo + "\n")


def menuPrincipal():
    global menuOp
    menuOp = 1
    while menuOp > 0:
        descProgram()
        print('\n MENU PRINCIPAL:')
        print(' [1] - TRADER')
        print(' [2] - RANKING')
        print(' [3] - CONFIGURAÇÕES')
        print(Fore.LIGHTRED_EX + '\n [0] - SAIR')

        menuOp = int(input('\n Digite o número da opção escolhida: '))

        if menuOp == 1:
            print(Fore.LIGHTYELLOW_EX + '\n ... abrindo opção selecionada')
            print(Fore.RED + " Erro! Opção não configurada")
            time.sleep(2)
        elif menuOp == 2:
            print(Fore.LIGHTYELLOW_EX + '\n ... abrindo opção selecionada')
            funListarRanking()
            time.sleep(2)
        elif menuOp == 3:
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
        print('    [3] - Alterar tempo do gráfico')

        print(Fore.LIGHTRED_EX + '\n    [0] - VOLTAR AO MENU PRINCIPAL')

        confOp = int(input("\n Digite o número da opção escolhida: "))

        if confOp == 1:
            alteraModo()
        elif confOp == 2:
            alteraOption()
        elif confOp == 3:
            alteraTempoGrafico()
        menuOp = 1

def avisos():
    global modoOperacao
    if modoOperacao == "":
        modoOperacao = "PRACTICE"
        print(Fore.LIGHTYELLOW_EX + " ... definindo modo de operação para Treinamento")


def alteraModo():
    global modoOperacao, api, caixaInicial
    if modoOperacao == "PRACTICE":
        print(Fore.GREEN + " ... alterando modo de operação para Uso real")
        modoOperacao = "REAL"
    else:
        print(Fore.LIGHTYELLOW_EX + " ... alterando modo de operação para Treinamento")
        modoOperacao = "PRACTICE"
    print(Fore.RED + '\n ... voltando para menu anterior')
    caixaInicial = api.get_balance()
    time.sleep(2)

def alteraOption():
    global optionCod
    
    os.system('cls')
    optionCod = str.upper(input('\n Informe uma opção para operar: '))

    if optionCod == "":
        print(' Nenhuma opção foi definida')
    else:
        print(' Opção padrão alterada com sucesso para', Fore.GREEN + optionCod)

    print(Fore.RED + '\n ... voltando para o menu anterior')
    time.sleep(2)

def alteraTempoGrafico():
    global tempoGrafReal, tempoGrafInfo
    tempos = [1, 5, 10, 15, 30, 60, 120, 300, 600, 900, 1800, 3600, 7200, 14400, 28800, 43200, 86400, 604800, 2592000]
    escala = ['segundos', 'minutos', 'horas', 'dia', 'semana', 'mês']

    os.system('cls')
    print(" ESCOLHA A ESCALA DE TEMPO: ")

    cont = 1
    for i in escala:
        print("    [" + str(cont) + "] - " + i.upper())
        cont += 1

    tempoEscala = int(input(" > "))-1

    print(" ESCOLHA O TEMPO DO GRÁFICO EM", escala[tempoEscala].upper() + ": ")
    if tempoEscala == 0:
        print("    [1] - SEGUNDO")
        print("    [5] - SEGUNDOS")
        print("    [10] - SEGUNDOS")
        print("    [15] - SEGUNDOS")
        print("    [30] - SEGUNDOS")
        tempo = input(" > ")
        tempoGrafReal = tempo
    elif tempoEscala == 1:
        print("    [1] - MINUTO")
        print("    [2] - MINUTOS")
        print("    [5] - MINUTOS")
        print("    [10] - MINUTOS")
        print("    [15] - MINUTOS")
        print("    [30] - MINUTOS")
        tempo = input(" > ")
        tempoGrafReal = int(tempo) * 60
    elif tempoEscala == 2:
        print("    [1] - HORA")
        print("    [2] - HORAS")
        print("    [4] - HORAS")
        print("    [8] - HORAS")
        print("    [12] - HORAS")
        tempo = input(" > ")
        tempoGrafReal = int(tempo) * 3600
    elif tempoEscala == 3:
        tempo = 1
        tempoGrafReal = tempos[16]
    elif tempoEscala == 4:
        tempo = 1
        tempoGrafReal = tempos[17]
    else:
        tempo = 1
        tempoGrafReal = tempos[18]

    tempoGrafInfo = str(tempo) + " " + str(escala[tempoEscala])
    print(' Tempo gráfico alterado com sucesso para', Fore.GREEN + tempoGrafInfo)

    print(Fore.RED + '\n ... voltando para o menu anterior')
    time.sleep(2)


def perfil():
    global api
    perfil = json.loads(json.dumps(api.get_profile_ansyc()))
	
    return perfil

def timestamp_converter(x, retorno=1):
    hora = datetime.strptime(datetime.utcfromtimestamp(x).strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
    hora = hora.replace(tzinfo=tz.gettz('GMT'))

    return str(hora.astimezone(tz.gettz('America/Sao Paulo')))[:-6] if retorno == 1 else hora.astimezone(
        tz.gettz('America/Sao Paulo'))


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

def funListarRanking():
    global api, menuOp2

    menuOp2 = 1
    frequentOptions = []
    tradersOnline = []
    countTrader = 0
    os.system('cls')

    while menuOp2 == 1:
        qtdTraders = int(input(" Informe quantos traders quer listar: "))
        os.system('cls')
        print(" ... aguarde, buscando lista de traders")
        listaRanking = api.get_leader_board('Worldwide', 1, int(qtdTraders), 0, 0, 0, 0, 0, 2)['result']['positional']
        descProgram()
        print('\n    RANKING')
        print('\n    Listando os', qtdTraders, 'melhores traders \n')

        for n in listaRanking:
            traderId = listaRanking[n]['user_id']
            traderPais = listaRanking[n]['flag']
            traderPerfil = listaRanking[n]['user_name']
            print(api.get_user_profile_client(traderId)[0])

            status = api.get_users_availability(traderId)
            '''traderOption = api.get_name_by_activeId(traderId['statuses'][0]['selected_asset_id'])'''
            traderOptionType = api.get_user_profile_client['statuses'][0]['selected_instrument_type']
            

            if (status['statuses'][0]['status'] == 'online'):
                print('\n', str(n) + ".", traderPerfil, Fore.GREEN + '● online', '(' + traderPais + ') - ID:', traderId)
                print('  operando agora', traderOptionType)
                tradersOnline.append(traderId)
                '''frequentOptions.append(traderOption)'''
                countTrader = countTrader + 1
            else:
                print('\n', str(n) + ".", traderPerfil, '(' + str(traderPais) + ') - ID:', traderId)
        
        if countTrader == 0:
            print('\n Nenhum dos', qtdTraders, 'primeiros traders está online no momento')
        else:
            print('\n ', countTrader, 'dos', qtdTraders, ' estão online no momento')
            print(' Traders online no momento: ', tradersOnline)
        
        listarNovamente()

def listarNovamente():
    global menuOp2
    op2 = input('\n Deseja listar novamente? [S] SIM | [N] Não ')
    if op2 == 'S' or op2 == 's':
        menuOp2 = 1
        os.system('cls')
    else:
        menuOp2 = 0


''' Definições finais antes de iniciar '''

def conexao():
    global api, user, caixaInicial, modoOperacao
    
    print(Fore.LIGHTYELLOW_EX + "\n ... iniciando aplicativo")
    print(Fore.LIGHTYELLOW_EX + " ... estabelecendo conexão com o servidor")
    api.connect()
   
    while True:
        if api.check_connect() == False:
            print(Fore.LIGHTYELLOW_EX + "\n ... tentativa de reconexão")
            api.connect()
        else:
            print(Fore.LIGHTGREEN_EX + "\n     conectado com sucesso!")
            break
    
    time.sleep(2)
    modoOperacao = api.get_balance_mode()
    caixaInicial = api.get_balance()


''' Início do programa '''
conexao()
avisos()
menuPrincipal()
''' Importações de bibliotecas '''
import userdata
import iqoptionapi.country_id as Paises
import time
import json
import os
import collections
import logging
import locale
from colorama import init, Fore, Back, Style
from iqoptionapi.stable_api import IQ_Option
from iqoptionapi.api import Logout
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
modoOperacao = ""


def descProgram():
    version = "1.02.04 Build 10"
    appname = "IQ Option Auxiliar - Jorge Reis "
    os.system('cls')
    print("APP " + appname + "   Versão: " + version)

def descPainel():
    global modoOperacao, caixaInicial, optionCod, optionType
    
    if modoOperacao == "REAL":
        modoOperacaoPainel = "REAL"
    else:
        modoOperacaoPainel = "TREINAMENTO"

    print("Modo: ", Fore.GREEN + modoOperacaoPainel, "    Caixa: ", Fore.GREEN + str(caixaInicial), "    Opção: ", Fore.GREEN + str(optionType), "/", Fore.GREEN + str(optionCod), "    Tempo do gráfico:", Fore.GREEN + tempoGrafInfo + "\n")



def menuPrincipal():
    global menuOp
    menuOp = 1
    while menuOp != 0:
        descProgram()
        print('\n MENU PRINCIPAL:')
        print('\n [1] - Trader (Copy / MHI / Candles)\n')
        print(' [2] - Buscador (Traders / Ranking / Payout / Opções')
        print(' [3] - Opções do Desenvolvedor (Atualizar Ativos)')
        print(' [4] - Configurações')
        
        print(Fore.LIGHTRED_EX + '\n pressione qualquer outra tecla para sair')

        menuOp = input('\n Digite o número da opção escolhida: ')

        if menuOp == '1':
            print(Fore.LIGHTYELLOW_EX + '\n ... abrindo opção selecionada')
            print(Fore.RED + " Erro! Opção não configurada")
            time.sleep(3)
        elif menuOp == '2':
            menuBuscador()
            time.sleep(1)
        elif menuOp == '4':
            menuConfig()
            time.sleep(1)
        elif menuOp == '3':
            menuDev()
            time.sleep(1)
        else:
            print(Fore.YELLOW + "\n ... encerrando aplicativo")
            time.sleep(2)
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

        print(' 4. CONFIGURAÇÕES:\n')
        print('    [1] - Alterar modo de operação para', Fore.LIGHTYELLOW_EX + modoRun)
        print('    [2] - Alterar opção')
        print('    [3] - Alterar tempo do gráfico')

        print(Fore.LIGHTRED_EX + '\n    pressione qualquer outra tecla para voltar')

        confOp = input("\n Digite o número da opção escolhida: ")
        if confOp == '1':
            alteraModo()
        elif confOp == '2':
            alteraOption()
        elif confOp == '3':
            alteraTempoGrafico()
        else:
            break
        
        menuOp = 1

def menuBuscador():
    global modoOperacao, menuOp
    confOp = 1

    while confOp != 0:
        descProgram()
        
        print('\n 2. BUSCAR:\n')
        print('    [1] - Buscar Ranking de traders')

        print(Fore.LIGHTRED_EX + '\n    pressione qualquer outra tecla para voltar')

        confOp = input("\n Digite o número da opção escolhida: ")
        if confOp == '1':
            print(Fore.LIGHTYELLOW_EX + '\n ... abrindo opção selecionada')
            funListarRanking()
            time.sleep(2)
        else:
            break
        
        menuOp = 1

def menuDev():
    global modoOperacao, menuOp
    confOp = 1

    while confOp != 0:
        descProgram()
        
        print('\n 3. DESENVOLVEDOR:\n')
        print('    [1] - Atualizar lista de ativos')

        print(Fore.LIGHTRED_EX + '\n    pressione qualquer outra tecla para voltar')

        confOp = input("\n Digite o número da opção escolhida: ")
        if confOp == '1':
            print(Fore.LIGHTYELLOW_EX + '\n ... abrindo opção selecionada')
            runListarConst()
            time.sleep(2)
        else:
            break
        
        menuOp = 1
        

def alteraModo():
    global modoOperacao, api, caixaInicial
    os.system('cls')
    
    if modoOperacao == "PRACTICE":
        print(Fore.LIGHTYELLOW_EX + " Modo alterado para Real")
        api.change_balance("REAL")
        caixaInicial = locale.currency(api.get_balances()['msg'][0]['amount'], grouping=True)
    else:
        print(Fore.LIGHTYELLOW_EX + " Modo alterado para Treinamento")
        api.change_balance("PRACTICE")
        caixaInicial = locale.currency(api.get_balances()['msg'][1]['amount'], grouping=True)
    print('\n ... voltando para menu anterior')
    modoOperacao = api.get_balance_mode()
    
    time.sleep(2)

def alteraOption():
    global optionCod
    os.system('cls')
    optionCod = str.upper(input('\n Informe uma opção para operar: '))

    if optionCod == "":
        print(' Nenhuma opção foi definida')
    else:
        print(Fore.LIGHTYELLOW_EX + ' Opção padrão alterada para', Fore.GREEN + optionCod)

    print('\n ... voltando para o menu anterior')
    time.sleep(2)

def alteraTempoGrafico():
    global tempoGrafReal, tempoGrafInfo
    tempos = [1, 5, 10, 15, 30, 60, 120, 300, 600, 900, 1800, 3600, 7200, 14400, 28800, 43200, 86400, 604800, 2592000]
    escala = ['segundo', 'minuto', 'hora', 'dia', 'semana', 'mês']
    tempoGrafReal = ""
    tempoGrafInfo = ""
    os.system('cls')
    print(" ESCOLHA A ESCALA DE TEMPO: ")

    cont = 1
    for i in escala:
        print("    [" + str(cont) + "] - " + i.upper())
        cont += 1
    tempoEscala = int(input("\n Informe a escala: "))-1
  
    os.system('cls')
    print(" ESCOLHA O TEMPO DO GRÁFICO: ")
    if tempoEscala == 0:
        tempoSeg = tempos[0:5]
        cont = 0
        for i in tempoSeg:
            if i != 1:
                plural = 's'
            else:
                plural = ''
            print("    " + str(i), (escala[0] + plural).upper())
        
        while tempoGrafReal == "":
            tempo = input("\n Informe o tempo gráfico: ")
            for i in tempoSeg:
                if tempo == str(i):
                    tempoGrafReal = tempo
                    tempoGrafInfo = str(tempo) + " " + str(escala[0]) + plural
                    
    elif tempoEscala == 1:
        tempoMin = tempos[5:11]
        cont = 0
        for i in tempoMin:
            j = int(i/60)
            if j != 1:
                plural = 's'
            else:
                plural = ''
            print("    " + str(j), (escala[1] + plural).upper())
        
        while tempoGrafReal == "":
            tempo = input("\n Informe o tempo gráfico: ")
            for i in tempoMin:
                j = int(i/60)
                if tempo == str(j):
                    if j > 1:
                        plural = 's'
                    else:
                        plural = ''
                    tempoGrafReal = int(tempo) * 60
                    tempoGrafInfo = str(tempo) + " " + str(escala[1]) + plural

    elif tempoEscala == 2:
        tempoHor = tempos[11:16]
        cont = 0
        for i in tempoHor:
            j = int(i/3600)
            if j > 1:
                plural = 's'
            else:
                plural = ''
            print("    " + str(j), (escala[2] + plural).upper())
        
        while tempoGrafReal == "":
            tempo = input("\n Informe o tempo gráfico: ")
            for i in tempoHor:
                j = int(i/3600)
                if tempo == str(j):
                    if j > 1:
                        plural = 's'
                    else:
                        plural = ''
                    tempoGrafReal = int(tempo) * 3600
                    tempoGrafInfo = str(tempo) + " " + str(escala[2]) + plural
                    
    elif tempoEscala == 3:
        tempo = 1
        tempoGrafReal = tempos[16]
        tempoGrafInfo = str(tempo) + " " + str(escala[3])
    elif tempoEscala == 4:
        tempo = 1
        tempoGrafReal = tempos[17]
        tempoGrafInfo = str(tempo) + " " + str(escala[4])
    else:
        tempo = 1
        tempoGrafReal = tempos[18]
        tempoGrafInfo = str(tempo) + " " + str(escala[5])

    print(Fore.LIGHTYELLOW_EX + ' Tempo gráfico alterado para', Fore.GREEN + tempoGrafInfo)
    print('\n ... voltando para o menu anterior')
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

def runListarConst():
    n = 1
    while n <= 1400:
        if api.get_financial_information(n)['msg']['data']['active'] != None:
            option = api.get_financial_information(n)['msg']['data']['active']['name']
            print("'" + option.upper() + "':", str(n) + ",")
        n = n + 1
    
    listarNovamente()

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
            traderPerfil = api.get_user_profile_client(traderId)['user_name']
            traderVip = api.get_user_profile_client(traderId)['is_vip']
            
            
            try:
                traderOption = api.get_name_by_activeId(api.get_users_availability(traderId)['statuses'][0]['selected_asset_id'])
                #print(api.get_users_availability(traderId)['statuses'][0]['selected_asset_id'])
            except:
                traderOption = ""
            
            try:
                # api.get_users_availability(traderId)['statuses'][0]['selected_asset_id']
                # api.get_financial_information(api.get_users_availability(traderId)['statuses'][0]
                traderOptionType = api.get_users_availability(traderId)['statuses'][0]['selected_instrument_type'].upper()
            except:
                traderOptionType = ""
                        
            status = api.get_users_availability(traderId)
            
            if (status['statuses'][0]['status'] == 'online'):
                if traderVip == True:
                    infoVip = "VIP"
                else:
                    infoVip = ""
                                                    
                print('\n', str(n) + ".", Fore.GREEN + traderPerfil, Fore.GREEN + infoVip + '● online', '(' + traderPais + ') - ID:', traderId)
                if traderOption != "":
                    print('     operando agora', traderOptionType, "-", traderOption)
                                    
                tradersOnline.append(traderId)
                frequentOptions.append(traderOption)
                countTrader = countTrader + 1
            else:
                print('\n', str(n) + ".", traderPerfil, '(' + str(traderPais) + ') - ID:', traderId)
        
        if countTrader == 0:
            print('\n\n Nenhum dos', qtdTraders, 'melhores traders está online no momento')
        else:
            print('\n\n', countTrader, 'dos', qtdTraders, 'melhores traders estão online no momento')
            print(' Ids: ', tradersOnline)
        
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
    os.system('cls')
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
    
    time.sleep(1)
    modoOperacao = api.get_balance_mode()
    
    locale.setlocale(locale.LC_MONETARY, 'pt-BR.UTF-8')
    caixaInicial = locale.currency(api.get_balance(), grouping=True)
    menuPrincipal()


''' Início do programa '''
conexao()
Logout(api)
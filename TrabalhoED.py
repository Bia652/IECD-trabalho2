import sqlite3
import pandas as pd
import numpy as np
import datetime

# Conectar e criar o ficheiro de dados
con = sqlite3.connect('GestaoHospital.db')
cur = con.cursor()
data_hora_atual = datetime.datetime.now()
data_atual = data_hora_atual.strftime('%d/%m/%Y')
hora_atual = data_hora_atual.strftime('%H:%M:%S')

# TABELAS DA BASE DE DADOS
# Ficheiro JSON
utentes = pd.read_json(r"Utentes.json")
utentes_data = pd.DataFrame(utentes)

# Tabela relativa ao menu de secretariado
cur.execute('''CREATE TABLE Secretariado
            ([ID_Utente] integer,
            [Nome] text,
            [Data_Nascimento] date,
            [Genero] integer,
            [Localidade] text,
            [ID_registo] INTEGER PRIMARY KEY,
            [Data_registo] date,
            [Hora_registo] time, 
            [Contacto] contacto
            )
            ''')
con.commit()
utentes_data['Data_registo'] = data_atual
utentes_data['Hora_registo'] = hora_atual
utentes_data.to_sql('Secretariado', con, if_exists='append', index=False)
con.commit()
con.close()

# Tabela relativa ao menu de triagem
con = sqlite3.connect('GestaoHospital.db')
cur = con.cursor()
cur.execute('''CREATE TABLE Triagem
([ID_Utente] integer,
[Nome] text,
[Data_Nascimento] date,
[Genero] integer,
[Localidade] text,
[ID_registo] integer,
[Data_registo] date,
[Hora_registo] time,
[Contacto] integer,
[Peso] integer,
[Dores] binary,
[Alinhamento_arco_pe] integer,
[Media_horas_corrida] float
)''')
con.commit()
con.close()

# Tabela relativa ao menu de consulta médica
con = sqlite3.connect('GestaoHospital.db')
cur = con.cursor()
cur.execute('''CREATE TABLE Consulta_medica
([ID_Utente] text,
[Nome] text,
[Data_Nascimento] date,
[Genero] integer,
[Localidade] text,
[ID_registo] integer,
[Data_registo] date,
[Hora_registo] time,
[Contacto] int,
[Peso] integer,
[Dores] binary,
[Alinhamento_arco_pe] integer,
[Media_horas_corrida] float,
[Idade] integer,
[Diagnostico_previsto] binary,
[Diagnostico_medico] binary
)''')
con.commit()
con.close()

# FUNÇÕES GERAIS
# Verificação de números (se são int e estão dentro do intervalo)
def verifica_num(num_min, num_max, pergunta):
    resp = 0
    while type(resp) is not int or resp > num_max or resp < num_min:
        resp = eval(input(pergunta))
        if type(resp) != int or resp > num_max or resp < num_min:
            print("Tem de inserir um número entre", num_min, "e", num_max)

    return resp

# MENU PRINCIPAL
def menu_principal():
    print()
    print("MENU PRINCIPAL")
    print("1 - Secretariado")
    print("2 - Triagem")
    print("3 - Consulta médica")
    print("4 - Utente")
    print("5 - Desligar")
    print()
    resposta = verifica_num (1, 5, "Insira a opção que pretende: ")
    match resposta:
        case 1:
            menu_secretariado()
        case 2:
            menu_triagem()
        case 3:
            menu_consulta_medica()
        case 4:
            menu_utente()
        case 5:
            print("Pretende mesmo desligar? (1 - Sim, 2 - Não)")
            resposta = verifica_num (1, 2, "Indique a sua resposta: ")
            print()
            match resposta:
                case 1:
                    print("Programa Finalizado")
                case 2:
                    print ('Regressando ao menu principal...')
                    menu_principal()
                    
# 1 - MENU DE SECRETARIADO
def menu_secretariado():
    print()
    print("MENU SECRETARIADO")
    print("1 - Criação de ficha de utente")
    print("2 - Consulta dos dados de utente")
    print("3 - Atualização dos dados de utente")
    print("4 - Eliminação de ficha de utente")
    print("5 - Relatório estatístico")
    print("6 - Página Anterior")
    print()
    resposta = verifica_num(1, 6, "Insira a opção que pretende: ")
    match resposta:
        case 1:
            cartao = input("Insira o seu número de utente: ")
            cria_utente(cartao)
        case 2:
            cartao = input("Insira o seu número de utente: ")
            consulta_secretariado(cartao)
        case 3:
            cartao = input("Insira o seu número de utente: ")
            atualiza_secretariado(cartao)
        case 4:
            cartao = input("Insira o seu número de utente: ")
            elimina_utente(cartao)
        case 5:
            relatorio_estatistico()
        case 6:
            menu_principal()

# Criação de nova ficha de utente
def cria_utente(cartao):
    data_hora_atual = datetime.datetime.now()
    data_atual = data_hora_atual.strftime('%d/%m/%Y')
    hora_atual = data_hora_atual.strftime('%H:%M:%S')
    con = sqlite3.connect('GestaoHospital.db')
    cur = con.cursor()
    cur.execute('''SELECT * FROM Secretariado WHERE ID_Utente = ?''', (cartao,))
    # se o cartão já existe
    if cur.fetchone():
        print()
        print('Já existe ficha de utente com esse número de utente!')
        print('Tentar de novo? (1 - Sim, 2 - Não)')
        resp = verifica_num(1, 2, 'Insira a opção que pretende: ')
        match resp:
            case 1:
                print('Regressando ao menu de secretariado...')
                menu_secretariado()
            case 2:
                print()
                print('Operação cancelada')
                print('Regressando ao menu principal...')
                menu_principal()
    # se o cartão não existe
    else:
        nome = input("Nome: ")
        data = input("Data de nascimento: ")
        genero = int(input('Género (0 - Feminino, 1 - Masculino): '))
        localidade = input("Localidade a que pertence: ")
        contacto = input("Contacto: ")
        print()
        cur.execute('''INSERT INTO Secretariado (ID_Utente, Nome, Data_Nascimento, Genero, Localidade, Data_registo, Hora_registo, Contacto)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                    (cartao, nome, data, genero, localidade, data_atual, hora_atual, contacto))
        con.commit()
        print()
        print('Ficha de utente criada com sucesso')
        print('Regressando ao menu principal...')
        menu_principal()
    con.close()

# Consulta dos dados de utente (Secretariado)
def consulta_secretariado(cartao):
    con = sqlite3.connect('GestaoHospital.db')
    cur = con.cursor()
    cur.execute('''SELECT * FROM Secretariado WHERE ID_Utente = ?''', (cartao,))
    resultado = cur.fetchone()
    if resultado:
        print()
        print('ID de utente: ', resultado[0])
        print('Nome: ', resultado[1])
        print('Data de Nascimento: ', resultado[2])
        if resultado[3] == 0:
            res = 'Feminino'
        else:
            res = 'Masculino'
        print('Género: ', res)        
        print('Localidade: ', resultado[4])
        print('ID de registo: ', resultado[5])
        print('Data de Registo: ', resultado[6])
        print('Hora de Registo: ', resultado[7])
        print('Contacto: ', resultado[8])
        print()
        print('Regressando ao menu principal...')
        menu_principal()
    else:
        print()
        print('Não existe ficha de utente com esse número!')
        print('Regressando ao menu de secretariado...')
        menu_secretariado()
    con.close()

# Atualização dos dados de utente (Secretariado)
def atualiza_secretariado(cartao):
    con = sqlite3.connect('GestaoHospital.db')
    cur = con.cursor()
    cur.execute('''SELECT * FROM Secretariado WHERE ID_Utente = ?''', (cartao,))
    if cur.fetchone():
        print("Insira as informações de atualização de ficha de utente")
        nome = input("Nome: ")
        data = input("Data de nascimento: ")
        genero = input('Género (0 - Feminino, 1 - Masculino): ')
        localidade = input("Localidade a que pertence: ")
        contacto = input("Contacto: ")
        cur.execute('''UPDATE Secretariado 
        SET Nome = ?, Data_Nascimento = ?, Genero = ?, Localidade = ?, Contacto = ?
        WHERE ID_Utente = ?''', (nome, data, genero, localidade, contacto, cartao))
        con.commit()
        # e atualiza a ficha do utente caso também esteja na triagem
        cur.execute('''SELECT * FROM Triagem WHERE ID_Utente = ?''', (cartao,))
        resultado = cur.fetchone()
        if resultado:
            cur.execute('''UPDATE Triagem 
            SET Nome = ?, Data_Nascimento = ?, Genero = ?, Localidade = ?, Contacto = ?
            WHERE ID_Utente = ?''', (nome, data, genero, localidade, contacto, cartao))
            con.commit()
        # ou caso esteja na consulta médica também
        cur.execute('''SELECT * FROM Consulta_medica WHERE ID_Utente = ?''', (cartao,))
        resultado = cur.fetchone()
        if resultado:
            cur.execute('''UPDATE Consulta_medica 
            SET Nome = ?, Data_Nascimento = ?, Genero = ?, Localidade = ?, Contacto = ?
            WHERE ID_Utente = ?''', (nome, data, genero, localidade, contacto, cartao))
            con.commit()
        print()
        print('Ficha de utente atualizada com sucesso!')
        print('Regressando ao menu principal...')
        menu_principal()
    else:
        print()
        print("Não existe ficha de utente com esse ID!")
        print("Regressando ao menu de secretariado...")
        menu_secretariado()
    con.close()

# Elimina utente com o id = cartao
def elimina_utente(cartao):
    con = sqlite3.connect('GestaoHospital.db')
    cur = con.cursor()
    cur.execute('''SELECT * FROM Secretariado WHERE ID_Utente = ?''', (cartao,))
    if cur.fetchone():
        cur.execute('''DELETE FROM Secretariado WHERE ID_Utente = ?''', (cartao,))
        con.commit()
        print()
        print('Utente eliminado com sucesso')
        print('Regressando ao menu principal...')
        menu_principal()
    else:
        print()
        print('Não existe ficha de utente com esse ID!')
        print('Regressando ao menu de secretariado...')
        menu_secretariado()
    con.close()

# Relatório estatístico (Secretariado)
def relatorio_estatistico():
    con = sqlite3.connect('GestaoHospital.db')
    cur = con.cursor()
    cur.execute('''SELECT * FROM Consulta_medica''')
    resultado = cur.fetchall()
    negativos = 0
    positivos = 0
    if resultado:
        for i in range(len(resultado)):
            if resultado[i][15] == 0:
                negativos += 1
            else:
                positivos += 1
        print()
        print('NÚMERO DE UTENTES COM FASCITE:', positivos, '; NÚMERO DE UTENTES SEM FASCITE:', negativos)
        print('Regressando ao menu principal...')
        menu_principal()
    else:
        print()
        print('NÚMERO DE UTENTES COM FASCITE: 0; NÚMERO DE UTENTES SEM FASCITE: 0')
        print('Regressando ao menu de secretariado...')
        menu_secretariado()
    con.close()

# 2 - MENU DE TRIAGEM
def menu_triagem():
    print()
    print("MENU TRIAGEM")
    print("1 - Atualização de ficha de utente")
    print("2 - Consulta dos dados de utente")
    print("3 - Página Anterior")
    print()
    resposta = verifica_num(1, 3, "Insira a opção que pretende: ")
    match resposta:
        case 1:
            cartao = input("Insira o seu número de utente: ")
            atualiza_triagem(cartao)
        case 2:
            cartao = input("Insira o seu número de utente: ")
            consulta_triagem(cartao)
        case 3:
            menu_principal()

# Atualização dos dados de utente (Triagem)
def atualiza_triagem(cartao):
    con = sqlite3.connect('GestaoHospital.db')
    cur = con.cursor()
    # Verificamos se paciente existe na tabela de triagem
    cur.execute('''SELECT * FROM Triagem WHERE ID_Utente = ?''', (cartao,))
    resultado1 = cur.fetchone()
    # se existe apenas atualizamos as informações de peso, dores, etc.
    if resultado1:
        print('Insira as informações a atualizar')
        peso = input('Insira o peso: ')
        dores = input("Dores nas articulações? (0 - Não, 1 - Sim): ")
        alinhamento_arco_pe = input("Alinhamento do arco do pé (0 - Normal, 1 - Arco alto, 2 - Pé chato): ")
        horas_corrida = media_horas_corrida()
        cur.execute('''UPDATE Triagem 
        SET Peso = ?, Dores = ?, Alinhamento_arco_pe = ?, Media_horas_corrida = ? 
        WHERE ID_Utente = ?''', (peso, dores, alinhamento_arco_pe, horas_corrida,cartao))
        con.commit()
        print()
        print('Atualizado com sucesso')
        print('Regressando ao menu principal...')
        menu_principal()
    # se não podem acontecer duas alternativas
    else:
        cur.execute('''SELECT * FROM Secretariado WHERE ID_Utente = ?''', (cartao,))
        resultado2 = cur.fetchone()
        # se estiver no secretariado, adicionamos e atualizamos os dados à tabela triagem
        if resultado2:
            peso = input("Insira o peso: ")
            dores = input("Dores nas articulações? (0 - Não, 1 - Sim): ")
            alinhamento_arco_pe = input("Alinhamento do arco do pé (0 - Normal, 1 - Arco alto, 2 - Pé chato): ")
            horas_corrida = media_horas_corrida()
            cur.execute('''INSERT INTO Triagem (ID_Utente, Nome, Data_Nascimento, Genero, Localidade,ID_registo, Data_registo, Hora_registo, Contacto, Peso, Dores, Alinhamento_arco_pe,Media_horas_corrida)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)''', (resultado2[0], resultado2[1], resultado2[2], resultado2[3], resultado2[4], resultado2[5], resultado2[6],
            resultado2[7], resultado2[8], peso, dores, alinhamento_arco_pe, horas_corrida))
            con.commit()
            print()
            print('Ficha de utente atualizada com sucesso!')
            print('Regressando ao menu principal...')
            menu_principal()
        # se não, não existe ficha de utente na base de dados
        else:
            print()
            print('Não existe ficha de utente com esse ID registado no Secretariado!')
            print("Regressando ao menu de triagem...")
            menu_triagem()
    con.close()

# Consulta da ficha de utente (Triagem)
def consulta_triagem(cartao):
    con = sqlite3.connect('GestaoHospital.db')
    cur = con.cursor()
    # Verificar se está na triagem
    cur.execute('''SELECT * FROM Triagem WHERE ID_Utente = ?''', (cartao,))
    resultado1 = cur.fetchone()
    # se estiver na triagem consultamos na própria tabela
    if resultado1:
        print()
        print('ID de utente: ', resultado1[0])
        print('Nome: ', resultado1[1])
        print('Data de Nascimento: ', resultado1[2])
        if resultado1[3] == 0:
            res1 = 'Feminino'
        else:
            res1 = 'Masculino'    
        print('Género: ', res1)
        print('Localidade: ', resultado1[4])
        print('ID de Registo: ', resultado1[5])
        print('Data de Registo: ', resultado1[6])
        print('Hora de Registo: ', resultado1[7])
        print('Contacto: ', resultado1[8])
        print('Peso: ', resultado1[9])
        if resultado1 [10] == 0:
            res2 = "Não tem"
        else:
            res2 = "Tem"
        print('Dores: ', res2)
        if resultado1 [11] == 0:
            res3 = "Normal"
        elif resultado1 [11] == 1:
            res3 = "Arco alto"
        elif resultado1 [11] == 2:
            res3 = "Pé chato"
        print('Alinhamento do arco do pé: ', res3)
        print('Média de horas de corrida por semana: ', resultado1[12])
        print()
        print('Regressando ao menu principal...')
        menu_principal()
    # se não estiver vamos buscar ao secretariado (se existir)
    else:
        cur.execute('''SELECT * FROM Secretariado WHERE ID_Utente = ?''', (cartao,))
        resultado2 = cur.fetchone()
        if resultado2:
            print()
            print('ID de utente: ', resultado2[0])
            print('Nome: ', resultado2[1])
            print('Data de Nascimento: ', resultado2[2])
            if resultado2[3] == 0:
                res1 = 'Feminino'
            else:
                res1 = 'Masculino'
            print('Género: ', res1)
            print('Localidade: ', resultado2[4])
            print('ID de Registo: ', resultado2[5])
            print('Data de Registo: ', resultado2[6])
            print('Hora de Registo: ', resultado2[7])
            print('Contacto: ', resultado2[8])
            print()
            print('Regressando ao menu principal...')
            menu_principal()
        else:
            print()
            print('Não existe ficha de utente com esse ID registado no Secretariado!')
            print('Regressando ao menu de triagem...')
            menu_triagem()
    con.close()

# 3 - MENU DE CONSULTA MÉDICA
def menu_consulta_medica():
    print ()
    print("MENU CONSULTA MÉDICA")
    print("1 - Consulta de ficha de utente")
    print("2 - Atualização da ficha de utente")
    print("3 - Página Anterior")
    print()
    resposta = verifica_num(1, 3, "Insira a opção que pretende: ")
    match resposta:
        case 1:
            cartao = input("Insira o seu número de utente: ")
            consulta_consulta_medica(cartao)
        case 2:
            cartao = input("Insira o seu número de utente: ")
            atualizacao_consulta_medica(cartao)
        case 3:
            menu_principal()

# Aquisição de dados
dados = np.loadtxt("dadosFascite.txt")
idade = dados[:, 1]
genero = dados[:, 2]
peso = dados[:, 3]
horasCorrida = dados[:, 4]
doresArticulacoes = dados[:, 6]
alinhamentoArcoPe = dados[:, 7]
diagnostico = dados[:, 12]

# Atualização da ficha de utente
def atualizacao_consulta_medica(cartao):
    data_atual = datetime.datetime.now().date()
    con = sqlite3.connect('GestaoHospital.db')
    cur = con.cursor()
    Doente = np.where(diagnostico == 1)  # índice dos doentes
    Saudavel = np.where(diagnostico == 0)  # índice dos saudáveis
    media_PesoD = np.mean(peso[Doente])  # média (do peso) representativa de uma pessoa doente
    media_PesoS = np.mean(peso[Saudavel])  # média (do peso) representativa de uma pessoa saudável
    media_Horas_CorridaD = np.mean(horasCorrida[Doente])
    media_Horas_CorridaS = np.mean(horasCorrida[Saudavel])
    media_AlinhamentoD = np.mean(alinhamentoArcoPe[Doente])
    media_AlinhamentoS = np.mean(alinhamentoArcoPe[Saudavel])
    # características representativas de uma pessoa saudável
    pessoa_Saudavel = np.array([media_PesoS, media_AlinhamentoS, media_Horas_CorridaS])
    # características representativas de uma pessoa doente
    pessoa_Doente = np.array([media_PesoD, media_AlinhamentoD, media_Horas_CorridaD])
    cur.execute('''SELECT * FROM Triagem WHERE ID_Utente = ?''', (cartao,))
    resultado = cur.fetchone()
    if resultado:
        # converter data de nascimento para objeto date
        data_nascimento = datetime.datetime.strptime(resultado[2], '%d/%m/%Y').date()
        # calcular a idade em anos
        idade = data_atual.year - data_nascimento.year
        # verificar se é necessário subtrair 1 ano
        if (data_atual.month, data_atual.day) < (data_nascimento.month, data_nascimento.day):
            idade -= 1
        pessoa = np.array([resultado[9], resultado[11], resultado[12]])
        d0 = np.linalg.norm(pessoa_Saudavel - pessoa)
        d1 = np.linalg.norm(pessoa_Doente - pessoa)
        if d1 < d0:
            diagnostico_previsto = 1
        else:
            diagnostico_previsto = 0
        print ()
        print ('O diagnóstico previsto é:', diagnostico_previsto)
        diagnostico_medico = input('Insira o diagnóstico do paciente (0 - Saudável, 1 - Tem fascite): ')
        cur.execute('''INSERT INTO Consulta_medica (ID_Utente, Nome, Data_Nascimento, Genero, Localidade, ID_registo,Data_registo, Hora_registo, Contacto, Peso, Dores, Alinhamento_arco_pe, Media_horas_corrida, Idade, Diagnostico_previsto,Diagnostico_medico) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',(resultado[0], resultado[1], resultado[2], resultado[3], resultado[4], resultado[5], resultado[6],resultado[7], resultado[8], resultado[9], resultado[10], resultado[11], resultado[12], idade,diagnostico_previsto, diagnostico_medico))
        con.commit()
        print()
        print('Atualizado com sucesso!')
        print('Regressando ao menu principal...')
        menu_principal()
    else:
        print()
        print('Não existe ficha de utente com esse ID na tabela de Triagem!')
        print('Regressando ao menu de consulta...')
        menu_consulta_medica()
    con.close()

# Consulta de ficha de utente (Consulta médica)
def consulta_consulta_medica(cartao):
    con = sqlite3.connect('GestaoHospital.db')
    cur = con.cursor()
    data_hora_atual = datetime.datetime.now()
    data_atual = data_hora_atual.strftime('%d/%m/%Y')
    hora_atual = data_hora_atual.strftime('%H:%M:%S')
    cur.execute('''SELECT * FROM Consulta_medica WHERE ID_Utente = ?''', (cartao,))
    resultado = cur.fetchone()
    if resultado:
        print()
        print('ID de utente: ', resultado[0])
        print('Nome: ', resultado[1])
        print('Data de Nascimento: ', resultado[2])
        if resultado[3] == 0:
            res1 = 'Feminino'
        else:
            res1 = 'Masculino'
        print('Género: ', res1)
        print('Localidade: ', resultado[4])
        print('ID de Registo: ', resultado[5])
        print('Data de Registo: ', resultado[6])
        print('Hora de Registo: ', resultado[7])
        print('Contacto: ', resultado[8])
        print('Peso: ', resultado[9])
        if resultado [10] == 0:
            res2 = "Não tem"
        else:
            res2 = "Tem"
        print('Dores: ', res2)
        if resultado [11] == 0:
            res3 = "Normal"
        elif resultado [11] == 1:
            res3 = "Arco alto"
        elif resultado [11] == 2:
            res3 = "Pé chato"
        print('Alinhamento do arco do pé: ', res3)  
        print('Média de horas de corrida por semana: ', resultado[12])
        print('Idade: ', resultado[13])
        if resultado[14] == 0:
            res2 = 'Negativo'
        else:
            res2 = 'Positivo'
        print('Diagnóstico previsto (através do modelo): ', res2)
        if resultado[15] == 0:
            res3 = 'Negativo'
        else:
            res3 = 'Positivo'
        print('Diagnóstico do médico : ', res3)
        print()
        print('Regressando ao menu principal...')
        menu_principal()
    else:
        cur.execute ('''SELECT * FROM Triagem WHERE ID_Utente = ?''', (cartao,))
        resultado = cur.fetchone ()
        if resultado:
            print()
            print('ID de utente: ', resultado[0])
            print('Nome: ', resultado[1])
            print('Data de Nascimento: ', resultado[2])
            if resultado[3] == 0:
                res1 = 'Feminino'
            else:
                res1 = 'Masculino'
            print('Género: ', res1)
            print('Localidade: ', resultado[4])
            print('ID de Registo: ', resultado[5])
            print('Data de Registo: ', resultado[6])
            print('Hora de Registo: ', resultado[7])
            print('Contacto: ', resultado[8])
            print('Peso: ', resultado[9])
            if resultado [10] == 0:
                res2 = "Não tem"
            else:
                res2 = "Tem"
            print('Dores: ', res2)
            if resultado [11] == 0:
                res3 = "Normal"
            elif resultado [11] == 1:
                res3 = "Arco alto"
            elif resultado [11] == 2:
                res3 = "Pé chato"
            print('Alinhamento do arco do pé: ', res3)   
            print('Média de horas de corrida por semana: ', resultado[12])
            print('Regressando ao menu principal...')
            menu_principal ()
        else:
            print()
            print('O utente ainda não passou por triagem!')
            print('Regressando ao menu de triagem...')
            menu_triagem()
    con.close()

# 4 - MENU DE UTENTE
def menu_utente():
    print()
    print("MENU UTENTE")
    print("1 - Consulta da decisão médica")
    print("2 - Página Anterior")
    print()
    resposta = verifica_num(1, 2, "Insira a opção que pretende: ")
    match resposta:
        case 1:
            cartao = input('Insira o seu número de utente: ')
            consulta_utente(cartao)
        case 2:
            menu_principal()

# Consulta de ficha de utente (Utente)
def consulta_utente(cartao):
    con = sqlite3.connect('GestaoHospital.db')
    cur = con.cursor()
    cur.execute('''SELECT * FROM Consulta_medica WHERE ID_Utente = ?''', (cartao,))
    resultado = cur.fetchone()
    if resultado:
        if resultado[15] == 0:
            res = 'Negativo'
        else:
            res = 'Positivo'
        print()
        print('Diagnóstico médico: Testou', res, 'para Fascite Plantar')
        print('Regressando ao menu principal...')
        menu_principal()

    else:
        print()
        print('Não existe utente com esse número que tenha tido consulta!')
        print('Regressando ao menu de utente...')
        menu_utente()
    con.close()

def media_horas_corrida():
    print ()
    print ('Média de horas de corrida por semana:')
    print ('1 - Ficheiro csv (calcula automaticamente)')
    print ('2 - Estimativa das horas corridas')
    print ('3 - Sem dados (retorna ao menu principal)')
    res = verifica_num (1,3,'Insira a opção que pretende: ')
    match res:
        case 1:
            nome_fich = input("Insira o nome do ficheiro csv: ")
            try:
                df = pd.read_csv(nome_fich, delimiter=';')
                df['Data'] = pd.to_datetime(df['Data'], dayfirst=True)
                # Calculamos a soma de horas de corrida por dia
                soma_horas_dia = df.groupby(df['Data'].dt.date)['Horas_corrida'].sum().reset_index()
                soma_horas_dia['Data'] = pd.to_datetime(soma_horas_dia['Data'])
                # isocalendar().week vai buscar o número da semana do ano correspondente
                soma_horas_dia['Semana'] = soma_horas_dia['Data'].dt.isocalendar().week
                # Agrupamos os registros por semana e calculamos a soma da coluna Horas_corrida
                soma_horas_semana = soma_horas_dia.groupby('Semana')['Horas_corrida'].sum().reset_index()
                # Exiba o resultado
                media_horas = soma_horas_semana['Horas_corrida'].mean()
                return media_horas
            except FileNotFoundError:
                print()
                print('Não existe ficheiro com esse nome! Aponte as suas horas de corrida e volte mais tarde!')
                print('Regressando ao menu de triagem...')
                menu_triagem() 
        case 2:
            media_horas = eval (input ('Insira a sua estimativa: '))
            return media_horas
        case 3:
            menu_principal ()

# Chamamos o menu principal
menu_principal()
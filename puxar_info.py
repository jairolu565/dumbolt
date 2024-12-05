import paramiko
import time
import threading
import json
from flask import Flask, jsonify, request, send_file, abort
import os


ip_novo_horizonte = '10.90.10.10'
ip_doron = '10.50.64.2'
ip_brotas = '10.50.61.252'
ip_eng_velho = '1'
ip_boca_do_rio = '10.50.61.254'
ip_sussuarana = '10.90.10.2'
ip_arvoredo = ''

# Função para inicializar a conexão SSH uma única vez
def inicializar_conexao_novo_horizonte(hostname, username, password):
    global client_novo_horizonte, shell_novo_horizonte
    client_novo_horizonte = paramiko.SSHClient()
    client_novo_horizonte.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    print(f"Tentando conectar ao {hostname}...")
    
    try:
        print('Iniciando conexão SSH...')
        client_novo_horizonte.connect(hostname=hostname, username=username, password=password, timeout=60)
        print(f"Conectado ao {hostname}")
        shell_novo_horizonte = client_novo_horizonte.invoke_shell()
        time.sleep(1)
        # envia conf t para entrar no modo de configuração
        shell_novo_horizonte.send('terminal length 0\n')
        time.sleep(1)
        shell_novo_horizonte.send('conf t\n')
        time.sleep(1)
        output = shell_novo_horizonte.recv(1000).decode('utf-8')
        print(output)
    except paramiko.SSHException as e:
        print(f"Erro de SSH: {e}")

def inicializar_conexao_doron(hostname, username, password):
    global client_doron, shell_doron
    client_doron = paramiko.SSHClient()
    client_doron.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    print(f"Tentando conectar ao {hostname}...")
    
    try:
        print('Iniciando conexão SSH...')
        client_doron.connect(hostname=hostname, username=username, password=password, timeout=60)
        print(f"Conectado ao {hostname}")
        shell_doron = client_doron.invoke_shell()
        time.sleep(1)
        # envia conf t para entrar no modo de configuração
        shell_doron.send('terminal length 0\n')
        time.sleep(1)
        shell_doron.send('conf t\n')
        time.sleep(1)
        output = shell_doron.recv(1000).decode('utf-8')
        print(output)
    except paramiko.SSHException as e:
        print(f"Erro de SSH: {e}")

def inicializar_conexao_brotas(hostname, username, password):
    global client_brotas, shell_brotas
    client_brotas = paramiko.SSHClient()
    client_brotas.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    print(f"Tentando conectar ao {hostname}...")
    
    try:
        print('Iniciando conexão SSH...')
        client_brotas.connect(hostname=hostname, username=username, password=password, timeout=60)
        print(f"Conectado ao {hostname}")
        shell_brotas = client_brotas.invoke_shell()
        time.sleep(1)
        # envia conf t para entrar no modo de configuração
        shell_brotas.send('terminal length 0\n')
        time.sleep(1)
        shell_brotas.send('conf t\n')
        time.sleep(1)
        output = shell_brotas.recv(1000).decode('utf-8')
        print(output)
    except paramiko.SSHException as e:
        print(f"Erro de SSH: {e}")

def inicializar_conexao_eng_velho(hostname, username, password):
    global client_eng_velho, shell_eng_velho
    client_eng_velho = paramiko.SSHClient()
    client_eng_velho.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    print(f"Tentando conectar ao {hostname}...")
    
    try:
        print('Iniciando conexão SSH...')
        client_eng_velho.connect(hostname=hostname, username=username, password=password, timeout=60)
        print(f"Conectado ao {hostname}")
        shell_eng_velho = client_eng_velho.invoke_shell()
        time.sleep(1)
        # envia conf t para entrar no modo de configuração
        shell_eng_velho.send('terminal length 0\n')
        time.sleep(1)
        shell_eng_velho.send('conf t\n')
        time.sleep(1)
        output = shell_eng_velho.recv(1000).decode('utf-8')
        print(output)
    except paramiko.SSHException as e:
        print(f"Erro de SSH: {e}")

def inicializar_conexao_boca_do_rio(hostname, username, password):
    global client_boca_do_rio, shell_boca_do_rio
    client_boca_do_rio = paramiko.SSHClient()
    client_boca_do_rio.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    print(f"Tentando conectar ao {hostname}...")
    
    try:
        print('Iniciando conexão SSH...')
        client_boca_do_rio.connect(hostname=hostname, username=username, password=password, timeout=60)
        print(f"Conectado ao {hostname}")
        shell_boca_do_rio = client_boca_do_rio.invoke_shell()
        time.sleep(1)
        # envia conf t para entrar no modo de configuração
        shell_boca_do_rio.send('terminal length 0\n')
        time.sleep(1)
        shell_boca_do_rio.send('conf t\n')
        time.sleep(1)
        output = shell_boca_do_rio.recv(1000).decode('utf-8')
        print(output)
    except paramiko.SSHException as e:
        print(f"Erro de SSH: {e}")

def inicializar_conexao_sussuarana(hostname, username, password):
    global client_sussuarana, shell_sussuarana
    client_sussuarana = paramiko.SSHClient()
    client_sussuarana.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    print(f"Tentando conectar ao {hostname}...")
    
    try:
        print('Iniciando conexão SSH...')
        client_sussuarana.connect(hostname=hostname, username=username, password=password, timeout=60)
        print(f"Conectado ao {hostname}")
        shell_sussuarana = client_sussuarana.invoke_shell()
        time.sleep(1)
        # envia conf t para entrar no modo de configuração
        shell_sussuarana.send('terminal length 0\n')
        time.sleep(1)
        shell_sussuarana.send('conf t\n')
        time.sleep(1)
        output = shell_sussuarana.recv(1000).decode('utf-8')
        print(output)
    except paramiko.SSHException as e:
        print(f"Erro de SSH: {e}")

#______________________________________________________________________________________________________________________

def gerar_comandos_novo_horizonte():
    print('Gerando comandos para o novo horizonte...')
    comandos = [
        'show processor',
        'show gpon onu uncfg',
        'show gpon onu state'
    ]

    output_data = []

    for comando in comandos:
        shell_novo_horizonte.send(comando + '\n')
        time.sleep(1)
        output = ''
        if 'show gpon onu state' in comando:
            while True:
                part = shell_novo_horizonte.recv(1000).decode('utf-8')
                output += part
                if 'ONU Number:' in output:
                    break
        else:
            output = shell_novo_horizonte.recv(100000).decode('utf-8')
        
        # Adiciona o comando e sua saída à lista de dados
        output_data.append(f'Comando: {comando}\n')
        output_data.append('Saída:\n')
        output_data.append(output)
        output_data.append('\n' + '-'*80 + '\n')

    # Escreve todos os dados no arquivo de uma vez
    with open('novo_horizonte.txt', 'w') as f:
        f.writelines(output_data)

    print('Comandos gerados com sucesso para o novo horizonte')

def gerar_comandos_doron():
    print('Gerando comandos para o doron...')
    comandos = [
        'show processor',
        'show gpon onu uncfg',
        'show gpon onu state'
    ]

    output_data = []

    for comando in comandos:
        shell_doron.send(comando + '\n')
        time.sleep(1)
        output = ''
        if 'show gpon onu state' in comando:
            while True:
                part = shell_doron.recv(1000).decode('utf-8')
                output += part
                if 'ONU Number:' in output:
                    break
        else:
            output = shell_doron.recv(100000).decode('utf-8')
        
        # Adiciona o comando e sua saída à lista de dados
        output_data.append(f'Comando: {comando}\n')
        output_data.append('Saída:\n')
        output_data.append(output)
        output_data.append('\n' + '-'*80 + '\n')

    # Escreve todos os dados no arquivo de uma vez
    with open('doron.txt', 'w') as f:
        f.writelines(output_data)

    print('Comandos gerados com sucesso para o doron')

def gerar_comandos_brotas():
    print('Gerando comandos para o brotas...')
    comandos = [
        'show processor',
        'show pon onu uncfg',
        'show gpon onu state'
    ]

    output_data = []

    for comando in comandos:
        shell_brotas.send(comando + '\n')
        time.sleep(1)
        output = ''
        if 'show gpon onu state' in comando:
            while True:
                part = shell_brotas.recv(1000).decode('utf-8')
                output += part
                if 'ONU Number:' in output:
                    break
        elif 'show pon onu uncfg' in comando:
            if 'gpon-onu' not in output:
                output = 'No related information to show.'
        else:
            output = shell_brotas.recv(100000).decode('utf-8')
        
        # Adiciona o comando e sua saída à lista de dados
        output_data.append(f'Comando: {comando}\n')
        output_data.append('Saída:\n')
        output_data.append(output)
        output_data.append('\n' + '-'*80 + '\n')

    # Escreve todos os dados no arquivo de uma vez
    with open('brotas.txt', 'w') as f:
        f.writelines(output_data)

    print('Comandos gerados com sucesso para o brotas')

def gerar_comandos_eng_velho():
    print('Gerando comandos para o eng velho...')
    comandos = [
        'show processor',
        'show gpon onu uncfg',
        'show gpon onu state'
    ]

    output_data = []

    for comando in comandos:
        shell_eng_velho.send(comando + '\n')
        time.sleep(1)
        output = ''
        if 'show gpon onu state' in comando:
            while True:
                part = shell_eng_velho.recv(1000).decode('utf-8')
                output += part
                if 'ONU Number:' in output:
                    break
        else:
            output = shell_eng_velho.recv(100000).decode('utf-8')
        
        # Adiciona o comando e sua saída à lista de dados
        output_data.append(f'Comando: {comando}\n')
        output_data.append('Saída:\n')
        output_data.append(output)
        output_data.append('\n' + '-'*80 + '\n')

    # Escreve todos os dados no arquivo de uma vez
    with open('eng_velho.txt', 'w') as f:
        f.writelines(output_data)

    print('Comandos gerados com sucesso para o eng velho')

def gerar_comandos_boca_do_rio():
    print('Gerando comandos para o boca do rio...')
    comandos = [
        'show processor',
        'show pon onu uncfg',
        'show gpon onu state'
    ]

    output_data = []

    for comando in comandos:
        shell_boca_do_rio.send(comando + '\n')
        time.sleep(1)
        output = ''
        if 'show gpon onu state' in comando:
            while True:
                part = shell_boca_do_rio.recv(1000).decode('utf-8')
                output += part
                if 'ONU Number:' in output:
                    break
        elif 'show pon onu uncfg' in comando:
            output = shell_boca_do_rio.recv(100000).decode('utf-8')
            if 'gpon-onu' not in output:
                output = 'No related information to show.'
        else:
            output = shell_boca_do_rio.recv(100000).decode('utf-8')
        
        # Adiciona o comando e sua saída à lista de dados
        output_data.append(f'Comando: {comando}\n')
        output_data.append('Saída:\n')
        output_data.append(output)
        output_data.append('\n' + '-'*80 + '\n')

    # Escreve todos os dados no arquivo de uma vez
    with open('boca_do_rio.txt', 'w') as f:
        f.writelines(output_data)

    print('Comandos gerados com sucesso para o boca do rio')

def gerar_comandos_sussuarana():
    print('Gerando comandos para o sussuarana...')
    comandos = [
        'show processor',
        'show gpon onu uncfg',
        'show gpon onu state'
    ]

    output_data = []

    for comando in comandos:
        shell_sussuarana.send(comando + '\n')
        time.sleep(1)
        output = ''
        if 'show gpon onu state' in comando:
            while True:
                part = shell_sussuarana.recv(1000).decode('utf-8')
                output += part
                if 'ONU Number:' in output:
                    break
        else:
            output = shell_sussuarana.recv(100000).decode('utf-8')
        
        # Adiciona o comando e sua saída à lista de dados
        output_data.append(f'Comando: {comando}\n')
        output_data.append('Saída:\n')
        output_data.append(output)
        output_data.append('\n' + '-'*80 + '\n')

    # Escreve todos os dados no arquivo de uma vez
    with open('sussuarana.txt', 'w') as f:
        f.writelines(output_data)

    print('Comandos gerados com sucesso para o sussuarana')

#______________________________________________________________________________________________________________________

def comando_procurar_onu(serial_number, olt, shell_dict):
    shell = shell_dict.get(olt)
    if shell:
        print(shell)
        time.sleep(1)
        shell.send('show gpon onu by sn ' + serial_number + '\n')
        time.sleep(1)
        output = shell.recv(100000).decode('utf-8')
        print(output)
        output = output.split('\n')
        onu_id = None
        for line in output:
            if 'gpon-onu' in line:
                print(line)
                onu_id = line.split('_')[1]
                break
            elif 'gpon_onu' in line:
                print(line)
                onu_id = line.split('-')[1]
                break
        if onu_id:
            shell.send('show gpon onu detail-info gpon-onu_' + onu_id + '\n')
            time.sleep(1)
            output = shell.recv(100000).decode('utf-8')
            print(output)
            return output
        else:
            return 'ONU não encontrada'
    else:
        raise ValueError('OLT não encontrada')
    
def comando_deletar_onu(serial_number, olt, shell_dict):
    shell = shell_dict.get(olt)
    if shell:
        print(shell)
        time.sleep(1)
        shell.send('show gpon onu by sn ' + serial_number + '\n')
        time.sleep(1)
        output = shell.recv(100000).decode('utf-8')
        print(output)
        output = output.split('\n')
        onu_id = None
        for line in output:
            if 'gpon-onu' in line:
                print(line)
                onu_id = line.split('_')[1]
                break
            elif 'gpon_onu-' in line:
                print(line)
                onu_idd = line.split('-')[1]
                break
        if onu_id:
            interface = onu_id.split(':')[0]
            shell.send('interface gpon-olt_' + interface + '\n')
            time.sleep(1)
            onu_id = onu_id.split(':')[1]
            shell.send('no onu ' + onu_id + '\n')
            time.sleep(1)
            output = shell.recv(100000).decode('utf-8')
            print(output)
            output = output.split('\n')
            output = [line for line in output if '.[Successful]' in line]
            if '.[Successful]' in output:
                return 'sucesso'
        elif onu_idd:
            interface = onu_idd.split(':')[0]
            shell.send('interface gpon_olt-' + interface + '\n')
            time.sleep(1)
            onu_idd = onu_idd.split(':')[1]
            shell.send('no onu ' + onu_idd + '\n')
            time.sleep(1)
            output = shell.recv(100000).decode('utf-8')
            print(output)
            output = output.split('\n')
            output = [line for line in output if '.[Successful]' in line]
            if 'The config does not exist.' in output:
                return 'falha'
            else:
                return 'sucesso'
        else:
            raise ValueError('ONU ID não encontrado')
    else:
        raise ValueError('OLT não encontrada')

# Função para inicializar conexões em threads separadas
def iniciar_conexoes():
    threads = []
    threads.append(threading.Thread(target=inicializar_conexao_novo_horizonte, args=(ip_novo_horizonte, 'luigi', 'Acessy@2024')))
    threads.append(threading.Thread(target=inicializar_conexao_doron, args=(ip_doron, 'luigi', 'Acessy@2024')))
    threads.append(threading.Thread(target=inicializar_conexao_brotas, args=(ip_brotas, 'luigi', 'Acessy@2024')))
    # threads.append(threading.Thread(target=inicializar_conexao_eng_velho, args=(ip_eng_velho, 'luigi', 'Acessy@2024')))
    threads.append(threading.Thread(target=inicializar_conexao_boca_do_rio, args=(ip_boca_do_rio, 'luigi', 'Acessy@2024')))
    threads.append(threading.Thread(target=inicializar_conexao_sussuarana, args=(ip_sussuarana, 'luigi', 'Acessy@2024')))


    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

iniciar_conexoes()

# Atualização contínua do arquivo JSON
def atualiza_dados_periodicamente():
    while True:
        gerar_comandos_doron()
        gerar_comandos_novo_horizonte()
        gerar_comandos_brotas()
        #gerar_comandos_eng_velho()
        gerar_comandos_boca_do_rio()
        gerar_comandos_sussuarana()
        time.sleep(120)  # Atualiza a cada 60 segundos

import time
from flask import Flask, jsonify

app = Flask(__name__)
    
@app.route('/novo_horizonte', methods=['GET'])
def get_novo_horizonte_data():
    with open('novo_horizonte.txt', 'r') as file:
        data = file.read()
    return jsonify({'data': data})

@app.route('/doron', methods=['GET'])
def get_doron_data():
    with open('doron.txt', 'r') as file:
        data = file.read()
    return jsonify({'data': data})

@app.route('/brotas', methods=['GET'])
def get_brotas_data():
    with open('brotas.txt', 'r') as file:
        data = file.read()
    return jsonify({'data': data})

@app.route('/boca_do_rio', methods=['GET'])
def get_boca_do_rio_data():
    with open('boca_do_rio.txt', 'r') as file:
        data = file.read()
    return jsonify({'data': data})

@app.route('/sussuarana', methods=['GET'])
def get_sussuarana_data():
    with open('sussuarana.txt', 'r') as file:
        data = file.read()
    return jsonify({'data': data})

FILES_DIRECTORY = 'C:\\Users\\Administrador.WIN-VVRBA7RCFO8\Documents\\tcc'

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    # Caminho completo do arquivo
    file_path = os.path.join(FILES_DIRECTORY, filename)

    # Verifica se o arquivo existe no servidor
    if os.path.exists(file_path):
        # Envia o arquivo como anexo para download
        return send_file(file_path, as_attachment=True)
    else:
        # Retorna erro 404 se o arquivo não for encontrado
        abort(404, description="File not found")

@app.route('/update', methods=['GET'])
def app_version():
    with open('version.txt', 'r') as file:
        data = file.read()
    return jsonify({'data': data})

# Função para carregar as credenciais de usuários do arquivo JSON
def load_users_data():
    with open('usuarios.json', 'r') as file:
        return json.load(file)

@app.route('/users', methods=['GET'])
def get_users():
    users_data = load_users_data()
    return jsonify(users_data)

# Rota para receber o POST
@app.route('/procurar_onu', methods=['POST'])
def procurar_onu():
    # Extrai os dados da requisição JSON
    data = request.get_json()
    serial_number = data.get('serial_number')
    olt = data.get('olt')

    shell_dict = {
        "olt_1": shell_novo_horizonte,
        "olt_2": shell_doron,
        "olt_3": shell_boca_do_rio,
        "olt_4": shell_sussuarana,
        "olt_5": shell_brotas
    }

    try:
        # Chama a função existente
        result = comando_procurar_onu(serial_number, olt, shell_dict)
        return result
    except ValueError as e:
        return e
    
@app.route('/deletar_onu', methods=['POST'])
def deletar_onu():
    # Extrai os dados da requisição JSON
    data = request.get_json()
    serial_number = data.get('serial_number')
    olt = data.get('olt')

    shell_dict = {
        "olt_1": shell_novo_horizonte,
        "olt_2": shell_doron,
        "olt_3": shell_boca_do_rio,
        "olt_4": shell_sussuarana,
        "olt_5": shell_brotas
    }

    try:
        # Chama a função existente
        result = comando_deletar_onu(serial_number, olt, shell_dict)
        return result
    except ValueError as e:
        return e

if __name__ == '__main__':
    # Inicia a coleta de dados em background
    import threading
    data_thread = threading.Thread(target=atualiza_dados_periodicamente)
    data_thread.start()
    
    # Executa a API Flask para atender às requisições dos clientes
    app.run(host='0.0.0.0', port=5000)
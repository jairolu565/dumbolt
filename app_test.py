import customtkinter
import customtkinter as ctk
import tkinter
from tkinter import Tk
import random
from PIL import Image, ImageEnhance, ImageDraw, ImageFont, ImageTk
from auth_google import login
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os
import time
import paramiko
import re
from collections import defaultdict
import threading
import requests
import json
import datetime

hostname = '10.90.10.10'
username = 'luigi'
password = '0Eq36!Q0Eq36Eq36'

# Variáveis globais para SSH
client = None
shell = None

# Função para inicializar a conexão SSH uma única vez
def inicializar_conexao_ssh(hostname, username, password):
    global client, shell
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        client.connect(hostname=hostname, username=username, password=password, timeout=60)
        shell = client.invoke_shell()
        time.sleep(1)
        # envia conf t para entrar no modo de configuração
        shell.send('terminal length 0\n')
        time.sleep(1)
        shell.send('conf t\n')
        time.sleep(1)
        output = shell.recv(1000).decode('utf-8')
    except paramiko.SSHException as e:
        print(f"Erro de SSH: {e}")
    
def fechar_conexao_ssh():
    global client
    if client:
        client.close()

# Reutilizar o shell já conectado para enviar comandos
def enviar_comando_shell(comando):
    global shell
    try:
        if shell:
            shell.send(comando + '\n')
            time.sleep(2)
            output = shell.recv(1000000).decode('utf-8')
            return output
        else:
            return "Erro: Conexão SSH não iniciada."
    except Exception as e:
        return f"Erro ao enviar comando: {e}"

def get_user_nam(token_path='token.json'):
    # Carrega as credenciais do arquivo token.json
    creds = None
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path)
    # Constrói o serviço do Google Drive
    service = build('drive', 'v3', credentials=creds)

    # Obtém informações do perfil do usuário
    try:
        about = service.about().get(fields='user').execute()
        print(f"Usuário: {about['user']['displayName']}")
        return about['user']['displayName']
        
    except Exception as e:
        print(f"Erro ao obter informações do usuário: {e}")
        if 'Token has been expired or revoked.' in str(e):
            print("O token expirou ou foi revogado. Por favor, gere um novo token.")
            return 'expired'

customtkinter.set_appearance_mode("system")  # set appearance mode to system

def home_page():
    app = customtkinter.CTk()  #creating cutstom tkinter window
    app.geometry("1600x800")
    app.title('Home')
    app._state_before_windows_set_titlebar_color = 'zoomed'

    tabview = customtkinter.CTkTabview(master=app, width=1600, height=1000, fg_color='transparent')
    tabview.pack(padx=20, pady=20)

    tabview.add("OLT ZTE - Novo Horizonte")  # add tab at the end
    tabview.add("OLT ZTE - Doron")  # add tab at the end
    tabview.add("OLT ZTE - Boca do Rio")  # add tab at the end
    tabview.add("OLT ZTE - Sussuarana")  # add tab at the end
    tabview.add("OLT ZTE - Brotas") # add tab at the end
    tabview.set("OLT ZTE - Novo Horizonte")  # set currently visible tab
    
    # Função para carregar configurações existentes do arquivo JSON
    def carregar_config():
        try:
            with open('config.json', 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
    
    # Função para salvar configurações atualizadas no arquivo JSON
    def salvar_config(config):
        with open('config.json', 'w') as f:
            json.dump(config, f)
        
    cor = carregar_config()
    if cor['cor'] == 'Azul':
        if cor['tema'] == 'Claro':
            customtkinter.set_appearance_mode("light")
            tabview.configure(segmented_button_selected_color=cor['azul_claro'])
            tabview.configure(text_color='black')
        else:
            customtkinter.set_appearance_mode("dark")
            tabview.configure(segmented_button_selected_color=cor['azul_escuro'])
            tabview.configure(text_color='white')
    elif cor['cor'] == 'Verde':
        if cor['tema'] == 'Claro':
            customtkinter.set_appearance_mode("light")
            tabview.configure(segmented_button_selected_color=cor['verde_claro'])
            tabview.configure(text_color='black')
        else:
            customtkinter.set_appearance_mode("dark")
            tabview.configure(segmented_button_selected_color=cor['verde_escuro'])
            tabview.configure(text_color='white')
    elif cor['cor'] == 'Acessy':
        if cor['tema'] == 'Claro':
            customtkinter.set_appearance_mode("light")
            tabview.configure(segmented_button_selected_color=cor['acessy_claro'])
            tabview.configure(text_color='black')
        else:
            customtkinter.set_appearance_mode("dark")
            tabview.configure(segmented_button_selected_color=cor['acessy_escuro'])
            tabview.configure(text_color='white')

    titulo_novo = customtkinter.CTkLabel(master=tabview.tab('OLT ZTE - Novo Horizonte'), text='OLT ZTE - Novo Horizonte', font=("Josefin Slab Bold", 30))
    titulo_novo.place(relx=0.5, rely=0.1, anchor=tkinter.CENTER)
    titulo_novo.pack_propagate()

    titulo_doron = customtkinter.CTkLabel(master=tabview.tab('OLT ZTE - Doron'), text='OLT ZTE - Doron', font=("Josefin Slab Bold", 30))
    titulo_doron.place(relx=0.5, rely=0.1, anchor=tkinter.CENTER)
    titulo_doron.pack_propagate()

    titulo_boca_do_rio = customtkinter.CTkLabel(master=tabview.tab('OLT ZTE - Boca do Rio'), text='OLT ZTE - Boca do Rio', font=("Josefin Slab Bold", 30))
    titulo_boca_do_rio.place(relx=0.5, rely=0.1, anchor=tkinter.CENTER)
    titulo_boca_do_rio.pack_propagate()

    titulo_sussuarana = customtkinter.CTkLabel(master=tabview.tab('OLT ZTE - Sussuarana'), text='OLT ZTE - Sussuarana', font=("Josefin Slab Bold", 30))
    titulo_sussuarana.place(relx=0.5, rely=0.1, anchor=tkinter.CENTER)
    titulo_sussuarana.pack_propagate()

    titulo_brotas = customtkinter.CTkLabel(master=tabview.tab('OLT ZTE - Brotas'), text='OLT ZTE - Brotas', font=("Josefin Slab Bold", 30))
    titulo_brotas.place(relx=0.5, rely=0.1, anchor=tkinter.CENTER)
    titulo_brotas.pack_propagate()

    logo = customtkinter.CTkImage(Image.open("assets\\logo_acessy.png"), size=(50,50))
    logo_label = customtkinter.CTkLabel(master=app, image=logo, text='')
    logo_label.place(relx=0.03, rely=0.05, anchor=tkinter.CENTER)

    version_label = customtkinter.CTkLabel(master=app, text="Versão - beta1.0.1_aGVhdmVu", font=("Product Sans Regular", 10))
    version_label.place(relx=0.955, rely=0.98, anchor=tkinter.CENTER)

    # IP do servidor onde o Flask está rodando
    server_ip = '100.127.0.250'

    # Função para puxar dados do servidor
    def obter_dados_olt(olt_name, dados_a_consultar):
        url = f'http://{server_ip}:5000/{olt_name}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            for key, value in data.items():
                if 'Comando: show processor' in dados_a_consultar:
                    return value
                elif 'Comando: show gpon onu uncfg' in dados_a_consultar:
                    return value
                elif 'Comando: show gpon onu state' in dados_a_consultar:
                    return value
                elif 'Comando: show pon onu uncfg' in dados_a_consultar:
                    return value

        else:
            print(f"Falha ao obter dados da OLT {olt_name}. Status: {response.status_code}")

    def olt_novo():
        def processamento():
            output = obter_dados_olt('novo_horizonte', 'Comando: show processor')
            time.sleep(2)

            # Expressão regular para capturar o valor de CPU(5s) e memória
            cpu_pattern = re.compile(r'^\s*\d+\s+\d+\s+\d+\s+(\d+)%', re.MULTILINE)
            mem_pattern = re.compile(r'^\s*\d+\s+\d+\s+\d+\s+\d+%\s+(\d+%)', re.MULTILINE)

            cpu_5s_values = cpu_pattern.findall(output)
            mem_values = mem_pattern.findall(output)

            # Exibindo os resultados

            global menu
            menu = customtkinter.CTkFrame(master=tabview.tab('OLT ZTE - Novo Horizonte'), width=400, height=200, corner_radius=30)
            menu.place(relx=0.17, rely=0.3, anchor=tkinter.CENTER)
            menu.pack_propagate(0)

            #faz o menu ser clicável
            menu.bind("<Button-1>", lambda e: print("Clicou no menu"))

            cor = carregar_config()
            if cor['cor'] == 'Azul':
                if cor['tema'] == 'Claro':
                    menu.configure(fg_color=cor['azul_claro'])
                else:
                    menu.configure(fg_color=cor['azul_escuro'])
            elif cor['cor'] == 'Verde':
                if cor['tema'] == 'Claro':
                    menu.configure(fg_color=cor['verde_claro'])
                else:
                    menu.configure(fg_color=cor['verde_escuro'])
            elif cor['cor'] == 'Acessy':
                if cor['tema'] == 'Claro':
                    menu.configure(fg_color=cor['acessy_claro'])
                else:
                    menu.configure(fg_color=cor['acessy_escuro'])

            titulo = customtkinter.CTkLabel(master=menu, text='Processamento', font=("Product Sans Regular", 20))
            titulo.place(relx=0.5, rely=0.15, anchor=tkinter.CENTER)


            labels = ["Rack", "Shelf", "Slot", "CPU", "Mem."]
            for i, label in enumerate(labels):
                customtkinter.CTkLabel(master=menu, text=label, font=("Product Sans Regular", 15)).place(relx=0.1 + i*0.2, rely=0.27, anchor=tkinter.CENTER)

            for i, (cpu, mem) in enumerate(zip(cpu_5s_values, mem_values), 1):
                y = 0.37 + (i-1)*0.1
                mem_percentage = int(mem[:-1])/100
                cpu_percentage = int(cpu)/100

                if mem_percentage < 0.5:
                    cor_mem = 'green'
                elif mem_percentage < 0.8:
                    cor_mem = 'yellow'
                else:
                    cor_mem = 'red'
                mem_bar = customtkinter.CTkProgressBar(master=menu, width=60, height=8, corner_radius=10, progress_color=cor_mem)
                mem_bar.set(mem_percentage)
                mem_bar.place(relx=0.9, rely=y, anchor=tkinter.CENTER)
                mem_label = customtkinter.CTkLabel(master=menu, text=mem, font=("Product Sans Regular", 10), fg_color='transparent')
                mem_label.place(relx=0.9, rely=y, anchor=tkinter.CENTER)

                if cpu_percentage < 0.5:
                    cor_cpu= 'green'
                elif cpu_percentage < 0.8:
                    cor_cpu= 'yellow'
                else:
                    cor_cpu = 'red'
                cpu_bar = customtkinter.CTkProgressBar(master=menu, width=60, height=8, corner_radius=10, progress_color=cor_cpu)
                cpu_bar.set(cpu_percentage)
                cpu_bar.place(relx=0.7, rely=y, anchor=tkinter.CENTER)
                cpu_label = customtkinter.CTkLabel(master=menu, text=cpu+'%', font=("Product Sans Regular", 10), fg_color='transparent')
                cpu_label.place(relx=0.7, rely=y, anchor=tkinter.CENTER)

                customtkinter.CTkLabel(master=menu, text='1', font=("Product Sans Regular", 15)).place(relx=0.1, rely=y, anchor=tkinter.CENTER)
                customtkinter.CTkLabel(master=menu, text='1', font=("Product Sans Regular", 15)).place(relx=0.3, rely=y, anchor=tkinter.CENTER)
                customtkinter.CTkLabel(master=menu, text=str(i), font=("Product Sans Regular", 15)).place(relx=0.5, rely=y, anchor=tkinter.CENTER)

        def onu_solic():
            global menu2
            menu2 = customtkinter.CTkFrame(master=tabview.tab('OLT ZTE - Novo Horizonte'), width=400, height=200, corner_radius=30)
            menu2.place(relx=0.5, rely=0.3, anchor=tkinter.CENTER)
            menu2.pack_propagate()

            cor = carregar_config()
            if cor['cor'] == 'Azul':
                if cor['tema'] == 'Claro':
                    menu2.configure(fg_color=cor['azul_claro'])
                else:
                    menu2.configure(fg_color=cor['azul_escuro'])
            elif cor['cor'] == 'Verde':
                if cor['tema'] == 'Claro':
                    menu2.configure(fg_color=cor['verde_claro'])
                else:
                    menu2.configure(fg_color=cor['verde_escuro'])
            elif cor['cor'] == 'Acessy':
                if cor['tema'] == 'Claro':
                    menu2.configure(fg_color=cor['acessy_claro'])
                else:
                    menu2.configure(fg_color=cor['acessy_escuro'])

            onu_solicitando = customtkinter.CTkLabel(master=menu2, text='ONUs Solicitando', font=("Product Sans Regular", 20))
            onu_solicitando.place(relx=0.5, rely=0.15, anchor=tkinter.CENTER)
            onu_solicitando.pack_propagate()

            posicao = customtkinter.CTkLabel(master=menu2, text='PON', font=("Product Sans Regular", 15))
            posicao.place(relx=0.3, rely=0.27, anchor=tkinter.CENTER)
            posicao.pack_propagate()

            sn = customtkinter.CTkLabel(master=menu2, text='Serial Number', font=("Product Sans Regular", 15))
            sn.place(relx=0.7, rely=0.27, anchor=tkinter.CENTER)
            sn.pack_propagate()

            output = obter_dados_olt('novo_horizonte', 'Comando: show gpon onu uncfg')
            time.sleep(2)
            if 'No related information to show.' in output:
                output = "Nenhuma ONU Solicitando no momento."
                warn = customtkinter.CTkLabel(master=menu2, text='', font=("Segoe Fluent Icons", 30), text_color='red')
                warn.place(relx=0.5, rely=0.38, anchor=tkinter.CENTER)
                info = customtkinter.CTkLabel(master=menu2, text=output, font=("Product Sans Regular", 15), text_color='red')
                info.place(relx=0.5, rely=0.55, anchor=tkinter.CENTER)
                sn.destroy()
                posicao.destroy()
                return
            else:
                output = [line for line in output.splitlines() if line.startswith("gpon-onu")]
                output = "\n".join(output)

                pattern = re.compile(r'(\S+)\s+(\S+)\s+\S+')
                matches = pattern.findall(output)

                for onuindex, sn in matches:
                    onu = customtkinter.CTkLabel(master=menu2, text=onuindex, font=("Product Sans Regular", 15))
                    onu.place(relx=0.3, rely=0.39, anchor=tkinter.CENTER)
                    onu.pack_propagate()

                    sn = customtkinter.CTkLabel(master=menu2, text=sn, font=("Product Sans Regular", 15))
                    sn.place(relx=0.7, rely=0.39, anchor=tkinter.CENTER)
                    sn.pack_propagate()
        
        def pon_percentage():
            global menu3
            menu3 = customtkinter.CTkFrame(master=tabview.tab('OLT ZTE - Novo Horizonte'), width=400, height=200, corner_radius=30)
            menu3.place(relx=0.83, rely=0.3, anchor=tkinter.CENTER)
            menu3.pack_propagate()

            def menu3_toplevel():
                global menu3toplevel
                
                #um grande agradecimento à HyperNylium pela função de centralização da janela: https://github.com/TomSchimansky/CustomTkinter/discussions/1820#discussion-5396625
                def CenterWindowToDisplay(Screen: Tk, width: int, height: int):
                    """Centers the window to the main display/monitor"""
                    screen_width = Screen.winfo_screenwidth()
                    screen_height = Screen.winfo_screenheight()
                    x = int((screen_width/2) - (width/2))
                    y = int((screen_height/2) - (height/1.5))
                    return f"{width}x{height}+{x}+{y}"
                
                menu3toplevel = customtkinter.CTkToplevel(app)
                menu3toplevel.title('Informações de PON')
                menu3toplevel.resizable(False, False)
                
                menu3toplevel.geometry(CenterWindowToDisplay(app, 1000, 800))

                menu3toplevel.attributes('-topmost', True)

                titulo = customtkinter.CTkLabel(master=menu3toplevel, text='Informações de PON', font=("Josefin Slab Bold", 25))
                titulo.place(relx=0.2, rely=0.1, anchor=tkinter.CENTER)
                scrollable_frame = customtkinter.CTkScrollableFrame(master=menu3toplevel, width=800, height=500)
                scrollable_frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

                search_bar = customtkinter.CTkEntry(master=menu3toplevel, width=200, font=("Product Sans Regular", 15), placeholder_text='Pesquisar ONU', corner_radius=40)
                search_bar.place(relx=0.7, rely=0.1, anchor=tkinter.CENTER)
                
                def search():
                    serial_number = search_bar.get()
                    url = 'http://100.127.0.250:5000/procurar_onu'
                    data = {
                        'serial_number': serial_number,
                        'olt': 'olt_1'
                    }

                    #um grande agradecimento à HyperNylium pela função de centralização da janela: https://github.com/TomSchimansky/CustomTkinter/discussions/1820#discussion-5396625
                    def CenterWindowToDisplay(Screen: Tk, width: int, height: int):
                        """Centers the window to the main display/monitor"""
                        screen_width = Screen.winfo_screenwidth()
                        screen_height = Screen.winfo_screenheight()
                        x = int((screen_width/2) - (width/2))
                        y = int((screen_height/2) - (height/1.5))
                        return f"{width}x{height}+{x}+{y}"

                    onu_info_top_level = customtkinter.CTkToplevel(app)
                    onu_info_top_level.title('Informações da ONU')
                    onu_info_top_level.resizable(False, False)

                    onu_info_top_level.geometry(CenterWindowToDisplay(app, 600, 600))

                    onu_info_top_level.attributes('-topmost', True)

                    response = requests.post(url, json=data)
                    response = response.text
                    # Dicionário para armazenar os dados extraídos
                    onu_data = {}

                    def parse_onu_output(output):
                        # Inicializa o dicionário onde os dados serão armazenados
                        onu_info = {}

                        # Separa o texto em linhas
                        lines = output.split('\n')
                        
                        # Variáveis de controle
                        history = []
                        history_section = False

                        # Expressão regular para identificar linhas importantes
                        key_value_pattern = re.compile(r"(\S.*?):\s*(.*)")
                        history_pattern = re.compile(r"\s*(\d+)\s+(\S+\s+\S+)\s+(\S+\s+\S+)\s+(\S+)")

                        for line in lines:
                            line = line.strip()
                            
                            # Verifica se estamos na seção de histórico
                            if line.startswith("Authpass Time"):
                                history_section = True
                                continue
                            
                            # Processa as linhas de histórico
                            if history_section:
                                match = history_pattern.match(line)
                                if match:
                                    event = {
                                        "Authpass Time": match.group(2),
                                        "Offline Time": match.group(3),
                                        "Cause": match.group(4)
                                    }
                                    history.append(event)
                                continue
                            
                            # Processa as linhas chave: valor
                            match = key_value_pattern.match(line)
                            if match:
                                key = match.group(1).strip()
                                value = match.group(2).strip()
                                onu_info[key] = value
                        
                        # Adiciona o histórico ao dicionário
                        if history:
                            onu_info["History"] = history

                        return onu_info
                    
                    onu_data = parse_onu_output(response)

                    x = 0.1
                    # Exibindo as informações da ONU
                    serial_number_label = customtkinter.CTkLabel(master=onu_info_top_level, text=f'Serial Number: {onu_data["Serial number"]}', font=("Josefin Slab Bold", 25))
                    serial_number_label.place(relx=0.5, rely=0.1, anchor=tkinter.CENTER)

                    def delete():
                        serial_number = search_bar.get()
                        url = 'http://100.127.0.250:5000/deletar_onu'
                        data = {
                            'serial_number': serial_number,
                            'olt': 'olt_1'
                        }

                        response = requests.post(url, json=data)
                        response = response.text
                        if response == 'sucesso':
                            onu_info_top_level.destroy()
                            menu3toplevel.destroy()
                        else:
                            print('')

                    delete_img = Image.open("assets\\delete.png", size=(20,20))
                    delete_button = customtkinter.CTkButton(master=onu_info_top_level, text='Deletar ONU', font=("Product Sans Regular", 10), corner_radius=40, fg_color='#fa0000', hover_color='#a80000', image=delete_img, command=delete)
                    delete_button.place(relx=0.5, rely=0.9, anchor=tkinter.CENTER)

                    onu_interface_label = customtkinter.CTkLabel(master=onu_info_top_level, text=f'Interface: {onu_data["ONU interface"]}', font=("Product Sans Regular", 15))
                    onu_interface_label.place(relx=x, rely=0.2, anchor=tkinter.W)

                    name_label = customtkinter.CTkLabel(master=onu_info_top_level, text=f'Nome: {onu_data["Name"]}', font=("Product Sans Regular", 15))
                    name_label.place(relx=x, rely=0.3, anchor=tkinter.W)

                    config_state = customtkinter.CTkLabel(master=onu_info_top_level, text=f'Estado de Configuração: {onu_data["Config state"]}', font=("Product Sans Regular", 15))
                    config_state.place(relx=x, rely=0.4, anchor=tkinter.W)

                    online_duration_label = customtkinter.CTkLabel(master=onu_info_top_level, text=f'Duração Online: {onu_data["Online Duration"]}', font=("Product Sans Regular", 15))
                    online_duration_label.place(relx=x, rely=0.5, anchor=tkinter.W)

                    distance_label = customtkinter.CTkLabel(master=onu_info_top_level, text=f'Distância: {onu_data["ONU Distance"]}', font=("Product Sans Regular", 15))
                    distance_label.place(relx=x, rely=0.6, anchor=tkinter.W)

                search_image = customtkinter.CTkImage(Image.open("assets\\search.png"), size=(20,20))
                search_button = customtkinter.CTkButton(master=menu3toplevel, text='', image=search_image, width=20, corner_radius=40, command=search, fg_color='black', hover_color='gray')
                search_button.place(relx=0.85, rely=0.1, anchor=tkinter.CENTER)

                
                # Função para separar os dados por OnuIndex e cada campo de cada linha
                # Função para separar os dados da ONU
                def separar_por_onuindex(dados):
                    print(dados)
                    # Expressão regular para capturar cada ONU e seus respectivos estados
                    padrao_onu = re.compile(r'(\d+/\d+/\d+:\d+)\s+(\w+)\s+(\w+)\s+(\w+)\s+(\d+\(GPON\))')
                    
                    # Um dicionário para armazenar os resultados separados por OnuIndex
                    onu_separado = {}
                    pon_separado = {}
                    
                    # Iterar sobre todas as correspondências no texto
                    for match in padrao_onu.findall(dados):
                        onuindex = match[0]
                        pon = onuindex.split(':')[0]
                        onu = onuindex.split(':')[1]
                        admin_state = match[1]
                        omcc_state = match[2]
                        phase_state = match[3]
                        channel = match[4]
                        
                        # Criando um dicionário para armazenar os valores de cada ONU
                        onu_detalhes = {
                            'OnuIndex': onuindex,
                            'PON': pon,
                            'ONU': onu,
                            'Admin State': admin_state,
                            'OMCC State': omcc_state,
                            'Phase State': phase_state,
                            'Channel': channel
                        }

                        if pon not in pon_separado:
                            pon_separado[pon] = []

                        pon_separado[pon].append(onu_detalhes)

                        # Adiciona a ONU ao dicionário
                        if onuindex not in onu_separado:
                            onu_separado[onuindex] = []
                        
                        onu_separado[onuindex].append(onu_detalhes)
                    
                    return pon_separado
                # Ensure pon_data is defined

                def obter_dados(olt_name, dados_a_consultar):
                    url = f'http://{server_ip}:5000/{olt_name}'
                    response = requests.get(url)
                    
                    if response.status_code == 200:
                        data = response.text  # Obtendo a resposta como texto bruto
                        # Dividindo o conteúdo por comandos
                        comandos = data.split('--------------------------------------------------------------------------------')

                        # Verifica qual comando foi solicitado e busca o bloco correspondente
                        for comando in comandos:
                            if dados_a_consultar in comando:
                                return comando    

                pon_data = obter_dados('novo_horizonte', 'show gpon onu state')
                time.sleep(2)
                
                # Separar os dados
                onu_separado = separar_por_onuindex(pon_data)

                global current_ponindex
                current_ponindex = 0

                # Função para exibir os dados começando a partir da linha 1
                def display_data():
                    if current_ponindex < len(onu_separado):
                        pon = list(onu_separado.keys())[current_ponindex]
                        registros = onu_separado[pon]

                        # Limpa o frame antes de adicionar novos widgets
                        for widget in scrollable_frame.winfo_children():
                            widget.destroy()

                        # Adiciona o título da PON

                        scrollable_frame.grid_columnconfigure(0, weight=1)
                        scrollable_frame.grid_columnconfigure(1, weight=1)
                        scrollable_frame.grid_columnconfigure(2, weight=1)
                        scrollable_frame.grid_columnconfigure(3, weight=1)
                        scrollable_frame.grid_columnconfigure(4, weight=1)

                        # Adiciona os títulos na linha 0
                        titulo_onuindex = customtkinter.CTkLabel(master=scrollable_frame, text='Onu Número', font=("Product Sans Bold", 20))
                        titulo_onuindex.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')

                        titulo_admin = customtkinter.CTkLabel(master=scrollable_frame, text='Estado Operacional', font=("Product Sans Bold", 20))
                        titulo_admin.grid(row=1, column=1, padx=5, pady=5, sticky='nsew')

                        titulo_omcc = customtkinter.CTkLabel(master=scrollable_frame, text='Estado na OLT', font=("Product Sans Bold", 20))
                        titulo_omcc.grid(row=1, column=2, padx=5, pady=5, sticky='nsew')

                        titulo_phase = customtkinter.CTkLabel(master=scrollable_frame, text='Estado Atual', font=("Product Sans Bold", 20))
                        titulo_phase.grid(row=1, column=3, padx=5, pady=5, sticky='nsew')

                        titulo_channel = customtkinter.CTkLabel(master=scrollable_frame, text='Canal', font=("Product Sans Bold", 20))
                        titulo_channel.grid(row=1, column=4, padx=5, pady=5, sticky='nsew')

                        titulo_pon = customtkinter.CTkLabel(master=scrollable_frame, text=f'PON {pon}', font=("Josefin Slab Bold", 30))
                        #titulo_pon.grid(row=0, column=1, columnspan=5, padx=5, pady=5, sticky='nsew')

                        scrollable_frame.configure(label_text=f'PON {pon}')

                        row_num = 2  # Começa na linha 2 (abaixo dos títulos)
                        for registro in registros:
                            adminstate = registro['Admin State']
                            if adminstate == 'enable':
                                adminstate = 'Ativo'
                            elif adminstate == 'disable':
                                adminstate = 'Inativo'
                            else:
                                adminstate = 'Desconhecido'

                            omccstate = registro['OMCC State']
                            if omccstate == 'enable':
                                omccstate = 'Ativo'
                            elif omccstate == 'disable':
                                omccstate = 'Inativo'

                            
                            label_onuindex = customtkinter.CTkLabel(master=scrollable_frame, text=registro['ONU'], font=("Product Sans Regular", 15))
                            label_onuindex.grid(row=row_num, column=0, padx=5, pady=5, sticky='nsew')
                            label_admin = customtkinter.CTkLabel(master=scrollable_frame, text=adminstate, font=("Product Sans Regular", 15))
                            label_admin.grid(row=row_num, column=1, padx=5, pady=5, sticky='nsew')
                            label_omcc = customtkinter.CTkLabel(master=scrollable_frame, text=omccstate, font=("Product Sans Regular", 15))
                            label_omcc.grid(row=row_num, column=2, padx=5, pady=5, sticky='nsew')
                            label_phase = customtkinter.CTkLabel(master=scrollable_frame, text=registro['Phase State'], width=80, font=("Product Sans Regular", 15), corner_radius=30)
                            label_phase.grid(row=row_num, column=3, padx=5, pady=5, sticky='nsew')

                            phase = registro['Phase State']
                            if phase == 'working':
                                phase = 'Online'
                                label_phase.configure(text=phase, bg_color='#02b302')
                            elif phase == 'OffLine':
                                phase = 'OffLine'
                                label_phase.configure(text=phase, bg_color='red')
                            elif phase == 'DyingGasp':
                                phase = 'Inativo'
                                label_phase.configure(text=phase, bg_color='orange')
                            elif phase == 'LOS':
                                phase = 'Sem Sinal'
                                label_phase.configure(text=phase, bg_color='gray')
                            else:
                                phase = 'Desconhecido'


                            label_channel = customtkinter.CTkLabel(master=scrollable_frame, text=registro['Channel'], font=("Product Sans Regular", 15))
                            label_channel.grid(row=row_num, column=4, padx=5, pady=5, sticky='nsew')
                            row_num += 1  # Próxima linha

                        # Adiciona o botão para o próximo PON
                        def next_pon():
                            global current_ponindex
                            current_ponindex += 1
                            display_data()

                        image_foward = customtkinter.CTkImage(Image.open('assets\\arrow_right.png'), size=(20,20))
                        image_backwards = customtkinter.CTkImage(Image.open('assets\\arrow_left.png'), size=(20,20))
                                                            
                        next_button = customtkinter.CTkButton(master=scrollable_frame, text="Próximo PON", image=image_foward, compound='right', command=next_pon)
                        next_button.grid(row=row_num, column=2, columnspan=5, pady=10)

                        # Adiciona o botão para o PON anterior
                        def previous_pon():
                            global current_ponindex
                            current_ponindex -= 1
                            display_data()

                        previous_button = customtkinter.CTkButton(master=scrollable_frame, text="PON Anterior", image=image_backwards, compound='left', command=previous_pon)
                        previous_button.grid(row=row_num, column=0, columnspan=5, pady=10)

                threading.Thread(target=display_data).start()
            #torna menu3 clicável
            menu3.bind("<Enter>", lambda e: menu3.configure(cursor="hand2"))
            menu3.bind("<Leave>", lambda e: menu3.configure(cursor=""))
            menu3.bind("<Button-1>", lambda e: menu3_toplevel())

            cor = carregar_config()
            if cor['cor'] == 'Azul':
                if cor['tema'] == 'Claro':
                    menu3.configure(fg_color=cor['azul_claro'])
                else:
                    menu3.configure(fg_color=cor['azul_escuro'])
            elif cor['cor'] == 'Verde':
                if cor['tema'] == 'Claro':
                    menu3.configure(fg_color=cor['verde_claro'])
                else:
                    menu3.configure(fg_color=cor['verde_escuro'])
            elif cor['cor'] == 'Acessy':
                if cor['tema'] == 'Claro':
                    menu3.configure(fg_color=cor['acessy_claro'])
                else:
                    menu3.configure(fg_color=cor['acessy_escuro'])

            pon_percentage = customtkinter.CTkLabel(master=menu3, text='PON Percentage', font=("Product Sans Regular", 20))
            pon_percentage.place(relx=0.5, rely=0.15, anchor=tkinter.CENTER)
            pon_percentage.pack_propagate()

            posicao = customtkinter.CTkLabel(master=menu3, text='Posição', font=("Product Sans Regular", 15))
            posicao.place(relx=0.3, rely=0.27, anchor=tkinter.CENTER)
            posicao.pack_propagate()

            sn = customtkinter.CTkLabel(master=menu3, text='Posiões Preenchidas', font=("Product Sans Regular", 15))
            sn.place(relx=0.7, rely=0.27, anchor=tkinter.CENTER)
            sn.pack_propagate()

            def update_pon_data():
                data = obter_dados_olt('novo_horizonte', 'Comando: show gpon onu state')
                time.sleep(2)
                # Expressão regular para capturar o OnuIndex, no formato 1/2/1, etc.
                pattern = re.compile(r'(\d+/\d+/\d+):\d+')

                # Dicionário para armazenar a contagem das ONUs por PON
                pon_counts = defaultdict(int)

                # Encontrar todas as ocorrências de PON e contar
                matches = pattern.findall(data)
                for pon in matches:
                    pon_counts[pon] += 1

                # Exibir o resultado
                for pon, count in pon_counts.items():
                    perc = count / 128

                y = 0.39
                for pon, count in pon_counts.items():
                    perc = count / 128

                    onu = customtkinter.CTkLabel(master=menu3, text=pon, font=("Product Sans Regular", 15))
                    onu.place(relx=0.3, rely=y, anchor=tkinter.CENTER)
                    onu.pack_propagate()

                    if perc < 0.5:
                        cor = 'green'
                    elif perc < 0.8:
                        cor = 'yellow'
                    else:
                        cor = 'red'

                    progress_bar = customtkinter.CTkProgressBar(master=menu3, width=200, height=10, corner_radius=10, progress_color=cor)
                    progress_bar.set(perc)
                    progress_bar.place(relx=0.7, rely=y, anchor=tkinter.CENTER)
                    sn = customtkinter.CTkLabel(master=menu3, text=f'{count}/128', font=("Product Sans Regular", 10), bg_color='transparent')
                    sn.place(relx=0.7, rely=y, anchor=tkinter.CENTER)
                    sn.pack_propagate()

                    y += 0.1

                    #se tiver mais de 6 itens, para a execução
                    if y > 0.9:
                        break

                texto_aguarde.destroy()

            # Run the update_pon_data function in a separate thread to keep the UI responsive
            threading.Thread(target=update_pon_data).start()

        def batch_commands():
            global menu4
            # Get the screen width to dynamically set the width of menu4
            screen_width = app.winfo_screenwidth()
            screen_height = app.winfo_screenheight()
            menu4_width = screen_width - 100  # Adjust the width as needed
            menu4_height = screen_height - 500  # Adjust the height as needed

            menu4 = customtkinter.CTkFrame(master=tabview.tab('OLT ZTE - Novo Horizonte'), width=menu4_width, height=menu4_height, corner_radius=30)
            menu4.place(relx=0.5, rely=0.75, anchor=tkinter.CENTER)

            # cor = carregar_config()
            # if cor['cor'] == 'Azul':
            #     if cor['tema'] == 'Claro':
            #         menu4.configure(fg_color=cor['azul_claro'])
            #     else:
            #         menu4.configure(fg_color=cor['azul_escuro'])
            # elif cor['cor'] == 'Verde':
            #     if cor['tema'] == 'Claro':
            #         menu4.configure(fg_color=cor['verde_claro'])
            #     else:
            #         menu4.configure(fg_color=cor['verde_escuro'])
            # elif cor['cor'] == 'Acessy':
            #     if cor['tema'] == 'Claro':
            #         menu4.configure(fg_color=cor['acessy_claro'])
            #     else:
            #         menu4.configure(fg_color=cor['acessy_escuro'])

            titulo = customtkinter.CTkLabel(master=menu4, text='Executar comandos em lotes', font=("Product Sans Regular", 20))
            titulo.place(relx=0.5, rely=0.1, anchor=tkinter.CENTER)
            titulo.pack_propagate()
    
        texto_aguarde = customtkinter.CTkLabel(master=tabview.tab('OLT ZTE - Novo Horizonte'), text='Por favor, aguarde enquanto as informações são carregadas...', font=("Josefin Slab Light", 20))
        texto_aguarde.place(relx=0.5, rely=0.7, anchor=tkinter.CENTER)

        def process_functions():
            # Wait for the SSH initialization thread to finish
            #ssh_thread.join()
            onu_solic()
            processamento()
            pon_percentage()
            batch_commands()

        # Create a thread to run the process_functions
        thread = threading.Thread(target=process_functions)
        thread.start()

    def olt_doron():
        def processamento():
            output = obter_dados_olt('doron', 'Comando: show processor')
            time.sleep(2)

            # Expressão regular para capturar o valor de CPU(5s) e memória
            cpu_pattern = re.compile(r'^\s*\d+\s+\d+\s+\d+\s+(\d+)%', re.MULTILINE)
            mem_pattern = re.compile(r'^\s*\d+\s+\d+\s+\d+\s+\d+%\s+(\d+%)', re.MULTILINE)

            cpu_5s_values = cpu_pattern.findall(output)
            mem_values = mem_pattern.findall(output)

            # Exibindo os resultados

            global menu_doron
            menu_doron = customtkinter.CTkFrame(master=tabview.tab('OLT ZTE - Doron'), width=400, height=200, corner_radius=30)
            menu_doron.place(relx=0.17, rely=0.3, anchor=tkinter.CENTER)
            menu_doron.pack_propagate(0)

            #faz o menu_doron ser clicável
            menu_doron.bind("<Button-1>", lambda e: print("Clicou no menu_doron"))

            cor = carregar_config()
            if cor['cor'] == 'Azul':
                if cor['tema'] == 'Claro':
                    menu_doron.configure(fg_color=cor['azul_claro'])
                else:
                    menu_doron.configure(fg_color=cor['azul_escuro'])
            elif cor['cor'] == 'Verde':
                if cor['tema'] == 'Claro':
                    menu_doron.configure(fg_color=cor['verde_claro'])
                else:
                    menu_doron.configure(fg_color=cor['verde_escuro'])
            elif cor['cor'] == 'Acessy':
                if cor['tema'] == 'Claro':
                    menu_doron.configure(fg_color=cor['acessy_claro'])
                else:
                    menu_doron.configure(fg_color=cor['acessy_escuro'])

            titulo = customtkinter.CTkLabel(master=menu_doron, text='Processamento', font=("Product Sans Regular", 20))
            titulo.place(relx=0.5, rely=0.15, anchor=tkinter.CENTER)


            labels = ["Rack", "Shelf", "Slot", "CPU", "Mem."]
            for i, label in enumerate(labels):
                customtkinter.CTkLabel(master=menu_doron, text=label, font=("Product Sans Regular", 15)).place(relx=0.1 + i*0.2, rely=0.27, anchor=tkinter.CENTER)

            for i, (cpu, mem) in enumerate(zip(cpu_5s_values, mem_values), 1):
                if i > 6:
                    break
                y = 0.37 + (i-1)*0.1
                mem_percentage = int(mem[:-1])/100
                cpu_percentage = int(cpu)/100

                if mem_percentage < 0.5:
                    cor_mem = 'green'
                elif mem_percentage < 0.8:
                    cor_mem = 'yellow'
                else:
                    cor_mem = 'red'
                mem_bar = customtkinter.CTkProgressBar(master=menu_doron, width=60, height=8, corner_radius=10, progress_color=cor_mem)
                mem_bar.set(mem_percentage)
                mem_bar.place(relx=0.9, rely=y, anchor=tkinter.CENTER)
                mem_label = customtkinter.CTkLabel(master=menu_doron, text=mem, font=("Product Sans Regular", 10), fg_color='transparent')
                mem_label.place(relx=0.9, rely=y, anchor=tkinter.CENTER)

                if cpu_percentage < 0.5:
                    cor_cpu= 'green'
                elif cpu_percentage < 0.8:
                    cor_cpu= 'yellow'
                else:
                    cor_cpu = 'red'
                cpu_bar = customtkinter.CTkProgressBar(master=menu_doron, width=60, height=8, corner_radius=10, progress_color=cor_cpu)
                cpu_bar.set(cpu_percentage)
                cpu_bar.place(relx=0.7, rely=y, anchor=tkinter.CENTER)
                cpu_label = customtkinter.CTkLabel(master=menu_doron, text=cpu+'%', font=("Product Sans Regular", 10), fg_color='transparent')
                cpu_label.place(relx=0.7, rely=y, anchor=tkinter.CENTER)

                customtkinter.CTkLabel(master=menu_doron, text='1', font=("Product Sans Regular", 15)).place(relx=0.1, rely=y, anchor=tkinter.CENTER)
                customtkinter.CTkLabel(master=menu_doron, text='1', font=("Product Sans Regular", 15)).place(relx=0.3, rely=y, anchor=tkinter.CENTER)
                customtkinter.CTkLabel(master=menu_doron, text=str(i), font=("Product Sans Regular", 15)).place(relx=0.5, rely=y, anchor=tkinter.CENTER)

        def onu_solic():
            global menu_doron2
            menu_doron2 = customtkinter.CTkFrame(master=tabview.tab('OLT ZTE - Doron'), width=400, height=200, corner_radius=30)
            menu_doron2.place(relx=0.5, rely=0.3, anchor=tkinter.CENTER)
            menu_doron2.pack_propagate()

            cor = carregar_config()
            if cor['cor'] == 'Azul':
                if cor['tema'] == 'Claro':
                    menu_doron2.configure(fg_color=cor['azul_claro'])
                else:
                    menu_doron2.configure(fg_color=cor['azul_escuro'])
            elif cor['cor'] == 'Verde':
                if cor['tema'] == 'Claro':
                    menu_doron2.configure(fg_color=cor['verde_claro'])
                else:
                    menu_doron2.configure(fg_color=cor['verde_escuro'])
            elif cor['cor'] == 'Acessy':
                if cor['tema'] == 'Claro':
                    menu_doron2.configure(fg_color=cor['acessy_claro'])
                else:
                    menu_doron2.configure(fg_color=cor['acessy_escuro'])

            onu_solicitando = customtkinter.CTkLabel(master=menu_doron2, text='ONUs Solicitando', font=("Product Sans Regular", 20))
            onu_solicitando.place(relx=0.5, rely=0.15, anchor=tkinter.CENTER)
            onu_solicitando.pack_propagate()

            posicao = customtkinter.CTkLabel(master=menu_doron2, text='PON', font=("Product Sans Regular", 15))
            posicao.place(relx=0.3, rely=0.27, anchor=tkinter.CENTER)
            posicao.pack_propagate()

            sn = customtkinter.CTkLabel(master=menu_doron2, text='Serial Number', font=("Product Sans Regular", 15))
            sn.place(relx=0.7, rely=0.27, anchor=tkinter.CENTER)
            sn.pack_propagate()

            output = obter_dados_olt('doron', 'Comando: show gpon onu uncfg')
            time.sleep(2)
            if 'No related information to show.' in output:
                output = "Nenhuma ONU Solicitando no momento."
                warn = customtkinter.CTkLabel(master=menu_doron2, text='', font=("Segoe Fluent Icons", 30), text_color='red')
                warn.place(relx=0.5, rely=0.38, anchor=tkinter.CENTER)
                info = customtkinter.CTkLabel(master=menu_doron2, text=output, font=("Product Sans Regular", 15), text_color='red')
                info.place(relx=0.5, rely=0.55, anchor=tkinter.CENTER)
                sn.destroy()
                posicao.destroy()
                return
            else:
                output = [line for line in output.splitlines() if line.startswith("gpon-onu")]
                output = "\n".join(output)

                pattern = re.compile(r'(\S+)\s+(\S+)\s+\S+')
                matches = pattern.findall(output)

                for onuindex, sn in matches:
                    onu = customtkinter.CTkLabel(master=menu_doron2, text=onuindex, font=("Product Sans Regular", 15))
                    onu.place(relx=0.3, rely=0.39, anchor=tkinter.CENTER)
                    onu.pack_propagate()

                    sn = customtkinter.CTkLabel(master=menu_doron2, text=sn, font=("Product Sans Regular", 15))
                    sn.place(relx=0.7, rely=0.39, anchor=tkinter.CENTER)
                    sn.pack_propagate()
        
        def pon_percentage():
            global menu_doron3
            menu_doron3 = customtkinter.CTkFrame(master=tabview.tab('OLT ZTE - Doron'), width=400, height=200, corner_radius=30)
            menu_doron3.place(relx=0.83, rely=0.3, anchor=tkinter.CENTER)
            menu_doron3.pack_propagate()

            def menu_doron3_toplevel():
                global menu_doron3toplevel
                
                #um grande agradecimento à HyperNylium pela função de centralização da janela: https://github.com/TomSchimansky/CustomTkinter/discussions/1820#discussion-5396625
                def CenterWindowToDisplay(Screen: Tk, width: int, height: int):
                    """Centers the window to the main display/monitor"""
                    screen_width = Screen.winfo_screenwidth()
                    screen_height = Screen.winfo_screenheight()
                    x = int((screen_width/2) - (width/2))
                    y = int((screen_height/2) - (height/1.5))
                    return f"{width}x{height}+{x}+{y}"
                
                menu_doron3toplevel = customtkinter.CTkToplevel(app)
                menu_doron3toplevel.title('Informações de PON')
                menu_doron3toplevel.resizable(False, False)
                
                menu_doron3toplevel.geometry(CenterWindowToDisplay(app, 1000, 800))

                menu_doron3toplevel.attributes('-topmost', True)

                titulo = customtkinter.CTkLabel(master=menu_doron3toplevel, text='Informações de PON', font=("Josefin Slab Bold", 25))
                titulo.place(relx=0.2, rely=0.1, anchor=tkinter.CENTER)
                scrollable_frame = customtkinter.CTkScrollableFrame(master=menu_doron3toplevel, width=800, height=500)
                scrollable_frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

                search_bar = customtkinter.CTkEntry(master=menu_doron3toplevel, width=200, font=("Product Sans Regular", 15), placeholder_text='Pesquisar ONU', corner_radius=40)
                search_bar.place(relx=0.7, rely=0.1, anchor=tkinter.CENTER)
                
                def search():
                    serial_number = search_bar.get()
                    url = 'http://100.127.0.250:5000/procurar_onu'
                    data = {
                        'serial_number': serial_number,
                        'olt': 'olt_2'
                    }

                    #um grande agradecimento à HyperNylium pela função de centralização da janela: https://github.com/TomSchimansky/CustomTkinter/discussions/1820#discussion-5396625
                    def CenterWindowToDisplay(Screen: Tk, width: int, height: int):
                        """Centers the window to the main display/monitor"""
                        screen_width = Screen.winfo_screenwidth()
                        screen_height = Screen.winfo_screenheight()
                        x = int((screen_width/2) - (width/2))
                        y = int((screen_height/2) - (height/1.5))
                        return f"{width}x{height}+{x}+{y}"

                    onu_info_top_level = customtkinter.CTkToplevel(app)
                    onu_info_top_level.title('Informações da ONU')
                    onu_info_top_level.resizable(False, False)

                    onu_info_top_level.geometry(CenterWindowToDisplay(app, 600, 600))

                    onu_info_top_level.attributes('-topmost', True)

                    response = requests.post(url, json=data)
                    response = response.text
                    # Dicionário para armazenar os dados extraídos
                    onu_data = {}

                    def parse_onu_output(output):
                        # Inicializa o dicionário onde os dados serão armazenados
                        onu_info = {}

                        # Separa o texto em linhas
                        lines = output.split('\n')
                        
                        # Variáveis de controle
                        history = []
                        history_section = False

                        # Expressão regular para identificar linhas importantes
                        key_value_pattern = re.compile(r"(\S.*?):\s*(.*)")
                        history_pattern = re.compile(r"\s*(\d+)\s+(\S+\s+\S+)\s+(\S+\s+\S+)\s+(\S+)")

                        for line in lines:
                            line = line.strip()
                            
                            # Verifica se estamos na seção de histórico
                            if line.startswith("Authpass Time"):
                                history_section = True
                                continue
                            
                            # Processa as linhas de histórico
                            if history_section:
                                match = history_pattern.match(line)
                                if match:
                                    event = {
                                        "Authpass Time": match.group(2),
                                        "Offline Time": match.group(3),
                                        "Cause": match.group(4)
                                    }
                                    history.append(event)
                                continue
                            
                            # Processa as linhas chave: valor
                            match = key_value_pattern.match(line)
                            if match:
                                key = match.group(1).strip()
                                value = match.group(2).strip()
                                onu_info[key] = value
                        
                        # Adiciona o histórico ao dicionário
                        if history:
                            onu_info["History"] = history

                        return onu_info
                    
                    onu_data = parse_onu_output(response)

                    x = 0.1
                    # Exibindo as informações da ONU
                    serial_number_label = customtkinter.CTkLabel(master=onu_info_top_level, text=f'Serial Number: {onu_data["Serial number"]}', font=("Josefin Slab Bold", 25))
                    serial_number_label.place(relx=0.5, rely=0.1, anchor=tkinter.CENTER)

                    def delete():
                        serial_number = search_bar.get()
                        url = 'http://100.127.0.250:5000/deletar_onu'
                        data = {
                            'serial_number': serial_number,
                            'olt': 'olt_2'
                        }

                        response = requests.post(url, json=data)
                        response = response.text
                        if response == 'sucesso':
                            onu_info_top_level.destroy()
                            menu_doron3toplevel.destroy()
                        else:
                            print('')

                    delete_img = Image.open("assets\\delete.png", size=(20,20))
                    delete_button = customtkinter.CTkButton(master=onu_info_top_level, text='Deletar ONU', font=("Product Sans Regular", 10), corner_radius=40, fg_color='#fa0000', hover_color='#a80000', image=delete_img, command=delete)
                    delete_button.place(relx=0.5, rely=0.9, anchor=tkinter.CENTER)

                    onu_interface_label = customtkinter.CTkLabel(master=onu_info_top_level, text=f'Interface: {onu_data["ONU interface"]}', font=("Product Sans Regular", 15))
                    onu_interface_label.place(relx=x, rely=0.2, anchor=tkinter.W)

                    name_label = customtkinter.CTkLabel(master=onu_info_top_level, text=f'Nome: {onu_data["Name"]}', font=("Product Sans Regular", 15))
                    name_label.place(relx=x, rely=0.3, anchor=tkinter.W)

                    config_state = customtkinter.CTkLabel(master=onu_info_top_level, text=f'Estado de Configuração: {onu_data["Config state"]}', font=("Product Sans Regular", 15))
                    config_state.place(relx=x, rely=0.4, anchor=tkinter.W)

                    online_duration_label = customtkinter.CTkLabel(master=onu_info_top_level, text=f'Duração Online: {onu_data["Online Duration"]}', font=("Product Sans Regular", 15))
                    online_duration_label.place(relx=x, rely=0.5, anchor=tkinter.W)

                    distance_label = customtkinter.CTkLabel(master=onu_info_top_level, text=f'Distância: {onu_data["ONU Distance"]}', font=("Product Sans Regular", 15))
                    distance_label.place(relx=x, rely=0.6, anchor=tkinter.W)

                search_image = customtkinter.CTkImage(Image.open("assets\\search.png"), size=(20,20))
                search_button = customtkinter.CTkButton(master=menu_doron3toplevel, text='', image=search_image, width=20, corner_radius=40, command=search, fg_color='black', hover_color='gray')
                search_button.place(relx=0.85, rely=0.1, anchor=tkinter.CENTER)

                
                # Função para separar os dados por OnuIndex e cada campo de cada linha
                # Função para separar os dados da ONU
                def separar_por_onuindex(dados):
                    # Expressão regular para capturar cada ONU e seus respectivos estados
                    padrao_onu = re.compile(r'(\d+/\d+/\d+:\d+)\s+(\w+)\s+(\w+)\s+(\w+)\s+(\d+\(GPON\))')
                    
                    # Um dicionário para armazenar os resultados separados por OnuIndex
                    onu_separado = {}
                    pon_separado = {}
                    
                    # Iterar sobre todas as correspondências no texto
                    for match in padrao_onu.findall(dados):
                        onuindex = match[0]
                        pon = onuindex.split(':')[0]
                        onu = onuindex.split(':')[1]
                        admin_state = match[1]
                        omcc_state = match[2]
                        phase_state = match[3]
                        channel = match[4]
                        
                        # Criando um dicionário para armazenar os valores de cada ONU
                        onu_detalhes = {
                            'OnuIndex': onuindex,
                            'PON': pon,
                            'ONU': onu,
                            'Admin State': admin_state,
                            'OMCC State': omcc_state,
                            'Phase State': phase_state,
                            'Channel': channel
                        }

                        if pon not in pon_separado:
                            pon_separado[pon] = []

                        pon_separado[pon].append(onu_detalhes)

                        # Adiciona a ONU ao dicionário
                        if onuindex not in onu_separado:
                            onu_separado[onuindex] = []
                        
                        onu_separado[onuindex].append(onu_detalhes)
                    
                    return pon_separado
                # Ensure pon_data is defined

                def obter_dados(olt_name, dados_a_consultar):
                    url = f'http://{server_ip}:5000/{olt_name}'
                    response = requests.get(url)
                    
                    if response.status_code == 200:
                        data = response.text  # Obtendo a resposta como texto bruto
                        # Dividindo o conteúdo por comandos
                        comandos = data.split('--------------------------------------------------------------------------------')

                        # Verifica qual comando foi solicitado e busca o bloco correspondente
                        for comando in comandos:
                            if dados_a_consultar in comando:
                                return comando    

                pon_data = obter_dados('doron', 'show gpon onu state')
                time.sleep(2)
                
                # Separar os dados
                onu_separado = separar_por_onuindex(pon_data)

                global current_ponindex
                current_ponindex = 0

                # Função para exibir os dados começando a partir da linha 1
                def display_data():
                    if current_ponindex < len(onu_separado):
                        pon = list(onu_separado.keys())[current_ponindex]
                        registros = onu_separado[pon]

                        # Limpa o frame antes de adicionar novos widgets
                        for widget in scrollable_frame.winfo_children():
                            widget.destroy()

                        # Adiciona o título da PON

                        scrollable_frame.grid_columnconfigure(0, weight=1)
                        scrollable_frame.grid_columnconfigure(1, weight=1)
                        scrollable_frame.grid_columnconfigure(2, weight=1)
                        scrollable_frame.grid_columnconfigure(3, weight=1)
                        scrollable_frame.grid_columnconfigure(4, weight=1)

                        # Adiciona os títulos na linha 0
                        titulo_onuindex = customtkinter.CTkLabel(master=scrollable_frame, text='Onu Número', font=("Product Sans Bold", 20))
                        titulo_onuindex.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')

                        titulo_admin = customtkinter.CTkLabel(master=scrollable_frame, text='Estado Operacional', font=("Product Sans Bold", 20))
                        titulo_admin.grid(row=1, column=1, padx=5, pady=5, sticky='nsew')

                        titulo_omcc = customtkinter.CTkLabel(master=scrollable_frame, text='Estado na OLT', font=("Product Sans Bold", 20))
                        titulo_omcc.grid(row=1, column=2, padx=5, pady=5, sticky='nsew')

                        titulo_phase = customtkinter.CTkLabel(master=scrollable_frame, text='Estado Atual', font=("Product Sans Bold", 20))
                        titulo_phase.grid(row=1, column=3, padx=5, pady=5, sticky='nsew')

                        titulo_channel = customtkinter.CTkLabel(master=scrollable_frame, text='Canal', font=("Product Sans Bold", 20))
                        titulo_channel.grid(row=1, column=4, padx=5, pady=5, sticky='nsew')

                        titulo_pon = customtkinter.CTkLabel(master=scrollable_frame, text=f'PON {pon}', font=("Josefin Slab Bold", 30))
                        #titulo_pon.grid(row=0, column=1, columnspan=5, padx=5, pady=5, sticky='nsew')

                        scrollable_frame.configure(label_text=f'PON {pon}')

                        row_num = 2  # Começa na linha 2 (abaixo dos títulos)
                        for registro in registros:
                            adminstate = registro['Admin State']
                            if adminstate == 'enable':
                                adminstate = 'Ativo'
                            elif adminstate == 'disable':
                                adminstate = 'Inativo'
                            else:
                                adminstate = 'Desconhecido'

                            omccstate = registro['OMCC State']
                            if omccstate == 'enable':
                                omccstate = 'Ativo'
                            elif omccstate == 'disable':
                                omccstate = 'Inativo'

                            
                            label_onuindex = customtkinter.CTkLabel(master=scrollable_frame, text=registro['ONU'], font=("Product Sans Regular", 15))
                            label_onuindex.grid(row=row_num, column=0, padx=5, pady=5, sticky='nsew')
                            label_admin = customtkinter.CTkLabel(master=scrollable_frame, text=adminstate, font=("Product Sans Regular", 15))
                            label_admin.grid(row=row_num, column=1, padx=5, pady=5, sticky='nsew')
                            label_omcc = customtkinter.CTkLabel(master=scrollable_frame, text=omccstate, font=("Product Sans Regular", 15))
                            label_omcc.grid(row=row_num, column=2, padx=5, pady=5, sticky='nsew')
                            label_phase = customtkinter.CTkLabel(master=scrollable_frame, text=registro['Phase State'], width=80, font=("Product Sans Regular", 15), corner_radius=30)
                            label_phase.grid(row=row_num, column=3, padx=5, pady=5, sticky='nsew')

                            phase = registro['Phase State']
                            if phase == 'working':
                                phase = 'Online'
                                label_phase.configure(text=phase, bg_color='#02b302')
                            elif phase == 'OffLine':
                                phase = 'OffLine'
                                label_phase.configure(text=phase, bg_color='red')
                            elif phase == 'DyingGasp':
                                phase = 'Inativo'
                                label_phase.configure(text=phase, bg_color='orange')
                            elif phase == 'LOS':
                                phase = 'Sem Sinal'
                                label_phase.configure(text=phase, bg_color='gray')
                            else:
                                phase = 'Desconhecido'


                            label_channel = customtkinter.CTkLabel(master=scrollable_frame, text=registro['Channel'], font=("Product Sans Regular", 15))
                            label_channel.grid(row=row_num, column=4, padx=5, pady=5, sticky='nsew')
                            row_num += 1  # Próxima linha

                        # Adiciona o botão para o próximo PON
                        def next_pon():
                            global current_ponindex
                            current_ponindex += 1
                            display_data()

                        image_foward = customtkinter.CTkImage(Image.open('assets\\arrow_right.png'), size=(20,20))
                        image_backwards = customtkinter.CTkImage(Image.open('assets\\arrow_left.png'), size=(20,20))
                                                            
                        next_button = customtkinter.CTkButton(master=scrollable_frame, text="Próximo PON", image=image_foward, compound='right', command=next_pon)
                        next_button.grid(row=row_num, column=2, columnspan=5, pady=10)

                        # Adiciona o botão para o PON anterior
                        def previous_pon():
                            global current_ponindex
                            current_ponindex -= 1
                            display_data()

                        previous_button = customtkinter.CTkButton(master=scrollable_frame, text="PON Anterior", image=image_backwards, compound='left', command=previous_pon)
                        previous_button.grid(row=row_num, column=0, columnspan=5, pady=10)

                threading.Thread(target=display_data).start()
            #torna menu_doron3 clicável
            menu_doron3.bind("<Enter>", lambda e: menu_doron3.configure(cursor="hand2"))
            menu_doron3.bind("<Leave>", lambda e: menu_doron3.configure(cursor=""))
            menu_doron3.bind("<Button-1>", lambda e: menu_doron3_toplevel())

            cor = carregar_config()
            if cor['cor'] == 'Azul':
                if cor['tema'] == 'Claro':
                    menu_doron3.configure(fg_color=cor['azul_claro'])
                else:
                    menu_doron3.configure(fg_color=cor['azul_escuro'])
            elif cor['cor'] == 'Verde':
                if cor['tema'] == 'Claro':
                    menu_doron3.configure(fg_color=cor['verde_claro'])
                else:
                    menu_doron3.configure(fg_color=cor['verde_escuro'])
            elif cor['cor'] == 'Acessy':
                if cor['tema'] == 'Claro':
                    menu_doron3.configure(fg_color=cor['acessy_claro'])
                else:
                    menu_doron3.configure(fg_color=cor['acessy_escuro'])

            pon_percentage = customtkinter.CTkLabel(master=menu_doron3, text='PON Percentage', font=("Product Sans Regular", 20))
            pon_percentage.place(relx=0.5, rely=0.15, anchor=tkinter.CENTER)
            pon_percentage.pack_propagate()

            posicao = customtkinter.CTkLabel(master=menu_doron3, text='Posição', font=("Product Sans Regular", 15))
            posicao.place(relx=0.3, rely=0.27, anchor=tkinter.CENTER)
            posicao.pack_propagate()

            sn = customtkinter.CTkLabel(master=menu_doron3, text='Posiões Preenchidas', font=("Product Sans Regular", 15))
            sn.place(relx=0.7, rely=0.27, anchor=tkinter.CENTER)
            sn.pack_propagate()

            def update_pon_data():
                data = obter_dados_olt('doron', 'Comando: show gpon onu state')
                time.sleep(2)
                # Expressão regular para capturar o OnuIndex, no formato 1/2/1, etc.
                pattern = re.compile(r'(\d+/\d+/\d+):\d+')

                # Dicionário para armazenar a contagem das ONUs por PON
                pon_counts = defaultdict(int)

                # Encontrar todas as ocorrências de PON e contar
                matches = pattern.findall(data)
                for pon in matches:
                    pon_counts[pon] += 1

                # Exibir o resultado
                for pon, count in pon_counts.items():
                    perc = count / 128

                y = 0.39
                for pon, count in pon_counts.items():
                    perc = count / 128

                    onu = customtkinter.CTkLabel(master=menu_doron3, text=pon, font=("Product Sans Regular", 15))
                    onu.place(relx=0.3, rely=y, anchor=tkinter.CENTER)
                    onu.pack_propagate()

                    if perc < 0.5:
                        cor = 'green'
                    elif perc < 0.8:
                        cor = 'yellow'
                    else:
                        cor = 'red'

                    progress_bar = customtkinter.CTkProgressBar(master=menu_doron3, width=200, height=10, corner_radius=10, progress_color=cor)
                    progress_bar.set(perc)
                    progress_bar.place(relx=0.7, rely=y, anchor=tkinter.CENTER)
                    sn = customtkinter.CTkLabel(master=menu_doron3, text=f'{count}/128', font=("Product Sans Regular", 10), bg_color='transparent')
                    sn.place(relx=0.7, rely=y, anchor=tkinter.CENTER)
                    sn.pack_propagate()

                    y += 0.1

                    #se tiver mais de 6 itens, para a execução
                    if y > 0.9:
                        break

                texto_aguarde.destroy()

            # Run the update_pon_data function in a separate thread to keep the UI responsive
            threading.Thread(target=update_pon_data).start()

        def batch_commands():
            global menu_doron4
            # Get the screen width to dynamically set the width of menu_doron4
            screen_width = app.winfo_screenwidth()
            screen_height = app.winfo_screenheight()
            menu_doron4_width = screen_width - 100  # Adjust the width as needed
            menu_doron4_height = screen_height - 500  # Adjust the height as needed

            menu_doron4 = customtkinter.CTkFrame(master=tabview.tab('OLT ZTE - Doron'), width=menu_doron4_width, height=menu_doron4_height, corner_radius=30)
            menu_doron4.place(relx=0.5, rely=0.75, anchor=tkinter.CENTER)

            # cor = carregar_config()
            # if cor['cor'] == 'Azul':
            #     if cor['tema'] == 'Claro':
            #         menu_doron4.configure(fg_color=cor['azul_claro'])
            #     else:
            #         menu_doron4.configure(fg_color=cor['azul_escuro'])
            # elif cor['cor'] == 'Verde':
            #     if cor['tema'] == 'Claro':
            #         menu_doron4.configure(fg_color=cor['verde_claro'])
            #     else:
            #         menu_doron4.configure(fg_color=cor['verde_escuro'])
            # elif cor['cor'] == 'Acessy':
            #     if cor['tema'] == 'Claro':
            #         menu_doron4.configure(fg_color=cor['acessy_claro'])
            #     else:
            #         menu_doron4.configure(fg_color=cor['acessy_escuro'])

            titulo = customtkinter.CTkLabel(master=menu_doron4, text='Executar comandos em lotes', font=("Product Sans Regular", 20))
            titulo.place(relx=0.5, rely=0.1, anchor=tkinter.CENTER)
            titulo.pack_propagate()
    
        texto_aguarde = customtkinter.CTkLabel(master=tabview.tab('OLT ZTE - Doron'), text='Por favor, aguarde enquanto as informações são carregadas...', font=("Josefin Slab Light", 20))
        texto_aguarde.place(relx=0.5, rely=0.7, anchor=tkinter.CENTER)

        def process_functions():
            # Wait for the SSH initialization thread to finish
            #ssh_thread.join()
            onu_solic()
            processamento()
            pon_percentage()
            batch_commands()

        # Create a thread to run the process_functions
        thread = threading.Thread(target=process_functions)
        thread.start()

    def olt_boca_do_rio():
        def processamento():
            output = obter_dados_olt('boca_do_rio', 'Comando: show processor')
            time.sleep(2)

           # Expressão regular para capturar os valores de CPU e Memória
            pattern = re.compile(
                r'(\S+)\s+(\S+)\s+(\d+)%\s+(\d+)%\s+(\d+)%\s+(\d+)%\s+(\d+)\s+(\d+)\s+(\d\d)'
            )

            # Encontrar todas as correspondências no output
            matches = pattern.findall(output)

            # Organizar os dados em um dicionário
            olt_data = []

            for match in matches:
                onu = {
                    'Component': match[0],
                    'Character': match[1],
                    'CPU_5s': match[2],
                    'CPU_1m': match[3],
                    'CPU_5m': match[4],
                    'Peak_CPU': match[5],
                    'PhyMem_MB': match[6],
                    'FreeMem_MB': match[7],
                    'Mem_Usage': match[8]
                }
                olt_data.append(onu)

            # Exibindo os resultados

            global menu_boca_do_rio
            menu_boca_do_rio = customtkinter.CTkFrame(master=tabview.tab('OLT ZTE - Boca do Rio'), width=400, height=200, corner_radius=30)
            menu_boca_do_rio.place(relx=0.17, rely=0.3, anchor=tkinter.CENTER)
            menu_boca_do_rio.pack_propagate(0)

            #faz o menu_boca_do_rio ser clicável
            menu_boca_do_rio.bind("<Button-1>", lambda e: print("Clicou no menu_boca_do_rio"))

            cor = carregar_config()
            if cor['cor'] == 'Azul':
                if cor['tema'] == 'Claro':
                    menu_boca_do_rio.configure(fg_color=cor['azul_claro'])
                else:
                    menu_boca_do_rio.configure(fg_color=cor['azul_escuro'])
            elif cor['cor'] == 'Verde':
                if cor['tema'] == 'Claro':
                    menu_boca_do_rio.configure(fg_color=cor['verde_claro'])
                else:
                    menu_boca_do_rio.configure(fg_color=cor['verde_escuro'])
            elif cor['cor'] == 'Acessy':
                if cor['tema'] == 'Claro':
                    menu_boca_do_rio.configure(fg_color=cor['acessy_claro'])
                else:
                    menu_boca_do_rio.configure(fg_color=cor['acessy_escuro'])

            titulo = customtkinter.CTkLabel(master=menu_boca_do_rio, text='Processamento', font=("Product Sans Regular", 20))
            titulo.place(relx=0.5, rely=0.15, anchor=tkinter.CENTER)


            labels = ["Componente", "CPU", "Uso Máx.", "Memória"]
            for i, label in enumerate(labels):
                customtkinter.CTkLabel(master=menu_boca_do_rio, text=label, font=("Product Sans Regular", 15)).place(relx=0.15 + i*0.25, rely=0.27, anchor=tkinter.CENTER)

            for i, onu in enumerate(olt_data, 1):
                y = 0.37 + (i-1)*0.1
                mem_percentage = float(onu['Mem_Usage']) / 100
                cpu_percentage = int(onu['CPU_1m']) / 100
                peak_cpu = int(onu['Peak_CPU']) / 100

                if mem_percentage < 0.5:
                    cor_mem = 'green'
                elif mem_percentage < 0.8:
                    cor_mem = 'yellow'
                else:
                    cor_mem = 'red'
                mem_bar = customtkinter.CTkProgressBar(master=menu_boca_do_rio, width=60, height=8, corner_radius=10, progress_color=cor_mem)
                mem_bar.set(mem_percentage)
                mem_bar.place(relx=0.9, rely=y, anchor=tkinter.CENTER)
                mem_label = customtkinter.CTkLabel(master=menu_boca_do_rio, text=f"{onu['Mem_Usage']}%", font=("Product Sans Regular", 10), fg_color='transparent')
                mem_label.place(relx=0.9, rely=y, anchor=tkinter.CENTER)

                if cpu_percentage < 0.5:
                    cor_cpu = 'green'
                elif cpu_percentage < 0.8:
                    cor_cpu = 'yellow'
                else:
                    cor_cpu = 'red'
                cpu_bar = customtkinter.CTkProgressBar(master=menu_boca_do_rio, width=60, height=8, corner_radius=10, progress_color=cor_cpu)
                cpu_bar.set(cpu_percentage)
                cpu_bar.place(relx=0.4, rely=y, anchor=tkinter.CENTER)
                cpu_label = customtkinter.CTkLabel(master=menu_boca_do_rio, text=f"{onu['CPU_1m']}%", font=("Product Sans Regular", 10), fg_color='transparent')
                cpu_label.place(relx=0.4, rely=y, anchor=tkinter.CENTER)

                if peak_cpu < 0.5:
                    cor_peak = 'green'
                elif peak_cpu < 0.8:
                    cor_peak = 'yellow'
                else:
                    cor_peak = 'red'
                peak_bar = customtkinter.CTkProgressBar(master=menu_boca_do_rio, width=60, height=8, corner_radius=10, progress_color=cor_peak)
                peak_bar.set(peak_cpu)
                peak_bar.place(relx=0.65, rely=y, anchor=tkinter.CENTER)
                peak_label = customtkinter.CTkLabel(master=menu_boca_do_rio, text=f"{onu['Peak_CPU']}%", font=("Product Sans Regular", 10), fg_color='transparent')
                peak_label.place(relx=0.65, rely=y, anchor=tkinter.CENTER)

                customtkinter.CTkLabel(master=menu_boca_do_rio, text=onu['Component'], font=("Product Sans Regular", 15)).place(relx=0.15, rely=y, anchor=tkinter.CENTER)

        def onu_solic():
            global menu_boca_do_rio2
            menu_boca_do_rio2 = customtkinter.CTkFrame(master=tabview.tab('OLT ZTE - Boca do Rio'), width=400, height=200, corner_radius=30)
            menu_boca_do_rio2.place(relx=0.5, rely=0.3, anchor=tkinter.CENTER)
            menu_boca_do_rio2.pack_propagate()

            cor = carregar_config()
            if cor['cor'] == 'Azul':
                if cor['tema'] == 'Claro':
                    menu_boca_do_rio2.configure(fg_color=cor['azul_claro'])
                else:
                    menu_boca_do_rio2.configure(fg_color=cor['azul_escuro'])
            elif cor['cor'] == 'Verde':
                if cor['tema'] == 'Claro':
                    menu_boca_do_rio2.configure(fg_color=cor['verde_claro'])
                else:
                    menu_boca_do_rio2.configure(fg_color=cor['verde_escuro'])
            elif cor['cor'] == 'Acessy':
                if cor['tema'] == 'Claro':
                    menu_boca_do_rio2.configure(fg_color=cor['acessy_claro'])
                else:
                    menu_boca_do_rio2.configure(fg_color=cor['acessy_escuro'])

            onu_solicitando = customtkinter.CTkLabel(master=menu_boca_do_rio2, text='ONUs Solicitando', font=("Product Sans Regular", 20))
            onu_solicitando.place(relx=0.5, rely=0.15, anchor=tkinter.CENTER)
            onu_solicitando.pack_propagate()

            posicao = customtkinter.CTkLabel(master=menu_boca_do_rio2, text='PON', font=("Product Sans Regular", 15))
            posicao.place(relx=0.3, rely=0.27, anchor=tkinter.CENTER)
            posicao.pack_propagate()

            sn = customtkinter.CTkLabel(master=menu_boca_do_rio2, text='Serial Number', font=("Product Sans Regular", 15))
            sn.place(relx=0.7, rely=0.27, anchor=tkinter.CENTER)
            sn.pack_propagate()

            output = obter_dados_olt('boca_do_rio', 'Comando: show pon onu uncfg')
            time.sleep(2)
            print(f'OUTPUTA ==================================================={output}')
            if 'No related information to show.' in output:
                output = "Nenhuma ONU Solicitando no momento."
                warn = customtkinter.CTkLabel(master=menu_boca_do_rio2, text='', font=("Segoe Fluent Icons", 30), text_color='red')
                warn.place(relx=0.5, rely=0.38, anchor=tkinter.CENTER)
                info = customtkinter.CTkLabel(master=menu_boca_do_rio2, text=output, font=("Product Sans Regular", 15), text_color='red')
                info.place(relx=0.5, rely=0.55, anchor=tkinter.CENTER)
                sn.destroy()
                posicao.destroy()
                return
            else:
                output = [line for line in output.splitlines() if line.startswith("gpon-onu")]
                output = "\n".join(output)

                pattern = re.compile(r'(\S+)\s+(\S+)\s+\S+')
                matches = pattern.findall(output)

                for onuindex, sn in matches:
                    onu = customtkinter.CTkLabel(master=menu_boca_do_rio2, text=onuindex, font=("Product Sans Regular", 15))
                    onu.place(relx=0.3, rely=0.39, anchor=tkinter.CENTER)
                    onu.pack_propagate()

                    sn = customtkinter.CTkLabel(master=menu_boca_do_rio2, text=sn, font=("Product Sans Regular", 15))
                    sn.place(relx=0.7, rely=0.39, anchor=tkinter.CENTER)
                    sn.pack_propagate()
        
        def pon_percentage():
            global menu_boca_do_rio3
            menu_boca_do_rio3 = customtkinter.CTkFrame(master=tabview.tab('OLT ZTE - Boca do Rio'), width=400, height=200, corner_radius=30)
            menu_boca_do_rio3.place(relx=0.83, rely=0.3, anchor=tkinter.CENTER)
            menu_boca_do_rio3.pack_propagate()

            def menu_boca_do_rio3_toplevel():
                global menu_boca_do_rio3toplevel
                
                #um grande agradecimento à HyperNylium pela função de centralização da janela: https://github.com/TomSchimansky/CustomTkinter/discussions/1820#discussion-5396625
                def CenterWindowToDisplay(Screen: Tk, width: int, height: int):
                    """Centers the window to the main display/monitor"""
                    screen_width = Screen.winfo_screenwidth()
                    screen_height = Screen.winfo_screenheight()
                    x = int((screen_width/2) - (width/2))
                    y = int((screen_height/2) - (height/1.5))
                    return f"{width}x{height}+{x}+{y}"
                
                menu_boca_do_rio3toplevel = customtkinter.CTkToplevel(app)
                menu_boca_do_rio3toplevel.title('Informações de PON')
                menu_boca_do_rio3toplevel.resizable(False, False)
                
                menu_boca_do_rio3toplevel.geometry(CenterWindowToDisplay(app, 1000, 800))

                menu_boca_do_rio3toplevel.attributes('-topmost', True)

                titulo = customtkinter.CTkLabel(master=menu_boca_do_rio3toplevel, text='Informações de PON', font=("Josefin Slab Bold", 25))
                titulo.place(relx=0.2, rely=0.1, anchor=tkinter.CENTER)
                scrollable_frame = customtkinter.CTkScrollableFrame(master=menu_boca_do_rio3toplevel, width=800, height=500)
                scrollable_frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

                search_bar = customtkinter.CTkEntry(master=menu_boca_do_rio3toplevel, width=200, font=("Product Sans Regular", 15), placeholder_text='Pesquisar ONU', corner_radius=40)
                search_bar.place(relx=0.7, rely=0.1, anchor=tkinter.CENTER)
                
                def search():
                    serial_number = search_bar.get()
                    url = 'http://100.127.0.250:5000/procurar_onu'
                    data = {
                        'serial_number': serial_number,
                        'olt': 'olt_3'
                    }

                    #um grande agradecimento à HyperNylium pela função de centralização da janela: https://github.com/TomSchimansky/CustomTkinter/discussions/1820#discussion-5396625
                    def CenterWindowToDisplay(Screen: Tk, width: int, height: int):
                        """Centers the window to the main display/monitor"""
                        screen_width = Screen.winfo_screenwidth()
                        screen_height = Screen.winfo_screenheight()
                        x = int((screen_width/2) - (width/2))
                        y = int((screen_height/2) - (height/1.5))
                        return f"{width}x{height}+{x}+{y}"

                    onu_info_top_level = customtkinter.CTkToplevel(app)
                    onu_info_top_level.title('Informações da ONU')
                    onu_info_top_level.resizable(False, False)

                    onu_info_top_level.geometry(CenterWindowToDisplay(app, 600, 600))

                    onu_info_top_level.attributes('-topmost', True)

                    response = requests.post(url, json=data)
                    response = response.text
                    # Dicionário para armazenar os dados extraídos
                    onu_data = {}

                    def parse_onu_output(output):
                        # Inicializa o dicionário onde os dados serão armazenados
                        onu_info = {}

                        # Separa o texto em linhas
                        lines = output.split('\n')
                        
                        # Variáveis de controle
                        history = []
                        history_section = False

                        # Expressão regular para identificar linhas importantes
                        key_value_pattern = re.compile(r"(\S.*?):\s*(.*)")
                        history_pattern = re.compile(r"\s*(\d+)\s+(\S+\s+\S+)\s+(\S+\s+\S+)\s+(\S+)")

                        for line in lines:
                            line = line.strip()
                            
                            # Verifica se estamos na seção de histórico
                            if line.startswith("Authpass Time"):
                                history_section = True
                                continue
                            
                            # Processa as linhas de histórico
                            if history_section:
                                match = history_pattern.match(line)
                                if match:
                                    event = {
                                        "Authpass Time": match.group(2),
                                        "Offline Time": match.group(3),
                                        "Cause": match.group(4)
                                    }
                                    history.append(event)
                                continue
                            
                            # Processa as linhas chave: valor
                            match = key_value_pattern.match(line)
                            if match:
                                key = match.group(1).strip()
                                value = match.group(2).strip()
                                onu_info[key] = value
                        
                        # Adiciona o histórico ao dicionário
                        if history:
                            onu_info["History"] = history

                        return onu_info
                    
                    onu_data = parse_onu_output(response)

                    x = 0.1
                    # Exibindo as informações da ONU
                    serial_number_label = customtkinter.CTkLabel(master=onu_info_top_level, text=f'Serial Number: {onu_data["Serial number"]}', font=("Josefin Slab Bold", 25))
                    serial_number_label.place(relx=0.5, rely=0.1, anchor=tkinter.CENTER)

                    def delete():
                        serial_number = search_bar.get()
                        url = 'http://100.127.0.250:5000/deletar_onu'
                        data = {
                            'serial_number': serial_number,
                            'olt': 'olt_3'
                        }

                        response = requests.post(url, json=data)
                        response = response.text
                        if response == 'sucesso':
                            onu_info_top_level.destroy()
                            menu_boca_do_rio3toplevel.destroy()
                        else:
                            print('')

                    delete_img = Image.open("assets\\delete.png", size=(20,20))
                    delete_button = customtkinter.CTkButton(master=onu_info_top_level, text='Deletar ONU', font=("Product Sans Regular", 10), corner_radius=40, fg_color='#fa0000', hover_color='#a80000', image=delete_img, command=delete)
                    delete_button.place(relx=0.5, rely=0.9, anchor=tkinter.CENTER)

                    onu_interface_label = customtkinter.CTkLabel(master=onu_info_top_level, text=f'Interface: {onu_data["ONU interface"]}', font=("Product Sans Regular", 15))
                    onu_interface_label.place(relx=x, rely=0.2, anchor=tkinter.W)

                    name_label = customtkinter.CTkLabel(master=onu_info_top_level, text=f'Nome: {onu_data["Name"]}', font=("Product Sans Regular", 15))
                    name_label.place(relx=x, rely=0.3, anchor=tkinter.W)

                    config_state = customtkinter.CTkLabel(master=onu_info_top_level, text=f'Estado de Configuração: {onu_data["Config state"]}', font=("Product Sans Regular", 15))
                    config_state.place(relx=x, rely=0.4, anchor=tkinter.W)

                    online_duration_label = customtkinter.CTkLabel(master=onu_info_top_level, text=f'Duração Online: {onu_data["Online Duration"]}', font=("Product Sans Regular", 15))
                    online_duration_label.place(relx=x, rely=0.5, anchor=tkinter.W)

                    distance_label = customtkinter.CTkLabel(master=onu_info_top_level, text=f'Distância: {onu_data["ONU Distance"]}', font=("Product Sans Regular", 15))
                    distance_label.place(relx=x, rely=0.6, anchor=tkinter.W)

                search_image = customtkinter.CTkImage(Image.open("assets\\search.png"), size=(20,20))
                search_button = customtkinter.CTkButton(master=menu_boca_do_rio3toplevel, text='', image=search_image, width=20, corner_radius=40, command=search, fg_color='black', hover_color='gray')
                search_button.place(relx=0.85, rely=0.1, anchor=tkinter.CENTER)

                
                # Função para separar os dados por OnuIndex e cada campo de cada linha
                # Função para separar os dados da ONU
                def separar_por_onuindex(dados):
                    # Expressão regular para capturar cada ONU e seus respectivos estados
                    padrao_onu = re.compile(r'(\d+/\d+/\d+:\d+)\s+(\w+)\s+(\w+)\s+(\w+)\s+(\w+)')
                    
                    # Um dicionário para armazenar os resultados separados por OnuIndex
                    onu_separado = {}
                    pon_separado = {}
                    
                    # Iterar sobre todas as correspondências no texto
                    for match in padrao_onu.findall(dados):
                        onuindex = match[0]
                        pon = onuindex.split(':')[0]
                        onu = onuindex.split(':')[1]
                        admin_state = match[1]
                        omcc_state = match[2]
                        phase_state = match[3]
                        channel = match[4]
                        
                        # Criando um dicionário para armazenar os valores de cada ONU
                        onu_detalhes = {
                            'OnuIndex': onuindex,
                            'PON': pon,
                            'ONU': onu,
                            'Admin State': admin_state,
                            'OMCC State': omcc_state,
                            'Phase State': phase_state,
                            'Channel': channel
                        }

                        if pon not in pon_separado:
                            pon_separado[pon] = []

                        pon_separado[pon].append(onu_detalhes)

                        # Adiciona a ONU ao dicionário
                        if onuindex not in onu_separado:
                            onu_separado[onuindex] = []
                        
                        onu_separado[onuindex].append(onu_detalhes)
                    
                    return pon_separado
                # Ensure pon_data is defined

                def obter_dados(olt_name, dados_a_consultar):
                    url = f'http://{server_ip}:5000/{olt_name}'
                    response = requests.get(url)
                    
                    if response.status_code == 200:
                        data = response.text  # Obtendo a resposta como texto bruto
                        # Dividindo o conteúdo por comandos
                        comandos = data.split('--------------------------------------------------------------------------------')

                        # Verifica qual comando foi solicitado e busca o bloco correspondente
                        for comando in comandos:
                            if dados_a_consultar in comando:
                                return comando    

                pon_data = obter_dados('boca_do_rio', 'show gpon onu state')
                time.sleep(2)
                
                # Separar os dados
                onu_separado = separar_por_onuindex(pon_data)

                global current_ponindex
                current_ponindex = 0

                # Função para exibir os dados começando a partir da linha 1
                def display_data():
                    if current_ponindex < len(onu_separado):
                        pon = list(onu_separado.keys())[current_ponindex]
                        registros = onu_separado[pon]

                        # Limpa o frame antes de adicionar novos widgets
                        for widget in scrollable_frame.winfo_children():
                            widget.destroy()

                        # Adiciona o título da PON

                        scrollable_frame.grid_columnconfigure(0, weight=1)
                        scrollable_frame.grid_columnconfigure(1, weight=1)
                        scrollable_frame.grid_columnconfigure(2, weight=1)
                        scrollable_frame.grid_columnconfigure(3, weight=1)
                        scrollable_frame.grid_columnconfigure(4, weight=1)

                        # Adiciona os títulos na linha 0
                        titulo_onuindex = customtkinter.CTkLabel(master=scrollable_frame, text='Onu Número', font=("Product Sans Bold", 20))
                        titulo_onuindex.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')

                        titulo_admin = customtkinter.CTkLabel(master=scrollable_frame, text='Estado Operacional', font=("Product Sans Bold", 20))
                        titulo_admin.grid(row=1, column=1, padx=5, pady=5, sticky='nsew')

                        titulo_omcc = customtkinter.CTkLabel(master=scrollable_frame, text='Estado na OLT', font=("Product Sans Bold", 20))
                        titulo_omcc.grid(row=1, column=2, padx=5, pady=5, sticky='nsew')

                        titulo_phase = customtkinter.CTkLabel(master=scrollable_frame, text='Estado Atual', font=("Product Sans Bold", 20))
                        titulo_phase.grid(row=1, column=3, padx=5, pady=5, sticky='nsew')

                        titulo_channel = customtkinter.CTkLabel(master=scrollable_frame, text='Canal', font=("Product Sans Bold", 20))
                        titulo_channel.grid(row=1, column=4, padx=5, pady=5, sticky='nsew')

                        titulo_pon = customtkinter.CTkLabel(master=scrollable_frame, text=f'PON {pon}', font=("Josefin Slab Bold", 30))
                        #titulo_pon.grid(row=0, column=1, columnspan=5, padx=5, pady=5, sticky='nsew')

                        scrollable_frame.configure(label_text=f'PON {pon}')

                        row_num = 2  # Começa na linha 2 (abaixo dos títulos)
                        for registro in registros:
                            adminstate = registro['Admin State']
                            if adminstate == 'enable':
                                adminstate = 'Ativo'
                            elif adminstate == 'disable':
                                adminstate = 'Inativo'
                            else:
                                adminstate = 'Desconhecido'

                            omccstate = registro['OMCC State']
                            if omccstate == 'enable':
                                omccstate = 'Ativo'
                            elif omccstate == 'disable':
                                omccstate = 'Inativo'

                            
                            label_onuindex = customtkinter.CTkLabel(master=scrollable_frame, text=registro['ONU'], font=("Product Sans Regular", 15))
                            label_onuindex.grid(row=row_num, column=0, padx=5, pady=5, sticky='nsew')
                            label_admin = customtkinter.CTkLabel(master=scrollable_frame, text=adminstate, font=("Product Sans Regular", 15))
                            label_admin.grid(row=row_num, column=1, padx=5, pady=5, sticky='nsew')
                            label_omcc = customtkinter.CTkLabel(master=scrollable_frame, text=omccstate, font=("Product Sans Regular", 15))
                            label_omcc.grid(row=row_num, column=2, padx=5, pady=5, sticky='nsew')
                            label_phase = customtkinter.CTkLabel(master=scrollable_frame, text=registro['Phase State'], width=80, font=("Product Sans Regular", 15), corner_radius=30)
                            label_phase.grid(row=row_num, column=3, padx=5, pady=5, sticky='nsew')

                            phase = registro['Phase State']
                            if phase == 'working':
                                phase = 'Online'
                                label_phase.configure(text=phase, bg_color='#02b302')
                            elif phase == 'OffLine':
                                phase = 'OffLine'
                                label_phase.configure(text=phase, bg_color='red')
                            elif phase == 'DyingGasp':
                                phase = 'Inativo'
                                label_phase.configure(text=phase, bg_color='orange')
                            elif phase == 'LOS':
                                phase = 'Sem Sinal'
                                label_phase.configure(text=phase, bg_color='gray')
                            else:
                                phase = 'Desconhecido'


                            label_channel = customtkinter.CTkLabel(master=scrollable_frame, text=registro['Channel'], font=("Product Sans Regular", 15))
                            label_channel.grid(row=row_num, column=4, padx=5, pady=5, sticky='nsew')
                            row_num += 1  # Próxima linha

                        # Adiciona o botão para o próximo PON
                        def next_pon():
                            global current_ponindex
                            current_ponindex += 1
                            display_data()

                        image_foward = customtkinter.CTkImage(Image.open('assets\\arrow_right.png'), size=(20,20))
                        image_backwards = customtkinter.CTkImage(Image.open('assets\\arrow_left.png'), size=(20,20))
                                                            
                        next_button = customtkinter.CTkButton(master=scrollable_frame, text="Próximo PON", image=image_foward, compound='right', command=next_pon)
                        next_button.grid(row=row_num, column=2, columnspan=5, pady=10)

                        # Adiciona o botão para o PON anterior
                        def previous_pon():
                            global current_ponindex
                            current_ponindex -= 1
                            display_data()

                        previous_button = customtkinter.CTkButton(master=scrollable_frame, text="PON Anterior", image=image_backwards, compound='left', command=previous_pon)
                        previous_button.grid(row=row_num, column=0, columnspan=5, pady=10)

                threading.Thread(target=display_data).start()
            #torna menu_boca_do_rio3 clicável
            menu_boca_do_rio3.bind("<Enter>", lambda e: menu_boca_do_rio3.configure(cursor="hand2"))
            menu_boca_do_rio3.bind("<Leave>", lambda e: menu_boca_do_rio3.configure(cursor=""))
            menu_boca_do_rio3.bind("<Button-1>", lambda e: menu_boca_do_rio3_toplevel())

            cor = carregar_config()
            if cor['cor'] == 'Azul':
                if cor['tema'] == 'Claro':
                    menu_boca_do_rio3.configure(fg_color=cor['azul_claro'])
                else:
                    menu_boca_do_rio3.configure(fg_color=cor['azul_escuro'])
            elif cor['cor'] == 'Verde':
                if cor['tema'] == 'Claro':
                    menu_boca_do_rio3.configure(fg_color=cor['verde_claro'])
                else:
                    menu_boca_do_rio3.configure(fg_color=cor['verde_escuro'])
            elif cor['cor'] == 'Acessy':
                if cor['tema'] == 'Claro':
                    menu_boca_do_rio3.configure(fg_color=cor['acessy_claro'])
                else:
                    menu_boca_do_rio3.configure(fg_color=cor['acessy_escuro'])

            pon_percentage = customtkinter.CTkLabel(master=menu_boca_do_rio3, text='PON Percentage', font=("Product Sans Regular", 20))
            pon_percentage.place(relx=0.5, rely=0.15, anchor=tkinter.CENTER)
            pon_percentage.pack_propagate()

            posicao = customtkinter.CTkLabel(master=menu_boca_do_rio3, text='Posição', font=("Product Sans Regular", 15))
            posicao.place(relx=0.3, rely=0.27, anchor=tkinter.CENTER)
            posicao.pack_propagate()

            sn = customtkinter.CTkLabel(master=menu_boca_do_rio3, text='Posiões Preenchidas', font=("Product Sans Regular", 15))
            sn.place(relx=0.7, rely=0.27, anchor=tkinter.CENTER)
            sn.pack_propagate()

            def update_pon_data():
                data = obter_dados_olt('boca_do_rio', 'Comando: show gpon onu state')
                time.sleep(2)
                # Expressão regular para capturar o OnuIndex, no formato 1/2/1, etc.
                pattern = re.compile(r'(\d+/\d+/\d+):\d+')

                # Dicionário para armazenar a contagem das ONUs por PON
                pon_counts = defaultdict(int)

                # Encontrar todas as ocorrências de PON e contar
                matches = pattern.findall(data)
                for pon in matches:
                    pon_counts[pon] += 1

                # Exibir o resultado
                for pon, count in pon_counts.items():
                    perc = count / 128

                y = 0.39
                for pon, count in pon_counts.items():
                    perc = count / 128

                    onu = customtkinter.CTkLabel(master=menu_boca_do_rio3, text=pon, font=("Product Sans Regular", 15))
                    onu.place(relx=0.3, rely=y, anchor=tkinter.CENTER)
                    onu.pack_propagate()

                    if perc < 0.5:
                        cor = 'green'
                    elif perc < 0.8:
                        cor = 'yellow'
                    else:
                        cor = 'red'

                    progress_bar = customtkinter.CTkProgressBar(master=menu_boca_do_rio3, width=200, height=10, corner_radius=10, progress_color=cor)
                    progress_bar.set(perc)
                    progress_bar.place(relx=0.7, rely=y, anchor=tkinter.CENTER)
                    sn = customtkinter.CTkLabel(master=menu_boca_do_rio3, text=f'{count}/128', font=("Product Sans Regular", 10), bg_color='transparent')
                    sn.place(relx=0.7, rely=y, anchor=tkinter.CENTER)
                    sn.pack_propagate()

                    y += 0.1

                    #se tiver mais de 6 itens, para a execução
                    if y > 0.9:
                        break

                texto_aguarde.destroy()

            # Run the update_pon_data function in a separate thread to keep the UI responsive
            threading.Thread(target=update_pon_data).start()

        def batch_commands():
            global menu_boca_do_rio4
            # Get the screen width to dynamically set the width of menu_boca_do_rio4
            screen_width = app.winfo_screenwidth()
            screen_height = app.winfo_screenheight()
            menu_boca_do_rio4_width = screen_width - 100  # Adjust the width as needed
            menu_boca_do_rio4_height = screen_height - 500  # Adjust the height as needed

            menu_boca_do_rio4 = customtkinter.CTkFrame(master=tabview.tab('OLT ZTE - Boca do Rio'), width=menu_boca_do_rio4_width, height=menu_boca_do_rio4_height, corner_radius=30)
            menu_boca_do_rio4.place(relx=0.5, rely=0.75, anchor=tkinter.CENTER)

            # cor = carregar_config()
            # if cor['cor'] == 'Azul':
            #     if cor['tema'] == 'Claro':
            #         menu_boca_do_rio4.configure(fg_color=cor['azul_claro'])
            #     else:
            #         menu_boca_do_rio4.configure(fg_color=cor['azul_escuro'])
            # elif cor['cor'] == 'Verde':
            #     if cor['tema'] == 'Claro':
            #         menu_boca_do_rio4.configure(fg_color=cor['verde_claro'])
            #     else:
            #         menu_boca_do_rio4.configure(fg_color=cor['verde_escuro'])
            # elif cor['cor'] == 'Acessy':
            #     if cor['tema'] == 'Claro':
            #         menu_boca_do_rio4.configure(fg_color=cor['acessy_claro'])
            #     else:
            #         menu_boca_do_rio4.configure(fg_color=cor['acessy_escuro'])

            titulo = customtkinter.CTkLabel(master=menu_boca_do_rio4, text='Executar comandos em lotes', font=("Product Sans Regular", 20))
            titulo.place(relx=0.5, rely=0.1, anchor=tkinter.CENTER)
            titulo.pack_propagate()
    
        texto_aguarde = customtkinter.CTkLabel(master=tabview.tab('OLT ZTE - Boca do Rio'), text='Por favor, aguarde enquanto as informações são carregadas...', font=("Josefin Slab Light", 20))
        texto_aguarde.place(relx=0.5, rely=0.7, anchor=tkinter.CENTER)

        def process_functions():
            # Wait for the SSH initialization thread to finish
            #ssh_thread.join()
            onu_solic()
            processamento()
            pon_percentage()
            batch_commands()

        # Create a thread to run the process_functions
        thread = threading.Thread(target=process_functions)
        thread.start()

    def olt_sussuarana():
        def processamento():
            output = obter_dados_olt('sussuarana', 'Comando: show processor')
            time.sleep(2)

            # Expressão regular para capturar o valor de CPU(5s) e memória
            cpu_pattern = re.compile(r'^\s*\d+\s+\d+\s+\d+\s+(\d+)%', re.MULTILINE)
            mem_pattern = re.compile(r'^\s*\d+\s+\d+\s+\d+\s+\d+%\s+(\d+%)', re.MULTILINE)

            cpu_5s_values = cpu_pattern.findall(output)
            mem_values = mem_pattern.findall(output)

            # Exibindo os resultados

            global menu_sussuarana
            menu_sussuarana = customtkinter.CTkFrame(master=tabview.tab('OLT ZTE - Sussuarana'), width=400, height=200, corner_radius=30)
            menu_sussuarana.place(relx=0.17, rely=0.3, anchor=tkinter.CENTER)
            menu_sussuarana.pack_propagate(0)

            #faz o menu_sussuarana ser clicável
            menu_sussuarana.bind("<Button-1>", lambda e: print("Clicou no menu_sussuarana"))

            cor = carregar_config()
            if cor['cor'] == 'Azul':
                if cor['tema'] == 'Claro':
                    menu_sussuarana.configure(fg_color=cor['azul_claro'])
                else:
                    menu_sussuarana.configure(fg_color=cor['azul_escuro'])
            elif cor['cor'] == 'Verde':
                if cor['tema'] == 'Claro':
                    menu_sussuarana.configure(fg_color=cor['verde_claro'])
                else:
                    menu_sussuarana.configure(fg_color=cor['verde_escuro'])
            elif cor['cor'] == 'Acessy':
                if cor['tema'] == 'Claro':
                    menu_sussuarana.configure(fg_color=cor['acessy_claro'])
                else:
                    menu_sussuarana.configure(fg_color=cor['acessy_escuro'])

            titulo = customtkinter.CTkLabel(master=menu_sussuarana, text='Processamento', font=("Product Sans Regular", 20))
            titulo.place(relx=0.5, rely=0.15, anchor=tkinter.CENTER)


            labels = ["Rack", "Shelf", "Slot", "CPU", "Mem."]
            for i, label in enumerate(labels):
                customtkinter.CTkLabel(master=menu_sussuarana, text=label, font=("Product Sans Regular", 15)).place(relx=0.1 + i*0.2, rely=0.27, anchor=tkinter.CENTER)

            for i, (cpu, mem) in enumerate(zip(cpu_5s_values, mem_values), 1):
                y = 0.37 + (i-1)*0.1
                mem_percentage = int(mem[:-1])/100
                cpu_percentage = int(cpu)/100

                if mem_percentage < 0.5:
                    cor_mem = 'green'
                elif mem_percentage < 0.8:
                    cor_mem = 'yellow'
                else:
                    cor_mem = 'red'
                mem_bar = customtkinter.CTkProgressBar(master=menu_sussuarana, width=60, height=8, corner_radius=10, progress_color=cor_mem)
                mem_bar.set(mem_percentage)
                mem_bar.place(relx=0.9, rely=y, anchor=tkinter.CENTER)
                mem_label = customtkinter.CTkLabel(master=menu_sussuarana, text=mem, font=("Product Sans Regular", 10), fg_color='transparent')
                mem_label.place(relx=0.9, rely=y, anchor=tkinter.CENTER)

                if cpu_percentage < 0.5:
                    cor_cpu= 'green'
                elif cpu_percentage < 0.8:
                    cor_cpu= 'yellow'
                else:
                    cor_cpu = 'red'
                cpu_bar = customtkinter.CTkProgressBar(master=menu_sussuarana, width=60, height=8, corner_radius=10, progress_color=cor_cpu)
                cpu_bar.set(cpu_percentage)
                cpu_bar.place(relx=0.7, rely=y, anchor=tkinter.CENTER)
                cpu_label = customtkinter.CTkLabel(master=menu_sussuarana, text=cpu+'%', font=("Product Sans Regular", 10), fg_color='transparent')
                cpu_label.place(relx=0.7, rely=y, anchor=tkinter.CENTER)

                customtkinter.CTkLabel(master=menu_sussuarana, text='1', font=("Product Sans Regular", 15)).place(relx=0.1, rely=y, anchor=tkinter.CENTER)
                customtkinter.CTkLabel(master=menu_sussuarana, text='1', font=("Product Sans Regular", 15)).place(relx=0.3, rely=y, anchor=tkinter.CENTER)
                customtkinter.CTkLabel(master=menu_sussuarana, text=str(i), font=("Product Sans Regular", 15)).place(relx=0.5, rely=y, anchor=tkinter.CENTER)

        def onu_solic():
            global menu_sussuarana2
            menu_sussuarana2 = customtkinter.CTkFrame(master=tabview.tab('OLT ZTE - Sussuarana'), width=400, height=200, corner_radius=30)
            menu_sussuarana2.place(relx=0.5, rely=0.3, anchor=tkinter.CENTER)
            menu_sussuarana2.pack_propagate()

            cor = carregar_config()
            if cor['cor'] == 'Azul':
                if cor['tema'] == 'Claro':
                    menu_sussuarana2.configure(fg_color=cor['azul_claro'])
                else:
                    menu_sussuarana2.configure(fg_color=cor['azul_escuro'])
            elif cor['cor'] == 'Verde':
                if cor['tema'] == 'Claro':
                    menu_sussuarana2.configure(fg_color=cor['verde_claro'])
                else:
                    menu_sussuarana2.configure(fg_color=cor['verde_escuro'])
            elif cor['cor'] == 'Acessy':
                if cor['tema'] == 'Claro':
                    menu_sussuarana2.configure(fg_color=cor['acessy_claro'])
                else:
                    menu_sussuarana2.configure(fg_color=cor['acessy_escuro'])

            onu_solicitando = customtkinter.CTkLabel(master=menu_sussuarana2, text='ONUs Solicitando', font=("Product Sans Regular", 20))
            onu_solicitando.place(relx=0.5, rely=0.15, anchor=tkinter.CENTER)
            onu_solicitando.pack_propagate()

            posicao = customtkinter.CTkLabel(master=menu_sussuarana2, text='PON', font=("Product Sans Regular", 15))
            posicao.place(relx=0.3, rely=0.27, anchor=tkinter.CENTER)
            posicao.pack_propagate()

            sn = customtkinter.CTkLabel(master=menu_sussuarana2, text='Serial Number', font=("Product Sans Regular", 15))
            sn.place(relx=0.7, rely=0.27, anchor=tkinter.CENTER)
            sn.pack_propagate()

            output = obter_dados_olt('sussuarana', 'Comando: show gpon onu uncfg')
            time.sleep(2)
            if 'No related information to show.' in output:
                output = "Nenhuma ONU Solicitando no momento."
                warn = customtkinter.CTkLabel(master=menu_sussuarana2, text='', font=("Segoe Fluent Icons", 30), text_color='red')
                warn.place(relx=0.5, rely=0.38, anchor=tkinter.CENTER)
                info = customtkinter.CTkLabel(master=menu_sussuarana2, text=output, font=("Product Sans Regular", 15), text_color='red')
                info.place(relx=0.5, rely=0.55, anchor=tkinter.CENTER)
                sn.destroy()
                posicao.destroy()
                return
            else:
                output = [line for line in output.splitlines() if line.startswith("gpon-onu")]
                output = "\n".join(output)

                pattern = re.compile(r'(\S+)\s+(\S+)\s+\S+')
                matches = pattern.findall(output)

                for onuindex, sn in matches:
                    onu = customtkinter.CTkLabel(master=menu_sussuarana2, text=onuindex, font=("Product Sans Regular", 15))
                    onu.place(relx=0.3, rely=0.39, anchor=tkinter.CENTER)
                    onu.pack_propagate()

                    sn = customtkinter.CTkLabel(master=menu_sussuarana2, text=sn, font=("Product Sans Regular", 15))
                    sn.place(relx=0.7, rely=0.39, anchor=tkinter.CENTER)
                    sn.pack_propagate()
        
        def pon_percentage():
            global menu_sussuarana3
            menu_sussuarana3 = customtkinter.CTkFrame(master=tabview.tab('OLT ZTE - Sussuarana'), width=400, height=200, corner_radius=30)
            menu_sussuarana3.place(relx=0.83, rely=0.3, anchor=tkinter.CENTER)
            menu_sussuarana3.pack_propagate()

            def menu_sussuarana3_toplevel():
                global menu_sussuarana3toplevel
                
                #um grande agradecimento à HyperNylium pela função de centralização da janela: https://github.com/TomSchimansky/CustomTkinter/discussions/1820#discussion-5396625
                def CenterWindowToDisplay(Screen: Tk, width: int, height: int):
                    """Centers the window to the main display/monitor"""
                    screen_width = Screen.winfo_screenwidth()
                    screen_height = Screen.winfo_screenheight()
                    x = int((screen_width/2) - (width/2))
                    y = int((screen_height/2) - (height/1.5))
                    return f"{width}x{height}+{x}+{y}"
                
                menu_sussuarana3toplevel = customtkinter.CTkToplevel(app)
                menu_sussuarana3toplevel.title('Informações de PON')
                menu_sussuarana3toplevel.resizable(False, False)
                
                menu_sussuarana3toplevel.geometry(CenterWindowToDisplay(app, 1000, 800))

                menu_sussuarana3toplevel.attributes('-topmost', True)

                titulo = customtkinter.CTkLabel(master=menu_sussuarana3toplevel, text='Informações de PON', font=("Josefin Slab Bold", 25))
                titulo.place(relx=0.2, rely=0.1, anchor=tkinter.CENTER)
                scrollable_frame = customtkinter.CTkScrollableFrame(master=menu_sussuarana3toplevel, width=800, height=500)
                scrollable_frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

                search_bar = customtkinter.CTkEntry(master=menu_sussuarana3toplevel, width=200, font=("Product Sans Regular", 15), placeholder_text='Pesquisar ONU', corner_radius=40)
                search_bar.place(relx=0.7, rely=0.1, anchor=tkinter.CENTER)
                
                def search():
                    serial_number = search_bar.get()
                    url = 'http://100.127.0.250:5000/procurar_onu'
                    data = {
                        'serial_number': serial_number,
                        'olt': 'olt_4'
                    }

                    #um grande agradecimento à HyperNylium pela função de centralização da janela: https://github.com/TomSchimansky/CustomTkinter/discussions/1820#discussion-5396625
                    def CenterWindowToDisplay(Screen: Tk, width: int, height: int):
                        """Centers the window to the main display/monitor"""
                        screen_width = Screen.winfo_screenwidth()
                        screen_height = Screen.winfo_screenheight()
                        x = int((screen_width/2) - (width/2))
                        y = int((screen_height/2) - (height/1.5))
                        return f"{width}x{height}+{x}+{y}"

                    onu_info_top_level = customtkinter.CTkToplevel(app)
                    onu_info_top_level.title('Informações da ONU')
                    onu_info_top_level.resizable(False, False)

                    onu_info_top_level.geometry(CenterWindowToDisplay(app, 600, 600))

                    onu_info_top_level.attributes('-topmost', True)

                    response = requests.post(url, json=data)
                    response = response.text
                    # Dicionário para armazenar os dados extraídos
                    onu_data = {}

                    def parse_onu_output(output):
                        # Inicializa o dicionário onde os dados serão armazenados
                        onu_info = {}

                        # Separa o texto em linhas
                        lines = output.split('\n')
                        
                        # Variáveis de controle
                        history = []
                        history_section = False

                        # Expressão regular para identificar linhas importantes
                        key_value_pattern = re.compile(r"(\S.*?):\s*(.*)")
                        history_pattern = re.compile(r"\s*(\d+)\s+(\S+\s+\S+)\s+(\S+\s+\S+)\s+(\S+)")

                        for line in lines:
                            line = line.strip()
                            
                            # Verifica se estamos na seção de histórico
                            if line.startswith("Authpass Time"):
                                history_section = True
                                continue
                            
                            # Processa as linhas de histórico
                            if history_section:
                                match = history_pattern.match(line)
                                if match:
                                    event = {
                                        "Authpass Time": match.group(2),
                                        "Offline Time": match.group(3),
                                        "Cause": match.group(4)
                                    }
                                    history.append(event)
                                continue
                            
                            # Processa as linhas chave: valor
                            match = key_value_pattern.match(line)
                            if match:
                                key = match.group(1).strip()
                                value = match.group(2).strip()
                                onu_info[key] = value
                        
                        # Adiciona o histórico ao dicionário
                        if history:
                            onu_info["History"] = history

                        return onu_info
                    
                    onu_data = parse_onu_output(response)

                    x = 0.1
                    # Exibindo as informações da ONU
                    print(f'dadoooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooosssssssssssssssssss {onu_data}')
                    serial_number_label = customtkinter.CTkLabel(master=onu_info_top_level, text=f'Serial Number: {onu_data["Serial number"]}', font=("Josefin Slab Bold", 25))
                    serial_number_label.place(relx=0.5, rely=0.1, anchor=tkinter.CENTER)

                    def delete():
                        serial_number = search_bar.get()
                        url = 'http://100.127.0.250:5000/deletar_onu'
                        data = {
                            'serial_number': serial_number,
                            'olt': 'olt_4'
                        }

                        response = requests.post(url, json=data)
                        response = response.text
                        if response == 'sucesso':
                            onu_info_top_level.destroy()
                            menu_sussuarana3toplevel.destroy()
                        else:
                            print('')

                    delete_img = customtkinter.CTkImage(Image.open("assets\\delete.png"), size=(20,20))
                    delete_button = customtkinter.CTkButton(master=onu_info_top_level, text='Deletar ONU', font=("Product Sans Regular", 10), corner_radius=40, fg_color='#fa0000', hover_color='#a80000', image=delete_img, command=delete)
                    delete_button.place(relx=0.5, rely=0.9, anchor=tkinter.CENTER)

                    onu_interface_label = customtkinter.CTkLabel(master=onu_info_top_level, text=f'Interface: {onu_data["ONU interface"]}', font=("Product Sans Regular", 15))
                    onu_interface_label.place(relx=x, rely=0.2, anchor=tkinter.W)

                    name_label = customtkinter.CTkLabel(master=onu_info_top_level, text=f'Nome: {onu_data["Name"]}', font=("Product Sans Regular", 15))
                    name_label.place(relx=x, rely=0.3, anchor=tkinter.W)

                    config_state = customtkinter.CTkLabel(master=onu_info_top_level, text=f'Estado de Configuração: {onu_data["Config state"]}', font=("Product Sans Regular", 15))
                    config_state.place(relx=x, rely=0.4, anchor=tkinter.W)

                    online_duration_label = customtkinter.CTkLabel(master=onu_info_top_level, text=f'Duração Online: {onu_data["Online Duration"]}', font=("Product Sans Regular", 15))
                    online_duration_label.place(relx=x, rely=0.5, anchor=tkinter.W)

                    distance_label = customtkinter.CTkLabel(master=onu_info_top_level, text=f'Distância: {onu_data["ONU Distance"]}', font=("Product Sans Regular", 15))
                    distance_label.place(relx=x, rely=0.6, anchor=tkinter.W)

                search_image = customtkinter.CTkImage(Image.open("assets\\search.png"), size=(20,20))
                search_button = customtkinter.CTkButton(master=menu_sussuarana3toplevel, text='', image=search_image, width=20, corner_radius=40, command=search, fg_color='black', hover_color='gray')
                search_button.place(relx=0.85, rely=0.1, anchor=tkinter.CENTER)

                
                # Função para separar os dados por OnuIndex e cada campo de cada linha
                # Função para separar os dados da ONU
                def separar_por_onuindex(dados):
                    # Expressão regular para capturar cada ONU e seus respectivos estados
                    padrao_onu = re.compile(r'(\d+/\d+/\d+:\d+)\s+(\w+)\s+(\w+)\s+(\w+)\s+(\d+\(GPON\))')
                    
                    # Um dicionário para armazenar os resultados separados por OnuIndex
                    onu_separado = {}
                    pon_separado = {}
                    
                    # Iterar sobre todas as correspondências no texto
                    for match in padrao_onu.findall(dados):
                        onuindex = match[0]
                        pon = onuindex.split(':')[0]
                        onu = onuindex.split(':')[1]
                        admin_state = match[1]
                        omcc_state = match[2]
                        phase_state = match[3]
                        channel = match[4]
                        
                        # Criando um dicionário para armazenar os valores de cada ONU
                        onu_detalhes = {
                            'OnuIndex': onuindex,
                            'PON': pon,
                            'ONU': onu,
                            'Admin State': admin_state,
                            'OMCC State': omcc_state,
                            'Phase State': phase_state,
                            'Channel': channel
                        }

                        if pon not in pon_separado:
                            pon_separado[pon] = []
                            pon_separado[pon] = []

                        pon_separado[pon].append(onu_detalhes)

                        if onuindex not in onu_separado:
                            onu_separado[onuindex] = []
                        if onuindex not in onu_separado:
                            onu_separado[onuindex] = []
                        
                        onu_separado[onuindex].append(onu_detalhes)
                    
                    return pon_separado
                # Ensure pon_data is defined

                def obter_dados(olt_name, dados_a_consultar):
                    url = f'http://{server_ip}:5000/{olt_name}'
                    response = requests.get(url)
                    
                    if response.status_code == 200:
                        data = response.text  # Obtendo a resposta como texto bruto
                        # Dividindo o conteúdo por comandos
                        comandos = data.split('--------------------------------------------------------------------------------')

                        # Verifica qual comando foi solicitado e busca o bloco correspondente
                        for comando in comandos:
                            if dados_a_consultar in comando:
                                return comando    

                pon_data = obter_dados('sussuarana', 'show gpon onu state')
                time.sleep(2)
                
                # Separar os dados
                onu_separado = separar_por_onuindex(pon_data)

                global current_ponindex
                current_ponindex = 0

                # Função para exibir os dados começando a partir da linha 1
                def display_data():
                    if current_ponindex < len(onu_separado):
                        pon = list(onu_separado.keys())[current_ponindex]
                        registros = onu_separado[pon]

                        # Limpa o frame antes de adicionar novos widgets
                        for widget in scrollable_frame.winfo_children():
                            widget.destroy()

                        # Adiciona o título da PON

                        scrollable_frame.grid_columnconfigure(0, weight=1)
                        scrollable_frame.grid_columnconfigure(1, weight=1)
                        scrollable_frame.grid_columnconfigure(2, weight=1)
                        scrollable_frame.grid_columnconfigure(3, weight=1)
                        scrollable_frame.grid_columnconfigure(4, weight=1)

                        # Adiciona os títulos na linha 0
                        titulo_onuindex = customtkinter.CTkLabel(master=scrollable_frame, text='Onu Número', font=("Product Sans Bold", 20))
                        titulo_onuindex.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')

                        titulo_admin = customtkinter.CTkLabel(master=scrollable_frame, text='Estado Operacional', font=("Product Sans Bold", 20))
                        titulo_admin.grid(row=1, column=1, padx=5, pady=5, sticky='nsew')

                        titulo_omcc = customtkinter.CTkLabel(master=scrollable_frame, text='Estado na OLT', font=("Product Sans Bold", 20))
                        titulo_omcc.grid(row=1, column=2, padx=5, pady=5, sticky='nsew')

                        titulo_phase = customtkinter.CTkLabel(master=scrollable_frame, text='Estado Atual', font=("Product Sans Bold", 20))
                        titulo_phase.grid(row=1, column=3, padx=5, pady=5, sticky='nsew')

                        titulo_channel = customtkinter.CTkLabel(master=scrollable_frame, text='Canal', font=("Product Sans Bold", 20))
                        titulo_channel.grid(row=1, column=4, padx=5, pady=5, sticky='nsew')

                        titulo_pon = customtkinter.CTkLabel(master=scrollable_frame, text=f'PON {pon}', font=("Josefin Slab Bold", 30))
                        #titulo_pon.grid(row=0, column=1, columnspan=5, padx=5, pady=5, sticky='nsew')

                        scrollable_frame.configure(label_text=f'PON {pon}')

                        row_num = 2  # Começa na linha 2 (abaixo dos títulos)
                        for registro in registros:
                            adminstate = registro['Admin State']
                            if adminstate == 'enable':
                                adminstate = 'Ativo'
                            elif adminstate == 'disable':
                                adminstate = 'Inativo'
                            else:
                                adminstate = 'Desconhecido'

                            omccstate = registro['OMCC State']
                            if omccstate == 'enable':
                                omccstate = 'Ativo'
                            elif omccstate == 'disable':
                                omccstate = 'Inativo'

                            
                            label_onuindex = customtkinter.CTkLabel(master=scrollable_frame, text=registro['ONU'], font=("Product Sans Regular", 15))
                            label_onuindex.grid(row=row_num, column=0, padx=5, pady=5, sticky='nsew')
                            label_admin = customtkinter.CTkLabel(master=scrollable_frame, text=adminstate, font=("Product Sans Regular", 15))
                            label_admin.grid(row=row_num, column=1, padx=5, pady=5, sticky='nsew')
                            label_omcc = customtkinter.CTkLabel(master=scrollable_frame, text=omccstate, font=("Product Sans Regular", 15))
                            label_omcc.grid(row=row_num, column=2, padx=5, pady=5, sticky='nsew')
                            label_phase = customtkinter.CTkLabel(master=scrollable_frame, text=registro['Phase State'], width=80, font=("Product Sans Regular", 15), corner_radius=30)
                            label_phase.grid(row=row_num, column=3, padx=5, pady=5, sticky='nsew')

                            phase = registro['Phase State']
                            if phase == 'working':
                                phase = 'Online'
                                label_phase.configure(text=phase, bg_color='#02b302')
                            elif phase == 'OffLine':
                                phase = 'OffLine'
                                label_phase.configure(text=phase, bg_color='red')
                            elif phase == 'DyingGasp':
                                phase = 'Inativo'
                                label_phase.configure(text=phase, bg_color='orange')
                            elif phase == 'LOS':
                                phase = 'Sem Sinal'
                                label_phase.configure(text=phase, bg_color='gray')
                            else:
                                phase = 'Desconhecido'


                            label_channel = customtkinter.CTkLabel(master=scrollable_frame, text=registro['Channel'], font=("Product Sans Regular", 15))
                            label_channel.grid(row=row_num, column=4, padx=5, pady=5, sticky='nsew')
                            row_num += 1  # Próxima linha

                        # Adiciona o botão para o próximo PON
                        def next_pon():
                            global current_ponindex
                            current_ponindex += 1
                            display_data()

                        image_foward = customtkinter.CTkImage(Image.open('assets\\arrow_right.png'), size=(20,20))
                        image_backwards = customtkinter.CTkImage(Image.open('assets\\arrow_left.png'), size=(20,20))
                                                            
                        next_button = customtkinter.CTkButton(master=scrollable_frame, text="Próximo PON", image=image_foward, compound='right', command=next_pon)
                        next_button.grid(row=row_num, column=2, columnspan=5, pady=10)

                        # Adiciona o botão para o PON anterior
                        def previous_pon():
                            global current_ponindex
                            current_ponindex -= 1
                            display_data()

                        previous_button = customtkinter.CTkButton(master=scrollable_frame, text="PON Anterior", image=image_backwards, compound='left', command=previous_pon)
                        previous_button.grid(row=row_num, column=0, columnspan=5, pady=10)

                threading.Thread(target=display_data).start()
            #torna menu_sussuarana3 clicável
            menu_sussuarana3.bind("<Enter>", lambda e: menu_sussuarana3.configure(cursor="hand2"))
            menu_sussuarana3.bind("<Leave>", lambda e: menu_sussuarana3.configure(cursor=""))
            menu_sussuarana3.bind("<Button-1>", lambda e: menu_sussuarana3_toplevel())

            cor = carregar_config()
            if cor['cor'] == 'Azul':
                if cor['tema'] == 'Claro':
                    menu_sussuarana3.configure(fg_color=cor['azul_claro'])
                else:
                    menu_sussuarana3.configure(fg_color=cor['azul_escuro'])
            elif cor['cor'] == 'Verde':
                if cor['tema'] == 'Claro':
                    menu_sussuarana3.configure(fg_color=cor['verde_claro'])
                else:
                    menu_sussuarana3.configure(fg_color=cor['verde_escuro'])
            elif cor['cor'] == 'Acessy':
                if cor['tema'] == 'Claro':
                    menu_sussuarana3.configure(fg_color=cor['acessy_claro'])
                else:
                    menu_sussuarana3.configure(fg_color=cor['acessy_escuro'])

            pon_percentage = customtkinter.CTkLabel(master=menu_sussuarana3, text='PON Percentage', font=("Product Sans Regular", 20))
            pon_percentage.place(relx=0.5, rely=0.15, anchor=tkinter.CENTER)
            pon_percentage.pack_propagate()

            posicao = customtkinter.CTkLabel(master=menu_sussuarana3, text='Posição', font=("Product Sans Regular", 15))
            posicao.place(relx=0.3, rely=0.27, anchor=tkinter.CENTER)
            posicao.pack_propagate()

            sn = customtkinter.CTkLabel(master=menu_sussuarana3, text='Posiões Preenchidas', font=("Product Sans Regular", 15))
            sn.place(relx=0.7, rely=0.27, anchor=tkinter.CENTER)
            sn.pack_propagate()

            def update_pon_data():
                data = obter_dados_olt('sussuarana', 'Comando: show gpon onu state')
                time.sleep(2)
                # Expressão regular para capturar o OnuIndex, no formato 1/2/1, etc.
                pattern = re.compile(r'(\d+/\d+/\d+):\d+')

                # Dicionário para armazenar a contagem das ONUs por PON
                pon_counts = defaultdict(int)

                # Encontrar todas as ocorrências de PON e contar
                matches = pattern.findall(data)
                for pon in matches:
                    pon_counts[pon] += 1

                # Exibir o resultado
                for pon, count in pon_counts.items():
                    perc = count / 128

                y = 0.39
                for pon, count in pon_counts.items():
                    perc = count / 128

                    onu = customtkinter.CTkLabel(master=menu_sussuarana3, text=pon, font=("Product Sans Regular", 15))
                    onu.place(relx=0.3, rely=y, anchor=tkinter.CENTER)
                    onu.pack_propagate()

                    if perc < 0.5:
                        cor = 'green'
                    elif perc < 0.8:
                        cor = 'yellow'
                    else:
                        cor = 'red'

                    progress_bar = customtkinter.CTkProgressBar(master=menu_sussuarana3, width=200, height=10, corner_radius=10, progress_color=cor)
                    progress_bar.set(perc)
                    progress_bar.place(relx=0.7, rely=y, anchor=tkinter.CENTER)
                    sn = customtkinter.CTkLabel(master=menu_sussuarana3, text=f'{count}/128', font=("Product Sans Regular", 10), bg_color='transparent')
                    sn.place(relx=0.7, rely=y, anchor=tkinter.CENTER)
                    sn.pack_propagate()

                    y += 0.1

                    #se tiver mais de 6 itens, para a execução
                    if y > 0.9:
                        break

                texto_aguarde.destroy()

            # Run the update_pon_data function in a separate thread to keep the UI responsive
            threading.Thread(target=update_pon_data).start()

        def batch_commands():
            global menu_sussuarana4
            # Get the screen width to dynamically set the width of menu_sussuarana4
            screen_width = app.winfo_screenwidth()
            screen_height = app.winfo_screenheight()
            menu_sussuarana4_width = screen_width - 100  # Adjust the width as needed
            menu_sussuarana4_height = screen_height - 500  # Adjust the height as needed

            menu_sussuarana4 = customtkinter.CTkFrame(master=tabview.tab('OLT ZTE - Sussuarana'), width=menu_sussuarana4_width, height=menu_sussuarana4_height, corner_radius=30)
            menu_sussuarana4.place(relx=0.5, rely=0.75, anchor=tkinter.CENTER)

            # cor = carregar_config()
            # if cor['cor'] == 'Azul':
            #     if cor['tema'] == 'Claro':
            #         menu_sussuarana4.configure(fg_color=cor['azul_claro'])
            #     else:
            #         menu_sussuarana4.configure(fg_color=cor['azul_escuro'])
            # elif cor['cor'] == 'Verde':
            #     if cor['tema'] == 'Claro':
            #         menu_sussuarana4.configure(fg_color=cor['verde_claro'])
            #     else:
            #         menu_sussuarana4.configure(fg_color=cor['verde_escuro'])
            # elif cor['cor'] == 'Acessy':
            #     if cor['tema'] == 'Claro':
            #         menu_sussuarana4.configure(fg_color=cor['acessy_claro'])
            #     else:
            #         menu_sussuarana4.configure(fg_color=cor['acessy_escuro'])

            titulo = customtkinter.CTkLabel(master=menu_sussuarana4, text='Executar comandos em lotes', font=("Product Sans Regular", 20))
            titulo.place(relx=0.5, rely=0.1, anchor=tkinter.CENTER)
            titulo.pack_propagate()
    
        texto_aguarde = customtkinter.CTkLabel(master=tabview.tab('OLT ZTE - Sussuarana'), text='Por favor, aguarde enquanto as informações são carregadas...', font=("Josefin Slab Light", 20))
        texto_aguarde.place(relx=0.5, rely=0.7, anchor=tkinter.CENTER)

        def process_functions():
            # Wait for the SSH initialization thread to finish
            #ssh_thread.join()
            onu_solic()
            processamento()
            pon_percentage()
            batch_commands()

        # Create a thread to run the process_functions
        thread = threading.Thread(target=process_functions)
        thread.start()

    def olt_brotas():
        def processamento():
            output = obter_dados_olt('brotas', 'Comando: show processor')
            time.sleep(2)

            # Expressão regular para capturar os valores de CPU e Memória
            pattern = re.compile(
                r'(\S+)\s+(\S+)\s+(\d+)%\s+(\d+)%\s+(\d+)%\s+(\d+)%\s+(\d+)\s+(\d+)\s+(\d\d)'
            )

            # Encontrar todas as correspondências no output
            matches = pattern.findall(output)

            # Organizar os dados em um dicionário
            olt_data = []

            for match in matches:
                onu = {
                    'Component': match[0],
                    'Character': match[1],
                    'CPU_5s': match[2],
                    'CPU_1m': match[3],
                    'CPU_5m': match[4],
                    'Peak_CPU': match[5],
                    'PhyMem_MB': match[6],
                    'FreeMem_MB': match[7],
                    'Mem_Usage': match[8]
                }
                olt_data.append(onu)

            # Exibindo os resultados

            global menu_brotas
            menu_brotas = customtkinter.CTkFrame(master=tabview.tab('OLT ZTE - Brotas'), width=400, height=200, corner_radius=30)
            menu_brotas.place(relx=0.17, rely=0.3, anchor=tkinter.CENTER)
            menu_brotas.pack_propagate(0)

            #faz o menu_brotas ser clicável
            menu_brotas.bind("<Button-1>", lambda e: print("Clicou no menu_brotas"))

            cor = carregar_config()
            if cor['cor'] == 'Azul':
                if cor['tema'] == 'Claro':
                    menu_brotas.configure(fg_color=cor['azul_claro'])
                else:
                    menu_brotas.configure(fg_color=cor['azul_escuro'])
            elif cor['cor'] == 'Verde':
                if cor['tema'] == 'Claro':
                    menu_brotas.configure(fg_color=cor['verde_claro'])
                else:
                    menu_brotas.configure(fg_color=cor['verde_escuro'])
            elif cor['cor'] == 'Acessy':
                if cor['tema'] == 'Claro':
                    menu_brotas.configure(fg_color=cor['acessy_claro'])
                else:
                    menu_brotas.configure(fg_color=cor['acessy_escuro'])

            titulo = customtkinter.CTkLabel(master=menu_brotas, text='Processamento', font=("Product Sans Regular", 20))
            titulo.place(relx=0.5, rely=0.15, anchor=tkinter.CENTER)


            labels = ["Componente", "CPU", "Uso Máx.", "Memória"]
            for i, label in enumerate(labels):
                customtkinter.CTkLabel(master=menu_brotas, text=label, font=("Product Sans Regular", 15)).place(relx=0.15 + i*0.25, rely=0.27, anchor=tkinter.CENTER)

            for i, onu in enumerate(olt_data, 1):
                y = 0.37 + (i-1)*0.1
                mem_percentage = float(onu['Mem_Usage']) / 100
                cpu_percentage = int(onu['CPU_1m']) / 100
                peak_cpu = int(onu['Peak_CPU']) / 100

                if mem_percentage < 0.5:
                    cor_mem = 'green'
                elif mem_percentage < 0.8:
                    cor_mem = 'yellow'
                else:
                    cor_mem = 'red'
                mem_bar = customtkinter.CTkProgressBar(master=menu_brotas, width=60, height=8, corner_radius=10, progress_color=cor_mem)
                mem_bar.set(mem_percentage)
                mem_bar.place(relx=0.9, rely=y, anchor=tkinter.CENTER)
                mem_label = customtkinter.CTkLabel(master=menu_brotas, text=f"{onu['Mem_Usage']}%", font=("Product Sans Regular", 10), fg_color='transparent')
                mem_label.place(relx=0.9, rely=y, anchor=tkinter.CENTER)

                if cpu_percentage < 0.5:
                    cor_cpu = 'green'
                elif cpu_percentage < 0.8:
                    cor_cpu = 'yellow'
                else:
                    cor_cpu = 'red'
                cpu_bar = customtkinter.CTkProgressBar(master=menu_brotas, width=60, height=8, corner_radius=10, progress_color=cor_cpu)
                cpu_bar.set(cpu_percentage)
                cpu_bar.place(relx=0.4, rely=y, anchor=tkinter.CENTER)
                cpu_label = customtkinter.CTkLabel(master=menu_brotas, text=f"{onu['CPU_1m']}%", font=("Product Sans Regular", 10), fg_color='transparent')
                cpu_label.place(relx=0.4, rely=y, anchor=tkinter.CENTER)

                if peak_cpu < 0.5:
                    cor_peak = 'green'
                elif peak_cpu < 0.8:
                    cor_peak = 'yellow'
                else:
                    cor_peak = 'red'
                peak_bar = customtkinter.CTkProgressBar(master=menu_brotas, width=60, height=8, corner_radius=10, progress_color=cor_peak)
                peak_bar.set(peak_cpu)
                peak_bar.place(relx=0.65, rely=y, anchor=tkinter.CENTER)
                peak_label = customtkinter.CTkLabel(master=menu_brotas, text=f"{onu['Peak_CPU']}%", font=("Product Sans Regular", 10), fg_color='transparent')
                peak_label.place(relx=0.65, rely=y, anchor=tkinter.CENTER)

                customtkinter.CTkLabel(master=menu_brotas, text=onu['Component'], font=("Product Sans Regular", 15)).place(relx=0.15, rely=y, anchor=tkinter.CENTER)

        def onu_solic():
            global menu_brotas2
            menu_brotas2 = customtkinter.CTkFrame(master=tabview.tab('OLT ZTE - Brotas'), width=400, height=200, corner_radius=30)
            menu_brotas2.place(relx=0.5, rely=0.3, anchor=tkinter.CENTER)
            menu_brotas2.pack_propagate()

            cor = carregar_config()
            if cor['cor'] == 'Azul':
                if cor['tema'] == 'Claro':
                    menu_brotas2.configure(fg_color=cor['azul_claro'])
                else:
                    menu_brotas2.configure(fg_color=cor['azul_escuro'])
            elif cor['cor'] == 'Verde':
                if cor['tema'] == 'Claro':
                    menu_brotas2.configure(fg_color=cor['verde_claro'])
                else:
                    menu_brotas2.configure(fg_color=cor['verde_escuro'])
            elif cor['cor'] == 'Acessy':
                if cor['tema'] == 'Claro':
                    menu_brotas2.configure(fg_color=cor['acessy_claro'])
                else:
                    menu_brotas2.configure(fg_color=cor['acessy_escuro'])

            onu_solicitando = customtkinter.CTkLabel(master=menu_brotas2, text='ONUs Solicitando', font=("Product Sans Regular", 20))
            onu_solicitando.place(relx=0.5, rely=0.15, anchor=tkinter.CENTER)
            onu_solicitando.pack_propagate()

            posicao = customtkinter.CTkLabel(master=menu_brotas2, text='PON', font=("Product Sans Regular", 15))
            posicao.place(relx=0.3, rely=0.27, anchor=tkinter.CENTER)
            posicao.pack_propagate()

            sn = customtkinter.CTkLabel(master=menu_brotas2, text='Serial Number', font=("Product Sans Regular", 15))
            sn.place(relx=0.7, rely=0.27, anchor=tkinter.CENTER)
            sn.pack_propagate()

            output = obter_dados_olt('brotas', 'Comando: show gpon onu uncfg')
            time.sleep(2)
            if 'No related information to show.' in output:
                output = "Nenhuma ONU Solicitando no momento."
                warn = customtkinter.CTkLabel(master=menu_brotas2, text='', font=("Segoe Fluent Icons", 30), text_color='red')
                warn.place(relx=0.5, rely=0.38, anchor=tkinter.CENTER)
                info = customtkinter.CTkLabel(master=menu_brotas2, text=output, font=("Product Sans Regular", 15), text_color='red')
                info.place(relx=0.5, rely=0.55, anchor=tkinter.CENTER)
                sn.destroy()
                posicao.destroy()
                return
            else:
                output = [line for line in output.splitlines() if line.startswith("gpon-onu")]
                output = "\n".join(output)

                pattern = re.compile(r'(\S+)\s+(\S+)\s+\S+')
                matches = pattern.findall(output)

                for onuindex, sn in matches:
                    onu = customtkinter.CTkLabel(master=menu_brotas2, text=onuindex, font=("Product Sans Regular", 15))
                    onu.place(relx=0.3, rely=0.39, anchor=tkinter.CENTER)
                    onu.pack_propagate()

                    sn = customtkinter.CTkLabel(master=menu_brotas2, text=sn, font=("Product Sans Regular", 15))
                    sn.place(relx=0.7, rely=0.39, anchor=tkinter.CENTER)
                    sn.pack_propagate()
        
        def pon_percentage():
            global menu_brotas3
            menu_brotas3 = customtkinter.CTkFrame(master=tabview.tab('OLT ZTE - Brotas'), width=400, height=200, corner_radius=30)
            menu_brotas3.place(relx=0.83, rely=0.3, anchor=tkinter.CENTER)
            menu_brotas3.pack_propagate()

            def menu_brotas3_toplevel():
                global menu_brotas3toplevel
                
                #um grande agradecimento à HyperNylium pela função de centralização da janela: https://github.com/TomSchimansky/CustomTkinter/discussions/1820#discussion-5396625
                def CenterWindowToDisplay(Screen: Tk, width: int, height: int):
                    """Centers the window to the main display/monitor"""
                    screen_width = Screen.winfo_screenwidth()
                    screen_height = Screen.winfo_screenheight()
                    x = int((screen_width/2) - (width/2))
                    y = int((screen_height/2) - (height/1.5))
                    return f"{width}x{height}+{x}+{y}"
                
                menu_brotas3toplevel = customtkinter.CTkToplevel(app)
                menu_brotas3toplevel.title('Informações de PON')
                menu_brotas3toplevel.resizable(False, False)
                
                menu_brotas3toplevel.geometry(CenterWindowToDisplay(app, 1000, 800))

                menu_brotas3toplevel.attributes('-topmost', True)

                titulo = customtkinter.CTkLabel(master=menu_brotas3toplevel, text='Informações de PON', font=("Josefin Slab Bold", 25))
                titulo.place(relx=0.2, rely=0.1, anchor=tkinter.CENTER)
                scrollable_frame = customtkinter.CTkScrollableFrame(master=menu_brotas3toplevel, width=800, height=500)
                scrollable_frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

                search_bar = customtkinter.CTkEntry(master=menu_brotas3toplevel, width=200, font=("Product Sans Regular", 15), placeholder_text='Pesquisar ONU', corner_radius=40)
                search_bar.place(relx=0.7, rely=0.1, anchor=tkinter.CENTER)
                
                def search():
                    serial_number = search_bar.get()
                    url = 'http://100.127.0.250:5000/procurar_onu'
                    data = {
                        'serial_number': serial_number,
                        'olt': 'olt_5'
                    }

                    #um grande agradecimento à HyperNylium pela função de centralização da janela: https://github.com/TomSchimansky/CustomTkinter/discussions/1820#discussion-5396625
                    def CenterWindowToDisplay(Screen: Tk, width: int, height: int):
                        """Centers the window to the main display/monitor"""
                        screen_width = Screen.winfo_screenwidth()
                        screen_height = Screen.winfo_screenheight()
                        x = int((screen_width/2) - (width/2))
                        y = int((screen_height/2) - (height/1.5))
                        return f"{width}x{height}+{x}+{y}"

                    onu_info_top_level = customtkinter.CTkToplevel(app)
                    onu_info_top_level.title('Informações da ONU')
                    onu_info_top_level.resizable(False, False)

                    onu_info_top_level.geometry(CenterWindowToDisplay(app, 600, 600))

                    onu_info_top_level.attributes('-topmost', True)

                    response = requests.post(url, json=data)
                    response = response.text
                    # Dicionário para armazenar os dados extraídos
                    onu_data = {}

                    def parse_onu_output(output):
                        # Inicializa o dicionário onde os dados serão armazenados
                        onu_info = {}

                        # Separa o texto em linhas
                        lines = output.split('\n')
                        
                        # Variáveis de controle
                        history = []
                        history_section = False

                        # Expressão regular para identificar linhas importantes
                        key_value_pattern = re.compile(r"(\S.*?):\s*(.*)")
                        history_pattern = re.compile(r"\s*(\d+)\s+(\S+\s+\S+)\s+(\S+\s+\S+)\s+(\S+)")

                        for line in lines:
                            line = line.strip()
                            
                            # Verifica se estamos na seção de histórico
                            if line.startswith("Authpass Time"):
                                history_section = True
                                continue
                            
                            # Processa as linhas de histórico
                            if history_section:
                                match = history_pattern.match(line)
                                if match:
                                    event = {
                                        "Authpass Time": match.group(2),
                                        "Offline Time": match.group(3),
                                        "Cause": match.group(4)
                                    }
                                    history.append(event)
                                continue
                            
                            # Processa as linhas chave: valor
                            match = key_value_pattern.match(line)
                            if match:
                                key = match.group(1).strip()
                                value = match.group(2).strip()
                                onu_info[key] = value
                        
                        # Adiciona o histórico ao dicionário
                        if history:
                            onu_info["History"] = history

                        return onu_info
                    
                    onu_data = parse_onu_output(response)

                    x = 0.1
                    # Exibindo as informações da ONU
                    serial_number_label = customtkinter.CTkLabel(master=onu_info_top_level, text=f'Serial Number: {onu_data["Serial number"]}', font=("Josefin Slab Bold", 25))
                    serial_number_label.place(relx=0.5, rely=0.1, anchor=tkinter.CENTER)

                    def delete():
                        serial_number = search_bar.get()
                        url = 'http://100.127.0.250:5000/deletar_onu'
                        data = {
                            'serial_number': serial_number,
                            'olt': 'olt_5'
                        }

                        response = requests.post(url, json=data)
                        response = response.text
                        if response == 'sucesso':
                            onu_info_top_level.destroy()
                            menu_brotas3toplevel.destroy()
                        else:
                            print('')

                    delete_img = Image.open("assets\\delete.png", size=(20,20))
                    delete_button = customtkinter.CTkButton(master=onu_info_top_level, text='Deletar ONU', font=("Product Sans Regular", 10), corner_radius=40, fg_color='#fa0000', hover_color='#a80000', image=delete_img, command=delete)
                    delete_button.place(relx=0.5, rely=0.9, anchor=tkinter.CENTER)

                    onu_interface_label = customtkinter.CTkLabel(master=onu_info_top_level, text=f'Interface: {onu_data["ONU interface"]}', font=("Product Sans Regular", 15))
                    onu_interface_label.place(relx=x, rely=0.2, anchor=tkinter.W)

                    name_label = customtkinter.CTkLabel(master=onu_info_top_level, text=f'Nome: {onu_data["Name"]}', font=("Product Sans Regular", 15))
                    name_label.place(relx=x, rely=0.3, anchor=tkinter.W)

                    config_state = customtkinter.CTkLabel(master=onu_info_top_level, text=f'Estado de Configuração: {onu_data["Config state"]}', font=("Product Sans Regular", 15))
                    config_state.place(relx=x, rely=0.4, anchor=tkinter.W)

                    online_duration_label = customtkinter.CTkLabel(master=onu_info_top_level, text=f'Duração Online: {onu_data["Online Duration"]}', font=("Product Sans Regular", 15))
                    online_duration_label.place(relx=x, rely=0.5, anchor=tkinter.W)

                    distance_label = customtkinter.CTkLabel(master=onu_info_top_level, text=f'Distância: {onu_data["ONU Distance"]}', font=("Product Sans Regular", 15))
                    distance_label.place(relx=x, rely=0.6, anchor=tkinter.W)

                search_image = customtkinter.CTkImage(Image.open("assets\\search.png"), size=(20,20))
                search_button = customtkinter.CTkButton(master=menu_brotas3toplevel, text='', image=search_image, width=20, corner_radius=40, command=search, fg_color='black', hover_color='gray')
                search_button.place(relx=0.85, rely=0.1, anchor=tkinter.CENTER)

                
                # Função para separar os dados por OnuIndex e cada campo de cada linha
                # Função para separar os dados da ONU
                def separar_por_onuindex(dados):
                    print(dados)
                    # Expressão regular para capturar cada ONU e seus respectivos estados
                    padrao_onu = re.compile(r'(\d+/\d+/\d+:\d+)\s+(\w+)\s+(\w+)\s+(\w+)\s+(\w+)')
                    
                    # Um dicionário para armazenar os resultados separados por OnuIndex
                    onu_separado = {}
                    pon_separado = {}
                    
                    # Iterar sobre todas as correspondências no texto
                    for match in padrao_onu.findall(dados):
                        onuindex = match[0]
                        pon = onuindex.split(':')[0]
                        onu = onuindex.split(':')[1]
                        admin_state = match[1]
                        omcc_state = match[2]
                        phase_state = match[3]
                        channel = match[4]
                        
                        # Criando um dicionário para armazenar os valores de cada ONU
                        onu_detalhes = {
                            'OnuIndex': onuindex,
                            'PON': pon,
                            'ONU': onu,
                            'Admin State': admin_state,
                            'OMCC State': omcc_state,
                            'Phase State': phase_state,
                            'Channel': channel
                        }

                        if pon not in pon_separado:
                            pon_separado[pon] = []

                        pon_separado[pon].append(onu_detalhes)

                        # Adiciona a ONU ao dicionário
                        if onuindex not in onu_separado:
                            onu_separado[onuindex] = []
                        
                        onu_separado[onuindex].append(onu_detalhes)
                    
                    return pon_separado
                # Ensure pon_data is defined

                def obter_dados(olt_name, dados_a_consultar):
                    url = f'http://{server_ip}:5000/{olt_name}'
                    response = requests.get(url)
                    
                    if response.status_code == 200:
                        data = response.text  # Obtendo a resposta como texto bruto
                        # Dividindo o conteúdo por comandos
                        comandos = data.split('--------------------------------------------------------------------------------')

                        # Verifica qual comando foi solicitado e busca o bloco correspondente
                        for comando in comandos:
                            if dados_a_consultar in comando:
                                return comando    

                pon_data = obter_dados('brotas', 'show gpon onu state')
                time.sleep(2)
                
                # Separar os dados
                onu_separado = separar_por_onuindex(pon_data)

                print(onu_separado)

                global current_ponindex
                current_ponindex = 0

                # Função para exibir os dados começando a partir da linha 1
                def display_data():
                    if current_ponindex < len(onu_separado):
                        pon = list(onu_separado.keys())[current_ponindex]
                        registros = onu_separado[pon]

                        # Limpa o frame antes de adicionar novos widgets
                        for widget in scrollable_frame.winfo_children():
                            widget.destroy()

                        # Adiciona o título da PON

                        scrollable_frame.grid_columnconfigure(0, weight=1)
                        scrollable_frame.grid_columnconfigure(1, weight=1)
                        scrollable_frame.grid_columnconfigure(2, weight=1)
                        scrollable_frame.grid_columnconfigure(3, weight=1)
                        scrollable_frame.grid_columnconfigure(4, weight=1)

                        # Adiciona os títulos na linha 0
                        titulo_onuindex = customtkinter.CTkLabel(master=scrollable_frame, text='Onu Número', font=("Product Sans Bold", 20))
                        titulo_onuindex.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')

                        titulo_admin = customtkinter.CTkLabel(master=scrollable_frame, text='Estado Operacional', font=("Product Sans Bold", 20))
                        titulo_admin.grid(row=1, column=1, padx=5, pady=5, sticky='nsew')

                        titulo_omcc = customtkinter.CTkLabel(master=scrollable_frame, text='Estado na OLT', font=("Product Sans Bold", 20))
                        titulo_omcc.grid(row=1, column=2, padx=5, pady=5, sticky='nsew')

                        titulo_phase = customtkinter.CTkLabel(master=scrollable_frame, text='Estado Atual', font=("Product Sans Bold", 20))
                        titulo_phase.grid(row=1, column=3, padx=5, pady=5, sticky='nsew')

                        titulo_channel = customtkinter.CTkLabel(master=scrollable_frame, text='Canal', font=("Product Sans Bold", 20))
                        titulo_channel.grid(row=1, column=4, padx=5, pady=5, sticky='nsew')

                        titulo_pon = customtkinter.CTkLabel(master=scrollable_frame, text=f'PON {pon}', font=("Josefin Slab Bold", 30))
                        #titulo_pon.grid(row=0, column=1, columnspan=5, padx=5, pady=5, sticky='nsew')

                        scrollable_frame.configure(label_text=f'PON {pon}')

                        row_num = 2  # Começa na linha 2 (abaixo dos títulos)
                        for registro in registros:
                            adminstate = registro['Admin State']
                            if adminstate == 'enable':
                                adminstate = 'Ativo'
                            elif adminstate == 'disable':
                                adminstate = 'Inativo'
                            else:
                                adminstate = 'Desconhecido'

                            omccstate = registro['OMCC State']
                            if omccstate == 'enable':
                                omccstate = 'Ativo'
                            elif omccstate == 'disable':
                                omccstate = 'Inativo'

                            
                            label_onuindex = customtkinter.CTkLabel(master=scrollable_frame, text=registro['ONU'], font=("Product Sans Regular", 15))
                            label_onuindex.grid(row=row_num, column=0, padx=5, pady=5, sticky='nsew')
                            label_admin = customtkinter.CTkLabel(master=scrollable_frame, text=adminstate, font=("Product Sans Regular", 15))
                            label_admin.grid(row=row_num, column=1, padx=5, pady=5, sticky='nsew')
                            label_omcc = customtkinter.CTkLabel(master=scrollable_frame, text=omccstate, font=("Product Sans Regular", 15))
                            label_omcc.grid(row=row_num, column=2, padx=5, pady=5, sticky='nsew')
                            label_phase = customtkinter.CTkLabel(master=scrollable_frame, text=registro['Phase State'], width=80, font=("Product Sans Regular", 15), corner_radius=30)
                            label_phase.grid(row=row_num, column=3, padx=5, pady=5, sticky='nsew')

                            phase = registro['Phase State']
                            if phase == 'working':
                                phase = 'Online'
                                label_phase.configure(text=phase, bg_color='#02b302')
                            elif phase == 'OffLine':
                                phase = 'OffLine'
                                label_phase.configure(text=phase, bg_color='red')
                            elif phase == 'DyingGasp':
                                phase = 'Inativo'
                                label_phase.configure(text=phase, bg_color='orange')
                            elif phase == 'LOS':
                                phase = 'Sem Sinal'
                                label_phase.configure(text=phase, bg_color='gray')
                            else:
                                phase = 'Desconhecido'


                            label_channel = customtkinter.CTkLabel(master=scrollable_frame, text=registro['Channel'], font=("Product Sans Regular", 15))
                            label_channel.grid(row=row_num, column=4, padx=5, pady=5, sticky='nsew')
                            row_num += 1  # Próxima linha

                        # Adiciona o botão para o próximo PON
                        def next_pon():
                            global current_ponindex
                            current_ponindex += 1
                            display_data()

                        image_foward = customtkinter.CTkImage(Image.open('assets\\arrow_right.png'), size=(20,20))
                        image_backwards = customtkinter.CTkImage(Image.open('assets\\arrow_left.png'), size=(20,20))
                                                            
                        next_button = customtkinter.CTkButton(master=scrollable_frame, text="Próximo PON", image=image_foward, compound='right', command=next_pon)
                        next_button.grid(row=row_num, column=2, columnspan=5, pady=10)

                        # Adiciona o botão para o PON anterior
                        def previous_pon():
                            global current_ponindex
                            current_ponindex -= 1
                            display_data()

                        previous_button = customtkinter.CTkButton(master=scrollable_frame, text="PON Anterior", image=image_backwards, compound='left', command=previous_pon)
                        previous_button.grid(row=row_num, column=0, columnspan=5, pady=10)

                threading.Thread(target=display_data).start()
            #torna menu_brotas3 clicável
            menu_brotas3.bind("<Enter>", lambda e: menu_brotas3.configure(cursor="hand2"))
            menu_brotas3.bind("<Leave>", lambda e: menu_brotas3.configure(cursor=""))
            menu_brotas3.bind("<Button-1>", lambda e: menu_brotas3_toplevel())

            cor = carregar_config()
            if cor['cor'] == 'Azul':
                if cor['tema'] == 'Claro':
                    menu_brotas3.configure(fg_color=cor['azul_claro'])
                else:
                    menu_brotas3.configure(fg_color=cor['azul_escuro'])
            elif cor['cor'] == 'Verde':
                if cor['tema'] == 'Claro':
                    menu_brotas3.configure(fg_color=cor['verde_claro'])
                else:
                    menu_brotas3.configure(fg_color=cor['verde_escuro'])
            elif cor['cor'] == 'Acessy':
                if cor['tema'] == 'Claro':
                    menu_brotas3.configure(fg_color=cor['acessy_claro'])
                else:
                    menu_brotas3.configure(fg_color=cor['acessy_escuro'])

            pon_percentage = customtkinter.CTkLabel(master=menu_brotas3, text='PON Percentage', font=("Product Sans Regular", 20))
            pon_percentage.place(relx=0.5, rely=0.15, anchor=tkinter.CENTER)
            pon_percentage.pack_propagate()

            posicao = customtkinter.CTkLabel(master=menu_brotas3, text='Posição', font=("Product Sans Regular", 15))
            posicao.place(relx=0.3, rely=0.27, anchor=tkinter.CENTER)
            posicao.pack_propagate()

            sn = customtkinter.CTkLabel(master=menu_brotas3, text='Posiões Preenchidas', font=("Product Sans Regular", 15))
            sn.place(relx=0.7, rely=0.27, anchor=tkinter.CENTER)
            sn.pack_propagate()

            def update_pon_data():
                data = obter_dados_olt('brotas', 'Comando: show gpon onu state')
                time.sleep(2)
                # Expressão regular para capturar o OnuIndex, no formato 1/2/1, etc.
                pattern = re.compile(r'(\d+/\d+/\d+):\d+')

                # Dicionário para armazenar a contagem das ONUs por PON
                pon_counts = defaultdict(int)

                # Encontrar todas as ocorrências de PON e contar
                matches = pattern.findall(data)
                for pon in matches:
                    pon_counts[pon] += 1

                # Exibir o resultado
                for pon, count in pon_counts.items():
                    perc = count / 128

                y = 0.39
                for pon, count in pon_counts.items():
                    perc = count / 128

                    onu = customtkinter.CTkLabel(master=menu_brotas3, text=pon, font=("Product Sans Regular", 15))
                    onu.place(relx=0.3, rely=y, anchor=tkinter.CENTER)
                    onu.pack_propagate()

                    if perc < 0.5:
                        cor = 'green'
                    elif perc < 0.8:
                        cor = 'yellow'
                    else:
                        cor = 'red'

                    progress_bar = customtkinter.CTkProgressBar(master=menu_brotas3, width=200, height=10, corner_radius=10, progress_color=cor)
                    progress_bar.set(perc)
                    progress_bar.place(relx=0.7, rely=y, anchor=tkinter.CENTER)
                    sn = customtkinter.CTkLabel(master=menu_brotas3, text=f'{count}/128', font=("Product Sans Regular", 10), bg_color='transparent')
                    sn.place(relx=0.7, rely=y, anchor=tkinter.CENTER)
                    sn.pack_propagate()

                    y += 0.1

                    #se tiver mais de 6 itens, para a execução
                    if y > 0.9:
                        break

                texto_aguarde.destroy()

            # Run the update_pon_data function in a separate thread to keep the UI responsive
            threading.Thread(target=update_pon_data).start()

        def batch_commands():
            global menu_brotas4
            # Get the screen width to dynamically set the width of menu_brotas4
            screen_width = app.winfo_screenwidth()
            screen_height = app.winfo_screenheight()
            menu_brotas4_width = screen_width - 100  # Adjust the width as needed
            menu_brotas4_height = screen_height - 500  # Adjust the height as needed

            menu_brotas4 = customtkinter.CTkFrame(master=tabview.tab('OLT ZTE - Brotas'), width=menu_brotas4_width, height=menu_brotas4_height, corner_radius=30)
            menu_brotas4.place(relx=0.5, rely=0.75, anchor=tkinter.CENTER)

            # cor = carregar_config()
            # if cor['cor'] == 'Azul':
            #     if cor['tema'] == 'Claro':
            #         menu_brotas4.configure(fg_color=cor['azul_claro'])
            #     else:
            #         menu_brotas4.configure(fg_color=cor['azul_escuro'])
            # elif cor['cor'] == 'Verde':
            #     if cor['tema'] == 'Claro':
            #         menu_brotas4.configure(fg_color=cor['verde_claro'])
            #     else:
            #         menu_brotas4.configure(fg_color=cor['verde_escuro'])
            # elif cor['cor'] == 'Acessy':
            #     if cor['tema'] == 'Claro':
            #         menu_brotas4.configure(fg_color=cor['acessy_claro'])
            #     else:
            #         menu_brotas4.configure(fg_color=cor['acessy_escuro'])

            titulo = customtkinter.CTkLabel(master=menu_brotas4, text='Executar comandos em lotes', font=("Product Sans Regular", 20))
            titulo.place(relx=0.5, rely=0.1, anchor=tkinter.CENTER)
            titulo.pack_propagate()
    
        texto_aguarde = customtkinter.CTkLabel(master=tabview.tab('OLT ZTE - Brotas'), text='Por favor, aguarde enquanto as informações são carregadas...', font=("Josefin Slab Light", 20))
        texto_aguarde.place(relx=0.5, rely=0.7, anchor=tkinter.CENTER)

        def process_functions():
            # Wait for the SSH initialization thread to finish
            #ssh_thread.join()
            onu_solic()
            processamento()
            pon_percentage()
            batch_commands()

        # Create a thread to run the process_functions
        thread = threading.Thread(target=process_functions)
        thread.start()  
  
    #top_level para o menu de configurações
    def settings():
        
        toplevel = customtkinter.CTkToplevel(app)
        toplevel.title('Configurações')
        toplevel.resizable(False, False)
        titulo = customtkinter.CTkLabel(master=toplevel, text='Configurações', font=("Josefin Slab Bold", 25))
        titulo.place(relx=0.5, rely=0.15, anchor=tkinter.CENTER)

        #um grande agradecimento à HyperNylium pela função de centralização da janela: https://github.com/TomSchimansky/CustomTkinter/discussions/1820#discussion-5396625
        def CenterWindowToDisplay(Screen: Tk, width: int, height: int):
            """Centers the window to the main display/monitor"""
            screen_width = Screen.winfo_screenwidth()
            screen_height = Screen.winfo_screenheight()
            x = int((screen_width/2) - (width/2))
            y = int((screen_height/2) - (height/1.5))
            return f"{width}x{height}+{x}+{y}"
        
        toplevel.geometry(CenterWindowToDisplay(app, 400, 300))

        toplevel.attributes('-topmost', True)

        def logout():
            toplevel.destroy()
            app.destroy()
            config = carregar_config()
            config['usuario'] = ''
            salvar_config(config)
            login_page()

        def mudar_tema(tema):
            config = carregar_config()
            if tema == 'Padrão do sistema':
                customtkinter.set_appearance_mode("system")
            elif tema == 'Claro':
                config['tema'] = 'Claro'
                salvar_config(config)
                customtkinter.set_appearance_mode("light")
                mudar_cores(config['cor'])
            elif tema == 'Escuro':
                config['tema'] = 'Escuro'
                salvar_config(config)
                customtkinter.set_appearance_mode("dark")
                mudar_cores(config['cor'])
            else:
                customtkinter.set_appearance_mode("system")

        label_tema = customtkinter.CTkLabel(master=toplevel, text='Tema:', font=("Product Sans Regular", 15))
        label_tema.place(relx=0.05, rely=0.3, anchor=tkinter.W)
        opcoes_tema = customtkinter.CTkOptionMenu(master=toplevel, dynamic_resizing=False, width=200, values=['Claro', 'Escuro'], font=("Product Sans Regular", 15), command=mudar_tema)
        opcoes_tema.place(relx=0.05, rely=0.4, anchor=tkinter.W)
        opcoes_tema.set('Escuro')


        def mudar_cores(cor):
            global menu, menu2, menu3, menu_doron, menu_doron2, menu_doron3
            if cor == 'Padrão':
                menu.configure(fg_color='default')
                menu2.configure(fg_color='default')
                menu3.configure(fg_color='default')
                #menu4.configure(fg_color='default')
                menu_doron.configure(fg_color='default')
                menu_doron2.configure(fg_color='default')
                menu_doron3.configure(fg_color='default')
                menu_boca_do_rio.configure(fg_color='default')
                menu_boca_do_rio2.configure(fg_color='default')
                menu_boca_do_rio3.configure(fg_color='default')
                menu_brotas.configure(fg_color='default')
                menu_brotas2.configure(fg_color='default')
                menu_brotas3.configure(fg_color='default')
                menu_sussuarana.configure(fg_color='default')
                menu_sussuarana2.configure(fg_color='default')
                menu_sussuarana3.configure(fg_color='default')
            elif cor == 'Azul':
                #grava no arquivo de configuração config.json
                config = carregar_config()
                config['cor'] = 'Azul'
                salvar_config(config)
                #carrega a cor do tema do arquivo de configuração
                if config['tema'] == 'Claro':
                    menu.configure(fg_color='#c2e1ff')
                    menu2.configure(fg_color='#c2e1ff')
                    menu3.configure(fg_color='#c2e1ff')
                    #menu4.configure(fg_color='#c2e1ff')
                    menu_doron.configure(fg_color='#c2e1ff')
                    menu_doron2.configure(fg_color='#c2e1ff')
                    menu_doron3.configure(fg_color='#c2e1ff')
                    menu_boca_do_rio.configure(fg_color='#c2e1ff')
                    menu_boca_do_rio2.configure(fg_color='#c2e1ff')
                    menu_boca_do_rio3.configure(fg_color='#c2e1ff')
                    menu_brotas.configure(fg_color='#c2e1ff')
                    menu_brotas2.configure(fg_color='#c2e1ff')
                    menu_brotas3.configure(fg_color='#c2e1ff')
                    menu_sussuarana.configure(fg_color='#c2e1ff')
                    menu_sussuarana2.configure(fg_color='#c2e1ff')
                    menu_sussuarana3.configure(fg_color='#c2e1ff')
                    tabview.configure(segmented_button_selected_color='#c2e1ff')
                    tabview.configure(text_color='black')
                else:
                    menu.configure(fg_color='#002345')
                    menu2.configure(fg_color='#002345')
                    menu3.configure(fg_color='#002345')
                    #menu4.configure(fg_color='#002345')
                    menu_doron.configure(fg_color='#002345')
                    menu_doron2.configure(fg_color='#002345')
                    menu_doron3.configure(fg_color='#002345')
                    menu_boca_do_rio.configure(fg_color='#002345')
                    menu_boca_do_rio2.configure(fg_color='#002345')
                    menu_boca_do_rio3.configure(fg_color='#002345')
                    menu_brotas.configure(fg_color='#002345')
                    menu_brotas2.configure(fg_color='#002345')
                    menu_brotas3.configure(fg_color='#002345')
                    menu_sussuarana.configure(fg_color='#002345')
                    menu_sussuarana2.configure(fg_color='#002345')
                    menu_sussuarana3.configure(fg_color='#002345')
                    tabview.configure(segmented_button_selected_color='#002345')
                    tabview.configure(text_color='white')
            elif cor == 'Verde':
                config = carregar_config()
                config['cor'] = 'Verde'
                salvar_config(config)
                if config['tema'] == 'Claro':
                    menu.configure(fg_color='#cbf7d4')
                    menu2.configure(fg_color='#cbf7d4')
                    menu3.configure(fg_color='#cbf7d4')
                    #menu4.configure(fg_color='#cbf7d4')
                    menu_doron.configure(fg_color='#cbf7d4')
                    menu_doron2.configure(fg_color='#cbf7d4')
                    menu_doron3.configure(fg_color='#cbf7d4')
                    menu_boca_do_rio.configure(fg_color='#cbf7d4')
                    menu_boca_do_rio2.configure(fg_color='#cbf7d4')
                    menu_boca_do_rio3.configure(fg_color='#cbf7d4')
                    menu_brotas.configure(fg_color='#cbf7d4')
                    menu_brotas2.configure(fg_color='#cbf7d4')
                    menu_brotas3.configure(fg_color='#cbf7d4')
                    menu_sussuarana.configure(fg_color='#cbf7d4')
                    menu_sussuarana2.configure(fg_color='#cbf7d4')
                    menu_sussuarana3.configure(fg_color='#cbf7d4')
                    tabview.configure(segmented_button_selected_color='#cbf7d4')
                    tabview.configure(text_color='black')
                else:
                    menu.configure(fg_color='#002908')
                    menu2.configure(fg_color='#002908')
                    menu3.configure(fg_color='#002908')
                    #menu4.configure(fg_color='#002908')
                    menu_doron.configure(fg_color='#002908')
                    menu_doron2.configure(fg_color='#002908')
                    menu_doron3.configure(fg_color='#002908')
                    menu_boca_do_rio.configure(fg_color='#002908')
                    menu_boca_do_rio2.configure(fg_color='#002908')
                    menu_boca_do_rio3.configure(fg_color='#002908')
                    menu_brotas.configure(fg_color='#002908')
                    menu_brotas2.configure(fg_color='#002908')
                    menu_brotas3.configure(fg_color='#002908')
                    menu_sussuarana.configure(fg_color='#002908')
                    menu_sussuarana2.configure(fg_color='#002908')
                    menu_sussuarana3.configure(fg_color='#002908')
                    tabview.configure(segmented_button_selected_color='#002908')
                    tabview.configure(text_color='white')
            elif cor == 'Acessy':
                config = carregar_config()
                config['cor'] = 'Acessy'
                salvar_config(config)
                if config['tema'] == 'Claro':
                    menu.configure(fg_color='#ffbd80')
                    menu2.configure(fg_color='#ffbd80')
                    menu3.configure(fg_color='#ffbd80')
                    #menu4.configure(fg_color='#ffbd80')
                    menu_doron.configure(fg_color='#ffbd80')
                    menu_doron2.configure(fg_color='#ffbd80')
                    menu_doron3.configure(fg_color='#ffbd80')
                    menu_boca_do_rio.configure(fg_color='#ffbd80')
                    menu_boca_do_rio2.configure(fg_color='#ffbd80')
                    menu_boca_do_rio3.configure(fg_color='#ffbd80')
                    menu_brotas.configure(fg_color='#ffbd80')
                    menu_brotas2.configure(fg_color='#ffbd80')
                    menu_brotas3.configure(fg_color='#ffbd80')
                    menu_sussuarana.configure(fg_color='#ffbd80')
                    menu_sussuarana2.configure(fg_color='#ffbd80')
                    menu_sussuarana3.configure(fg_color='#ffbd80')
                    tabview.configure(segmented_button_selected_color='#ffbd80')
                    tabview.configure(text_color='black')
                else:
                    menu.configure(fg_color='#ff7b00')
                    menu2.configure(fg_color='#ff7b00')
                    menu3.configure(fg_color='#ff7b00')
                    #menu4.configure(fg_color='#ff7b00')
                    menu_doron.configure(fg_color='#ff7b00')
                    menu_doron2.configure(fg_color='#ff7b00')
                    menu_doron3.configure(fg_color='#ff7b00')
                    menu_boca_do_rio.configure(fg_color='#ff7b00')
                    menu_boca_do_rio2.configure(fg_color='#ff7b00')
                    menu_boca_do_rio3.configure(fg_color='#ff7b00')
                    menu_brotas.configure(fg_color='#ff7b00')
                    menu_brotas2.configure(fg_color='#ff7b00')
                    menu_brotas3.configure(fg_color='#ff7b00')
                    menu_sussuarana.configure(fg_color='#ff7b00')
                    menu_sussuarana2.configure(fg_color='#ff7b00')
                    menu_sussuarana3.configure(fg_color='#ff7b00')
                    tabview.configure(segmented_button_selected_color='#ff7b00')
                    tabview.configure(text_color='white')
            elif cor == 'Roxo':
                config = carregar_config()
                config['cor'] = 'Roxo'
                salvar_config(config)
                if config['tema'] == 'Claro':
                    menu.configure(fg_color='#ddabff')
                    menu2.configure(fg_color='#ddabff')
                    menu3.configure(fg_color='#ddabff')
                    #menu4.configure(fg_color='#ddabff')
                    menu_doron.configure(fg_color='#ddabff')
                    menu_doron2.configure(fg_color='#ddabff')
                    menu_doron3.configure(fg_color='#ddabff')
                    menu_boca_do_rio.configure(fg_color='#ddabff')
                    menu_boca_do_rio2.configure(fg_color='#ddabff')
                    menu_boca_do_rio3.configure(fg_color='#ddabff')
                    menu_brotas.configure(fg_color='#ddabff')
                    menu_brotas2.configure(fg_color='#ddabff')
                    menu_brotas3.configure(fg_color='#ddabff')
                    menu_sussuarana.configure(fg_color='#ddabff')
                    menu_sussuarana2.configure(fg_color='#ddabff')
                    menu_sussuarana3.configure(fg_color='#ddabff')
                    tabview.configure(segmented_button_selected_color='#ddabff')
                    tabview.configure(text_color='black')
                else:
                    menu.configure(fg_color='#49007a')
                    menu2.configure(fg_color='#49007a')
                    menu3.configure(fg_color='#49007a')
                    #menu4.configure(fg_color='#49007a')
                    menu_doron.configure(fg_color='#49007a')
                    menu_doron2.configure(fg_color='#49007a')
                    menu_doron3.configure(fg_color='#49007a')
                    menu_boca_do_rio.configure(fg_color='#49007a')
                    menu_boca_do_rio2.configure(fg_color='#49007a')
                    menu_boca_do_rio3.configure(fg_color='#49007a')
                    menu_brotas.configure(fg_color='#49007a')
                    menu_brotas2.configure(fg_color='#49007a')
                    menu_brotas3.configure(fg_color='#49007a')
                    menu_sussuarana.configure(fg_color='#49007a')
                    menu_sussuarana2.configure(fg_color='#49007a')
                    menu_sussuarana3.configure(fg_color='#49007a')
                    tabview.configure(segmented_button_selected_color='#49007a')
                    tabview.configure(text_color='white')
            elif cor == 'Rosa':
                config = carregar_config()
                config['cor'] = 'Rosa'
                salvar_config(config)
                if config['tema'] == 'Claro':
                    menu.configure(fg_color='#fcb6df')
                    menu2.configure(fg_color='#fcb6df')
                    menu3.configure(fg_color='#fcb6df')
                    #menu4.configure(fg_color='#fcb6df')
                    menu_doron.configure(fg_color='#fcb6df')
                    menu_doron2.configure(fg_color='#fcb6df')
                    menu_doron3.configure(fg_color='#fcb6df')
                    menu_boca_do_rio.configure(fg_color='#fcb6df')
                    menu_boca_do_rio2.configure(fg_color='#fcb6df')
                    menu_boca_do_rio3.configure(fg_color='#fcb6df')
                    menu_brotas.configure(fg_color='#fcb6df')
                    menu_brotas2.configure(fg_color='#fcb6df')
                    menu_brotas3.configure(fg_color='#fcb6df')
                    menu_sussuarana.configure(fg_color='#fcb6df')
                    menu_sussuarana2.configure(fg_color='#fcb6df')
                    menu_sussuarana3.configure(fg_color='#fcb6df')
                    tabview.configure(segmented_button_selected_color='#fcb6df')
                    tabview.configure(text_color='black')
                else:
                    menu.configure(fg_color='#4d0020')
                    menu2.configure(fg_color='#4d0020')
                    menu3.configure(fg_color='#4d0020')
                    #menu4.configure(fg_color='#4d0020')
                    menu_doron.configure(fg_color='#4d0020')
                    menu_doron2.configure(fg_color='#4d0020')
                    menu_doron3.configure(fg_color='#4d0020')
                    menu_boca_do_rio.configure(fg_color='#4d0020')
                    menu_boca_do_rio2.configure(fg_color='#4d0020')
                    menu_boca_do_rio3.configure(fg_color='#4d0020')
                    menu_brotas.configure(fg_color='#4d0020')
                    menu_brotas2.configure(fg_color='#4d0020')
                    menu_brotas3.configure(fg_color='#4d0020')
                    menu_sussuarana.configure(fg_color='#4d0020')
                    menu_sussuarana2.configure(fg_color='#4d0020')
                    menu_sussuarana3.configure(fg_color='#4d0020')
                    tabview.configure(segmented_button_selected_color='#4d0020')
                    tabview.configure(text_color='white')
            else:
                customtkinter.set_appearance_mode("system")
        
        label_cores = customtkinter.CTkLabel(master=toplevel,text='Cores:', font=("Product Sans Regular", 15))
        label_cores.place(relx=0.05, rely=0.5, anchor=tkinter.W)
        opcoes_cores = customtkinter.CTkOptionMenu(master=toplevel, dynamic_resizing = False, width=200, values=['Azul', 'Verde', 'Acessy', 'Roxo', 'Rosa'], font=("Product Sans Regular", 15), command=mudar_cores)
        opcoes_cores.place(relx=0.05, rely=0.6, anchor=tkinter.W)
        opcoes_cores.set('Azul')

        logout_icon = customtkinter.CTkImage(Image.open("assets\\logout.png"), size=(20,20))
        logout_button = customtkinter.CTkButton(master=toplevel, text='Logout', fg_color='#fa0000', hover_color = '#a80000', corner_radius=100, width=20, height=12, font=("Product Sans Regular", 10), image=logout_icon, command=logout)
        logout_button.place(relx=0.85, rely=0.1, anchor=tkinter.CENTER)

    profile_photo = customtkinter.CTkImage(Image.open('assets\\profile.png'), size=(40,40))
    #settings_button = customtkinter.CTkButton(master=app, bg_color='transparent', text='', fg_color='transparent', hover_color='#bababa', image=profile_photo, width=40, height=40, corner_radius=500, command=settings)
    #settings_button.place(relx=0.97, rely=0.05, anchor=tkinter.CENTER)
    profile_photo_label = customtkinter.CTkLabel(master=app, image=profile_photo, text='')
    profile_photo_label.place(relx=0.97, rely=0.05, anchor=tkinter.CENTER)

    profile_photo_label.bind("<Enter>", lambda e: profile_photo_label.configure(cursor="hand2"))
    profile_photo_label.bind("<Leave>", lambda e: profile_photo_label.configure(cursor=""))
    profile_photo_label.bind("<Button-1>", lambda e: settings())

    threading.Thread(target=olt_novo).start()
    threading.Thread(target=olt_doron).start()
    threading.Thread(target=olt_boca_do_rio).start()
    threading.Thread(target=olt_brotas).start()
    threading.Thread(target=olt_sussuarana).start()

    app.iconbitmap('assets\\icon.ico')
    app.mainloop()
    

def login_page():

    app = customtkinter.CTk()  
    app.geometry("1000x800")
    app.title('Login')
    app.resizable(False, False)

    termos_de_uso = """1 de outubro de 2024.
    
                        Este programa coleta e utiliza estatísticas de uso dos usuários com o objetivo de realizar pesquisas de satisfação e promover melhorias contínuas na experiência e no desempenho do software. As informações coletadas são utilizadas exclusivamente para aprimoramento interno e desenvolvimento de novas funcionalidades, garantindo uma melhor usabilidade e atendimento às necessidades dos usuários.

                        Em conformidade com a Lei Geral de Proteção de Dados (LGPD), asseguramos que os dados coletados não serão vendidos, compartilhados, ou disponibilizados a terceiros sob nenhuma circunstância. Todas as informações coletadas são armazenadas de forma segura e tratadas com o mais alto nível de proteção para garantir a privacidade e a confidencialidade dos dados dos nossos usuários.

                        Ao utilizar o programa, o usuário consente com a coleta e tratamento dessas estatísticas conforme descrito, com total garantia de privacidade e segurança.
                    """

    #top_level para os termos de uso
    def termos():
        toplevel = customtkinter.CTkToplevel(app)
        toplevel.title('Termos de Uso')
        toplevel.geometry('800x600')
        toplevel.resizable(False, False)
        titulo = customtkinter.CTkLabel(master=toplevel, text='Termos de Uso', font=("Josefin Slab Bold", 40))
        titulo.place(relx=0.5, rely=0.1, anchor=tkinter.CENTER)

        # Use a Text widget to handle long text with automatic line breaks and justification
        texto_frame = customtkinter.CTkFrame(master=toplevel, width=700, height=400)
        texto_frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
        texto_frame.pack_propagate(False)

        texto = tkinter.Text(master=texto_frame, wrap=tkinter.WORD, font=("Product Sans Regular", 15), bg='#2b2b2b', fg='white', bd=0)
        texto.insert(tkinter.END, termos_de_uso)
        texto.config(state=tkinter.DISABLED)
        texto.pack(expand=True, fill=tkinter.X)

        toplevel.deiconify()

        def accept():
            toplevel.destroy()
            with open('config.json', 'r') as f:
                config = json.load(f)
                config['aceitou_termos'] = True
            with open('config.json', 'w') as f:
                json.dump(config, f)

        aceitar = customtkinter.CTkButton(master=toplevel, text='Aceitar', text_color='black', fg_color='#33ff55', hover_color='#21a336', width=100, height=40, corner_radius=100, font=("Product Sans Bold", 15), command=accept)
        aceitar.place(relx=0.7, rely=0.9, anchor=tkinter.CENTER)
        recusar = customtkinter.CTkButton(master=toplevel, text='Recusar', fg_color='#707070', hover_color='#525252', width=100, height=40, corner_radius=100, font=("Product Sans Regular", 15), command=app.destroy)
        recusar.place(relx=0.3, rely=0.9, anchor=tkinter.CENTER)
    
    with open('config.json', 'r') as f:
        config = json.load(f)
        if config['aceitou_termos'] == True:
            pass
        else:
            termos()

    def quinto_dia_útil():
        # Verificar se é o quinto dia útil do mês
        data_atual = datetime.now()
        dia = data_atual.day
        dia_da_semana = data_atual.weekday()
        if dia_da_semana == 4 and dia <= 5:
            return True
        else:
            return False

    def get_title():
        return random.choice(title_list)

    text2 = 'Bem vindo ao DumbOLT'
    num_char = len(text2)
    i = 0

    def update_text():
        nonlocal i
        if i < num_char:
            text3 = text2[:i+1] 
            texto.configure(text=text3)
            i += 1
            texto.after(70, update_text)

    title_list = ['E aí? Show? Certinho?']

    text1 = get_title()

    texto = customtkinter.CTkLabel(master=app, text=text1, font=("Josefin Slab Bold", 70))
    texto.place(relx=0.5, rely=0.25, anchor=tkinter.CENTER)
    texto.pack_propagate()

    texto2 = customtkinter.CTkLabel(master=app, text='', font=("Josefin Slab Light", 30))
    texto2.place(relx=0.5, rely=0.36, anchor=tkinter.CENTER)
    texto2.pack_propagate()

    texto.after(3000, update_text)

    def auth_button():
        login()
        texto2.configure(text='Aguardando autenticação...')

    def get_users_info():
        response = requests.get('http://100.127.0.250:5000/users')
        if response.status_code == 200:
            data = response.json()
            return data
        
    # Função para carregar configurações existentes do arquivo JSON
    def carregar_config():
        try:
            with open('config.json', 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
    
    # Função para salvar configurações atualizadas no arquivo JSON
    def salvar_config(config):
        with open('config.json', 'w') as f:
            json.dump(config, f)

    def check_credentials():
        users = get_users_info()
        login = login_box.get()
        password = password_box.get()
        if login in users and password == users[login]:
            texto2.configure(text='Login efetuado com sucesso')
            #salva no arquivo de configuração o usuário logado
            config = carregar_config()
            config['usuario'] = login
            salvar_config(config)
            app.destroy()
            home_page()
        
        else:
            texto2.configure(text='Credenciais inválidas')

    img1=customtkinter.CTkImage(Image.open("assets\\google.png"), size=(30,30))
    button2= customtkinter.CTkButton(master=app, image=img1, text="Sign up using Google", width=400, height=55, compound="left", fg_color='white', text_color='black', hover_color='#AFAFAF', corner_radius=70, font=("Josefin Slab Medium", 30), command=auth_button)
    #button2.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

    login_box = customtkinter.CTkEntry(master=app, placeholder_text='E-mail...', width=400, height=40, corner_radius=100, fg_color='white', border_color='white', text_color='black', placeholder_text_color='gray', font=("Product Sans", 15))
    login_box.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

    password_box = customtkinter.CTkEntry(master=app, placeholder_text='Senha...', width=400, height=40, corner_radius=100, fg_color='white', border_color='white', text_color='black', placeholder_text_color='gray', font=("Product Sans", 15), show='*')
    password_box.place(relx=0.5, rely=0.58, anchor=tkinter.CENTER)

    def forgot():
        texto2.configure(text='Abre um chamado.')

    forgot_password = customtkinter.CTkButton(master=app, text='Esqueceu a senha?', font=("Product Sans Regular", 15), hover_color='#595959', fg_color='transparent', command=forgot)
    forgot_password.place(relx=0.62, rely=0.63, anchor=tkinter.CENTER)

    login_img = customtkinter.CTkImage(Image.open("assets\\arrow_foward.png"), size=(20,20))
    login_button = customtkinter.CTkButton(master=app, image=login_img, text='', width=20, height=40, fg_color='#99bdf6', hover_color='#AFAFAF', corner_radius=500, command=check_credentials)
    login_button.place(relx=0.5, rely=0.66, anchor=tkinter.CENTER)

    version_label = customtkinter.CTkLabel(master=app, text="Versão - beta1.0_aGVhdmVu", font=("Product Sans Regular", 10))
    version_label.place(relx=0.9, rely=0.95, anchor=tkinter.CENTER)

    app.iconbitmap('assets\\icon.ico')

    app.mainloop()

    # Função para carregar configurações existentes do arquivo JSON
def carregar_config():
    try:
        with open('config.json', 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}
    
    # Função para salvar configurações atualizadas no arquivo JSON
def salvar_config(config):
    with open('config.json', 'w') as f:
        json.dump(config, f)

def verificar_usuario():
    #verifica se o usuário já está logado
    config = carregar_config()
    if config['usuario'] != '':
        home_page()
    else:
        login_page()

verificar_usuario()
#home_page()
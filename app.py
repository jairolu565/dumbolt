import customtkinter
import customtkinter as ctk
import tkinter
import random
from PIL import Image, ImageEnhance, ImageDraw, ImageFont
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

    print(f"Tentando conectar ao {hostname}...")
    
    try:
        print('Iniciando conexão SSH...')
        client.connect(hostname=hostname, username=username, password=password, timeout=60)
        print(f"Conectado ao {hostname}")
        shell = client.invoke_shell()
        time.sleep(1)
        # envia conf t para entrar no modo de configuração
        shell.send('terminal length 0\n')
        time.sleep(1)
        shell.send('conf t\n')
        time.sleep(1)
        output = shell.recv(1000).decode('utf-8')
        print(output)
    except paramiko.SSHException as e:
        print(f"Erro de SSH: {e}")
    
def fechar_conexao_ssh():
    global client
    if client:
        client.close()
        print("Conexão SSH fechada.")

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

    tabview = customtkinter.CTkTabview(master=app, width=1600, height=800, fg_color='transparent')
    tabview.pack(padx=20, pady=20)

    tabview.add("OLT ZTE - Novo Horizonte")  # add tab at the end
    tabview.add("OLT ZTE - Doron")  # add tab at the end
    tabview.add("OLT ZTE - Boca do Rio")  # add tab at the end
    tabview.add("OLT ZTE - Sussuarana")  # add tab at the end
    tabview.add("OLT ZTE - Arvoredo") # add tab at the end
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

    logo = customtkinter.CTkImage(Image.open("logo_acessy.png"), size=(50,50))
    logo_label = customtkinter.CTkLabel(master=app, image=logo, text='')
    logo_label.place(relx=0.03, rely=0.05, anchor=tkinter.CENTER)

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

        else:
            print(f"Falha ao obter dados da OLT {olt_name}. Status: {response.status_code}")


    def olt_doron():
        def processamento():
            output = obter_dados_olt('doron', 'Comando: show processor')
            time.sleep(2)
            print(output)

            # Expressão regular para capturar o valor de CPU(5s) e memória
            cpu_pattern = re.compile(r'^\s*\d+\s+\d+\s+\d+\s+(\d+)%', re.MULTILINE)
            mem_pattern = re.compile(r'^\s*\d+\s+\d+\s+\d+\s+\d+%\s+(\d+%)', re.MULTILINE)

            cpu_5s_values = cpu_pattern.findall(output)
            mem_values = mem_pattern.findall(output)

            # Exibindo os resultados
            print("CPU(5s) valores por linha:")
            for i, cpu in enumerate(cpu_5s_values, 1):
                print(f"Linha {i}: {cpu}%")

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

                # Se tiver mais de 6 itens, para a execução
                if i >= 6:
                    break

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
            print(output)
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
                print("Contagem de ONUs por PON:")
                for pon, count in pon_counts.items():
                    perc = count / 128
                    print(f"PON {pon}: {count} ONUs ({perc:.2f}%)")

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

                icone_label.destroy()
                texto_aguarde.destroy()

            # Run the update_pon_data function in a separate thread to keep the UI responsive
            threading.Thread(target=update_pon_data).start()
        
        # Sequência de caracteres para a animação
        icones = ""
        # Índice inicial da sequência de ícones
        indice_atual = 0

        # Função para alternar entre os ícones
        def atualizar_icone():
            nonlocal indice_atual
            # Define o texto do ícone atual
            icone_label.configure(text=icones[indice_atual])
            # Atualiza o índice para o próximo ícone
            indice_atual = (indice_atual + 1) % len(icones)
            # Chama a função novamente após 15 milissegundos
            app.after(2, atualizar_icone)

        # Adicionar o primeiro ícone na tela como um texto qualquer
        icone_label = customtkinter.CTkLabel(master=tabview.tab('OLT ZTE - Doron'), text=icones[indice_atual], font=("Segoe Boot Semilight", 40))
        icone_label.place(relx=0.5, rely=0.8, anchor=tkinter.CENTER)
        texto_aguarde = customtkinter.CTkLabel(master=tabview.tab('OLT ZTE - Doron'), text='Por favor, aguarde enquanto as informações são carregadas...', font=("Josefin Slab Light", 20))
        texto_aguarde.place(relx=0.5, rely=0.7, anchor=tkinter.CENTER)

        # Inicia a animação
        atualizar_icone()

        def process_functions():
            # Wait for the SSH initialization thread to finish
            #ssh_thread.join()
            onu_solic()
            processamento()
            pon_percentage()

        # Create a thread to run the process_functions
        thread = threading.Thread(target=process_functions)
        thread.start()

    def olt_novo():
        def processamento():
            output = obter_dados_olt('novo_horizonte', 'Comando: show processor')
            time.sleep(2)
            print(output)

            # Expressão regular para capturar o valor de CPU(5s) e memória
            cpu_pattern = re.compile(r'^\s*\d+\s+\d+\s+\d+\s+(\d+)%', re.MULTILINE)
            mem_pattern = re.compile(r'^\s*\d+\s+\d+\s+\d+\s+\d+%\s+(\d+%)', re.MULTILINE)

            cpu_5s_values = cpu_pattern.findall(output)
            mem_values = mem_pattern.findall(output)

            # Exibindo os resultados
            print("CPU(5s) valores por linha:")
            for i, cpu in enumerate(cpu_5s_values, 1):
                print(f"Linha {i}: {cpu}%")

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
            print(output)
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
                print("Contagem de ONUs por PON:")
                for pon, count in pon_counts.items():
                    perc = count / 128
                    print(f"PON {pon}: {count} ONUs ({perc:.2f}%)")

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

                icone_label.destroy()
                texto_aguarde.destroy()

            # Run the update_pon_data function in a separate thread to keep the UI responsive
            threading.Thread(target=update_pon_data).start()
        
        # Sequência de caracteres para a animação
        icones = ""
        # Índice inicial da sequência de ícones
        indice_atual = 0

        # Função para alternar entre os ícones
        def atualizar_icone():
            nonlocal indice_atual
            # Define o texto do ícone atual
            icone_label.configure(text=icones[indice_atual])
            # Atualiza o índice para o próximo ícone
            indice_atual = (indice_atual + 1) % len(icones)
            # Chama a função novamente após 15 milissegundos
            app.after(2, atualizar_icone)

        # Adicionar o primeiro ícone na tela como um texto qualquer
        icone_label = customtkinter.CTkLabel(master=tabview.tab('OLT ZTE - Novo Horizonte'), text=icones[indice_atual], font=("Segoe Boot Semilight", 40))
        icone_label.place(relx=0.5, rely=0.8, anchor=tkinter.CENTER)
        texto_aguarde = customtkinter.CTkLabel(master=tabview.tab('OLT ZTE - Novo Horizonte'), text='Por favor, aguarde enquanto as informações são carregadas...', font=("Josefin Slab Light", 20))
        texto_aguarde.place(relx=0.5, rely=0.7, anchor=tkinter.CENTER)

        # Inicia a animação
        atualizar_icone()

        def process_functions():
            # Wait for the SSH initialization thread to finish
            #ssh_thread.join()
            onu_solic()
            processamento()
            pon_percentage()

        # Create a thread to run the process_functions
        thread = threading.Thread(target=process_functions)
        thread.start()
  
    #top_level para o menu de configurações
    def settings():
        
        toplevel = customtkinter.CTkToplevel(app)
        toplevel.title('Configurações')
        toplevel.geometry('400x300')
        toplevel.resizable(False, False)
        titulo = customtkinter.CTkLabel(master=toplevel, text='Configurações', font=("Josefin Slab Bold", 25))
        titulo.place(relx=0.5, rely=0.15, anchor=tkinter.CENTER)

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
        opcoes_tema = customtkinter.CTkOptionMenu(master=toplevel, dynamic_resizing=False, width=200, values=['Padrão do sistema','Claro', 'Escuro'], font=("Product Sans Regular", 15), command=mudar_tema)
        opcoes_tema.place(relx=0.05, rely=0.4, anchor=tkinter.W)
        opcoes_tema.set('Padrão do sistema')


        def mudar_cores(cor):
            global menu, menu2, menu3, menu_doron, menu_doron2, menu_doron3
            if cor == 'Padrão':
                menu.configure(fg_color='default')
                menu2.configure(fg_color='default')
                menu3.configure(fg_color='default')
                menu_doron.configure(fg_color='default')
                menu_doron2.configure(fg_color='default')
                menu_doron3.configure(fg_color='default')
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
                    menu_doron.configure(fg_color='#c2e1ff')
                    menu_doron2.configure(fg_color='#c2e1ff')
                    menu_doron3.configure(fg_color='#c2e1ff')
                    tabview.configure(segmented_button_selected_color='#c2e1ff')
                    tabview.configure(text_color='black')
                else:
                    menu.configure(fg_color='#002345')
                    menu2.configure(fg_color='#002345')
                    menu3.configure(fg_color='#002345')
                    menu_doron.configure(fg_color='#002345')
                    menu_doron2.configure(fg_color='#002345')
                    menu_doron3.configure(fg_color='#002345')
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
                    menu_doron.configure(fg_color='#cbf7d4')
                    menu_doron2.configure(fg_color='#cbf7d4')
                    menu_doron3.configure(fg_color='#cbf7d4')
                    tabview.configure(segmented_button_selected_color='#cbf7d4')
                    tabview.configure(text_color='black')
                else:
                    menu.configure(fg_color='#002908')
                    menu2.configure(fg_color='#002908')
                    menu3.configure(fg_color='#002908')
                    menu_doron.configure(fg_color='#002908')
                    menu_doron2.configure(fg_color='#002908')
                    menu_doron3.configure(fg_color='#002908')
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
                    menu_doron.configure(fg_color='#ffbd80')
                    menu_doron2.configure(fg_color='#ffbd80')
                    menu_doron3.configure(fg_color='#ffbd80')
                    tabview.configure(segmented_button_selected_color='#ffbd80')
                    tabview.configure(text_color='black')
                else:
                    menu.configure(fg_color='#ff7b00')
                    menu2.configure(fg_color='#ff7b00')
                    menu3.configure(fg_color='#ff7b00')
                    menu_doron.configure(fg_color='#ff7b00')
                    menu_doron2.configure(fg_color='#ff7b00')
                    menu_doron3.configure(fg_color='#ff7b00')
                    tabview.configure(segmented_button_selected_color='#ff7b00')
                    tabview.configure(text_color='white')
            else:
                customtkinter.set_appearance_mode("system")
        
        label_cores = customtkinter.CTkLabel(master=toplevel,text='Cores:', font=("Product Sans Regular", 15))
        label_cores.place(relx=0.05, rely=0.5, anchor=tkinter.W)
        opcoes_cores = customtkinter.CTkOptionMenu(master=toplevel, dynamic_resizing = False, width=200, values=['Padrão', 'Azul', 'Verde', 'Acessy'], font=("Product Sans Regular", 15), command=mudar_cores)
        opcoes_cores.place(relx=0.05, rely=0.6, anchor=tkinter.W)
        opcoes_cores.set('Padrão')

        logout_icon = customtkinter.CTkImage(Image.open("logout.png"), size=(20,20))
        logout_button = customtkinter.CTkButton(master=toplevel, text='Logout', fg_color='red', corner_radius=100, width=20, height=12, font=("Product Sans Regular", 10), image=logout_icon, command=logout)
        logout_button.place(relx=0.85, rely=0.1, anchor=tkinter.CENTER)

    settings_button = customtkinter.CTkButton(master=app, text='', width=40, height=40, corner_radius=500, font=("Segoe Fluent Icons", 20), command=settings)
    settings_button.place(relx=0.97, rely=0.05, anchor=tkinter.CENTER)

    threading.Thread(target=olt_novo).start()
    threading.Thread(target=olt_doron).start()

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
        print(f'dados: {users}')
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

    img1=customtkinter.CTkImage(Image.open("google.png"), size=(30,30))
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

    login_img = customtkinter.CTkImage(Image.open("arrow_foward.png"), size=(20,20))
    login_button = customtkinter.CTkButton(master=app, image=login_img, text='', width=20, height=40, fg_color='#99bdf6', hover_color='#AFAFAF', corner_radius=500, command=check_credentials)
    login_button.place(relx=0.5, rely=0.66, anchor=tkinter.CENTER)

    version_label = customtkinter.CTkLabel(master=app, text="Versão - beta1.0_aGVhdmVu", font=("Product Sans Regular", 10))
    version_label.place(relx=0.9, rely=0.95, anchor=tkinter.CENTER)

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
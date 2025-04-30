import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, CallbackContext
import asyncio
import nest_asyncio
import google.generativeai as genai
import paramiko
import time
import re
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import threading
from io import BytesIO
import requests
import vertexai
from vertexai.generative_models import GenerativeModel, GenerationConfig, Part
import os
import pathlib

nest_asyncio.apply()

API_TOKEN = 'api-token'
CHAT_ID = 'chat-id'

with open('system_instructions.txt', 'r', encoding='utf-8') as file:
    system_instruction = file.read()

genai.configure(api_key="api-key")
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=system_instruction,
    safety_settings={
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
    }
)

chats = {}

def get_chat(user_id):
    if user_id not in chats:
        chats[user_id] = model.start_chat()
    return chats[user_id]

def search(serial_number, olt):
    olt_dict = {
        'novo_horizonte': 'olt_1',
        'doron': 'olt_2',
        'boca_do_rio': 'olt_3',
        'sussuarana': 'olt_4',
        'brotas': 'olt_5'
    }
    olt = olt_dict[olt]
    url = 'http://100.127.0.250:5000/procurar_onu'
    data = {
            'serial_number': serial_number,
            'olt': olt
            }
    
    response = requests.post(url, json=data)
    return response.text

def deletar(serial_number, olt):
    olt_dict = {
        'novo_horizonte': 'olt_1',
        'doron': 'olt_2',
        'boca_do_rio': 'olt_3',
        'sussuarana': 'olt_4',
        'brotas': 'olt_5'
    }
    olt = olt_dict[olt]
    url = 'http://100.127.0.250:5000/deletar_onu'
    data = {
            'serial_number': serial_number,
            'olt': olt
            }

    response = requests.post(url, json=data)
    return response.text

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def salvar_mensagens(mensagem, nome, user):
    #para cada nome de usuário, cria um arquivo com o nome do usuário e salva as mensagens
    with open(f'chats\\{user}.txt', 'a', encoding='utf-8') as file:
        data_e_hora = time.strftime('%d/%m/%Y %H:%M:%S')
        file.write(f'{data_e_hora} - {nome}: {mensagem}\n')

async def start(update: Update, context):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Bot inicializado no grupo!")

def transcrever_audio(file_path):
    prompt = """
    Transcreva esse áudio, por favor. Se houver mais de uma voz, separe por Locutor A, Locutor B, etc.
    """

    response = model.generate_content([
        prompt,
        {
            "mime_type": "audio/ogg",
            "data": pathlib.Path(file_path).read_bytes()
        }
])
    
    print(response.text)
    
    return response.text

def interpretar_imagem(caminho):
    prompt = """
    Interprete essa imagem e descreva-a detalhadamente.
    """

    response = model.generate_content([
        prompt,
        {
            "mime_type": "image/jpeg",
            "data": pathlib.Path(caminho).read_bytes()
        }
])
    
    print(response.text)
    
    return response.text

    
async def handle_message(update: Update, context: CallbackContext):
    message = update.message
    if update.message.voice or update.message.audio:
        audio_file = await update.message.voice.get_file()
        file_path = f"downloads/{audio_file.file_id}.ogg"
        
        os.makedirs("downloads", exist_ok=True)
        await audio_file.download_to_drive(file_path)
        
        transcription = transcrever_audio(file_path)

        await update.message.reply_text(f"Transcrição do áudio:\n{transcription}")
        os.remove(file_path)
        
    elif message.photo:  # Imagem enviada como foto
        image_file = await message.photo[-1].get_file()  # Maior qualidade
        file_path = f"downloads/{image_file.file_id}.jpg"
        
        os.makedirs("downloads", exist_ok=True)
        await image_file.download_to_drive(file_path)  # Corrigido
        
        try:
            print("Imagem recebida como foto.")
            descricao = interpretar_imagem(file_path)
            await message.reply_text(f"Descrição da imagem:\n{descricao}")
        except Exception as e:
            await message.reply_text("Erro ao interpretar a imagem.")
            print(f"Erro: {e}")
        finally:
            os.remove(file_path)

    elif update.message.document and update.message.document.mime_type.startswith("image/"):  
        # Arquivo de imagem (PNG, BMP, etc.)
        file_id = update.message.document.file_id
        new_file = context.bot.get_file(file_id)
        file_path = update.message.document.file_name  # Mantém nome original
        new_file.download(file_path)
        print(f"Imagem recebida como arquivo: {file_path}")

        descricao = interpretar_imagem(file_path)
        await update.message.reply_text(f"Descrição da imagem:\n{descricao}")
        os.remove(file_path)
    else:

        user_message = update.message
        logger.info(f"Recebendo mensagem: {user_message}")
        nome = user_message.from_user.first_name
        user_message = user_message.text
        salvar_mensagens(user_message, nome , user=nome)

        if user_message == "!help":
            label = model.generate_content("Me fale um pouco sobre quem você é e o que você faz.")
            response = label.text.strip()
            salvar_mensagens(response, "Bot", user=nome)
            await context.bot.send_message(chat_id=update.effective_chat.id, text=response)
        elif user_message == "!comandos":
            i = '''!deletar -  Deleta (desautoriza) uma ONU de uma OLT. Formato: !deletar SERIAL_NUMBER OLT_NAME

    !procurar - Procura um Serial em uma OLT. Formato: !procurar SERIAL_NUMBER OLT_NAME

    !offline - Mostra as ONUs offline de uma OLT. Formato: !offline OLT_NAME

    !online - Mostra as ONUs online de uma OLT. Formato: !online OLT_NAME

    !status - Mostra o status de uma OLT. Formato: !status OLT_NAME
    '''
            await context.bot.send_message(chat_id=update.effective_chat.id, text=i)         
        else:
            label = get_chat(nome).send_message(f'{user_message} + nome: {nome}')
            fun_fact = model.generate_content("Um fato curioso.")
            response = label.text.strip()
            salvar_mensagens(response, "Bot", user=nome)

            logger.info(f"Resultado da classificação: {response}")

            if '!deletar' in response:
                p = response.split()
                serial_number = p[1]
                olt_name = p[-1]
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f'Deletando ONU *{serial_number}* da OLT *{olt_name}*\.\.\.', parse_mode='MarkdownV2')
                r = deletar(serial_number, olt_name)
                if 'sucesso' in r:
                    response = f'ONU *{serial_number}* deletada com sucesso da OLT *{olt_name}*\.'
                else:
                    response = f'Erro ao deletar ONU *{serial_number}* da OLT *{olt_name}*\. Verifique se o serial number e o nome da OLT estão corretos\.'
                await context.bot.send_message(chat_id=update.effective_chat.id, text=response, parse_mode='MarkdownV2') 
            elif '!procurar' in response:
                onu_id = None
                p = response.split()
                serial_number = p[1]
                olt_name = p[-1]
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f'Procurando ONU *{serial_number}* na OLT *{olt_name}*\.\.\.', parse_mode='MarkdownV2')
                r = search(serial_number, olt_name)
                #print(r)
                if 'ONU não encontrada' in r:
                    response = f'ONU *{serial_number}* não encontrada na OLT *{olt_name}*\. Verifique se o serial number e o nome da OLT estão corretos\.'
                elif 'No related information to show' in r:
                    response = f'ONU *{serial_number}* não encontrada na OLT *{olt_name}*\. Verifique se o serial number e o nome da OLT estão corretos\.'
                else:
                    r = r.split('\n')
                    for i in r:
                        print(i)
                        if 'gpon-onu' in i:
                            onu_id = i.split('_')[1]
                        elif 'gpon_onu' in i:
                            onu_id = i.split('-')[1]
                    response = f'ONU *{serial_number}* encontrada na OLT *{olt_name}* com o ID *{onu_id}*\.'
                await context.bot.send_message(chat_id=update.effective_chat.id, text=response, parse_mode='MarkdownV2')
            else:
                #identifica se tem parenteses na resposta e coloca duas barras invertidas antes para não dar erro no markdown
                if '(' in response:
                    response = response.replace('(', '\\(')
                if ')' in response:
                    response = response.replace(')', '\\)')
                if '[' in response:
                    response = response.replace('[', '\\[')
                if ']' in response:
                    response = response.replace(']', '\\]')
                if '{' in response:
                    response = response.replace('{', '\\{')
                if '}' in response:
                    response = response.replace('}', '\\}')
                if '!' in response:
                    response = response.replace('!', '\\!')
                if '#' in response:
                    response = response.replace('#', '\\#')
                if '+' in response:
                    response = response.replace('+', '\\+')
                if '-' in response:
                    response = response.replace('-', '\\-')
                if '.' in response:
                    response = response.replace('.', '\\.')
                if '>' in response:
                    response = response.replace('>', '\\>')
                if '<' in response:
                    response = response.replace('<', '\\<')
                if '=' in response:
                    response = response.replace('=', '\\=')
                if '|' in response:
                    response = response.replace('|', '\\|')
                if '~' in response:
                    response = response.replace('~', '\\~')
                if '`' in response:
                    response = response.replace('`', '\\`')
                if '_' in response:
                    response = response.replace('_', '\\_')
                if ':' in response:
                    response = response.replace(':', '\\:')
                if '/' in response:
                    response = response.replace('/', '\\/')
                if '**' in response:
                    response = response.replace('**', '*')
                response = response + '\n\n' + '_*Este bot ainda está em fase de desenvolvimento\. Ele pode cometer erros\.*_'
                await context.bot.send_message(chat_id=update.effective_chat.id, text=response, parse_mode='MarkdownV2')

async def main():
    application = Application.builder().token(API_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, handle_message))
    await application.run_polling()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    if not loop.is_running():        
        loop.run_until_complete(main())
    else:
        print("O event loop já está em execução.")
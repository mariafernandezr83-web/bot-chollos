import os
import time
import threading
import requests
from bs4 import BeautifulSoup
from flask import Flask
from telegram import Bot, Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# --- 1. Servidor web para mantener activo el bot 24/7 en FadeHost ---
web_app = Flask(__name__)

@web_app.route('/')
def home():
    return "¡El bot de chollos permanente está activo!"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    web_app.run(host="0.0.0.0", port=port)

# --- Configuración del Bot ---
TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "") 

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "¡Hola! Estoy configurado para **buscar chollos de forma permanente** en segundo plano.\n"
        "Te avisaré automáticamente en cuanto encuentre una nueva oferta."
    )

# --- 2. Tarea de búsqueda automática permanente ---
def tarea_busqueda_continua(bot_token, chat_id):
    if not chat_id:
        print("Aviso: No se ha configurado un TELEGRAM_CHAT_ID para las alertas automáticas.")
        return

    bot = Bot(token=bot_token)
    
    while True:
        try:
            print("🔍 Buscando chollos de forma automática...")
            chollo_encontrado = False # Cambiar a True cuando detectes una oferta real
            
            if chollo_encontrado:
                import asyncio
                async def enviar_alerta():
                    await bot.send_message(
                        chat_id=chat_id, 
                        text="🚨 ¡CHOLLO DETECTADO!\n\n¡Se ha encontrado una nueva oferta increíble!"
                    )
                asyncio.run(enviar_alerta())

        except Exception as e:
            print(f"Error en la búsqueda automática: {e}")

        time.sleep(1800) # Espera 30 minutos

if __name__ == "__main__":
    t_web = threading.Thread(target=run_web)
    t_web.daemon = True
    t_web.start()

    if not TOKEN:
        print("Error: Falta configurar el TELEGRAM_TOKEN en las variables de entorno.")
    else:
        if CHAT_ID:
            t_busqueda = threading.Thread(target=tarea_busqueda_continua, args=(TOKEN, CHAT_ID))
            t_busqueda.daemon = True
            t_busqueda.start()

        app = ApplicationBuilder().token(TOKEN).build()
        app.add_handler(CommandHandler("start", start))
        
        print("Bot permanente de chollos iniciado correctamente...")
        app.run_polling()

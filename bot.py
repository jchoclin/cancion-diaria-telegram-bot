from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
#import pandas as pd
from dotenv import load_dotenv
from handlers import today, yesterday, subscribe, unsubscribe, hello, week, send, help, suggestasong
from scheduler import schedule
from database import create_tables, insert_songs_from_google_sheet
import os

load_dotenv()

async def post_init(app):
    insert_songs_from_google_sheet(os.getenv("GOOGLE_SHEET_URL"))
    schedule(insert_songs_from_google_sheet, send, os.getenv("GOOGLE_SHEET_URL"), "America/Argentina/Buenos_Aires", app.bot)

def main(): 
    create_tables()
    app = ApplicationBuilder().token(os.getenv("BOT_TOKEN")).post_init(post_init).build()
    app.bot_data["my_chat_id"] = os.getenv("MY_CHAT_ID")
    app.add_handler(CommandHandler("hola", hello))
    app.add_handler(CommandHandler("start", hello))
    app.add_handler(CommandHandler("ayuda", help))
    app.add_handler(CommandHandler("hoy", today))
    app.add_handler(CommandHandler("ayer", yesterday))
    app.add_handler(CommandHandler("sugerir", suggestasong))
    app.add_handler(CommandHandler("mixsemanal", week))
    app.add_handler(CommandHandler("suscribir", subscribe))
    app.add_handler(CommandHandler("desuscribir", unsubscribe))
                    
    app.run_polling()

if __name__ == "__main__":
    main()

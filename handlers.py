from datetime import datetime, timedelta
from database import get_song_from_date, get_weeks_songs, get_subscribers, to_unsubscribe, add_subscriber
from telegram import Update
from telegram.ext import ContextTypes

async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'holaa {update.effective_user.first_name}! bienvenide al bot de canciones, si queres saber que puedo hacer, tirá /help')

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    comandos = f"/hola - te saluda\n/hoy - te devulve la canción de hoy\n/ayer - te devuelve la canción de ayer\n/mixsemanal - te da las canciones de la última semana\n/sugerir - te deja mandar una sugerencia de canción al bot\n/suscribir - te suscribe para que te llegue un mensaje diario con la canción del día\n/desuscribir - te desuscribe para que no te lleguen más los mensajes diarios\n/ayuda - te devuelve este mensaje espantoso"
    await update.message.reply_text(comandos)


async def today(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    todays_song = get_song_from_date(datetime.today())
    if todays_song is None:
        await update.message.reply_text(f'no hay canción hoy! volvé mañana :)')
    else:
        song = f"la canción de hoy es {todays_song[1]} de {todays_song[2]}, escuchala acá: {todays_song[3]}"
        await update.message.reply_text(song)

async def yesterday(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        yesterday = datetime.today() - timedelta(days=1)
        yesterdays_song = get_song_from_date(yesterday)
        if yesterdays_song is None:
            await update.message.reply_text(f'no encontré la canción de ayer :(')
        else:
            song = f"la canción de ayer fue {yesterdays_song[1]} de {yesterdays_song[2]}, escuchala acá: {yesterdays_song[3]}"
            await update.message.reply_text(song)

async def week(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    today = datetime.today()
    saturday = today - timedelta(days=(today.weekday() - 5) % 7)
    sunday = saturday - timedelta(days=6)
    songs = get_weeks_songs(sunday, saturday)
    if not songs:
        await update.message.reply_text(f'no hay canciones de la semana pasada')
    else:
        mix = ""
        for song in songs:
            mix += f"- {song[1]} by {song[2]}\n"
        thisweek = f"las canciones de la ultima semana fueron:\n" + mix + f" mira la playlist:"
        await update.message.reply_text(thisweek)

async def suggestasong(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args:
        ejemplo = """ ejemplo de uso:
  /sugerir  titulo - artista
"""
        msg = await update.message.reply_text(ejemplo, quote=False)
        return
    user = update.message.from_user
    msg = f"{user.first_name}(@{user.username}): " +  ' '.join(context.args)
    await context.bot.send_message(chat_id=context.bot_data["my_chat_id"], text=msg)
    await update.message.reply_text(f'gracias por la sugerencia! :)')

async def subscribe(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    add_subscriber(update.effective_chat)
    await update.message.reply_text(f'gracias por suscribirte!!!')

async def unsubscribe(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    to_unsubscribe(update.effective_chat)
    await update.message.reply_text(f'ya te desuscribiste! :(')

async def send(bot) -> None:
    todays_song = get_song_from_date(datetime.today())
    subscribers = get_subscribers()
    for sub in subscribers:
        if todays_song is None:
            await bot.send_message(chat_id=sub[0], text=f'no hay canción hoy! volvé mañana :)')
        else:
            song = f"la canción de hoy es {todays_song[1]} de {todays_song[2]}, escuchala acá: {todays_song[3]}"
            await bot.send_message(chat_id=sub[0],text=song)
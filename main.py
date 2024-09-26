from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import re
import sqlalchemy as db


data_storage = {"322": "Это 322"}
data_storage = {"228": "ОПА"}
data_storage = {"666": "КОЙЛ КОЙЛ КОЙЛ"}

async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        f'Здарова, {update.effective_user.first_name}, пиши:\n/get "code" - повторит за тобой\n/set "code" "text" - запись'
    )

async def get(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    code = re.findall(r'"(.*?)"', update.message.text)[0].replace('"',"")
    await update.message.reply_text(
        data_storage[code]
    )

async def get_one_news(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    raw = update.message.text.split(" ")
    id = int(raw[1])
    engine = db.create_engine("mysql+pymysql://root@127.0.0.1/PRIVET2?charset=utf8mb4")
    conn = engine.connect()
    query = db.text(f"SELECT * FROM news1 WHERE id = {id}")
    news = conn.execute(query).fetchall()
    await update.message.reply_text(str(news[0][0])+str("\n\n") +str(news[0][1]))

async def set_one_news(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message_text = update.message.text
    
    
    matches = re.findall(r'"(.*?)"', message_text)

    
    if len(matches) < 2:
        await update.message.reply_text("Ошибка: Братан, ты общаешься не по понятиям, вот как нужно: /set \"code\" \"text\".")
        return
    code = str(matches[0])
    text_value = str(matches[1])

    engine = db.create_engine("mysql+pymysql://root@127.0.0.1/PRIVET2?charset=utf8mb4")


    with engine.connect() as conn:

        query = db.text(f"INSERT INTO news1 (name, description) VALUES('{code}', '{text_value}')")
        conn.execute(query)
        conn.commit()

    await update.message.reply_text("Добавлен!")
    
async def add(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    message_text = update.message.text
    

    matches = re.findall(r'"(.*?)"', message_text)

    if len(matches) < 2:
        await update.message.reply_text("Ошибка: Братан, ты общаешься не по понятиям, вот как нужно: /set \"code\" \"text\".")
        return
    code = matches[0]  
    text = matches[1]  
    data_storage[code] = text
    await update.message.reply_text(f'Код: {code}, Текст: {text}')

app = ApplicationBuilder().token("7766801451:AAHN5Re96mMvZKS9E2ZBcGixfBTI-pJMCOI").build()

app.add_handler(CommandHandler("start", hello))
app.add_handler(CommandHandler("set", add))
app.add_handler(CommandHandler("get", get))
app.add_handler(CommandHandler("getn",get_one_news))
app.add_handler(CommandHandler("setn",set_one_news))

app.run_polling()
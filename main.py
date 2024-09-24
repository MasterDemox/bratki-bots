from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import re


data_storage = {"322": "Это 322"}
data_storage = {"228": "ОПА"}
data_storage = {"666": "ААААААААААА"}

async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        f'Здарова, {update.effective_user.first_name}, пиши:\n/get "code" - повторит за тобой\n/set "code" "text" - запись'
    )

async def get(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    code = re.findall(r'"(.*?)"', update.message.text)[0].replace('"',"")
    await update.message.reply_text(
        data_storage[code]
    )

async def keyboard(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    
    pass

    
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

app.run_polling()
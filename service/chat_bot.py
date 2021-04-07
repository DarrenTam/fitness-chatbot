import datetime
import json
from telegram import ParseMode
from apscheduler.schedulers.background import BackgroundScheduler
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import os
import logging
from database.fitness_service import create_user, get_user_fitness_info, update_weight
from utils.config import ACCESS_TOKEN

global redis1
import boto3


def start_chatbot():
    updater = Updater(token=ACCESS_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    global dynamodb
    dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-1')

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)

    echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    dispatcher.add_handler(echo_handler)

    dispatcher.add_handler(CommandHandler("start", init_user))
    dispatcher.add_handler(CommandHandler("weight_history", get_user_weight_history))
    dispatcher.add_handler(CommandHandler("update_weight", update_user_weight))

    updater.start_polling()
    updater.idle()


def echo(update, context):
    reply_message = "input :/start {age} {sex} {kg} to start your training.  " \
                    "input :/weight_history to get all history  " \
                    "input :/update_weight {kg} to get all history  "
    logging.info("Update: " + str(update))
    logging.info("context: " + str(context))
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply_message,parse_mode=ParseMode.HTML)


def init_user(update: Update, context: CallbackContext) -> None:
    try:
        global dynamodb
        logging.info(context.args[0])
        user_id = update.message.chat.username
        user_info = get_user_fitness_info(user_id, dynamodb=dynamodb)
        if user_info:
            update.message.reply_text("You can't create account more than once.")
            return
        create_user(user_id, context.args[0], context.args[1], context.args[2], dynamodb=dynamodb)
        update.message.reply_text('Account create success')
    except (IndexError, ValueError):
        update.message.reply_text('Usage: /start {age} {sex} {weight}')


def get_user_weight_history(update: Update, context: CallbackContext) -> None:
    try:
        global dynamodb
        user_id = update.message.chat.username
        user_info = get_user_fitness_info(user_id, dynamodb=dynamodb)
        logging.info(user_info)
        if user_info:
            html_table = "|     Date    | Weight | " \
                         "|-------------|--------|  "

            for history in user_info["weightHistory"]:
                html_table += f"|-{history['date']}--|-{history['weight']}kg--|  "
            context.bot.send_message(
                chat_id=update.effective_chat.id, text=f'<pre>{html_table}</pre>',
                parse_mode=ParseMode.HTML
            )
        if not user_info:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Please active your account first by using command /start {age} {sex} {weight}."
            )

    except (IndexError, ValueError):
        update.message.reply_text('Usage: /weight_history')


def update_user_weight(update: Update, context: CallbackContext) -> None:
    try:
        global dynamodb
        user_id = update.message.chat.username
        user_info = get_user_fitness_info(user_id, dynamodb=dynamodb)
        weight = context.args[0]

        if not user_info:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Please active your account first by using command /start {age} {sex} {weight}."
            )

        user_info["weightHistory"].append(
            {
                "weight": weight,

                "date": f"{datetime.datetime.now().strftime('%Y-%m-%d')}"

            }
        )

        weight_history = user_info["weightHistory"]
        update_weight(user_id, weight, weight_history, dynamodb=dynamodb)

        context.bot.send_message(
            chat_id=update.effective_chat.id, text="Update complete."
        )

    except (IndexError, ValueError):
        update.message.reply_text('Usage: /update_weight {weight}')
# def getWeeklyWorkOutSchedule(update: Update, context: CallbackContext) -> None:
#     try:
#         global redis1
#         logging.info(context.args[0])
#         msg = context.args[0]  # /add keyword <-- this should store the keyword
#         redis1.incr(msg)
#         update.message.reply_text('You have said ' + msg + ' for ' + redis1.get(msg).decode('UTF-8') + ' times.')
#     except (IndexError, ValueError):
#         update.message.reply_text('Usage: /add <keyword>')
#
#
# def getTodayWorkOutSchedule(update: Update, context: CallbackContext) -> None:
#     try:
#         global redis1
#         logging.info(context.args[0])
#         msg = context.args[0]  # /add keyword <-- this should store the keyword
#         redis1.incr(msg)
#         update.message.reply_text('You have said ' + msg + ' for ' + redis1.get(msg).decode('UTF-8') + ' times.')
#     except (IndexError, ValueError):
#         update.message.reply_text('Usage: /add <keyword>')
#
#
# def record_wieght(update: Update, context: CallbackContext) -> None:
#     try:
#         global redis1
#         logging.info(context.args[0])
#         msg = context.args[0]  # /add keyword <-- this should store the keyword
#         redis1.incr(msg)
#         update.message.reply_text('You have said ' + msg + ' for ' + redis1.get(msg).decode('UTF-8') + ' times.')
#     except (IndexError, ValueError):
#         update.message.reply_text('Usage: /add <keyword>')
#
#
# def get_wieght_history(update: Update, context: CallbackContext) -> None:
#     try:
#         global redis1
#         logging.info(context.args[0])
#         msg = context.args[0]  # /add keyword <-- this should store the keyword
#         redis1.incr(msg)
#         update.message.reply_text('You have said ' + msg + ' for ' + redis1.get(msg).decode('UTF-8') + ' times.')
#     except (IndexError, ValueError):
#         update.message.reply_text('Usage: /add <keyword>')
#
#
# def calculating_calories(update: Update, context: CallbackContext) -> None:
#     try:
#         global redis1
#         logging.info(context.args[0])
#         msg = context.args[0]  # /add keyword <-- this should store the keyword
#         redis1.incr(msg)
#         update.message.reply_text('You have said ' + msg + ' for ' + redis1.get(msg).decode('UTF-8') + ' times.')
#     except (IndexError, ValueError):
#         update.message.reply_text('Usage: /add <keyword>')

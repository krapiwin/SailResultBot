# -*- coding: utf-8 -*-
import logging
import os

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (CallbackContext, CommandHandler, ConversationHandler,
                          Filters, MessageHandler, Updater)

from regatta import Regatta

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

load_dotenv()
TOKEN = os.getenv('TOKEN')

NEW_NAME, INPUT_RACE, RACE_CREATED = range(3)

memory = {}


def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        'Привет! Я SailResultBot!\n\n'
        'Нажми /help чтобы прочитать подсказку.\n\n'
        'Или /new_regatta чтобы создать новую регату.')


def help(update: Update, context: CallbackContext):
    update.message.reply_text(
        'Привет! Я SailResultBot!\n\n'
        'Нажми /help чтобы прочитать подсказку.\n\n'
        'Или /new_regatta чтобы создать новую регату.\n\n'
        'Каждую гонку нужно вводить в формате "2,3,1,5,4", '
        'где цифры это номера лодок, '
        'а их порядок соответсвует месту на финише. '
        'Чтобы добавить лодке наказание (dnf, ocs, dsq), '
        'напишите его через "-".\nНапример: 2,3-dsq,1,5,4\n\n'
        'Когда закончите добавлять результаты - нажмите /show_results')


def new_regatta(update: Update, context: CallbackContext):
    user = update.message.from_user
    regatta = Regatta()
    memory[user.id] = {'regatta': regatta}
    update.message.reply_text(
        'Вы создали новую регату. Как назовёте?\n\n'
        'Чтобы пропустить, нажмите /skip'
    )
    return NEW_NAME


def new_name(update: Update, context: CallbackContext):
    user = update.message.from_user
    regatta = memory[user.id]['regatta']
    name = update.message.text
    regatta.name = name
    update.message.reply_text(
        'Красивое имя!\n'
        'Можно вводить приходы первой гонки!'
    )
    return INPUT_RACE


def skip_name(update: Update, context: CallbackContext):
    update.message.reply_text(
        'И без названия сойдёт!\n'
        'Можно вводить приходы первой гонки!'
    )
    return INPUT_RACE


def input_race(update: Update, context: CallbackContext):
    user = update.message.from_user
    regatta = memory[user.id]['regatta']
    race = update.message.text
    regatta.create_race(race)
    update.message.reply_text(
        'Записали!\n\n'
        'Нажмите /new_race чтобы записать еще одну гонку '
        'или /show_results чтобы посмотреть результаты.'
    )
    return RACE_CREATED


def text_for_input(update: Update, context: CallbackContext):
    update.message.reply_text(
        'Введите приходы этой гонки:'
    )
    return INPUT_RACE


def show_results(update: Update, context: CallbackContext):
    user = update.message.from_user
    regatta = memory[user.id]['regatta']
    results = regatta.create_results()
    results_str = (list(map(str, results)))
    m = ''
    if regatta.name:
        m = (f'{regatta.name}\n')
    i = 0
    for res in results_str:
        i += 1
        m += (f'{i}. {res}\n')
    update.message.reply_text(m)
    update.message.reply_text('Чтобы записать еще гонку нажмите /new_race')
    return RACE_CREATED


def cancel(update: Update, context: CallbackContext):
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    memory[user] = {}
    update.message.reply_text(
        'До скорых встреч!'
    )
    return ConversationHandler.END


def main():
    """Run the bot."""
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('new_regatta', new_regatta)],
        states={
            NEW_NAME: [
                CommandHandler('skip', skip_name),
                MessageHandler(Filters.text, new_name)],
            INPUT_RACE: [MessageHandler(Filters.text, input_race)],
            RACE_CREATED: [
                CommandHandler('new_race', text_for_input),
                CommandHandler('show_results', show_results)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    start_handler = CommandHandler('start', start)
    help_handler = CommandHandler('help', help)

    dispatcher.add_handler(conv_handler)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(help_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()

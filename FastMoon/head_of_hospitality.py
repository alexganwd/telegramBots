#owner: Alex Gandara
#contact: alex@alexgan.net
#linkedin: https://www.linkedin.com/in/alejandrogandaraalvarez/

from telegram.ext import Updater, MessageHandler, Filters
import telegram
import logging
import secrets
import json
import re
#Defaulting to basic logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
def get_static_answers():
    regex_by_alias_dict = dict()
    with open('static_answers.json') as static_answers_json_file:
        static_answers = json.load(static_answers_json_file)
        return static_answers
        #Let's flat out the alias so we can search more efficiently

#We don't want to read a file for every message
static_answers = get_static_answers ()

def find_text_by_alias(text):
    for static_answer in static_answers:
        for pattern in static_answer['patterns']:
            if re.search(pattern, text, re.IGNORECASE):
                return static_answer['text']
    return 404

def reload(update, context):
    print(f'Reloading static answers')
    context.bot.send_message(chat_id=update.message.chat.id, text='reloading static answers')

def automatic_static_replies(update, context):
    text_msg = find_text_by_alias(update.message.text)
    if update.message.forward_from_chat:
        pass
    elif text_msg != 404:
        context.bot.send_message(chat_id=update.effective_chat.id, text=text_msg, reply_to_message_id=update.message.message_id,parse_mode=telegram.ParseMode.HTML)

def main():
    updater = Updater(token=secrets.get_prod_token(), use_context=True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.text, automatic_static_replies))


    #Polling al servidor de telegram
    updater.start_polling(drop_pending_updates=True)
    updater.idle()

if __name__ == '__main__':
    main()
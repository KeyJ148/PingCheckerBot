import telebot
import os
import traceback


class TelegramBot:
    def __init__(self, get_state_func, new_subscriber_listener):
        self.TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
        self.TELEGRAM_MESSAGE_HELLO = os.environ.get('TELEGRAM_MESSAGE_HELLO')
        self.TELEGRAM_MESSAGE_ONLINE = os.environ.get('TELEGRAM_MESSAGE_ONLINE')
        self.TELEGRAM_MESSAGE_OFFLINE = os.environ.get('TELEGRAM_MESSAGE_OFFLINE')
        self.get_state_func = get_state_func
        self.new_subscriber_listener = new_subscriber_listener

        self.bot = telebot.TeleBot(self.TELEGRAM_TOKEN)

        self.bot.message_handler(commands=['start'])(self.start_handler)

    def start_handler(self, message):
        print(f"[TelegramBot.start_handler] Request: {str(message)}")
        self.new_subscriber_listener(message.chat.id)
        self.send_message(message.chat.id, self.TELEGRAM_MESSAGE_HELLO)
        self.send_current_state(message.chat.id)

    def send_current_state(self, chat_id):
        message = self.TELEGRAM_MESSAGE_ONLINE if self.get_state_func() else self.TELEGRAM_MESSAGE_OFFLINE
        self.send_message(chat_id, message)

    def send_message(self, chat_id, text):
        print(f"[TelegramBot.send_message] Response: chat_id={chat_id}, text={text}")
        self.bot.send_message(chat_id, text=text, parse_mode="Markdown", disable_web_page_preview=True)

    def start(self):
        print("[TelegramBot.start] Start...")
        while True:
            try:
                print("[TelegramBot.start] Polling...")
                self.bot.polling(none_stop=True, interval=0)
            except Exception as e:
                print("[TelegramBot.start] Error while polling: " + str(e))
                traceback.print_exc()

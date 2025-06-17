import threading

from telegram import TelegramBot
from user_manager import UserManager
from host_monitor import HostMonitor

class PingCheckerBot:
    def __init__(self):
        self.telegram_bot = TelegramBot(self.__get_current_state, self.__new_subscriber_listener)
        self.user_manager = UserManager()
        self.host_monitor = HostMonitor(self.__state_listener)

    def start(self):
        threading.Thread(target=self.telegram_bot.start).start()
        threading.Thread(target=self.host_monitor.start).start()

    def __get_current_state(self):
        return self.host_monitor.get_state()

    def __new_subscriber_listener(self, chat_id):
        self.user_manager.add_user(chat_id)

    def __state_listener(self, new_state):
        for user_id in self.user_manager.get_all_users():
            self.telegram_bot.send_current_state(user_id)


ping_checker_bot = PingCheckerBot()
ping_checker_bot.start()
import json
import os


class UserManager:
    def __init__(self):
        self.filepath = os.environ.get('USERS_FILE')

    def __save_users(self, users):
        with open(self.filepath, "w") as file:
            json.dump(users, file)

    def get_all_users(self):
        if not os.path.exists(self.filepath):
            return []
        with open(self.filepath, "r") as file:
            return json.load(file)

    def add_user(self, user_id):
        print(f"[UserManager.add_user] Add new user: {user_id}")
        users = self.get_all_users()
        if user_id not in users:
            users.append(user_id)
            self.__save_users(users)
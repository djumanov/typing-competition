from tinydb import TinyDB


class DB:
    def __init__(self, file_name: str):
        self.db         = TinyDB(file_name, indent=4)
        self.temp_users = self.db.table('temp_users')
        self.users      = self.db.table('users')
        self.stages    = self.db.table('stages')
        self.results    = self.db.table('results')

    def is_user(self, chat_id: str): 
        return self.users.contains(chat_id=chat_id)

    # def add_temp_user(self, chat_id, )
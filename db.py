from tinydb import TinyDB, Query
from tinydb.table import Document


class DB:
    def __init__(self, file_name: str):
        self.db = TinyDB(file_name, indent=4)
        self.temp_users = self.db.table('temp_users')
        self.users = self.db.table('users')
        # self.stages = self.db.table('stages')
        self.results = self.db.table('results')

    def add_or_update_temp_user(self, chat_id, first_name=None, last_name=None, group=None):
        user = self.temp_users.get(doc_id=chat_id)
        if user is None:
            user = Document(
                value={
                    "chat_id": chat_id,
                    'step': 'first_name'
                },
                doc_id=chat_id
            )
            self.temp_users.insert(user)
            return user['step']

        if first_name is not None:
            user['first_name'] = first_name
            user['step'] = 'last_name'
        elif last_name is not None:
            user['last_name'] = last_name
            user['step'] = 'group'
        elif group is not None:
            user['group'] = group
            user['step'] = 'finnal'

        self.temp_users.upsert(user)
        return user['step']

    def get_temp_user(self, chat_id):
        return self.temp_users.get(doc_id=chat_id)

    def is_temp_user(self, chat_id):
        return self.temp_users.contains(doc_id=chat_id)

    def delete_temp_user(self, chat_id):
        return self.temp_users.remove(doc_ids=[chat_id])    

    def clear_temp_user(self, chat_id):
        user = Document(
            value={
                'step': 'first_name'
            },
            doc_id=chat_id
        )
        self.temp_users.upsert(user)

    def is_user(self, chat_id):
        return self.users.contains(doc_id=chat_id)

    def add_user(self, chat_id):
        if self.is_user(chat_id=chat_id):
            return
        user = self.get_temp_user(chat_id=chat_id)
        if user and user['step'] == 'finnal':
            self.users.insert(user)
            print(chat_id)
            self.delete_temp_user(chat_id=chat_id)
            return True
        else:
            return False

    # def add_stage(self, doc_id, name):
    #     Stage = Query()
    #     stage_data = {
    #         "name": name,
    #     }

    #     if not self.stages.get(Stage.name == name):
    #         self.stages.insert(stage_data)

    def add_result(self, chat_id, first_name, last_name, group, wpm, accuracy, consistency, date):
        result_data = Document(
            value={
                "firt_name": first_name,
                "last_name": last_name,
                "group": group,
                "wpm": wpm,
                "accuracy": accuracy,
                "consistency": consistency,
                "date": date,
            },
            doc_id=chat_id
        )

        if not self.results.contains(doc_id=chat_id):
            self.results.insert(result_data)
            return True

        return False

    def get_all_results(self):
        return self.results.all()

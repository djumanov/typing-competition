from dotenv import load_dotenv
import os

def get_token():
    load_dotenv()
    token = os.environ.get('BOT_TOKEN')

    return token

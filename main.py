import csv
from os import environ
from deepl import Translator
from dotenv import load_dotenv

load_dotenv()
FILE = "data/test_data.csv"


def translate(text: str):
    """Translate text with the deepL-API"""

    auth_key = environ.get('AUTH_KEY')

    translator = Translator(auth_key=auth_key)
    result = translator.translate_text(text=text, target_lang="DE")
    result_clean = result.replace(',', '')

    return result_clean



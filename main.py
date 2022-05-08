from os import environ
from deepl import Translator
from dotenv import load_dotenv

load_dotenv()

auth_key = environ.get('AUTH_KEY')

translator = Translator(auth_key=auth_key)

result = translator.translate_text("Hello World!", target_lang="DE")

print(result)

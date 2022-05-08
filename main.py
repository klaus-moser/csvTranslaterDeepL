import csv
from os import environ
from os.path import join, exists
from deepl import Translator
from dotenv import load_dotenv

load_dotenv()


def translate(text: str):
    """Translate text with the deepL-API."""

    auth_key = environ.get('AUTH_KEY')

    translator = Translator(auth_key=auth_key)
    result = translator.translate_text(text=text, target_lang="DE")
    result_clean = result.replace(',', '')

    return result_clean


class TranslateCsv:
    """Super Class."""

    def __init__(self, file):
        self.FILE_IN = self.check_file(file=file)
        self.FILE_OUT = self.new_file_path()
        self.headers = None

    @staticmethod
    def check_file(file):
        """Check if file exists & is a .csv."""

        if not exists(file) or not file.endswith('.csv'):
            print("File not found / no .csv!")
            exit()
        else:
            return file

    def new_file_path(self):
        """Creates a new file path for the translated file."""

        temp = self.FILE_IN.split('.')
        return join(temp[0] + '_translated.csv')

    def edit_csv(self):
        with open(file=self.FILE_IN, mode='r', encoding='utf-8') as r, open(file=self.FILE_OUT, mode='w', encoding='utf-8') as w:
            r_csv = csv.reader(r)
            w_csv = csv.writer(w)

            if self.headers is None:
                self.headers = next(r_csv)

            w_csv.writerow(self.headers)

            for row in r_csv:
                w_csv.writerow(row)


if __name__ == "__main__":
    FILE = "data/test_data.csv"
    c = TranslateCsv(FILE)
    c.edit_csv()


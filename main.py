import csv
from os import environ
from os.path import join, exists
from deepl import Translator
from dotenv import load_dotenv

load_dotenv()


class TranslateCsv:
    """Super Class."""

    def __init__(self, file):
        self.FILE_IN = self.check_file(file=file)
        self.FILE_OUT = self.new_file_path()
        self.auth_key = environ.get('AUTH_KEY')
        self.translator = self.create_translator()
        self.headers = None
        self.text = None
        self.text_translated = None

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

    def create_translator(self):
        """Create a translator object."""

        try:
            return Translator(auth_key=self.auth_key)
        except Exception as e:
            print(e)
            exit()

    def translate_text(self):
        """Translate text with the deepL-API."""

        result = self.translator.translate_text(text=self.text, target_lang="DE")
        result_clean = result.text.replace(',', '')

        self.text_translated = result_clean

    def translate_csv(self):
        """Open .csv and translate line by line."""

        with open(file=self.FILE_IN, mode='r', encoding='utf-8') as r,\
                open(file=self.FILE_OUT, mode='w', newline='', encoding='utf-8') as w:
            r_csv = csv.reader(r)
            w_csv = csv.writer(w)

            if self.headers is None:
                self.headers = next(r_csv)

            w_csv.writerow(self.headers)

            for row in r_csv:
                if self.deepl_limit_exceeded():
                    break

                temp = row[1:]
                self.text = ' '.join(temp)
                self.translate_text()
                row[1] = self.text_translated
                w_csv.writerow(row)

    def deepl_limit_exceeded(self):
        """Check deepl account for its limit."""

        usage = self.translator.get_usage()
        if usage.character.limit_exceeded:
            return True
        else:
            return False


if __name__ == "__main__":
    FILE = "data/test_data.csv"
    c = TranslateCsv(FILE)
    #c.translate_csv()
    print(c.deepl_limit_exceeded())


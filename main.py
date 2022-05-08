import csv
from os import environ, getcwd
from os.path import join, exists

import deepl.exceptions
from deepl import Translator
from dotenv import load_dotenv
from tqdm import tqdm
from tkinter import Tk, filedialog

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
        try:
            result = self.translator.translate_text(text=self.text, target_lang="DE")
            result_clean = result.text.replace(',', '')
            self.text_translated = result_clean

        except deepl.exceptions.QuotaExceededException as e:
            print("Limit exceeded!")
            return False

    def translate_csv(self):
        """Open .csv and translate line by line."""

        with open(file=self.FILE_IN, mode='r', encoding='utf-8') as r,\
                open(file=self.FILE_OUT, mode='w', newline='', encoding='utf-8') as w:
            r_csv = csv.reader(r)
            w_csv = csv.writer(w)

            if self.headers is None:
                self.headers = next(r_csv)

            w_csv.writerow(self.headers)

            for row in tqdm(r_csv):
                temp = row[1:]
                self.text = ' '.join(temp)
                if not self.translate_text():
                    break
                row = [row[0], self.text_translated]
                w_csv.writerow(row)

    def deepl_limit_exceeded(self):
        """Check deepl account for its limit."""

        usage = self.translator.get_usage()
        if usage.character.limit_exceeded:
            return True
        else:
            return False

    def print_limit(self):
        """Print deepL limits."""

        usage = self.translator.get_usage()
        print("Usage:", usage.character)


if __name__ == "__main__":
    print("\n" + 10*"* " + "CSV-Translator" + 10*" *" + "\n")

    root = Tk()
    root.withdraw()
    FILE = filedialog.askopenfilename(filetypes=(("csv files", "*.csv"), ("csv files", "*.CSV")),
                                      parent=root,
                                      initialdir=getcwd(),
                                      title='Choose .csv:')

    c = TranslateCsv(FILE)
    c.print_limit()
    c.translate_csv()

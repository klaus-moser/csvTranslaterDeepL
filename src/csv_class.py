# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import csv
import deepl.exceptions
from os import environ
from os.path import join, exists
from deepl import Translator, exceptions
from tqdm import tqdm
from exceptions import TranslationException
from googletrans import Translator


class TranslateCsv:
    """CSV Translator class."""

    def __init__(self, file, type_='google', src='en', dest='de'):
        self.FILE_IN = self.check_file(file=file)
        self.FILE_OUT = self.new_file_path()
        self.type = type_
        self.translator = self.create_translator()
        self.headers = None
        self.text = None
        self.text_translated = None
        self.limit = 0
        self.src_lang = src
        self.dst_lang = dest

    @staticmethod
    def check_file(file):
        """Check if file exists & is a .csv."""

        if exists(file) and file.endswith('.csv'):
            return file
        else:
            exit("File not found / no .csv!")

    def new_file_path(self):
        """Creates a new file path for the translated file."""

        temp = self.FILE_IN.split('.')
        return join(temp[0] + '_translated.csv')

    def create_translator(self):
        """Create a translator object."""

        if self.type == 'google':
            return Translator()

        else:
            try:
                return Translator(auth_key=environ.get('AUTH_KEY'))

            except deepl.exceptions.AuthorizationException as e:
                exit("Authorization failed!")

    def translate_text(self):
        """Translate text with the deepL-API."""

        if self.type == 'google':
            try:
                self.text_translated = self.translator.translate(text=self.text,
                                                                 src=self.src_lang.lower(),
                                                                 dest=self.dst_lang.lower()).text

            except Exception as e:
                return False
        else:
            try:
                self.text_translated = self.translator.translate_text(text=self.text,
                                                                      source_lang=self.src_lang.upper(),
                                                                      target_lang=self.dst_lang.upper())

            except exceptions.QuotaExceededException as e:
                print("Limit exceeded!")
                return False
        return True

    def clean_text(self, letter=','):
        """Remove chosen letters."""

        self.text_translated = self.text_translated.replace(letter, '')

    def translate_csv(self):
        """Open .csv and translate line by line."""

        with open(file=self.FILE_IN, mode='r', encoding='utf-8') as r, \
                open(file=self.FILE_OUT, mode='w', newline='', encoding='utf-8') as w:
            r_csv = csv.reader(r)
            w_csv = csv.writer(w)

            if self.headers is None:
                self.headers = next(r_csv)

            w_csv.writerow(self.headers)

            try:
                for row in tqdm(r_csv):
                    temp = []
                    for column in row:
                        self.text = column

                        if not self.translate_text():
                            raise TranslationException
                        self.clean_text()
                        temp.append(self.text_translated)
                    w_csv.writerow(temp)

            except TranslationException:
                pass

    def check_limit(self):
        """Check deepl account for its limit."""

        usage = self.translator.get_usage()
        if usage.character.limit_exceeded:
            exit(f"Character limit already reached: {usage.character}")

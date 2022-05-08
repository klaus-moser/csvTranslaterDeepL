# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


""" CSV-Translator with deepl.com """


__version__ = "1.0"
__author__ = "github.com/klaus-moser"


from csv_class import TranslateCsv
from os import getcwd
from dotenv import load_dotenv
from tkinter import Tk, filedialog


load_dotenv()   # Load .env environment variables


def main(file):
    """Main app."""

    print("\n" + 10 * "*" + " CSV-Translator " + 10 * "*" + "\n")
    translator = TranslateCsv(file=file)
    translator.translate_csv()


if __name__ == "__main__":
    root = Tk()
    root.withdraw()
    FILE = filedialog.askopenfilename(filetypes=(("csv files", "*.csv"), ("csv files", "*.CSV")),
                                      parent=root,
                                      initialdir=getcwd(),
                                      title='Choose .csv:')
    main(FILE)


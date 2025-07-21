from pathlib import Path
from textwrap import dedent

from PIL import Image
import pytesseract

IMAGES = Path(__file__).parent / 'ocr_test_images'

pytesseract.pytesseract.tesseract_cmd = r'c:\Program Files\Tesseract-OCR\tesseract.exe'

def test_tesseract():
    text = pytesseract.image_to_string(Image.open(str(IMAGES / 'test_tess.png')))
    assert dedent("""\
                This is a lot of 12 point text to test the
                ocr code and see if it works on all types
                of file format.""") in text
    
def test_dataview_scrape():
    
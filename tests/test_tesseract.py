from pathlib import Path
from textwrap import dedent

from PIL import Image
from pyscreeze import _locateAll_pillow
import pytesseract

IMAGES = Path(__file__).parent / 'ocr_test_images'

pytesseract.pytesseract.tesseract_cmd = r'c:\Program Files\Tesseract-OCR\tesseract.exe'

def test_tesseract():
    text = pytesseract.image_to_string(Image.open(str(IMAGES / 'test_tess.png')))
    assert dedent("""\
                This is a lot of 12 point text to test the
                ocr code and see if it works on all types
                of file format.""") in text

def test_tesseract_on_dataview_rows():
    int_line_image = Image.open(str(IMAGES / 'dataview_line_int.png'))
    size = int_line_image.size
    large = int_line_image.resize((size[0]*2, size[1]*2))
    text = pytesseract.image_to_string(large)
    assert "Drive_MainWheel_Write.RunFrequency" in text
    assert "15" in text

    bool_line_image = Image.open(str(IMAGES / 'dataview_line_bool.png'))
    size = bool_line_image.size
    large = bool_line_image.resize((size[0]*2, size[1]*2))
    text = pytesseract.image_to_string(large)
    assert "Drive_MainWheel_Write. Timeout" in text
    filled_boxes = _locateAll_pillow(str(IMAGES / "checkbox_checked.png"), str(IMAGES / 'dataview_line_bool.png'))
    assert list(filled_boxes)

    bool_line_image = Image.open(str(IMAGES / 'dataview_line_bool_unchecked.png'))
    size = bool_line_image.size
    large = bool_line_image.resize((size[0]*2, size[1]*2))
    text = pytesseract.image_to_string(large)
    assert "Drive_MainWheel_Write.Error" in text
    filled_boxes = _locateAll_pillow(str(IMAGES / "checkbox_empty.png"), str(IMAGES / 'dataview_line_bool_unchecked.png'))
    assert list(filled_boxes)

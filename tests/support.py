from pathlib import Path
from textwrap import dedent

from PIL import Image
from pyscreeze import _locateAll_pillow
import pytesseract

IMAGES = Path(__file__).parent / 'ocr_test_images'

pytesseract.pytesseract.tesseract_cmd = r'c:\Program Files\Tesseract-OCR\tesseract.exe'

def assert_image_contains_text(path: Path | str, text: str, resize = 1):
    text = text.strip().replace(" ", "")
    image = Image.open(str(path))
    if resize != 1:
        size = image.size
        image = image.resize((size[0]*resize, size[1]*resize))
    ocr_text = pytesseract.image_to_string(image)
    assert dedent(text) in ocr_text.strip().replace(" ", "")

def assert_image_contains_image(haystack_image: Path | str, needle_image: Path):
        assert list(_locateAll_pillow(str(needle_image), str(haystack_image)))
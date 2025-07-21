import csv
from pathlib import Path
from textwrap import dedent
import os
import uuid
from typing import Generator

from PIL import Image
from pyscreeze import _locateAll_pillow, locate
import pytesseract
import pyautogui

IMAGES = Path(__file__).parent / 'ocr_test_images'

pytesseract.pytesseract.tesseract_cmd = r'c:\Program Files\Tesseract-OCR\tesseract.exe'
WORDS_PATH = Path(__file__).parent / 'words.txt'
CSV_PATH = Path(__file__).parent.parent / "727_ladder_Basic.csv"

class NoMatchingImageException(pyautogui.ImageNotFoundException):
    def __init__(self, *args: object) -> None:
        img = args[0]
        name = args[1] if len(args) > 1 else None
        msg = f"Could not find {name if name else 'pixels matching ' + str(img)} on primary monitor {f"({str(img)})" if name else ""}"
        super().__init__(msg)

def normalize_tag_name(tagname: str | None) -> str | None:
    #TODO make this better
    if not tagname: return tagname
    return (tagname.strip(" |_\n")
            .replace(" ", "")
            .replace("|", "")
            .replace("\n", "")
        )

def generate_user_words_from_file(file) -> Generator[str]:
    with open(file, "r") as f:
        lines = [line for line in f if not line.startswith("## 2.0")]
    for line in csv.DictReader(lines):
        try:
            yield line['Tag Name']
        except IndexError as err:
            print(line)
            raise err

def dump_user_words_to_file(data_file: str | Path = CSV_PATH, outfile = WORDS_PATH):
    with open (outfile, "w") as f:
        for line in generate_user_words_from_file(data_file):
            f.write(line + "\n")

def robust_image_to_string(img: Path | str | Image.Image, left_steps = 10, resize = 1, use_words = False, dump = False) -> str | None:
    if not isinstance(img, Image.Image):
        img = Image.open(str(img))

    
    if resize != 1:
        size = img.size
        img = img.resize((size[0]*resize, size[1]*resize), Image.Resampling.LANCZOS)
    
    for _ in range(left_steps):
        if text := pytesseract.image_to_string(img, config='--psm 7 --oem 3' +  f' --user-words {WORDS_PATH.absolute()}' if use_words else ''): return text
        img = img.crop((.1, 0, img.width, img.height))
    if dump: img.save(f".out/{uuid.uuid4()}.png")
    return None



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



def get_data_from_dataview(img: Path | str | Image.Image) -> dict[str, int | str | None]:
    """Feed an image of the whole dataview window, extract data

    Args:
        path (Path | str | Image): The file path to the dataview screenshot, or an image file in memeory

    Returns:
        dict[str, int]: Tag:Value pairs
    """
    dump_user_words_to_file()
    ## TODO remove this when it's no longer needed for debugging
    debug_path = IMAGES.parent.parent / ".out"
    if os.path.isdir(debug_path):
        for filename in os.listdir(debug_path):
            file_path = os.path.join(debug_path, filename)
            if os.path.isfile(file_path):
                try:
                    os.remove(file_path)
                except OSError as e:
                    print(f"Error deleting {file_path}: {e}")

    if not isinstance(img, Image.Image):
         img = Image.open(str(img))
   
    # Find the "Tagname" text on screen
    tagname_header = locate(str(IMAGES / "tagname.png"), img)
    assert tagname_header

    TOP_OF_ROWS = tagname_header.top + 16
    ROW_LEFT = tagname_header.left + 15
    ROW_RIGHT = ROW_LEFT + 201
    ROW_HEIGHT = 16
    ROW_HEIGHT_PAD = 3

    VALUE_LEFT = ROW_LEFT + 308
    VALUE_RIGHT = VALUE_LEFT + 57

    values: dict[str, int | str | None] = {}

    row_index = 0
    while True:
        row_top = TOP_OF_ROWS + row_index * ROW_HEIGHT
        tagname_image = img.crop((ROW_LEFT, row_top, ROW_RIGHT, row_top + ROW_HEIGHT + ROW_HEIGHT_PAD))
        tagname = normalize_tag_name(robust_image_to_string(tagname_image, resize=3, use_words=True, dump=True))
        if not tagname:
            tagname_image.save(".out/first_failed_tagname_lookup.png")
            break

        value_image = img.crop((VALUE_LEFT, row_top, VALUE_RIGHT, row_top + ROW_HEIGHT + ROW_HEIGHT_PAD))

        unchecked_box = locate(str(IMAGES / "checkbox_empty.png"), value_image)
        checked_box = locate(str(IMAGES / "checkbox_checked.png"), value_image)

        if checked_box and not unchecked_box: value = 1
        elif unchecked_box and not checked_box: value = 0
        elif checked_box and unchecked_box: raise ValueError(f"Box for tagname {tagname} was detected as both checked and not checked")
        else:
            value = robust_image_to_string(value_image, resize=4, left_steps=1)
            print(f"Initial OCR: {tagname!r}:{value}")

        values[tagname] = value
        row_index += 1
        
    return values
    

    # Derive the location of the tag names
    # Scan down until there are none left on screen
    # Scroll down if there are more??
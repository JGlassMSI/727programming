import csv
from itertools import chain
from pathlib import Path
from textwrap import dedent
import os
import uuid
from typing import Generator

from PIL import Image, ImageOps
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
    return (tagname.strip(" |\n").rstrip("_")
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

def robust_image_to_string(img: Path | str | Image.Image, left_steps=1, resize = 1, use_words = False, dump = False) -> str | None:
    if not isinstance(img, Image.Image):
        img = Image.open(str(img))

    # TODO This is the experiemntal filters section
    thresh = 127
    fn = lambda x : 255 if x > thresh else 0
    img = img.convert("L")
    if resize != 1:
        size = img.size
        resized_image = img.resize((size[0]*resize, size[1]*resize), Image.Resampling.LANCZOS)
    else:
        resized_image = img
    
    for _ in range(left_steps):
        if text := pytesseract.image_to_string(resized_image, config='--psm 7 --oem 3 ' +  f' --user-words {WORDS_PATH.absolute()} -c load_system_dawg=F -c load_freq_dawg=F' if use_words else ''): return text
        resized_image = resized_image.crop((.1, 0, resized_image.width, resized_image.height))

    #If OCR fails, try looking up by pre-saved image in original image
    for obj in chain(os.listdir(IMAGES / "tagname_images"), os.listdir(IMAGES / "value_images")):
        full_path = str(IMAGES / "tagname_images" / obj)
        if os.path.isfile(full_path):
            match_image = Image.open(full_path)
            #print(f"{match_image.size=} {img.size=}")
            if all(match_image.size[i] <= img.size[i] for i in (0, 1)):
                print(f"Checking {full_path} in image")
                if locate(full_path, img):
                    print(f"Found in image for {Path(full_path).stem}!")
                    return Path(full_path).stem

    if dump: resized_image.save(f".out/{uuid.uuid4()}.png")
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

    VALUE_LEFT = ROW_LEFT + 313
    VALUE_RIGHT = VALUE_LEFT + 57

    values: dict[str, int | str | None] = {}

    row_index = 0
    while True:
        row_top = TOP_OF_ROWS + row_index * ROW_HEIGHT
        tagname_image = img.crop((ROW_LEFT, row_top, ROW_RIGHT, row_top + ROW_HEIGHT + ROW_HEIGHT_PAD))
        tagname = normalize_tag_name(robust_image_to_string(tagname_image, resize=3, use_words=True))
        if not tagname:
            tagname_image.save(".out/first_failed_tagname_lookup.png")
            break
        if row_index > 30: break #DEBUG

        value_image = img.crop((VALUE_LEFT, row_top, VALUE_RIGHT, row_top + ROW_HEIGHT + ROW_HEIGHT_PAD))

        unchecked_box = locate(str(IMAGES / "checkbox_empty.png"), value_image)
        checked_box = locate(str(IMAGES / "checkbox_checked.png"), value_image)

        if checked_box and not unchecked_box: value = True
        elif unchecked_box and not checked_box: value = False
        elif checked_box and unchecked_box: raise ValueError(f"Box for tagname {tagname} was detected as both checked and not checked")
        else:
            value = robust_image_to_string(value_image, resize=3, left_steps=5, dump=True)

        _og_value = value
        try:
            value = int(str(value).strip())
        except ValueError as err:
            value = _og_value
        values[tagname] = value
        row_index += 1
        
    return values
    

    # Derive the location of the tag names
    # Scan down until there are none left on screen
    # Scroll down if there are more??
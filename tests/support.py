import csv
from functools import cache
from pathlib import Path

from pyscreeze import _locateAll_pillow, locate
import pyautogui

CSV_BASIC_PATH = Path(__file__).parent.parent / "727_ladder_Basic.csv"

class NoMatchingImageException(pyautogui.ImageNotFoundException):
    def __init__(self, *args: object) -> None:
        img = args[0]
        name = args[1] if len(args) > 1 else None
        msg = f"Could not find {name if name else 'pixels matching ' + str(img)} on primary monitor {f"({str(img)})" if name else ""}"
        super().__init__(msg)

def assert_image_contains_image(haystack_image: Path | str, needle_image: Path):
        assert list(_locateAll_pillow(str(needle_image), str(haystack_image)))

@cache
def get_tag_info_from_file(file = CSV_BASIC_PATH) -> dict[str, dict[str, str]]:
    values = {}
    with open(file, "r") as lines:
        for line in csv.DictReader(lines):
            if name := line.get("Tag Name"):
                if name in values:
                     raise ValueError(f"Tag Name {name} already present in tag info.")
                values[name] = line
    return values
from pathlib import Path

from pyscreeze import _locateAll_pillow, locate
import pyautogui

class NoMatchingImageException(pyautogui.ImageNotFoundException):
    def __init__(self, *args: object) -> None:
        img = args[0]
        name = args[1] if len(args) > 1 else None
        msg = f"Could not find {name if name else 'pixels matching ' + str(img)} on primary monitor {f"({str(img)})" if name else ""}"
        super().__init__(msg)

def assert_image_contains_image(haystack_image: Path | str, needle_image: Path):
        assert list(_locateAll_pillow(str(needle_image), str(haystack_image)))


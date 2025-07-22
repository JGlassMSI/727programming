from contextlib import contextmanager
from pathlib import Path
from typing import Sequence

import pyautogui


IMAGES = Path(__file__).parent / 'testbasic_images'

class NoMatchingImageException(pyautogui.ImageNotFoundException):
    def __init__(self, *args: object) -> None:
        img = args[0]
        name = args[1] if len(args) > 1 else None
        msg = f"Could not find {name if name else 'pixels matching ' + str(img)} on primary monitor {f"({str(img)})" if name else ""}"
        super().__init__(msg)


def get_location(img: Path | str | Sequence[Path | str], name = None, center = True):
    """Get the location onscreen of the center of an image

    Args:
        img (Path | str | | Sequence[Path | str]): Path to the screenshot
        name (_type_, optional): Descriptive name to print in case the image can't be found

    Raises:
        NoMatchingImageException

    Returns:
        pyautogui.POINT: The center of the image if found
    """
    if isinstance(img, Path) or isinstance (img, str):
        try:
            if center: loc = pyautogui.locateCenterOnScreen(str(img))
            else: loc = pyautogui.locateOnScreen(str(img))
        except pyautogui.ImageNotFoundException as err:
            raise NoMatchingImageException(img, name) from err
        return loc
    else:
        if images := iter(img):
            for i in images:
                try:
                    loc = get_location(i, name)
                    return loc
                except pyautogui.ImageNotFoundException as err:
                    pass
        
        # If no matching images found, raise exception
        raise NoMatchingImageException(img, name)


def click_image(img: Path | str | Sequence[Path | str], name = None):
    """Click on the center of an image, or the first matching of a sequence of images.

    Raises:
        NoMatchingImageException

    Args:
        img (pathlib.Path | str): Path to the image (screenshot) to click
        name (_type_, optional): Descriptive name to print in case the image can't be found
    """
    loc = get_location(img, name)
    pyautogui.moveTo(loc)
    pyautogui.leftClick(loc)



@contextmanager    
def pause_length(pause_per_step: float):
    _previous_pause = pyautogui.PAUSE
    pyautogui.PAUSE = pause_per_step
    try:
        yield 
    finally:
        pyautogui.PAUSE = _previous_pause


def test_compile():
    # Maximize main productivity suite window
    click_image(IMAGES / 'mainwindow_header.PNG', name="Production Suite Programming Software window")
    pyautogui.hotkey('super', 'up') 

    # Try to compile program early - if it doesn't compile, might as well bail
    with pause_length(0.5):
        click_image(IMAGES / "compile_icon.PNG", "compile button")
        comp_label = get_location(IMAGES / "project_compiled_successfully.PNG", "compilation success message")
    pyautogui.moveTo(comp_label)
    pyautogui.moveRel(0, 40)
    pyautogui.leftClick()
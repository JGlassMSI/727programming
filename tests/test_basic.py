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


def test_setup():
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

    # Open data view window is it's not already open
    with pause_length(0.5):
        pyautogui.hotkey('ctrl', 'shift', 'f3') 
        data_view = get_location([IMAGES / "dataview_icon.PNG"])
    
    # Move dataview window out of the way of the menu bar
    pyautogui.moveTo(data_view)
    pyautogui.dragTo(20, 20, duration=.5)

    # Resize the dataview window to a known size
    # Shrink window
    upper_data_corner = get_location(IMAGES / "dataview_icon.PNG", center=False)
    pyautogui.moveTo(upper_data_corner)
    pyautogui.moveRel(-12, -12)
    pyautogui.dragRel(pyautogui.size()[0]-200, pyautogui.size()[1]-200, duration=.5) 
    # Reposition
    upper_data_corner = get_location(IMAGES / "dataview_icon.PNG", center=False) 
    pyautogui.moveTo(upper_data_corner)
    pyautogui.dragTo(200, 200, duration = .5)
    # Resize applicable dataview columns so we can find values later
    with pause_length(0.5):
        corner = get_location(IMAGES / "dataview_icon.PNG", center=False)
        pyautogui.moveTo(corner)
        pyautogui.moveRel(32, 36)
    pyautogui.dragRel(800, 800, duration=.5)

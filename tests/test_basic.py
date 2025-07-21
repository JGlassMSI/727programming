import pathlib

import pyautogui

TESTS = pathlib.Path(__file__).parent

def test_setup():
    # Maximize main productivity suite window
    try:
        header_location = pyautogui.locateCenterOnScreen(str(TESTS / 'testbasic_images/mainwindow_header.PNG'))
    except pyautogui.ImageNotFoundException as err:
        raise ValueError("Could not find Production Suite Programming Software window on primary monitor")
    pyautogui.moveTo(header_location)
    pyautogui.leftClick()
    pyautogui.hotkey('super', 'up') 

    # Open data view window is it's not already open
    # TODO
    
    # Move dataview window out of the way of the menu bar
    # TODO

    # Resize the dataview window to a known size
    # TODO

    # Resize applicable dataview columns so we can find values later
    # TODO
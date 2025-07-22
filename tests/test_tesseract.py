from itertools import zip_longest
from pathlib import Path

import pyscreeze

from .support import assert_image_contains_text, assert_image_contains_image, get_data_from_dataview

pyscreeze.USE_IMAGE_NOT_FOUND_EXCEPTION = False

IMAGES = Path(__file__).parent / 'ocr_test_images'

def test_tesseract():
    assert_image_contains_text(IMAGES / 'test_tess.png', """\
                This is a lot of 12 point text to test the
                ocr code and see if it works on all types
                of file format.""")

def test_tesseract_on_dataview_rows():
    assert_image_contains_text(IMAGES / 'dataview_line_int.png', "Drive_MainWheel_Write.RunFrequency", resize=2)
    assert_image_contains_text(IMAGES / 'dataview_line_int.png', "15", resize=2)

    assert_image_contains_text(IMAGES / 'dataview_line_bool.png', "Drive_MainWheel_Write.Timeout")
    assert_image_contains_image(IMAGES / 'dataview_line_bool.png', IMAGES / "checkbox_checked.png")

    assert_image_contains_text(IMAGES / 'dataview_line_bool_unchecked.png', "Drive_MainWheel_Write.Error")
    assert_image_contains_image(IMAGES / 'dataview_line_bool_unchecked.png', IMAGES / "checkbox_empty.png")

def test_getting_dataview_data():
    data = get_data_from_dataview(IMAGES / "dataview_2.png")
    expected_data = {
        "MainWheel_Run"                         : True,
        "Drive_MainWheel_Write.RunFrequency"    : 15,
        "Drive_MainWheel_Write.JogFrequency"    : 0,
        "Drive_MainWheel_Write.Timeout"         : True,
        "Drive_MainWheel_Write.Error"           : True,
        "Drive_MainWheel_Write.Success"         : True,
        "Drive_MainWheel_Write.Complete"        : False,
        "Drive_MainWheel_Write.InProgress"      : False,
        "Drive_MainWheel_Write.ExcResponse"     : None,
        "MainWheel_Direction"                   : 9999,
        "MainWheel_FaultReset"                  : 0,
        "MainWheel_Jog"                         : False,
        "MainWheel_RunModeData"                 : False,
        "MainWheel_StopModeData"                : False,
        "NoseGear_Request_Down_Ext"             : False,
        "NoseGear_Request_Up_Ext"               : False,
        "_NoseGear_Up_Request"                  : False,
    }

    formatstring = "{key: <50} : {found: <50}"

    print(formatstring.format(key="Expected Tagnames", found="Found Tagnames"))
    print(formatstring.format(key="-----------------", found="--------------"))
    for expected_key, ocr_key in zip_longest(sorted(expected_data.keys()), sorted(data.keys())):
        print(formatstring.format(key=str(expected_key), found=str(ocr_key)))
    print("\n\n")

    formatstring = "{key: <50} : {found: <30} / {expected: <30}"
    print(formatstring.format(key = "Tag Name", found = "Ocr Data", expected = "Expected Value"))
    print(formatstring.format(key = "--------", found = "--------", expected = "--------------"))
    for k, v in data.items():
        print(formatstring.format(key = str(k), found = str(v), expected = str(expected_data[k])))
    for k, v in data.items():
        assert data[k] == v, f"OCR found {str(k) + ":" + str(data[k])} but it should have been {str(v)}"
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
    print(data)
    assert False
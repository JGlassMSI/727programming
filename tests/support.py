import csv
from functools import cache, cached_property
from contextlib import contextmanager
from typing import NamedTuple
from pathlib import Path
from time import sleep
from typing import Sequence

import pyautogui
from pyscreeze import _locateAll_pillow, locate, Point, Box
import pytest

from pymodbus.client import ModbusTcpClient
from pymodbus.pdu.pdu import pack_bitstring

CSV_BASIC_PATH = Path(__file__).parent.parent / "727_ladder_Basic.csv"

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


IMAGES = Path(__file__).parent / 'testbasic_images'
DEBUG_IMAGES = Path(__file__).parent / 'debug_images'

class NoMatchingImageException(pyautogui.ImageNotFoundException):
    def __init__(self, *args: object) -> None:
        img = args[0]
        name = args[1] if len(args) > 1 else None
        msg = f"Could not find {name if name else 'pixels matching ' + str(img)} on primary monitor {f"({str(img)})" if name else ""}"
        super().__init__(msg)

class AddressInfo(NamedTuple):
    address: int
    length: int = 1
    ending: str = "big"
    
    @property
    def address_type(self) -> int:
        return int(self.address / 100_000)
    
    @property
    def real_modbus_address(self) -> int:
        return self.address % 100_000

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

def wait_for_image(img, msg = None, *, timeout = 10) -> Point | Box:
    for _ in range(timeout):
        sleep(1)
        img = None
        try:
            img = get_location(IMAGES / "need_to_transfer.PNG", msg)
        except pyautogui.ImageNotFoundException:
            pass
        if img: break
    else:
        raise NoMatchingImageException(IMAGES / "need_to_transfer.PNG", msg)
    return img

@pytest.mark.usefixtures("modbus_client")
@pytest.mark.usefixtures("startup")
class ProductivitySuiteTest:
    @pytest.fixture(scope="session")
    def maximize(self):
        # Maximize main productivity suite window
        click_image(IMAGES / 'mainwindow_header.PNG', name="Production Suite Programming Software window")
        pyautogui.hotkey('super', 'up') 
        
        # Save to ensure tag defs are up to date
        pyautogui.hotkey('ctrl', 's') 

    @pytest.fixture(scope="session")
    def compile_all(self):
        # Try to compile program early - if it doesn't compile, might as well bail
        with pause_length(0.5):
            click_image([IMAGES / "stop_button.PNG", IMAGES / "stop2.PNG", IMAGES / "stop3.PNG"], "stop button button")
            click_image(IMAGES / "compile_icon.PNG", "compile button")
            comp_label = get_location(IMAGES / "project_compiled_successfully.PNG", "compilation success message")
        pyautogui.moveTo(comp_label)
        pyautogui.moveRel(0, 40)
        pyautogui.leftClick()

    @pytest.fixture(scope="session")
    def online_and_transfer(self):
            # Go Offline and Online Again
            with pause_length(1):
                click_image([IMAGES / "offline.PNG", IMAGES / "offline2.PNG"], "offline button")
                click_image(IMAGES / "online.PNG", "online button")

            # Wait for the WARNING about the need to transfer to pop up, make it go away
            transfer_label = wait_for_image(IMAGES / "need_to_transfer.PNG", "transfer warning message")
            pyautogui.moveTo(transfer_label)
            pyautogui.moveRel(0, 40)
            pyautogui.leftClick()

            # Transfer project to CPU
            with pause_length(1):
                click_image(IMAGES / "transfer.PNG", "transfer button")
                cont = get_location(IMAGES / "retentive_warning.PNG", "retentive tags warning")
                pyautogui.moveTo(cont)
                pyautogui.moveRel(0, 40)
                pyautogui.leftClick()

            # Wait for transfer to complete
            for _ in range(20):
                sleep(1)
                try:
                    _ = get_location(IMAGES / "transfer_project_to_CPU.png", "project transfer window")
                except pyautogui.ImageNotFoundException:
                    break
            else:
                raise NoMatchingImageException(IMAGES / "transfer_project_to_CPU.png", "project transfer window")
    
    @pytest.fixture(scope="session")
    def debug(self):
        click_image(IMAGES / "debug.PNG", "debug button")
        sleep(.5)
            
    @pytest.fixture
    def modbus_client(self):
        self.client = ModbusTcpClient('127.0.0.1')      
        self.client.connect()      
        yield
        self.client.close()

    @pytest.fixture(scope="session")
    def startup(self, maximize, compile_all, online_and_transfer, debug):
        pass

    def run_one_scan(self):
        click_image([DEBUG_IMAGES / "onescan.PNG", DEBUG_IMAGES / "onescan2.PNG"], "run one scan button")
        sleep(.1)

    def _get_tag_address(self, tagname: str) -> AddressInfo:
        tagsinfo = get_tag_info_from_file()
        start_address = tagsinfo[tagname].get('MODBUS Start Address', -1)
        if start_address == -1:
            raise ValueError(f"Could not find start address for {tagname} in file")
        if start_address == '':
            raise ValueError(f"{tagname} has not been assigned an address in the Tag Database")
        
        try:
            address = int(start_address) - 1 # Off-by-one from the l isted address
        except ValueError as err:
            raise ValueError(f"Found a non-integer value for the address of {tagname} : '{start_address}' \n full tag was {tagsinfo[tagname]}") from err
        
        length = int(tagsinfo[tagname].get('MODBUS End Address', start_address)) - int(start_address) + 1

        return AddressInfo(address, length)

    def get_value(self, tagname) -> int | str:
        address = self._get_tag_address(tagname)
        
        match address.address_type:
            case 0:
                r = pack_bitstring(self.client.read_coils(address.real_modbus_address).bits)
                return int.from_bytes(r)
            case 3:
                return self.client.read_input_registers(address.real_modbus_address).registers[0]
            case 4:
                return self.client.read_holding_registers(address.real_modbus_address).registers[0]
            case _:
                raise ValueError(f"Unknown message type for address {address}")
            
    def set_value(self, tagname: str, val: bool | int):
        address = self._get_tag_address(tagname)
        
        match address.address_type:
            case 0:
                self.client.write_coil(address.real_modbus_address, bool(val))
            case 6:
                self.client.write_register(address.real_modbus_address, int(val))
            case _:
                raise ValueError(f"Unknown message type for address {address}")

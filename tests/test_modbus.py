from time import sleep


from pymodbus.client import ModbusTcpClient
from pymodbus.pdu.pdu import pack_bitstring
import pytest

from .support import get_tag_info_from_file 

def get_tag_value(tagname) -> int | str:
    client = ModbusTcpClient('127.0.0.1')      
    client.connect()                              

    tagsinfo = get_tag_info_from_file()
    address = tagsinfo[tagname].get('MODBUS Start Address', -1)
    if address == -1:
        raise ValueError(f"Could not find start address for {tagname} in file")
    
    try:
        address = int(address) - 1 # Off-by-one from the l isted address
    except ValueError as err:
        raise ValueError(f"Found a non-integer value for the address of {tagname} : '{address}'") from err
    
    address_type = int(address / 100_000)
    real_address = address % 100_000


    match address_type:
        case 0:
            return int(pack_bitstring(client.read_coils(real_address).bits))
        case 3:
            return client.read_input_registers(real_address).registers[0]
        case 4:
            return client.read_holding_registers(real_address).registers[0]
        case _:
            raise ValueError(f"Unknown message type for address {address}")
    
    client.close()   


@pytest.mark.xfail(reason="This only works on the simple sample program")
def test_modbus_orig():
    START_ADDR = 1
    MOTOR_ADDR = 0
    client = ModbusTcpClient('127.0.0.1')       # Create client object
    client.connect()                               # connect to device

    client.write_coil(START_ADDR, False) # Turn start on
    sleep(.1)
    assert client.read_coils(START_ADDR).bits[0] == 0 # Start Off
    assert client.read_coils(MOTOR_ADDR).bits[0] == 0 # Motor Off

    client.write_coil(START_ADDR, True) # Turn start on
    sleep(.1)
    assert client.read_coils(MOTOR_ADDR).bits[0] == 1 # Motor On

    client.write_coil(START_ADDR, False) # Turn start on
    sleep(.1)
    assert client.read_coils(MOTOR_ADDR).bits[0] == 0 # Motor Off


if __name__ == "__main__":
    ...
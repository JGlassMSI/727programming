from time import sleep
from pymodbus.client import ModbusTcpClient
from pymodbus.pdu.pdu import pack_bitstring

from support import get_tag_info_from_file

def modbus_experiment():
    client = ModbusTcpClient('127.0.0.1')       # Create client object
    client.connect()                               # connect to device
    #client.write_coil(1, False)        # set information in device
    

    try:
        count = 0
        while True:
            print(f"{count: <6}: ", end = "")
            for i in range(6):
                result = client.read_coils(i)  # get information from device
                print(f"{i}/{result.bits[0]} ", end = "")                          # use information
            print("")
            sleep(1)
            count += 1
    except KeyboardInterrupt:
        client.close()                                 # Disconnect devic

def modbus_experiment_2():
    taginfo = get_tag_info_from_file()
    for tagname, data in taginfo.items():
        print(f"{tagname: <50} : {data.get('MODBUS Start Address')}")
    for key in ["MainWheel_FaultReset"]:
        print(f"{key: <40} has value {get_tag_value(key)}")
    

def get_tag_value(tagname):
    client = ModbusTcpClient('127.0.0.1')       # Create client object
    client.connect()                               # connect to device

    tagsinfo = get_tag_info_from_file()
    address = tagsinfo[tagname].get('MODBUS Start Address')
    if address: response = client.read_coils(int(address))
    client.close()   

    if address: 
        print(f"{response!r}")
        print(dir(response))
        print(pack_bitstring(response.bits))
    return None


def test_modbus():
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
    modbus_experiment_2()
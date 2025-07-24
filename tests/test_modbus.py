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
            for i in range(12):
                result = client.read_coils(i)  # get information from device
                print(f"{i}/{result.bits[0]} ", end = "")                          # use information
            print("")
            sleep(1)
            count += 1
    except KeyboardInterrupt:
        client.close()                                 # Disconnect devic

def modbus_experiment_2():
    #This fails asis because MainWheel FaultReset is in the 400,000's
    taginfo = get_tag_info_from_file()
    for tagname, data in taginfo.items():
        print(f"{tagname: <50} : {data.get('MODBUS Start Address')}")
    for key in ["MainWheel_FaultReset"]:
        print(f"{key: <40} has value {get_tag_value(key)}")

def modbus_experiment_3():
    client = ModbusTcpClient('127.0.0.1')       # Create client object
    client.connect()   
    faultreset = get_tag_value('_NoseGear_AnyRequest')
    #print(f"{pack_bitstring(faultreset.bits)} : {faultreset.bits}")
    client.close()   
    #print(f"{faultreset.bits=}")
    #print(f"{pack_bitstring(faultreset.bits)=}")
    

def get_tag_value(tagname) -> int | str:
    client = ModbusTcpClient('127.0.0.1')       # Create client object
    client.connect()                               # connect to device

    tagsinfo = get_tag_info_from_file()
    print(tagsinfo[tagname])
    address = tagsinfo[tagname].get('MODBUS Start Address', -1)
    if address == -1:
        raise ValueError(f"Could not find start address for {tagname} in file")
    print(f"Address of {tagname} is {address}")
    
    try:
        address = int(address) - 1
    except ValueError as err:
        raise ValueError(f"Found a non-integer value for the address of {tagname} : '{address}'") from err
    
    address_type = int(address / 100_000)
    real_address = address % 100_000

    print(f"{address_type=} {real_address=}")

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

def modbus_experiment_4():
    """Successfully reads value of coil at address 000_009"""
    client = ModbusTcpClient('127.0.0.1')       # Create client object
    client.connect()
    response = client.read_coils(8)
    print(response)
    print(pack_bitstring(response.bits))

def modbus_experiment_5():
    """Successfully reads register at 400_004 Result is in the registers attribute!"""
    client = ModbusTcpClient('127.0.0.1')       # Create client object
    client.connect()
    response = client.read_holding_registers(3)
    print(response)
    print(response.registers)

#Successfully reads register at 300_0061 (Clock Hours)
#Result is in the registers attribute!
def modbus_experiment_6():
    """"""
    client = ModbusTcpClient('127.0.0.1')       # Create client object
    client.connect()
    response = client.read_input_registers(60)
    print(response)
    print(response.registers)


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
    modbus_experiment_6()
from time import sleep
from pymodbus.client import ModbusTcpClient

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
    modbus_experiment()
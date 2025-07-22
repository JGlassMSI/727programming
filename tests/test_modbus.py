from time import sleep

def modbus_experiment():
    from pymodbus.client import ModbusTcpClient

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

if __name__ == "__main__":
    modbus_experiment()
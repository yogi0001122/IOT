import sys, time
#import iothub_service_client

from iothub_service_client import IoTHubDeviceMethod, IoTHubError, IoTHubDeviceTwin

CONNECTION_STRING = "HostName=IoTDemoDeviceManage.azure-devices.net;DeviceId=NCRLaptop-Device1;SharedAccessKey=E0csgq93mwZtVRB3OIH2p2uuSPxR61uQZaORmZ+9Fok="
DEVICE_ID = "NCRLaptop-Device1"

METHOD_NAME = "rebootDevice"
METHOD_PAYLOAD = "{\"method_number\":\"42\"}"
TIMEOUT = 60
WAIT_COUNT = 10

def iothub_devicemethod_sample_run():
    try:
        iothub_twin_method = IoTHubDeviceTwin(CONNECTION_STRING)
        iothub_device_method = IoTHubDeviceMethod(CONNECTION_STRING)

        print ( "" )
        print ( "Invoking device to reboot..." )

        response = iothub_device_method.invoke(DEVICE_ID, METHOD_NAME, METHOD_PAYLOAD, TIMEOUT)

        print ( "" )
        print ( "Successfully invoked the device to reboot." )

        print ( "" )
        print ( response.payload )

        while True:
            print ( "" )
            print ( "IoTHubClient waiting for commands, press Ctrl-C to exit" )

            status_counter = 0
            while status_counter <= WAIT_COUNT:
                twin_info = iothub_twin_method.get_twin(DEVICE_ID)

                if twin_info.find("rebootTime") != -1:
                    print ( "Last reboot time: " + twin_info[twin_info.find("rebootTime")+11:twin_info.find("rebootTime")+37])
                else:
                    print ("Waiting for device to report last reboot time...")

                time.sleep(5)
                status_counter += 1

    except IoTHubError as iothub_error:
        print ( "" )
        print ( "Unexpected error {0}".format(iothub_error) )
        return
    except KeyboardInterrupt:
        print ( "" )
        print ( "IoTHubDeviceMethod sample stopped" )

if __name__ == '__main__':
    print ( "Starting the IoT Hub Service Client DeviceManagement Python sample..." )
    print ( "    Connection string = {0}".format(CONNECTION_STRING) )
    print ( "    Device ID         = {0}".format(DEVICE_ID) )

    iothub_devicemethod_sample_run()

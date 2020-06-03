import random
import time, datetime
import sys
import os
import iothub_client
import webbrowser
from iothub_client import IoTHubClient, IoTHubClientError, IoTHubTransportProvider, IoTHubClientResult, IoTHubError, DeviceMethodReturnValue

#CONNECTION_STRING = "HostName=DCS-IOT-POC-HUB.azure-devices.net;DeviceId=DCS-POC-Device1-Laptop;SharedAccessKey=vcZZacjY4H0dvOoGD/YJ6bsFwR8moWrW0nkhwwl3EIA="
CONNECTION_STRING = "HostName=NCR-Unconference-Demo.azure-devices.net;DeviceId=NCR-Unconference-Device-1;SharedAccessKey=Vn6UH2Vck1Gsx9JTX8iuoD69I5t1kplJ/Yc1T3jJjFc="
PROTOCOL = IoTHubTransportProvider.MQTT

CLIENT = IoTHubClient(CONNECTION_STRING, PROTOCOL)

WAIT_COUNT = 5

SEND_REPORTED_STATE_CONTEXT = 0
METHOD_CONTEXT = 0

SEND_REPORTED_STATE_CALLBACKS = 0
METHOD_CALLBACKS = 0

def send_reported_state_callback(status_code, user_context):
    global SEND_REPORTED_STATE_CALLBACKS

    print ( "Device twins updated." )

def device_method_callback(method_name, payload, user_context):
    global METHOD_CALLBACKS

    if "reboot" in method_name:
        print ( "Rebooting device..." )
        time.sleep(50)
        os.system("shutdown /r /t 1")
        time.sleep(20)

        print ( "Device rebooted." )

        current_time = str(datetime.datetime.now())
        reported_state = "{\"rebootTime\":\"" + current_time + "\"}"
        CLIENT.send_reported_state(reported_state, len(reported_state), send_reported_state_callback, SEND_REPORTED_STATE_CONTEXT)

        print ( "Updating device twins: rebootTime" )
        print (reported_state)
        print (method_name)
        print ( "Updating device twins: rebootTime" )
    elif "IOT" in method_name:
        print ("Playing Azure Video on Youtube.......")
        webbrowser.open("https://www.youtube.com/watch?v=smuZaZZXKsU")

    device_method_return_value = DeviceMethodReturnValue()
    device_method_return_value.response = "{ \"Response\": \"This is the response from the device \" }"
    device_method_return_value.status = 200

    return device_method_return_value

def iothub_client_init():
    if CLIENT.protocol == IoTHubTransportProvider.MQTT or client.protocol == IoTHubTransportProvider.MQTT_WS:
        CLIENT.set_device_method_callback(device_method_callback, METHOD_CONTEXT)

def iothub_client_sample_run():
    try:
        iothub_client_init()

        while True:
            print ( "IoTHubClient waiting for commands, press Ctrl-C to exit" )

            status_counter = 0
            while status_counter <= WAIT_COUNT:
                time.sleep(10)
                status_counter += 1

    except IoTHubError as iothub_error:
        print ( "Unexpected error %s from IoTHub" % iothub_error )
        return
    except KeyboardInterrupt:
        print ( "IoTHubClient sample stopped" )

if __name__ == '__main__':
    print ( "Starting the IoT Hub Python sample..." )
    print ( "    Protocol %s" % PROTOCOL )
    print ( "    Connection string=%s" % CONNECTION_STRING )

    iothub_client_sample_run()

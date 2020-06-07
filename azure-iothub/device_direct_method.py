# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for full license information.

import random
import time
import threading
import webbrowser

# Using the Python Device SDK for IoT Hub:
#   https://github.com/Azure/azure-iot-sdk-python
# The sample connects to a device-specific MQTT endpoint on your IoT Hub.
from azure.iot.device import IoTHubDeviceClient, Message, MethodResponse

# The device connection string to authenticate the device with your IoT hub.
# Using the Azure CLI:
# az iot hub device-identity show-connection-string --hub-name {YourIoTHubName} --device-id MyNodeDevice --output table
CONNECTION_STRING = "HostName=iothub-poc-demo.azure-devices.net;DeviceId=iot-device1;SharedAccessKey=fL8W+ivYhA/tDfs7KLAFk92bvLNO87XvAWRNRIaDJro="

WAIT_COUNT = 5

INTERVAL = 5

def iothub_client_init():
    # Create an IoT Hub client
    client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
    return client


def device_method_listener(device_client):
    global INTERVAL
    while True:
        method_request = device_client.receive_method_request()
        print (
            "\nMethod callback called with:\nmethodName = {method_name}\npayload = {payload}".format(
                method_name=method_request.name,
                payload=method_request.payload
            )
        )
        if method_request.name == "SetTelemetryInterval":
            try:
                INTERVAL = int(method_request.payload)
                print (INTERVAL)
            except ValueError:
                response_payload = {"Response": "Invalid parameter"}
                response_status = 400
            else:
                response_payload = {"Response": "Executed direct method {}".format(method_request.name)}
                response_status = 200
                
        elif method_request.name == "IOT Play":
            try:
                print ("Playing Azure Video on Youtube.......")
                webbrowser.open("https://www.youtube.com/watch?v=smuZaZZXKsU")
            except:
                response_payload = {"Response": "Invalid request"}
                response_status = 400
            else:
                response_payload = {"Response": "Executed direct method {}".format(method_request.name)}
                response_status = 200

        else:
            response_payload = {"Response": "Direct method {} not defined".format(method_request.name)}
            response_status = 404

        method_response = MethodResponse(method_request.request_id, response_status, payload=response_payload)
        device_client.send_method_response(method_response)



def iothub_client_telemetry_sample_run():

    try:
        client = iothub_client_init()
        print ( "IoT Hub device sending periodic messages, press Ctrl-C to exit" )

        # Start a thread to listen 
        device_method_thread = threading.Thread(target=device_method_listener, args=(client,))
        device_method_thread.daemon = True
        device_method_thread.start()

        while True:
            print ( "IoTHubClient waiting for commands, press Ctrl-C to exit" )

            status_counter = 0
            while status_counter <= WAIT_COUNT:
                time.sleep(INTERVAL)
                status_counter += 1

    except KeyboardInterrupt:
        print ( "IoTHubClient  stopped" )

if __name__ == '__main__':
    print ( "IoT Hub Quickstart # -  device" )
    print ( "Press Ctrl-C to exit" )
    iothub_client_telemetry_sample_run()

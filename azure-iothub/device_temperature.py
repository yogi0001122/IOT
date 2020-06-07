# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for full license information.

import random
import time
import sys
import wmi

# Using the Python Device SDK for IoT Hub:
#   https://github.com/Azure/azure-iot-sdk-python
# The sample connects to a device-specific MQTT endpoint on your IoT Hub.
#import iothub_client
from azure.iot.device import IoTHubDeviceClient, Message
# pylint: disable=E0611
#from iothub_client import IoTHubClient, IoTHubClientError, IoTHubTransportProvider, IoTHubClientResult
#from iothub_client import IoTHubMessage, IoTHubMessageDispositionResult, IoTHubError, DeviceMethodReturnValue

# The device connection string to authenticate the device with your IoT hub.
# Using the Azure CLI:
# az iot hub device-identity show-connection-string --hub-name {YourIoTHubName} --device-id MyNodeDevice --output table
CONNECTION_STRING = "HostName=iothub-poc-demo.azure-devices.net;DeviceId=iot-device1;SharedAccessKey=fL8W+ivYhA/tDfs7KLAFk92bvLNO87XvAWRNRIaDJro="

# Using the MQTT protocol.
#PROTOCOL = IoTHubTransportProvider.MQTT
MESSAGE_TIMEOUT = 10000

# Define the JSON message to send to IoT Hub.
TEMPERATURE = 20.0
HUMIDITY = 60
#MSG_TXT = "{\"temperature\": %.2f,\"humidity\": %.2f}"
MSG_TXT = "{\"temperature\": %.2f,\"sensorname\": \"%.15s\"}"


def send_confirmation_callback(message, result, user_context):
    print ( "IoT Hub responded to message with status: %s" % (result) )

def iothub_client_init():
    # Create an IoT Hub client
    #client = IoTHubClient(CONNECTION_STRING, PROTOCOL)
    client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
    return client

def iothub_client_telemetry_sample_run():

    try:
        client = iothub_client_init()
        print ( "IoT Hub device sending periodic messages, press Ctrl-C to exit" )

        while True:
            # Build the message with simulated telemetry values.
            #temperature = TEMPERATURE + (random.random() * 15)
			#temperature = temperature
            w = wmi.WMI(namespace="root\OpenHardwareMonitor")
            temperature_infos = w.Sensor()
            for sensor in temperature_infos:
                if sensor.SensorType == 'Temperature':
                  sensorname = str(sensor.Name)
                  temperature = sensor.Value				  
                  msg_txt_formatted = MSG_TXT % (temperature, sensorname)
                  print (msg_txt_formatted)
                  message = Message(msg_txt_formatted)
                  if temperature > 30:
                      message.custom_properties["temperatureAlert"] = "true"
                  else:
                      message.custom_properties["temperatureAlert"] = "false"
                  # Send the message.
                  print( "Sending message: {}".format(message) )
                  client.send_message(message)
                  print ( "Message successfully sent" )
            time.sleep(5)

    except KeyboardInterrupt:
        print ( "IoTHubClient sample stopped" )

if __name__ == '__main__':
    print ( "IoT Hub Quickstart #1 -  device" )
    print ( "Press Ctrl-C to exit" )
    iothub_client_telemetry_sample_run()
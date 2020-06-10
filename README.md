---
Page_type: IOT Use Cases
Languages: Python
Products:
  - Azure IOT HUB
---

# IOT Device Python SDK Code Samples 

These are code samples that show common scenario operations with iot solutions using Python. 

- [device_temperature.py](./azure-iothub/device_temperature.py) - Sample code to Send telemetry from a device to an IoT hub

    - Get windows machine temperature and send to IOT HUB
    - Device management using direct methods.
    - Handling the method request sent from IoT Hub.
    - This contains a direct method that reboots that device. Direct methods are invoked from the cloud.
    - Calls the reboot direct method in the simulated device app through your IoT hub.

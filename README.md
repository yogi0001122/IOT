---
Page_type: IOT Use Cases
Languages: Python
Products:
  - Azure IOT HUB
---

# IOT Device Python SDK Code Samples 

These are code samples that show common scenario operations with iot solutions using Python. 

- [SimulatedDevice.py](./azure-iothub/SimulatedDevice.py) - Sample code to Send telemetry from a device to an IoT hub and Device management using direct methods

    - Get windows machine temperature and send to IOT HUB
    - Handling the method request sent from IoT Hub
    - This contains a direct method that reboots that device. Calls the reboot direct method in the simulated device app through your IoT hub

- [receive_queue_async_elk_dataload.py](./azure-iothub/Sreceive_queue_async_elk_dataload.py) - Receive device telemetry messages from Azure Service BUS queue and load to elk index for visual representation of sensors data in Kibana.

   - Receiving messages from a Service Bus Queue asynchronously
   - Create Index in elk and insert/update data to elk index

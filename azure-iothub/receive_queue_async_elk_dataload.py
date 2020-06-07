import os
import asyncio
from azure.servicebus.aio import ServiceBusClient
# Import elasticsearch-py package
from datetime import datetime,date
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from elasticsearch import Elasticsearch,helpers
import json


CONNECTION_STR = "Connectionstring"
QUEUE_NAME  = "queueName"
now = datetime.now()
dt_string = now.strftime("%Y%m")
# Connect to hosts and http_auth using params
es = Elasticsearch('http://localhost:9250', http_auth=('elastic', 'password'))
MSG_TXT = "{\"temperature\": %.2f,\"sensorname\": \"%.15s\",\"EventProcessedUtcTime\": \"%.25s\",\"ConnectionDeviceId\": \"%.15s\"}"

async def main():

    def load_event_elk(item,index_name):
        # Get latest doc id of index
        try:
            a=helpers.scan(es,query={"query":{"match_all": {}}},scroll='1m',index=index_name)#like others so far
            IDs=[aa['_id'] for aa in a]
            id_v = IDs[-1]
            print ("ID value :", id_v)
        except:
            id_v = 0

        id_v = int(id_v) + 1
        result = es.index(index=index_name, doc_type='iothub', id=id_v, body=item)
        print(item)

    servicebus_client = ServiceBusClient.from_connection_string(conn_str=CONNECTION_STR)
    queue_client = servicebus_client.get_queue(QUEUE_NAME)
    async with queue_client.get_receiver() as messages:
        async for message in messages:
            #print(message)
            #load_event_elk(message)
            jsonObject = json.loads(str(message))
            temperature = jsonObject['temperature']
            sensorname = jsonObject['sensorname']
            EventProcessedUtcTime = jsonObject['EventProcessedUtcTime']
            ConnectionDeviceId = jsonObject['IoTHub']['ConnectionDeviceId']
            index_name = ConnectionDeviceId + "-" + str(dt_string)
            msg_txt_formatted = MSG_TXT % (temperature, sensorname,EventProcessedUtcTime,ConnectionDeviceId)
            print (msg_txt_formatted)
            load_event_elk(msg_txt_formatted,index_name)
            await message.complete()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())

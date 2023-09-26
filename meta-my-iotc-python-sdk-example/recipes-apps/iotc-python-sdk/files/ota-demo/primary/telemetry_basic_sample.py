"""
  ******************************************************************************
  * @file   : iotconnect-sdk-1.0-firmware-python_msg-2_1.py
  * @author : Softweb Solutions An Avnet Company
  * @modify : 02-January-2023
  * @brief  : Firmware part for Python SDK 1.0
  ******************************************************************************
"""

"""
 * Hope you have installed the Python SDK v1.0 as guided in README.md file or from documentation portal. 
 * Import the IoTConnect SDK package and other required packages
"""



app_version: str = "1.0"

import sys
import json
import time
import threading
import random

# if iotconnect module is not installed then use the local one
# note: this is if you are running the sample in the git repository folder
try:
    from iotconnect import IoTConnectSDK
except:
    sys.path.append("iotconnect-sdk-1.0")
    from iotconnect import IoTConnectSDK

from datetime import datetime
import os


import credentials
UniqueId: str = credentials.UniqueId 
sdk_identity: str = credentials.sdk_identity
SdkOptions: dict = credentials.SdkOptions


Sdk=None
interval = 30
directmethodlist={}
ACKdirect=[]
device_list=[]



"""
 * Type    : Callback Function "DeviceCallback()"
 * Usage   : Firmware will receive commands from cloud. You can manage your business logic as per received command.
 * Input   :  
 * Output  : Receive device command, firmware command and other device initialize error response 
"""

def DeviceCallback(msg):
    global Sdk
    print("\n--- Command Message Received in Firmware ---")
    print(json.dumps(msg))
    cmdType = None
    if msg != None and len(msg.items()) != 0:
        cmdType = msg["ct"] if "ct"in msg else None
    # Other Command
    if cmdType == 0:
        """
        * Type    : Public Method "sendAck()"
        * Usage   : Send device command received acknowledgment to cloud
        * 
        * - status Type
        *     st = 6; // Device command Ack status 
        *     st = 4; // Failed Ack
        * - Message Type
        *     msgType = 5; // for "0x01" device command 
        """
        data=msg
        if data != None:
            #print(data)
            if "id" in data:
                if "ack" in data and data["ack"]:
                    Sdk.sendAckCmd(data["ack"],7,"successful",data["id"])  #fail=4,executed= 5,success=7,6=executed ack
            else:
                if "ack" in data and data["ack"]:
                    Sdk.sendAckCmd(data["ack"],7,"successful") #fail=4,executed= 5,success=7,6=executed ack
    else:
        print("rule command",msg)



def DeviceConnectionCallback(msg):  
    cmdType = None
    if msg != None and len(msg.items()) != 0:
        cmdType = msg["ct"] if msg["ct"] != None else None
    #connection status
    if cmdType == 116:
        #Device connection status e.g. data["command"] = true(connected) or false(disconnected)
        print(json.dumps(msg))

"""
 * Type    : Public Method "UpdateTwin()"
 * Usage   : Update the twin reported property
 * Input   : Desired property "key" and Desired property "value"
 * Output  : 
"""
# key = "<< Desired property key >>"; // Desired property key received from Twin callback message
# value = "<< Desired Property value >>"; // Value of respective desired property
# Sdk.UpdateTwin(key,value)

"""
 * Type    : Callback Function "TwinUpdateCallback()"
 * Usage   : Manage twin properties as per business logic to update the twin reported property
 * Input   : 
 * Output  : Receive twin Desired and twin Reported properties
"""
def TwinUpdateCallback(msg):
    global Sdk
    if msg:
        print("--- Twin Message Received ---")
        print(json.dumps(msg))
        if ("desired" in msg) and ("reported" not in msg):
            for j in msg["desired"]:
                if ("version" not in j) and ("uniqueId" not in j):
                    Sdk.UpdateTwin(j,msg["desired"][j])

"""
 * Type    : Public data Method "SendData()"
 * Usage   : To publish the data on cloud D2C 
 * Input   : Predefined data object 
 * Output  : 
"""
def sendBackToSDK(sdk, dataArray):
    sdk.SendData(dataArray)
    time.sleep(interval)

def DirectMethodCallback1(msg,methodname,rId):
    global Sdk,ACKdirect
    print(msg)
    print(methodname)
    print(rId)
    data={"data":"succeeded"}
    #return data,200,rId
    ACKdirect.append({"data":data,"status":200,"reqId":rId})
    #Sdk.DirectMethodACK(data,200,rId)

def DirectMethodCallback(msg,methodname,rId):
    global Sdk,ACKdirect
    print(msg)
    print(methodname)
    print(rId)
    data={"data":"fail"}
    #return data,200,rId
    ACKdirect.append({"data":data,"status":200,"reqId":rId})
    #Sdk.DirectMethodACK(data,200,rId)

def DeviceChangCallback(msg):
    print(msg)

def InitCallback(response):
    print(response)

def delete_child_callback(msg):
    print(msg)

def attributeDetails(data):
    print ("attribute received in firmware")
    print (data)
    

def init_sdk():
    global sdk_identity,SdkOptions,Sdk,ACKdirect,device_list
    try:
        Sdk = IoTConnectSDK(UniqueId,sdk_identity,SdkOptions,DeviceConnectionCallback)
        Sdk.onDeviceCommand(DeviceCallback)
        Sdk.onTwinChangeCommand(TwinUpdateCallback)
        Sdk.onDeviceChangeCommand(DeviceChangCallback)
        Sdk.getTwins()
        device_list=Sdk.Getdevice()
    except Exception as ex:
        print(ex.message)


def generate_dummy_payload():
    data = {
    "sw_version": app_version,
    "temperature":random.randint(30, 50),
    "long1":random.randint(6000, 9000),
    "integer1": random.randint(100, 200),
    "decimal1":random.uniform(10.5, 75.5),
    "date1":datetime.utcnow().strftime("%Y-%m-%d"),
    "time1":"11:55:22",
    "bit1":1,
    "string1":"red",
    "datetime1":datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.000Z"),
    "gyro": {
        'bit1':0,
        'boolean1': True,
        'date1': datetime.utcnow().strftime("%Y-%m-%d"),
        "datetime1": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.000Z"),
        "decimal1":random.uniform(10.5, 75.5),
        "integer1":random.randint(60, 600),
        "latlong1":[random.uniform(10.5, 75.5),random.uniform(10.5, 75.5)],
        "long1":random.randint(60, 600000),
        "string1":"green",
        "time1":"11:44:22",
        "temperature":random.randint(50, 90)
        }
        }
    dObj = [{
        "uniqueId": UniqueId,
        "time": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.000Z"),
        "data": data
    }]

    return dObj

def main():

    print("basic sample version " + app_version)
    init_sdk()

    try:
        while Sdk._needs_exit == False:
            sendBackToSDK(Sdk, generate_dummy_payload())
    except KeyboardInterrupt:
        print ("Keyboard Interrupt Exception")
        # os.execl(sys.executable, sys.executable, *sys.argv)
        os.abort()
        # sys.exit(0)
    except Exception as ex:
        print(ex.message)
        sys.exit(0)

if __name__ == "__main__":
    print("execute from main.py")
   # main()

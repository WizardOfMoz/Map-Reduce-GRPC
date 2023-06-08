import grpc 
import consistency_pb2
import consistency_pb2_grpc
from concurrent import futures
import pandas as pd
import sys
import uuid
from google.protobuf import wrappers_pb2
from google.protobuf import timestamp_pb2
import os
import time
import threading
import json

PORT = 0

def parseData(input_string):
    input_string = input_string.replace(" ", "")
    input_string = input_string.replace("'", "\"")
    parsed_list = json.loads(input_string)
    return parsed_list

def getPartitionData(serverAddress, index):
    channel = grpc.insecure_channel(serverAddress)
    stub = consistency_pb2_grpc.Map_ReduceStub(channel)
    request = consistency_pb2.ReduceDataRequest(index=index)
    response = stub.getIntermediateData(request)
    path = response.path
    with open(path,"r") as f:
        data = f.readlines()
    key = []
    value = []
    for line in data:
        line = line.replace("\n","")
        idx = line.index(" ")
        key_temp = line[:idx]
        value_temp = line[idx+1:]
        val_list = parseData(value_temp)
        # value_temp = value_temp.replace(" ", "")
        key.append(key_temp)
        value.append(val_list)

    # key = sorted(key)
    return key, value

def saveData(data, port):
    with open(f"FinalData/reduce_{port}/output.txt","w") as f:
        f.write("Name, Age, Role\n")
        for row in data:
            f.write(f"{row[0]}, {row[1]}, {row[2]}\n")
            # f.write(f"{key} {data[key]}\n")


class Reduce_MasterService(consistency_pb2_grpc.Master_ReduceServicer):

    def getFinalData(self, request, context):
        with open(f"FinalData/reduce_{PORT}/output.txt","r") as f:
            data = f.readlines()
        key = []
        value = []
        for line in data:
            line = line.replace("\n","")
            line = line.split(" ")
            key.append(line[0])
            value.append(int(line[1]))
        return consistency_pb2.FinalData(key=key, value=value)


def run():

    global PORT
    if(len(sys.argv) != 2):
        print("Usage: python reduce.py <port>")
        exit(1)

    PORT = sys.argv[1]

    DIRECTORY = f"FinalData/reduce_{PORT}"
    if not os.path.exists(DIRECTORY):
        os.makedirs(DIRECTORY,exist_ok=True)

    address  = f'localhost:{PORT}'
    reducer = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    reducer.add_insecure_port(f'[::]:{PORT}')
    channel = grpc.insecure_channel('localhost:8888')
    stub = consistency_pb2_grpc.Master_ReduceStub(channel)
    request = consistency_pb2.Reduce(address=f'localhost:{PORT}')
    response = stub.Register(request)

    consistency_pb2_grpc.add_Reduce_MasterServicer_to_server(Reduce_MasterService(), reducer)

    if(response.success):
        print("Registered with master")
    else:
        print("Master is full")
        exit(1)
    index = response.index
    mapServerList = list(stub.getRegisteredMaps(consistency_pb2.Void()))

    finalOutput = {}
    # print(mapServerList)
    all_keys = {}
    for mapServer in mapServerList:
        # print("\n==========================")
        # print(mapServer.address)
        key, value = getPartitionData(mapServer.address, index)

        # print("JKey valeuiss")
        # print(key)
        # print(value)

        for i in range(len(key)):
            if key[i] in all_keys:
                all_keys[key[i]].append(value[i])
            else:
                all_keys[key[i]] = [value[i]]

    # print(all_keys)

    final_output = []
    for key, value in all_keys.items():
        # print("In final", key, value)
        flat_value = []
        for val in value:
            for ex in val:
                flat_value.append(ex)
        t1 = [example if example[0] == "T1" else None for example in flat_value]
        t2 = [example if example[0] == "T2" else None for example in flat_value]

        t1 = [example for example in t1 if example is not None]
        t2 = [example for example in t2 if example is not None]
        for i in range(len(t1)):
            for j in range(len(t2)):
                final_output.append([key, t1[i][1], t2[j][1]])

    print(final_output)
    saveData(final_output, PORT)
        # print(data)
        # save the data to the directory
        # process the data
        # save the processed data to the directory
    
    

run()
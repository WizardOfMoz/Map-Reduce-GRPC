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
PORT = 0
def getPartitionData(serverAddress, index):
    channel = grpc.insecure_channel(serverAddress)
    stub = consistency_pb2_grpc.Map_ReduceStub(channel)
    request = consistency_pb2.ReduceDataRequest(index=index)
    response = stub.getIntermediateData(request)
    key = sorted(response.key)
    value = response.value

    print(key)
    print(value)
    return key, value

def saveData(data, port):
    with open(f"FinalData/reduce_{port}/output.txt","w") as f:
        for key in data:
            f.write(f"{key} {', '.join(map(str,data[key]))}\n")


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

    for mapServer in mapServerList:
        print(mapServer.address)
        key, value = getPartitionData(mapServer.address, index)
        for i in range(len(key)):
            if key[i] in finalOutput:
                finalOutput[key[i]] += [value[i]]
            else:
                finalOutput[key[i]] = [value[i]]
        
        for k in finalOutput:
            finalOutput[k] = list(set(finalOutput[k]))

    saveData(finalOutput, PORT)
        # print(data)
        # save the data to the directory
        # process the data
        # save the processed data to the directory

    

run()
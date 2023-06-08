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
from nltk.tokenize import word_tokenize
# import colorama
# from colorama import Fore

R = 0
PORT = 0
DATA = []
class Map_ReduceService(consistency_pb2_grpc.Map_ReduceServicer):

    def getIntermediateData(self, request, context):
        path = f"Intermediate_data/map_{PORT}/partition_{request.index}.txt"
        # with open(f"Intermediate_data/map_{PORT}/partition_{request.index}.txt","r") as f:
        #     data = f.readlines()
        # key = []
        # value = []
        # for line in data:
        #     line = line.replace("\n","")
        #     line = line.split(" ")
        #     key.append(line[0])
        #     value.append(int(line[1]))
        return consistency_pb2.IntermediateData(path=path)


def mapFunction(data):
    # this 1 is 1 an 1 apple 1
        key = []
        value = []
        table = "T2"
        for line in data:
            if("Name, Role" in line):
                table = "T2"
            elif("Name, Age" in line):
                table = "T1"
            else:
                line = line.replace("\n","")
                # print(line)
                pairs = line.split(", ")
                key.append(pairs[0])
                value.append([table, pairs[1]])

        # print(key)
        # print(value)
        # Merge duplicate keys
        # create an empty dictionary
        merged_dict = {}

        # loop through the keys and values lists
        for i in range(len(key)):
            # if key already exists in the dictionary, append the value to the existing list
            if key[i] in merged_dict:
                merged_dict[key[i]].append(value[i])
            # if key does not exist in the dictionary, add it and create a new list with the value
            else:
                merged_dict[key[i]] = [value[i]]
        keys_list = list(merged_dict.keys())
        values_list = list(merged_dict.values())

        # print(keys_list)
        # print(values_list)

        return keys_list, values_list

def paritionData(data):
    key, value = mapFunction(data)

    # print("###")
    # print(key)
    # print(value)
    

    partition = [[] for i in range(R)]
    # Length based partitioning
    for i in range(len(key)):
        partition[len(key[i])%R].append([key[i],value[i]])
    print("full data: ", partition)
    return partition

def storeData(partition, port):
    for i in range(len(partition)):
        with open(f"Intermediate_data/map_{port}/partition_{i}.txt","w") as f:
            for d in partition[i]:
                f.write(f"{d[0]} {d[1]}\n")


def run():
    global R
    global DATA
    global PORT
    if(len(sys.argv) != 2):
        print("Usage: python map.py <port>")
        exit(1)

    PORT = sys.argv[1]

    DIRECTORY = f"Intermediate_data/map_{PORT}"
    if not os.path.exists(DIRECTORY):
        os.makedirs(DIRECTORY,exist_ok=True)

    address  = f'localhost:{PORT}'
    mapper = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    mapper.add_insecure_port(f'[::]:{PORT}')
    channel = grpc.insecure_channel('localhost:8888')
    stub = consistency_pb2_grpc.Master_MapStub(channel)
    request = consistency_pb2.Map(address=f'localhost:{PORT}')
    response = stub.Register(request)
    # print(response.index)
    if(response.success):
        print(f"Registered with master, my index is {response.index}")
    else:
        print("Master is full")
        exit(1)
    request = consistency_pb2.MapDataRequest(address=f'localhost:{PORT}', index=response.index)
    response = stub.getInputData(request)
    DATA = response.data
    #TODO: Comment this
    print("\n")
    # print(PORT)
    # print(DATA)
    consistency_pb2_grpc.add_Map_ReduceServicer_to_server(Map_ReduceService(), mapper) #TODO:
    R = stub.getR(consistency_pb2.Void()).value

    partition = paritionData(DATA)
    storeData(partition, PORT)

    mapper.start()
    mapper.wait_for_termination()

    # store the requested data in a intermediate files as parition

    

run()
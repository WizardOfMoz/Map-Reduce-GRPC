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

R = 0
PORT = 0
DATA = []
class Map_ReduceService(consistency_pb2_grpc.Map_ReduceServicer):

    def getIntermediateData(self, request, context):

        with open(f"Intermediate_data/map_{PORT}/partition_{request.index}.txt","r") as f:
            data = f.readlines()
        key = []
        value = []
        for line in data:
            line = line.replace("\n","")
            line = line.split(" ")
            key.append(line[0])
            value.append(int(line[1]))
        return consistency_pb2.IntermediateData(key=key, value=value)


def mapFunction(data,doc_id):
        key = []
        value = []
        for line in data:
            line = line.replace("\n","")
            words = [word.lower() for word in word_tokenize(line) if word.isalpha()]
            for word in words:
                key.append(word)
                value.append(doc_id)
        return key, value

def paritionData(data,doc_id):
    key, value = mapFunction(data,doc_id)
    partition = [[] for i in range(R)]
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
        print("Registered with master")
    else:
        print("Master is full")
        exit(1)
    request = consistency_pb2.MapDataRequest(address=f'localhost:{PORT}', index=response.index)
    response = stub.getInputData(request)
    DATA = response.data
    DOCID= response.doc_id
    print(DATA)
    print(DOCID)
    consistency_pb2_grpc.add_Map_ReduceServicer_to_server(Map_ReduceService(), mapper)
    R = stub.getR(consistency_pb2.Void()).value

    partition = paritionData(DATA,DOCID)
    storeData(partition, PORT)

    mapper.start()
    mapper.wait_for_termination()

    # store the requested data in a intermediate files as parition

    

run()
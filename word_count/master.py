import grpc
import consistency_pb2
import consistency_pb2_grpc
from concurrent import futures
import os
import threading
from time import sleep
MAPSERVERS = []
REDUCESERVERS = []
INPUT_PATH = 'data/input_path'
M = 0
R = 0
OUTPUT_PATH = ''
class Master_MapService(consistency_pb2_grpc.Master_MapServicer):
    def __init__(self):
        self.map = {}
    
    def getInputData(self, request, context):
        # iterate over files of INPUT_PATH
        address = request.address
        # get index of address in MAPSERVERS
        index = request.index
        print(f'Map Address : {address} Index : {index}')
        count = 0
        data_path = []
        for file in os.listdir(INPUT_PATH):
            if(count % M  == index):
                print(f'File : {file}')
                data_path.append(os.path.join(INPUT_PATH, file))        
            count += 1
        print(f'Length of data : {len(data_path)}')
        return consistency_pb2.InputData(data=data_path)
    
    def Register(self, request, context):
        address = request.address
        if(len(MAPSERVERS) == M):
            return consistency_pb2.MapRegResponse(success=False)
        MAPSERVERS.append(address)
        index = MAPSERVERS.index(address)
        print(f"Map Address added : {address}, Index : {index}")
        return consistency_pb2.MapRegResponse(success=True, index=index)
    
    def getR(self, request, context):
        return consistency_pb2.RValue(value=R)

class Master_ReduceService(consistency_pb2_grpc.Master_ReduceServicer):
    def __init__(self):
        self.map = {}

    def sendInputData(self, request, context):
        self.map[request.key] = request.value
        return consistency_pb2.Void()
    
    def Register(self, request, context):
        address = request.address
        print(f"Reduce Address added : {address}")
        if(len(REDUCESERVERS) == R):
            return consistency_pb2.ReduceRegResponse(success=False)
        REDUCESERVERS.append(address)
        index = REDUCESERVERS.index(address)
        return consistency_pb2.ReduceRegResponse(success=True, index=index)
    
    def getRegisteredMaps(self, request, context):
        for address in MAPSERVERS:
            yield consistency_pb2.Map(address=address)

event = threading.Event()
def listenForData(addresses):
    event.wait()
    print(f'Listening for data from {addresses}')
    for address in addresses:
        channel = grpc.insecure_channel(address)
        stub = consistency_pb2_grpc.Reduce_MasterStub(channel)
        for data in stub.getFinalData(consistency_pb2.Void()):
            key = data.key
            value = data.value
            with open(os.path.join('output.txt'), 'w') as f:
                f.write(f'{key} : {value}\n')
def run_map_reduce(N, R):
    sleep(5)
    import subprocess
    for i in range(N):
        subprocess.Popen(['python', 'map.py', str(i + 1)])
        sleep(1)
    
    for i in range(R):
        subprocess.Popen(['python', 'reduce.py', str(i + 1)])
        sleep(1)


def run():
    import sys
    global INPUT_PATH
    global M
    global R
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    consistency_pb2_grpc.add_Master_MapServicer_to_server(Master_MapService(), server)
    consistency_pb2_grpc.add_Master_ReduceServicer_to_server(Master_ReduceService(), server)
    server.add_insecure_port('[::]:8888')
    server.start()
    print(len(sys.argv))
    if(len(sys.argv) != 4):
        print("Usage: python master.py <input_path> <N> <R>")
        exit(1)
    
    INPUT_PATH = sys.argv[1]
    M = int(sys.argv[2])
    R = int(sys.argv[3])
    print(f'Input_path {INPUT_PATH}')
    print(f'M : {M} R : {R}')

    thread = threading.Thread(target=run_map_reduce,args=(M,R,))
    thread.start()
    


    server.wait_for_termination()

run()
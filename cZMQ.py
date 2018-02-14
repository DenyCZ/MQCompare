import math
import pandas as pd
from pandas import DataFrame
import zmq
import time
from openpyxl import load_workbook

class ZeroMQ:

    def __init__(self, channel_id):
        self.chId = channel_id
        self.times = []
        self.minTimes = []
        self.maxTimes = []
        self.avgTimes = []
        self.sizes = []
        self.context = zmq.Context()
        self.socketS = self.context.socket(zmq.REP)
        self.socketS.bind("tcp://*:5555")
        self.path = r"D:\ITIM\video2\MQCompare\times.xlsx"
        self.book = load_workbook(self.path)
        self.writer = pd.ExcelWriter(self.path, engine='openpyxl')
        self.writer.book = self.book
        
    def size(self, b64string):
        return str(len(b64string))

    def makebuffer(self, velikost):
        return int(velikost)*"A".encode("utf-8")
        
    def send(self, data):
        context = zmq.Context()
        socketC = context.socket(zmq.REQ)
        socketC.connect("tcp://localhost:5555")
        socketC.send(data)
        return time.time()
        
    def recv(self):    
        self.socketS.recv()
        self.socketS.send(b"OK")
        return time.time()
        
    def testLoop(self, test):
        for j in range(1,25):
            buffer = self.makebuffer(math.pow(2, j))
            self.sizes.append(math.pow(2,j))
            for i in range(1,11):
                sTime = self.send(buffer)
                rTime = self.recv()
                self.times.append(rTime - sTime)
            self.minTimes.append(str(int(round(min(self.times)*1000))))
            self.maxTimes.append(str(int(round(max(self.times)*1000))))
            self.avgTimes.append(str(int(round((sum(self.times) / float(len(self.times)))*1000))))
            self.output()   
            self.times = []
        self.socketS.close()
        self.context.term()
        
    def output(self):
        l1 = self.avgTimes
        l3 = self.minTimes
        l2 = self.maxTimes
        l4 = self.sizes
        df = DataFrame({'Avg [ms]': l1, 'Max [ms]':l2, 'Min [ms]':l3, 'Velikosti':l4})
        df.to_excel(self.writer, sheet_name='ZeroMQ', index=False)
        self.writer.save()
        
        
        
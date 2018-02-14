import math
import pandas as pd
from pandas import DataFrame
from kafka import KafkaConsumer, KafkaProducer
import time
from openpyxl import load_workbook

class KafkaMQ:

    def __init__(self, channel_id):
        self.chId = channel_id
        self.times = []
        self.minTimes = []
        self.maxTimes = []
        self.avgTimes = []
        self.sizes = []
        self.consumer = KafkaConsumer(bootstrap_servers='localhost:9092',auto_offset_reset='earliest', consumer_timeout_ms=1000)
        self.producer = KafkaProducer(bootstrap_servers='localhost:9002')
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
        self.producer.send('hello', data)
        return time.time()
        
    def recv(self):    
        for message in customer:
            print(message)
        return time.time()
        
    def testLoop(self, test):
        for j in range(1,25):
            buffer = self.makebuffer(math.pow(2, j))
            self.sizes.append(math.pow(2,j))
            self.consumer.subscribe(['hello'])
            for i in range(1,11):
                sTime = self.send(buffer)
                rTime = self.recv()
                self.times.append(rTime - sTime)
            self.minTimes.append(str(int(round(min(self.times)*1000))))
            self.maxTimes.append(str(int(round(max(self.times)*1000))))
            self.avgTimes.append(str(int(round((sum(self.times) / float(len(self.times)))*1000))))
            self.output()   
            self.times = []
        self.producer.close()
        self.consumer.close()
        
    def output(self):
        l1 = self.avgTimes
        l3 = self.minTimes
        l2 = self.maxTimes
        l4 = self.sizes
        df = DataFrame({'Avg [ms]': l1, 'Max [ms]':l2, 'Min [ms]':l3, 'Velikosti':l4})
        df.to_excel(self.writer, sheet_name='Kafka', index=False)
        self.writer.save()
        
        
        
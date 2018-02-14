import math
from pandas import DataFrame
import pandas as pd
import pika
import time
from openpyxl import load_workbook

class RabbitMQ:
    
    def __init__(self, channel_id):
        self.chId = channel_id
        self.times = []
        self.minTimes = []
        self.maxTimes = []
        self.avgTimes = []
        self.sizes = []
        self.path = r"D:\ITIM\video2\MQCompare\times.xlsx"
        self.book = load_workbook(self.path)
        self.writer = pd.ExcelWriter(self.path, engine='openpyxl')
        self.writer.book = self.book
        
    def size(self, b64string):
        return str(len(b64string))

    def makebuffer(self, velikost):
        return int(velikost)*"A".encode("utf-8")
        
    def send(self, data):
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        channel.queue_declare(queue='hello')
        channel.basic_publish(exchange='', routing_key='hello', body=data)
        connection.close()
        return time.time()
        
    def recv(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        channel.queue_declare(queue='hello')
        method_frame, header_frame, body = channel.basic_get(queue = 'hello')        
        if method_frame.NAME == 'Basic.GetEmpty':
            connection.close()
            return ''
        else:            
            channel.basic_ack(delivery_tag=method_frame.delivery_tag)
            connection.close() 
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
        
    def output(self):
        l1 = self.avgTimes
        l3 = self.minTimes
        l2 = self.maxTimes
        l4 = self.sizes
        df = DataFrame({'Avg [ms]': l1, 'Max [ms]':l2, 'Min [ms]':l3, 'Velikosti':l4})
        df.to_excel(self.writer, sheet_name='RabbitMQ', index=False)
        self.writer.save()
        
        
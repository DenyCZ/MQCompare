<<<<<<< HEAD
import sys
import pika
import base64
import datetime
import time

import os 
dir_path = os.path.dirname(os.path.realpath(__file__))

def size(b64string):
    return (len(b64string) * 3) / 4

def send(msg):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='hello')
    channel.basic_publish(exchange='', routing_key='hello', body=encoded_string)
    connection.close()
    return time.time()
    
def receive():
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

def calculate(i, sTime, rTime):
    val = rTime-sTime
    valms = int(round(val*1000))
    with open("test.txt", "a") as myFile:
        s = str(i) + ". " + str(valms) + "ms, " + str(val) + " unix\n"
        myFile.write(s)
        
for filename in os.listdir(dir_path):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        with open(filename, "rb") as imageFile:
            encoded_string = base64.b64encode(imageFile.read())
            with open("test.txt", "a") as myFile:
                s = "SENT " + str(size(encoded_string)) + " B\n"
                myFile.write(s)
            for i in range(1,11):
                sTime = send(encoded_string)
                rTime = receive()
                calculate(i, sTime, rTime)
    

=======
import sys
import pika
import base64
import datetime

connection = pika.BlockingConnection(pika.URLParameters('amqp://vxkguoqq:jEFv0BEO0iMiG3N0DpYd6L_hu3BVFn4x@duckbill.rmq.cloudamqp.com/vxkguoqq'))
channel = connection.channel()

def size(b64string):
    return (len(b64string) * 3) / 4

with open("image.jpg", "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read())
    with open("test.txt", "a") as myfile:
        s = "FILE LENGTH = " + str(size(encoded_string)) + " BYTES\n"
        myfile.write(s)

    
for i in range(1,10):
    print(" [x] SSending'")
    channel.basic_publish(exchange='',
                      routing_key='hello',
                      body=encoded_string)
    print(" [x] Sent message")
    with open("test.txt", "a") as myfile:
        s = datetime.datetime.now();
        myfile.write(str(i) + ". " + str(s) + "\n")

connection.close()
>>>>>>> 22555f44e260c493d94d5298f75abbd2851f6e07

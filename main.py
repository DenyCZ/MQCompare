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
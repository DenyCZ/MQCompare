import pika
import datetime

url = 'amqp://vxkguoqq:jEFv0BEO0iMiG3N0DpYd6L_hu3BVFn4x@duckbill.rmq.cloudamqp.com/vxkguoqq'

connection = pika.BlockingConnection(pika.URLParameters(url))
channel = connection.channel()


def callback(ch, method, properties, body):
    with open("test.txt", "a") as myfile:
        s = "RECEIVE - " + str(datetime.datetime.now()) + "\n"
        myfile.write(s)

channel.basic_consume(callback,
                      queue='hello',
                      no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()


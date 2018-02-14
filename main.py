from cRMQ import RabbitMQ
from cZMQ import ZeroMQ
from cKafka import KafkaMQ

kq = KafkaMQ("Hello")
kq.testLoop(kq)

#for i in range(1,6):
#    print("Testing RabbitMQ")
#    rq = RabbitMQ("hello")
#    rq.testLoop(rq)
#    print("Testing ZeroMQ")
#    zmq = ZeroMQ("hello")
#    zmq.testLoop(zmq)

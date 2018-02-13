import zmq
import os 
import base64
import time

dir_path = os.path.dirname(os.path.realpath(__file__))


context = zmq.Context()
context2 = zmq.Context()

# Starting server
print("Starting server")
socketS = context2.socket(zmq.REP)
socketS.bind("tcp://*:5555")

#  Socket to talk to server
print("Connecting to hello world server...")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

def size(b64string):
    return (len(b64string) * 3) / 4

def send(msg):
    socket.send(msg)
    return time.time()

def receive():
    socketS.recv()
    socketS.send(b"OK")
    return time.time()

def writedown(val):
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
            for i in range(1,21):
                timeS = send(encoded_string)
                timeR = receive()
                socket.recv()
                writedown(timeR - timeS)

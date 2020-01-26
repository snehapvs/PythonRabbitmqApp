import pika
import numpy as np
import json,codecs
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='hello')

datafile='code_challenge_data1.csv'
data1 = np.loadtxt(datafile, delimiter=',', skiprows=1)
data1.reshape(-1,1)
data1=data1[:,1:4]

def default(obj):
    if type(obj).__module__ == np.__name__:
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return obj.item()
    raise TypeError('Unknown type:', type(obj))

bdy = json.dumps(data1, default=default)

print(bdy,type(bdy))
channel.basic_publish(exchange='', routing_key='hello', body=bdy)
print(" [x] Sent 'Hello World!'")
connection.close()

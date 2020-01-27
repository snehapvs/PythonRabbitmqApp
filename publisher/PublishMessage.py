import pika
import numpy as np
import json,codecs
import uuid
import os
import sys
import logging
log = logging.getLogger("my-logger")
class Publisher:
    def default(self,obj):
        if type(obj).__module__ == np.__name__:
            if isinstance(obj, np.ndarray):
                return obj.tolist()
            else:
                return obj.item()
        raise TypeError('Unknown type:', type(obj))

    def __init__(self,datafile):
        self.setup_queue() #create a rabbitmq queue
        if self.connection or self.connection.is_closed:
            self.setup_queue()
        data1 = np.loadtxt(datafile, delimiter=',', skiprows=1)
        data1.reshape(-1,1)
        for row in data1:
            data=[row[1:4]]
            bdy = json.dumps(data, default=self.default)
            log.info(" Sent ",bdy," to Queue")
            response=self.publish_data_to_predictorqueue(bdy)
            log.info(" Probability that the given source belongs to Class 1 :  ",response)
            
    def setup_queue(self): 
        
        """ create a rabbitmq connection with rpc like setup to send request and receive back the response  """
    
        amqp_url = os.environ['AMQP_URL']
        log.info('Connecting in Publisher to : ' , amqp_url)
        self.parameters = pika.URLParameters(amqp_url)
        self.connection = pika.BlockingConnection(self.parameters)
        self.channel = self.connection.channel()
        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue
        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)    
         
    def publish_data_to_predictorqueue(self, data):
        
        """sending data to predictor and setting up the call back queue to receive back the response"""
        
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='Predictor',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=data)
        while self.response is None:
            self.connection.process_data_events()
        return float(self.response)


    def on_response(self, ch, method, props, body):
        
        """ get response and compare the correlation id to process the response"""
        
        if self.corr_id == props.correlation_id:
            self.response = body

if __name__ == "__main__": 
    args=sys.argv[1:]
    log.info("Data source given : ",os.environ['SOURCE'])
    datafile=os.environ['SOURCE']
    p=Publisher(datafile)
    


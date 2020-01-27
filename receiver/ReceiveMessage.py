import pika
import json,codecs
import numpy as np
import pickle
import os
import logging
log = logging.getLogger("my-logger")
class PredictorReceiver():
    def on_request(self,ch, method, props, body):
        modelfile ='code_challenge_model.p'
        message = json.loads(body)
        data = np.array(message)
        log.info("Received data : " , data)
        response=self.predict(modelfile,data)
        ch.basic_publish(exchange='',
                         routing_key=props.reply_to,
                         properties=pika.BasicProperties(correlation_id = \
                                                             props.correlation_id),
                         body=str(response))
        ch.basic_ack(delivery_tag=method.delivery_tag)
        
    def predict(self,modelfile,data):
        infile = open(modelfile,'rb')
        model = pickle.load(infile, encoding='bytes')
        a1=model.predict_proba(data)[0,1]
        return a1
    
    def __init__(self):

        self.setup_connection()
        if self.connection or self.connection.is_closed:
            self.setup_connection()
            
    def setup_connection(self):
        amqp_url = os.environ['AMQP_URL']
        log.info('Connecting in Receiver to : s' , amqp_url)
        self.parameters = pika.URLParameters(amqp_url)
        self.connection = pika.BlockingConnection(self.parameters)
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='Predictor')
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue='Predictor', on_message_callback=self.on_request)
        log.info("Awaiting Data requests")
        self.channel.start_consuming()
        
        
if __name__ == "__main__": 
    p=PredictorReceiver()
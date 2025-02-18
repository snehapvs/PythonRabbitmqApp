import pika
import json
import numpy as np
import pickle
import os
import warnings
warnings.filterwarnings("ignore")
import logging

class PredictorReceiver():
    def on_request(self, ch, method, props, body):
        
        message = json.loads(body)
        datamessage = np.array(message)
        print("Received data : ", datamessage)
        response = self.predict(self.modelfile, datamessage)
        ch.basic_publish(exchange='',
                         routing_key=props.reply_to,
                         properties=pika.BasicProperties
                         (correlation_id=props.correlation_id),
                         body=str(response))
        ch.basic_ack(delivery_tag=method.delivery_tag)
        
    def predict(self, modelfile, data):
        infile = open(modelfile, 'rb')
        model = pickle.load(infile, encoding='bytes')
        prob = model.predict_proba(data)[0, 1]
        return prob
    
    def __init__(self):
        self.modelfile = 'code_challenge_model.p'
        self.setup_connection()
        if self.connection or self.connection.is_closed:
            self.setup_connection()
            
    def setup_connection(self):
        amqp_url = os.environ['AMQP_URL']
        print('Connecting in Receiver to : ', amqp_url)
        self.parameters = pika.URLParameters(amqp_url)
        self.connection = pika.BlockingConnection(self.parameters)
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='Predictor')
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue='Predictor', 
                                   on_message_callback=self.on_request)
        print("Awaiting Data requests")
        self.channel.start_consuming()
        
        
if __name__ == "__main__": 
    try:
        p = PredictorReceiver()
    except:
        print("There is an error in establishing connection for queue in Receiver")

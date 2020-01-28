import pika
import numpy as np
import json
import uuid
import os
import logging
from flask import Flask
from flask_restful import Resource, Api
logging.getLogger('pika').setLevel(logging.INFO)


class Publisher:
    def __init__(self):
        self.setup_queue()  # create a rabbitmq queue
        if self.connection or self.connection.is_closed:
            self.setup_queue()
           
    def setup_queue(self): 
       
        """ create a rabbitmq connection with rpc like setup to send request 
        and receive back the response  """
    
        amqp_url = os.environ['AMQP_URL']
        print('Connecting in Publisher to : ', amqp_url)
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
        
        """sending data to predictor and setting up the call back queue 
        to receive back the response"""
        
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
        
        """get response and compare the correlation id 
        to process the response"""
        
        if self.corr_id == props.correlation_id:
            self.response = body
            
            
class DataSourceHandler(Resource):
    
    def dataDefault(self, obj):
        
        """ default object to process data from json """
        
        if type(obj).__module__ == np.__name__:
            if isinstance(obj, np.ndarray):
                return obj.tolist()
            else:
                return obj.item()
        raise TypeError('Unknown type:', type(obj))
    
    def get(self, dataSource):
        
        """ API method to return probability data response """ 
        try:
            print("Data source given : ", dataSource)
            try:
                publisher = Publisher()
            except:
                result = {"Error" :"There is an error in Establishing Rabbitmq connection in publisher"}
            try:
                sourceData = self.getSourceData(dataSource)
                result = self.getResponseProbabilityData(sourceData, dataSource, publisher)
            except:
                result = {"Error" :"There is an error in Processing data"}
            
            return (json.loads(json.dumps(result)))
        except:
            result = {"Error" :"There is an error in Publishing data"}
            return result
        
    
    def getSourceData(self, dataSource):
        
        """processing data with numpy"""
        
        sourceData = np.loadtxt(dataSource, delimiter=',', skiprows=1)
        sourceData.reshape(-1, 1)
        return sourceData
    
    def getResponseProbabilityData(self, sourceData, dataSource, publisher):
        
        """getting predictor data result, sending one row at a time to the queue
        assuming data file can be huge """
        
        result = []
        for row in sourceData: 
            requestData = row[1:4]
            requestData = requestData.reshape(1, -1)
            requestBody = json.dumps(requestData, default=self.dataDefault)
            print("Sent ", requestBody, " to Queue")
            response = publisher.publish_data_to_predictorqueue(requestBody)
            print(" Probability that the given source belongs to Class 1 : ", response)
            result.append({'dataSource': dataSource,
                           'inputData': requestBody, 'probability': response})
        return result
    
    
app = Flask(__name__)
api = Api(app)
api.add_resource(DataSourceHandler, "/api/predict/<dataSource>")

  
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)

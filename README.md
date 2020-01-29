## Rabbitmq
### Prerequisites
* Docker

### Running the application:
```sh
$ docker-compose up // from application's location
``` 
* From browser run the following 

` http://localhost:5001/api/predict/<dataSource> `

  Ex:
  ` http://localhost:5001/api/predict/code_challenge_data1.csv ` for first input data source
  
  ` http://localhost:5001/api/predict/code_challenge_data2.csv ` for second input data source
  
 OR 
 
* From Terminal Run the follwoing to input first data source
 
 `curl -X GET 'http://localhost:5001/api/predict/code_challenge_data1.csv'`
  
  or
  
* to give second data source as input
  
  `curl -X GET 'http://localhost:5001/api/predict/code_challenge_data2.csv'`
  
### Design Constaints and Assumptions:
* Used print statements in place of logging.info as logging module is efefcting pika module for establishing rabbitmq server conenction
* Added Publisher and Receiver as different services and respective requirements and dockerfile is added accordingly.
* Rabbitmq configuration is added in the docker-compsoe file directly
* Used Flask-restful to add a API endpoint to switch between input data sources easyly (this could be done via an environment variable too)
* Sending one row at a time to the queue from the publisher,As data file can be huge and sending the full data to queue might not be ideal in that case. Also,Giving predicted probability data as a list with each row's probability separately.


### Python Modules Used : all modules are mentioned in requiements.txt 
* pika for rabbitmq module
* flask-restful for to publish different data sources to queue
* numpy for data processing

### Improvements:
* Tests can be added and Exceptions can be handled better
* Here since the the data files are already available,the input service is taken as a GET request with the datafile name as a string param.To make it more dynamic, we can use a POST service and upload file from there directly.


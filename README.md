## Code Challenge
#### Prerequisites
* Docker

#### Running the application:
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
 
 `curl -X GET \
  'http://localhost:5001/api/predict/code_challenge_data1.csv'`
  
  or to give second data source as input
  
  `curl -X GET \
  'http://localhost:5001/api/predict/code_challenge_data2.csv'`
  


## Python Modules Used : all modules are mentioned in requiements.txt 
* pika for rabbitmq module
* flask-restful for to publish different data sources to queue
* numpy for data processing


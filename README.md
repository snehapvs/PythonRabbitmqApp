"""
docker-compose build
env SOURCE='code_challenge_data1.csv' 
docker-compose up
"""
## Prerequisites
* Docker

#### Running the application:

$ docker-compose up // from application's location

From browser run the following 
http://localhost:5001/api/predict/<dataSource> 
  Ex:
  http://localhost:5001/api/predict/code_challenge_data2.csv
  
 or 
 From Terminal Run the follwoing to input first data source
 `curl -X GET \
  'http://localhost:5001/api/predict/code_challenge_data1.csv'`
  or to give second data source as input
  `curl -X GET \
  'http://localhost:5001/api/predict/code_challenge_data2.csv'`
  


## Python Modules Used :
* used spring-boot for REST framework.
* h2 for database, as it is an embedded database ideal for test applications.
* git for version control.

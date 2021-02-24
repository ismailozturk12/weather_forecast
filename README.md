### Core dependencies
  - Python 3.7
  - Django
  - Postgresql

## How to run?
```sh
$ docker-compose up --build
```

## API Documentation
#### POST Weather

##### Request
```
Method: POST
Url: /weather/?city=istanbul
```
##### Successful Response
```
Response Code: 200
Body:   
{
    "city": "istanbul",
    "currently_temperature": 8.97,
    "daily_temperature_max": 9.5,
    "daily_temperature_min": 4.63,
    "weekly_temperature_max": 13.41,
    "weekly_temperature_min": 5.47
}
```
#### Create User
Creates a new user in the db
##### Request
```
Method: POST
Url: /user
{
    "username": "admin",
    "password": "admin"
}
```
##### Successful Response
```
Response Code: 201
Body:   
{
    "username": "admin",
    "password": "pbkdf2_sha256$216000$UMSSHEO1bt02$WkSDqqYRYVTlK6JO/PxbMij/WfHECt7yqyR5MQJMKBw="
}
```
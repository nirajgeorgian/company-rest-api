# **company backend api**
#### (written in [_flask_](http://flask.pocoo.org))

## to test the app globally the app is hosted on (dododuck)[https://dododuck.herokuapp.com]. <== `heroku` app link
## How to `run` the app
```
git clone https://github.com/nirajgeorgian/company-rest-api
cd company-rest-api
pip install -r requirements.txt
source .env
flask run
```

> It will start one local server on [`http://localhost:5000`](http://localhost:5000)

### if any error due to database or something please add migrations
```
flask db init
flask db migratie
```

## Some `Key Feature`
- app api are preceded with '/api/v1'
- every endpoint is properly unit tested using unittest
- postgresql is used for development
- to change database url simple change the variable `DEFAULT_TEST_DB_URL` inside config.py appropiately
- chnage format for database
- `postgresql://{username}:{password}@host:port/database`

## and to run `test`
```
python run_tests.py
```

## Running in postman
for viewing the api endpoint's in postman simply import the company-rest-collection.postman_collection.json file into postman
and i have written postman script which after login set's up the JWT_KEY to the entire app.
postman also uses one environment with two variable
```
API_URL=http://localhost:3030
# for globally
API_URL=https://dododuck.herokuapp.com
JWT_KEY="YOUR_JWT_TOEKN"
```
JWT_KEY will be automatically populated after login

### Author: [`@nirajgeorgian`](https://github.com/nirajgeorgian)

# sap_server

*Recommend: Python 3.6*
            *PostgresSQL 11.1*

# Installation

First install virtualenv if you haven't `pip install virtualenv`

Next, generate virtualenv `virtualenv venv`

Then, activate virtualenv `source venv/Scripts/activate` and `deactivate` to deactivate.

Last install dependencies run `pip install -r requirements.txt`

Copy and rename `.envexample` file to `.env` and provide proper settings:

`cp .envexample .env`

#installation of the postgresql database

Installation command:
`apt-get install postgresql-10`

Creation of a user:
`sudo -u postgres createuser <username>`
           
Creation of the database
`sudo -u postgres createdb <dbname>`

Giving the user a password
`sudo -u postgres psql
psql=# alter user <username> with encrypted password '<password>';`

Grant privileges on the database
`psql=# grant all privileges on database <dbname> to <username>;`

# Running tests

If you want to run tests with `python manage.py jenkins` make sure to give the user the ability to create databases.

# Test RPC call
```
curl -X POST \
http://127.0.0.1:8000/rpc/ \
-H 'Content-Type: application/json' \
-d '{"jsonrpc": "2.0", "method": "echo", "params": ["echo this"], "id": 1}'
```

# Launch server:

`python manage.py runserver`
# API documentation
The API documentation can be found on http://localhost:8000/rpc-doc

# SonarQube
Download and install SonarQube server
https://docs.sonarqube.org/7.4/setup/get-started-2-minutes/

Then download and install SonarQube scanner
https://docs.sonarqube.org/display/SCAN/Analyzing+with+SonarQube+Scanner

Copy and set the right values

`cp sonar-project.propertiesexample sonar-project.propertie`
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

Launch server:

`python manage.py runserver`
# API documentation
The API documentation can be found on http://localhost:8000/rpc-doc
# Test RPC call
```
curl -X POST \
http://127.0.0.1:8000/rpc/ \
-H 'Content-Type: application/json' \
-H 'Postman-Token: c7b1be21-e4eb-45eb-b91a-3d0a1ecd6c27' \
-H 'cache-control: no-cache' \
-d '{"jsonrpc": "2.0", "method": "test", "params": [], "id": 1}'
```

# sap_server
First install virtualenv if you haven't `pip install virtualenv`

Next, generate virtualenv `virtualenv venv`

Then, activate virtualenv `source venv/Scripts/activate` and `deactivate` to deactivate.

Last install dependencies run `pip install -r requirements.txt`

If MySQL doesn't install work `pip install --only-binary :all: mysqlclient`

#Test RPC call
```
curl -X POST \
http://127.0.0.1:8000/rpc/ \
-H 'Content-Type: application/json' \
-H 'Postman-Token: c7b1be21-e4eb-45eb-b91a-3d0a1ecd6c27' \
-H 'cache-control: no-cache' \
-d '{"jsonrpc": "2.0", "method": "test", "params": [], "id": 1}'
```
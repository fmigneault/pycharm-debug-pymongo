## Install 

```shell
pip install -r requirements.txt
pip install -e . 
```

## Running

Find `pserve` (installed via `gunicorn` in above requirements) and call it with `config.ini`.

```shell
$(which pserve) "$(realpath -p config.ini)"
```


## Operations

Create a service: 

```shell
curl -X POST -d '{"name": "new-service"}' "http://localhost:4000/services" -H "Content-Type: application/json"
```

Fetch a service:
```shell
curl -X GET "http://localhost:4000/services/new-service"
```

Delete a service:
```shell
curl -X DELETE "http://localhost:4000/services/new-service"
```

List all services:
```shell
curl -X GET "http://localhost:4000/services"
```

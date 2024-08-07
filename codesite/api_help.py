# GET
>>> import requests
>>> api_url = "https://jsonplaceholder.typicode.com/todos/1"
>>> api_url = "https://ukasz.eu.pythonanywhere.com/python/api/solutions/1/"
>>> response = requests.get(api_url)
>>> response.json()
{'userId': 1, 'id': 1, 'title': 'delectus aut autem', 'completed': False}

>> response.status_code
200

>>> response.headers["Content-type"]
'application/json; charset=utf-8'

# POST
api_url = "https://jsonplaceholder.typicode.com/todos"
todo = {"userId": 1, "title": "Buy milk", "completed": False}
response = requests.post(api_url, json=todo)
response.json()
{'userId': 1, 'title': 'Buy milk', 'completed': False, 'id': 201}

# PUT
>>> api_url = "https://jsonplaceholder.typicode.com/todos/10"
>>> response = requests.get(api_url)
>>> response.json()
{'userId': 1, 'id': 10, 'title': 'illo est ratione doloremque quia maiores aut', 'completed': True}
>>> todo = {"userId": 1, "title": "Wash car", "completed": True}
>>> response = requests.put(api_url, json=todo)
>>> response.json()

# PATCH
response = requests.patch(api_url, json=todo)

# DELETE
>>> import requests
>>> api_url = "https://jsonplaceholder.typicode.com/todos/10"
>>> response = requests.delete(api_url)
>>> response.json()
{}

>>> response.status_code
200


# GET request to Codesite:
$ curl -i http://127.0.0.1:8000/python/api/languages/ -w '\n'
$ curl -i https://ukasz.eu.pythonanywhere.com/python/api/languages/ -w '\n'

$ curl -i https://ukasz.eu.pythonanywhere.com/python/api/languages/1/ -w '\n'

# POST
$ curl -i https://ukasz.eu.pythonanywhere.com/python/api/languages/ \
-X POST \
-H 'Content-Type: application/json' \
-d '{"name":"Java"}' \
-w '\n'

$ curl -i https://ukasz.eu.pythonanywhere.com/python/api/solutions/ \
-X POST \
-H 'Content-Type: application/json' \
-d '{"problem":"Some"}' \
-w '\n'





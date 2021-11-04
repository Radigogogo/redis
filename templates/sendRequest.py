import requests
for x in range(10000):
    response = requests.get("http://localhost/demo")
    print(response)

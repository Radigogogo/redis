import requests
for x in range(1000):
    response = requests.get("http://localhost/demo")
    print(response)

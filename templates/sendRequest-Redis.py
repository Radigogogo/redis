import requests
for x in range(1000):
    response = requests.get("http://localhost/demo-redis")
    print(response)

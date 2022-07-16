import requests

response = requests.get("https://embedded-hust.herokuapp.com/api/test")

print(response.json())

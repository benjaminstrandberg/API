import requests

BASE = "http://127.0.0.1:5000/"

response = requests.post(BASE + "recipes", { "name":"BaconAndEggs", "ingredients" : ["Bacon","Egg"],"amount":[100,100]})
print(response.json())

# input()

# response = requests.get(BASE + "recipes", {"name":"all"})
# print(response.json())


#[("Bacon",100),("Eggs",100)]
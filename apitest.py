import requests

BASE = "http://127.0.0.1:5000/"

# response = requests.post(BASE + "recipes", { "name":"BaconAndEggs", "ingredients" : ["Bacon","Egg"],"amount":[100,100]})
# print(response.json())

# # input()

response = requests.get("https://cohesive-photon-346611.ew.r.appspot.com/" + "recipes", {"name":"all"})
print(response.text)

#https://cohesive-photon-346611.ew.r.appspot.com

#[("Bacon",100),("Eggs",100)]
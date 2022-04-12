import requests

BASE = "http://127.0.0.1:5000/"
URL = "https://cohesive-photon-346611.ew.r.appspot.com/recipes"

# response = requests.post(BASE + "recipes", { "name":"BaconAndEggs", "ingredients" : ["Bacon","Egg"],"amount":[100,100]})
# print(response.json())

 # input()

response = requests.get("https://cohesive-photon-346611.ew.r.appspot.com/recipes", {"name":"Carbonara"})
#response = requests.get("https://cohesive-photon-346611.ew.r.appspot.com/recipes")
print(response.text)



#[("Bacon",100),("Eggs",100)]
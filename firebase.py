import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from Recipe import Recipe
from flask import Flask
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

#ALL returns ALL RECIPES
# ? == space in curl request

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

#Lägger upp recept på databasen 
def addData(recipe:Recipe):
    ref = db.collection(u"Recipes").document(recipe.name)
    if(ref.get().exists):
        print("Recipe couldn't be added, choose another name!")
        return
    ref.set({'ingredients' : ["(" + str(i[1]) + "g" + ", " + i[0].name + ")" for i in recipe.ingredients]})
    ref.update({db.field_path('Total CO2-eq') : "{:.2f}".format(recipe.getTotalCo2())})
    ref.update({db.field_path('nutrition') : ["Fat: " + str(recipe.getTotalFat()), 
                                              "Carbs: " + str(recipe.getTotalCarbs()),                                             
                                              "Protein: " + str(recipe.getTotalProtein()),
                                              "Kcal: " + str(recipe.getTotalKcal())]})
    ref.update({db.field_path('name') : recipe.name})

#Returnerar receptet name
def getRecipes(name): 
    result = db.collection('Recipes').document(name).get()
    if result.exists:
        return (result.to_dict())
    return None

#Returnerar hela collectionen Recipes
def getCollection():
    docs = db.collection('Recipes').get()
    a = list()
    for i in docs:
        a.append(i.to_dict())
    return a

#Returnerar en lista av alla recept som innehåller ingrediensen string
def recipeContains(string):
    reference = db.collection('Recipes').get()
    recipes = list()
    for j in reference:
        if j.to_dict()['name'] == string:
            recipes.append(j.to_dict()['name'])
    if recipes == []:
        for i in reference:
            temp = i.to_dict()
            l = list(temp['ingredients'])
            for x in l:
                if(string in x):
                    recipes.append(temp['name'])
    return recipes
    
    
def deleteRecipes(name):
    db.collection('Recipes').document(name).delete()
            
class Recipes(Resource):

    # Hämtar data om recept
    # argument: all -> returnerar dictionary med lista av alla recept i databasen
    # argument: namn på ingrediens -> returnerar lista med namn på alla recept som innehåller den ingrediensen
    # argument: namn på recept -> returnerar det receptet om det finns
    # no results returneras om ingrediensen eller receptet inte finns
    # automatiskt felmeddelande om argumentet saknas
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("name",type=str,help = "name of recipe or ingredient is required",required = True)
        args = parser.parse_args()

        if(args["name"] == 'all'):
            hej = getCollection()
            return {'data': hej},200

        recipes = getRecipes(args["name"])
        if(recipes != None):
            return recipes,200
        result = recipeContains(args["name"])
        if result != []:
            return result,200
        return "No results"

    #Lägger till recept
    #argument: lista av ingredienser & lista av mängden av varje ingrediens, ingrediens[0] hör ihop med mängd[0] osv
    #          anledning till detta är för att requestparser ej kan tolka nästlade strukturer såsom [(bacon,100g),...]
    # automatiskt felmeddelande om något av argumenten saknas
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("name",type=str,help = "name of recipe is required",required = True,location = 'form')
        parser.add_argument("ingredients", action = 'append',help = "ingredients are required",required = True, location = 'form')
        parser.add_argument("amount", action = 'append', help = "amounts are required",required = True, location = 'form')
        args = parser.parse_args()
        ings = list(zip(args['ingredients'],args['amount']))
        
        r = Recipe(args['name'], *ings)
        addData(r)
        return {'Successfully added':args['name']}

api.add_resource(Recipes,'/recipes')

if __name__ == "__main__":
    app.run(debug=True)





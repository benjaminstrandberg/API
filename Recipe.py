import pandas
from Ingredient import Ingredient
import re

# ingredients = [('Chicken',200)]
class Recipe:
    def __init__(self, name, *ingredients):
        self.name = name
        self.ingredients = [((self.getDataFromIngredient(ing[0])),ing[1]) for ing in ingredients]
        
    def toString(self):
        s = ""
        for i in self.ingredients:
            s += "|" + i[0].name + "," + str([key + ": " + i[0].attributes[key] for key in i[0].attributes]) + "|"
        return s
    
    def toFirebase(self):
        return {'name' : self.name , 'ingredients' : self.toString()}

    def getDataFromIngredient(self,ingredient):
        document = pandas.read_excel("braformatlivsmedelsdata.xlsx",sheet_name='Ra_500food')
        row = document.loc[ingredient == document['Namn']]
        name = "".join(filter(lambda x: not x.isdigit(), row['Namn'].to_string())).strip()
        co2 = re.sub(r"^[0-9]*\s*","",row['Total kg CO2-eq/kg'].to_string(),1)
        fat = re.sub(r"^[0-9]*\s*","",row['Fett (g/100 g)'].to_string(),1)
        protein = re.sub(r"^[0-9]*\s*","",row['Protein (g/100 g)'].to_string(),1)
        carbohydrates = re.sub(r"^[0-9]*\s*","",row['Kulhydrat (g/100 g)'].to_string(),1)
        kcal = re.sub(r"^[0-9]*\s*","",row['Energi (KJ/100 g)'].to_string(),1)

        attributes = {'co2':co2,'fat':fat,'protein':protein,'carbs':carbohydrates,'kcal':kcal}

        obj = Ingredient(name,attributes)
        return obj
    
    def getTotalFat(self):
        total = 0
        tmp = 0
        for i in self.ingredients:
            tmp = (float(i[0].attributes['fat']) / 100) * float(i[1])
            total = total + tmp
            tmp = 0
        return total//1

    def getTotalProtein(self):
        total = 0
        tmp = 0
        for i in self.ingredients:
            tmp = (float(i[0].attributes['protein']) / 100) * float(i[1])
            total = total + tmp
            tmp = 0
        return total//1

    def getTotalCarbs(self):
        total = 0
        tmp = 0
        for i in self.ingredients:
            tmp = (float(i[0].attributes['carbs']) / 100) * float(i[1])
            total = total + tmp
            tmp = 0
        return total//1

    def getTotalKcal(self):
        total = 0
        tmp = 0
        for i in self.ingredients:
            tmp = (float(i[0].attributes['kcal']) / 100) * float(i[1])
            total = total + tmp
            tmp = 0
        return (total * 0.2390057361)//1

    def getTotalCo2(self):
        total = 0
        tmp = 0
        for i in self.ingredients:
            tmp = (float(i[0].attributes['co2']) / 1000) * float(i[1])
            total = total + tmp
            tmp = 0
        return total

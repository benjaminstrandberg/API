class Ingredient:
    # co2, fat, protein, kcal, carbs
    def __init__(self,name,attributes): 
        self.name = name
        self.attributes = attributes
        
    def toFirebase(self):
        return {'name':self.name, 'attributes' : [key + self.attributes[key] for key in self.attributes]}
"""
These classes are for a POS at a grocery store. The Food class is the base class
and Produce, Alcohol, and Frozen are subclasses. Each inherit name and unitPrice from
the base class. Depending on the situation, each subclass has its own specific
methods for the POS to deal with.

The 3 design patterns used here are: Factory, Facade, and Prototype.
The FoodFactory class easily instantiates an object from a subclass that inherits from the Food class.
FoodFacade creates a menu interface to easily input an item code to instantiate the object.
Prototype is used in the Receipt class to make copies of receipts and even gift receipts
"""


from abc import ABCMeta, abstractmethod #imports abstract base class and abstract methods for that class
import datetime
import random
import copy

class Food(metaclass=ABCMeta):
    def __init__(self, name, unitPrice):
        self.name = name
        self.unitPrice = unitPrice
        
    @abstractmethod
    def getTax(self): #cannot be called/instatiated from the base class
        pass
    
    def discount(self, percentOff):
        decimal = percentOff / 100
        self.unitPrice *= (1 - decimal)
        
    def __str__(self):
        return "{}\nUnit Price: ${:.2f}\n".format(self.name, self.unitPrice)
    
class Produce(Food):
    def __init__(self, name, unitPrice, weight, isOrganic = False):
        super().__init__(name, unitPrice)
        self.weight = weight #in pounds
        self.isOrganic = isOrganic #can be used for statistical analysis and business decisions
        self.taxAmt = self.getTax()
        self.totalPrice = unitPrice * self.weight * (1+ self.taxAmt)
        
    def getTax(self): #each subclass has it's own tax rate
        taxAmt = 0.0
        return taxAmt
    
    def getWeight(self): 
        return self.weight
    
    def setWeight(self, w): #produce is usually weighed at the register and can be adjusted if you add more items
        self.weight = w
        return self.weight
    
    def __str__(self):
        return "\n{}\nUnit Price: ${:.2f}\nWeight: {:.2f} lbs.\nTotal Price: ${:.2f}\n".format(self.name, self.unitPrice, self.weight, self.totalPrice)
    
class Alcohol(Food):   
    def __init__(self, name, unitPrice, abv, ofAge = False):
        super().__init__(name, unitPrice)
        self.abv = abv #percent alcohol by volume
        self.ofAge = ofAge #Of age to purchase set to False until ID is verified
        self.taxAmt = self.getTax()
        self.totalPrice = unitPrice * (1 + self.taxAmt)
        
    def getTax(self): #beer, wine, and spirits have different tax amounts
        if self.abv <= 10: 
            taxAmt = 0.05 #these percentages are just examples (amounts vary state to state)
        elif self.abv > 10 and self.abv <= 20:
            taxAmt = 0.1
        else:
            taxAmt = 0.2
        return taxAmt
    
    def verifyId(self, year, month, date):
        birthday = datetime.datetime(year, month, date)
        today = datetime.datetime.today()
        dateStr = str((today - birthday)/365.25) #divides the days into years and converts the long datetime object to a string
        age = int(dateStr[:2]) #converts the first two characters of that string to an int
        if age >= 21:
            self.ofAge = True
        else:
            print("Not of age. Purchase prohibited.\n")       
    
    def __str__(self):
        return "\n{}\nUnit Price: ${:.2f}\nABV: {:.1f}%\nAlcohol Tax: {}%\nTotal Price: ${:.2f}\n".format(self.name, self.unitPrice, self.abv, self.taxAmt*100, self.totalPrice)

class Frozen(Food):
    def __init__(self, name, unitPrice, year, month, date, quantity = 1):
        super().__init__(name, unitPrice)
        self.expiration = datetime.datetime(year, month, date)
        self.quantity = quantity
        self.taxAmt = self.getTax()
        self.totalPrice = unitPrice * self.quantity * (1 + self.taxAmt)
        
    def getTax(self):
        taxAmt = 0.0
        return taxAmt
    
    def getQuantity(self):
        return self.quantity
    
    def setQuantity(self, q): #can have option to change quantity instead of scanning the same item multiple times
        self.quantity = q
        return self.quantity
    
    def expired(self):
        today = datetime.datetime.today()
        if today > self.expiration:
            print("Item has expired, please replace.")
            return True
        else:
            return False
        
    def __str__(self):
        return "\n{}\nUnit Price: ${:.2f}\nQuantity: {}\nTotal Price: ${:.2f}\n".format(self.name, self.unitPrice, self.quantity, self.totalPrice)

class FoodFactory(object): #does not need to be instantiated, used for its class method
    @classmethod
    def create(cls, name, *args): #takes in class name and and arguments needed for that class
        name = name.lower().strip() #since classes are usually capitalized, this simplifies it
        
        #Factory pushes out objects easily depending on the parameters it receives
        if name == "produce":
            return Produce(*args) 
        elif name == "alcohol":
            return Alcohol(*args)
        elif name == "frozen":
            return Frozen(*args)

class FoodFacade:
    def __init__(self, code = None): #takes an input to find the needed item to instatiate. Can add more items.
        self.code = input("[1]Apple \n[2]Potato \n[3]Cilantro \n[4]Beer \n[5]Wine \n[6]Whiskey \n[7]Ice Cream \n[8]TV Dinner \n[9]Pizza Rolls \n[0]Cancel \nInput number of your item: ")
        
    def getItem(self): #takes code and instatiates an object based on it's known price and values    
        if self.code == "1":
            weight = input("Weigh Item? (y/n)") #replicates action of weighing produce on the checkout scale
            if weight == "y":
                weight = random.randint(1, 5) #this is just a random number as a placeholder for the real weight
                return FoodFactory.create("Produce", "Apple", 0.75, weight)
        if self.code == "2":
            weight = input("Weigh Item? (y/n)")
            if weight == "y":
                weight = random.randint(1, 5)
                return FoodFactory.create("Produce", "Potato", 0.65, weight)
        if self.code == "3":
            weight = input("Weigh Item? (y/n)")
            if weight == "y":
                weight = random.randint(1, 5)
                return FoodFactory.create("Produce", "Cilantro", 0.50, weight)
        if self.code == "4":
            return FoodFactory.create("Alcohol", "Beer", 12.00, 5)
        if self.code == "5":
            return FoodFactory.create("Alcohol", "Wine", 30.00, 13)
        if self.code == "6":
           return FoodFactory.create("Alcohol", "Whiskey", 39.00, 40)
        if self.code == "7":
            return FoodFactory.create("Frozen", "Ice Cream", 8.00, 2020, 8, 31)
        if self.code == "8":
           return FoodFactory.create("Frozen", "TV Dinner", 5.00, 2020, 8, 2)
        if self.code == "9":
            return FoodFactory.create("Frozen", "Pizza Rolls", 12.00, 2020, 9, 30)

class Prototype:
    def clone(self):
        return copy.deepcopy(self) #imported the copy class to be able to use the clone method
    
class Receipt(Prototype): #inherite the Prototype class's clone method
    def __init__(self, groceryList):
        self.groceryList = groceryList #an array with all the items
        self.total = 0
        
    def totalPrice(self):
        for each in self.groceryList:
            self.total += each.totalPrice
    
    def __str__(self):
        return "Receipt Total: " + str(self.total)
    
def main():
    
    lineItem1 = FoodFacade().getItem() #the getItem() method uses the FoodFactory to instantiate an item object. You can type in any number on the menu you like to test it out.
    print(lineItem1)
    
    lineItem2 = FoodFacade().getItem()
    print(lineItem2)
    
    lineItem3 = FoodFacade().getItem()
    print(lineItem3)
    
    newReceipt = Receipt([lineItem1, lineItem2, lineItem3])
    newReceipt.totalPrice() #this method will total all the items in the list above
    
    print(newReceipt) #for now the receipt simply returns the total price
    
    cloneReceipt = newReceipt.clone()
    print(cloneReceipt) #this clone will print the same total as the receipt above
    
    cloneReceipt.total = "Gift Receipt" #you can change the attributes in the clone. In this case to hide the total from someone receiving it as a gift.
    print(cloneReceipt)
    
    
main()
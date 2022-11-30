from main import p, brands
from datetime import date

class Car(object):
    def __init__(self):
        self.brand = ""
        self.model = ""
        self.price = 0
        self.miles = 0
        self.year = 0

        self.name = ""
        self.nameList = ""
        self.phone = ""
        self.rating = ""
        self.distance = 0

        self.id = 0
        self.date = ""
        self.source = ""
        self.score = 0
        self.link = ""

    # SETTERS
    def setBrand(self, brand):
        self.brand = brand
    def setModel(self, model):
        self.model = model
    def setPrice(self, price):
        self.price = price
    def setMiles(self, miles):
        self.miles = miles
    def setYear(self, year):
        self.year = year
    def setName(self, name):
        self.name = name
        self.setNameList(name)
    def setNameList(self, name):
        self.nameList = name.lower().split()
    def setPhone(self, phone):
        self.phone = phone
    def setHash(self):
        self.id = self.hash()
    def setDate(self):
        self.date = date.today()
    def setSource(self, source):
        self.source = source
    def setRating(self, rating):
        self.rating = rating
    def setDistance(self, distance):
        self.distance = distance
    def setLink(self, link):
        self.link = link

    # ASSIGN SCORE OUT OF 100
    def setScore(self):
        score = 0
        numParam = p["mileageWeight"] + p["priceWeight"] + p["yearWeight"] + p["makeWeight"]
        milesInt = int(p["maxMiles"])
        priceInt = int(p["maxPrice"])
        yearInt = int(p["minYear"])
        # print("\n" + self.name)
        score += (milesInt - int(self.miles)) / milesInt * p["mileageWeight"] / numParam
        # print(score)
        score += (priceInt - int(self.price)) / priceInt * p["priceWeight"] / numParam
        # print(score)
        if int(self.year) > yearInt:
            score += (int(self.year) - yearInt) / (p["currentYear"] - yearInt) * p["yearWeight"] / numParam
        # print(score)
        score += self.makeVal() * p["makeWeight"] / numParam
        # print(score)
        self.score = score * (score + 0.45) * 100
        self.setHash()
        self.setDate()

    # ASSIGN MAKE PREFERENCES
    def makeVal(self):
        if self.brand != "Not recognized":
            return brands[self.brand]
        return 0.75

    def hash(self):
        return int(self.score) * int(self.price) * len(self.model) + \
               int(self.miles) * int(self.year) * len(self.brand)

    # CONVERT TO STRING
    def __str__(self):
        output = self.name
        output += "\nScore: " + str(round(self.score, 3))
        output += "\nPrice: " + str(self.price)
        output += "\nMiles: " + str(self.miles)
        output += "\nYear: " + str(self.year)
        output += "\nLink: " + str(self.link)
        output += "\nMake: " + str(self.brand).capitalize()
        output += "\nModel: " + str(self.model).capitalize()
        return output

    # CONVERT TO DICTIONARY FOR CSV
    def toDict(self):
        return {
            "Make": self.brand.capitalize(),
            "Model": " ".join([word.capitalize() for word in self.model.split()]),
            "Score": self.score,
            "Price": self.price,
            "Year": self.year,
            "Mileage": self.miles,
            "Date": self.date,
            "Source": self.source,
            "Link": self.link,
            "Hash": self.id,
        }
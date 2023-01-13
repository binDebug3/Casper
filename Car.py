import main

from datetime import date
from plyer import notification

class Car(object):
    def __init__(self):
        """
        Initialize a Car object. It's really just a dictionary because the only things it actually contributes are
            the score and hash functions
        Attriutes:
            brand: (string) the make of the car (ie Toyota, Ford, etc)
            model: (string) the model (ie Corolla, Focus, etc)
            price: (int) the price of the car in US dollars
            miles: (int) the mileage on the car at time of sale
            year: (int) the year the car was manufactured
            name: (string) the title on the listing of the car, typically year, make, model
            nameList: (list) the title information split by spaces into a list
            phone: (string) the contact phone number for the car
            rating: (string) the rating on the car or seller
            distance: (int) the distance of the sale from the zipcode of the user
            id: (int) unique id to identify the car
            date: (string) the date the car was first loaded into the database
            source: (string) the online dealership source the car was found on
            score: (int) the score of the car based on how well it matches your parameters
            link: (string) the link to the car's information
            image: (string) the path to the saved image of the car
        """
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
        self.image = ""
        self.addDetails = ""

    # SETTERS
    def setBrand(self, brand):
        """
        Set the brand attribute
        :param brand: (string) the brand of the car
        :return:
        """
        self.brand = brand
    def setModel(self, model):
        """
        Set the model attribute
        :param model: (string) the model of the car
        :return:
        """
        self.model = model
    def setPrice(self, price):
        """
        Set the price attribute
        :param price: (string) the price of the car
        :return:
        """
        self.price = price
    def setMiles(self, miles):
        """
        Set the mileage attribute
        :param miles: (string) the mileage of the car
        :return:
        """
        self.miles = miles
    def setYear(self, year):
        """
        Set the year attribute
        :param year: (string) the year of the car
        :return:
        """
        self.year = year
    def setName(self, name):
        """
        Set the name attribute
        :param name: (string) the name of the car
        :return:
        """
        self.name = name
        self.setNameList(name)
    def setNameList(self, name):
        """
        Build a list out of the name attribute
        :param name: (string) the name of the car
        :return:
        """
        self.nameList = name.lower().split()
    def setPhone(self, phone):
        # UNUSED
        """
        Set the phone attribute of the car
        :param phone: (string) the phone number for the car
        :return:
        """
        self.phone = phone
    def setHash(self):
        """
        Set the id attribute to the hash value
        :return:
        """
        self.id = self.hash()
    def setDate(self):
        """
        Set the retrieval date of the car as today's date
        :return:
        """
        self.date = date.today()
    def setSource(self, source):
        """
        Set the source attribute
        :param source: (string) the source of the car
        :return:
        """
        self.source = source
    def setRating(self, rating):
        # UNUSED
        """
        Set the rating attribute
        :param rating: (string) the rating of the car
        :return:
        """
        self.rating = rating
    def setDistance(self, distance):
        """
        Set the distance attribute
        :param distance: (string) the distance of the car's sale from input zipcode
        :return:
        """
        self.distance = distance
    def setLink(self, link):
        """
        Set the link attribute
        :param link: (string) the link to the listing of the car
        :return:
        """
        self.link = link
    def setImage(self, imagePath):
        """
        Set the image attribute
        :param imagePath: (string) the file folder path to the saved image of the car
        :return:
        """
        self.image = imagePath
    def setAddDetail(self, details):
        self.addDetails = details.toDict()

    # ASSIGN SCORE OUT OF 100
    def setScore(self):
        """
        Set the score attribute, which is a number 0-100 based on a nonlinear combination of weighted parameters
        :return:
        """
        # get parameters for score based on user input
        score = 0
        p = main.p
        numParam = p["mileageWeight"] + p["priceWeight"] + p["yearWeight"] + p["makeWeight"]
        milesInt = int(p["maxMiles"])
        priceInt = int(p["maxPrice"])
        yearInt = int(p["minYear"])

        # add the mileage score to the total
        score += (milesInt - int(self.miles)) / milesInt * p["mileageWeight"] / numParam
        # add the price score to the total
        score += (priceInt - int(self.price)) / priceInt * p["priceWeight"] / numParam
        # add the year score to the total
        if int(self.year) > yearInt:
            score += (int(self.year) - yearInt) / (p["currentYear"] - yearInt) * p["yearWeight"] / numParam
        # add the model score to the total
        score += self.makeVal() * p["makeWeight"] / numParam

        # make good scores better and bad scores worse with nonlinear function
        if 0 < score < 1:
            self.score = score * (score + 0.4) * 100
        else:
            self.score = score * 100
        self.setHash()
        self.setDate()

        # if a good score is found, send a notification
        if self.score > 90:
            notification.notify(
                title="Casper",
                message=f"I found a great ({round(self.score, 1)}) {self.cap(self.brand)} {self.cap(self.model)} "
                        f"for ${self.price} with {self.miles} miles.",
                # displaying time
                timeout=8
            )

    # ASSIGN MAKE PREFERENCES
    def makeVal(self):
        """
        Get the brand
        :return:
        """
        if self.brand != "Not recognized":
            return main.brands[self.brand.lower()]
        return 0.75

    def cap(self, title):
        nameList = title.split()
        caps = ""
        for name in nameList:
            caps += name[0].upper() + name[1:] + " "
        return caps[:-1]

    def hash(self):
        """
        Compute a hash function
        :return: (int) unique hash value based on parameters
        """
        return int(self.score) * int(self.price) * len(self.model) + \
               int(self.miles) * int(self.year) * len(self.brand)

    # CONVERT TO STRING
    def __str__(self):
        """
        Convert Car object to string
        :return: (string) Formatted string to display car data
        """
        output = self.name
        output += "\nScore: " + str(round(self.score, 3))
        output += "\nPrice: " + str(self.price)
        output += "\nMiles: " + str(self.miles)
        output += "\nYear: " + str(self.year)
        output += "\nLink: " + str(self.link)
        output += "\nImage Path: " + str(self.image)
        output += "\nMake: " + str(self.brand).capitalize()
        output += "\nModel: " + str(self.model).capitalize()

        adVals = self.addDetails.items()
        for val in adVals:
            output += "\n" + val[0] + ": " + str(val[1])
        return output

    # CONVERT TO DICTIONARY FOR CSV
    def toDict(self):
        """
        Convert Car object to dict
        :return: (dict) where keys are key details about the car and values are their values as strings
        """
        vals = {
            "Make": self.brand.capitalize(),
            "Model": " ".join([word.capitalize() for word in self.model.split()]),
            "Score": self.score,
            "Price": self.price,
            "Year": self.year,
            "Mileage": self.miles,
            "Date": self.date,
            "Source": self.source,
            "Link": self.link,
            "Image": self.image,
            "Hash": self.id,
        }
        if self.source in ["a"]:
            adVals = self.addDetails.items()
            for newVal in adVals:
                vals.update({newVal[0]: newVal[1]})
        return vals

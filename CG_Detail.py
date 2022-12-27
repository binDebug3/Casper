import time

# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common import NoSuchElementException

class CG_Detail(object):
    def __init__(self, driver, link):
        self.link = link.get_attribute('href')
        link.click()
        self.owners = ""
        self.accidents = ""
        self.title = ""
        self.condition = ""
        self.drivetrain = ""
        self.fuel_type = ""
        self.body = ""
        self.mileage = ""
        self.driver = driver
        self.trim = ""
        self.exterior = ""
        self.interior = ""
        self.transmission = ""
        self.engine = ""
        self.vin = ""
        self.stock_id = ""
        self.comments = self.findDescriptions()

        self.findAttributes()
        self.driver.back()

    def findAttributes(self):
        attPath = "//div/ul[@class='dTIusl']/li/div[2]/p[2]"
        attElems = self.driver.find_elements(By.XPATH, attPath)
        length = len(attElems)
        if 0 < length:
            self.mileage = attElems[0].text
        if 1 < length:
            self.drivetrain = attElems[1].text
        if 2 < length:
            self.exterior = attElems[2].text
        if 3 < length:
            self.interior = attElems[3].text
        if 4 < length:
            self.engine = attElems[4].text
        if 5 < length:
            self.fuel_type = attElems[5].text
        if 6 < length:
            self.transmission = attElems[6].text

    def findDescriptions(self):
        descClass = "//div/div/p"
        descElem = self.driver.find_element(By.XPATH, descClass)
        return descElem.text

    def findOverview(self):
        features = []
        featurePath = "//div/dl[@class='hP30qs']/dd"
        featureElems = self.driver.find_elements(By.XPATH, featurePath)
        # self.make = featureElems[0].text
        # self.model = featureElems[1].text
        # self.year = featureElems[2].text
        self.trim = featureElems[3].text
        self.body = featureElems[4].text
        self.exterior = featureElems[5].text
        self.interior = featureElems[6].text
        self.mileage = featureElems[7].text
        self.condition = featureElems[8].text
        self.vin = featureElems[9].text
        self.stock_id = featureElems[10].text
        return features

    def findHistory(self):
        historyClass = "sc-iJkHyd feZLPP"
        historyElems = self.driver.find_elements(By.CLASS_NAME, historyClass)
        title = historyElems[-3]
        accidents = historyElems[-2]
        owner = historyElems[-1]
        if "clean" in title.lower():
            self.title = "Clean"
        else:
            self.title = "Not clean"
        self.accidents = accidents.split()[0]
        self.owners = owner.split()[0]


    # CONVERT TO STRING
    def __str__(self):
        """
        Convert Detail object to string
        :return: (string) Formatted string to display car data
        """
        output = str(self.link)
        output += "\nExterior Color: " + self.exterior
        output += "\nInterior Color: " + self.interior
        output += "\nTransmission: " + self.transmission
        output += "\nTrim: " + self.trim
        output += "\nEngine: " + self.engine
        output += "\nVin: " + self.vin
        output += "\nStock ID: " + self.stock_id
        output += "\nDrive Train: " + self.drivetrain
        output += "\nFuel Type: " + self.fuel_type
        output += "\nBody: " + self.body
        output += "\nTitle: " + self.vin
        output += "\nCondition: " + self.condition
        output += "\nAccidents: " + self.accidents
        output += "\nOwners: " + self.owners
        output += "\nComments: " + self.comments
        return output

    # CONVERT TO DICTIONARY FOR CSV
    def toDict(self):
        """
        Convert Detail object to dict
        :return: (dict) where keys are key details about the car and values are their values as strings
        """
        return {
            "Link": str(self.link.get_attribute('href')),
            "Exterior Color": self.exterior,
            "Interior Color": self.interior,
            "Transmission": self.transmission,
            "Trim": self.trim,
            "Engine": self.engine,
            "Vin": self.vin,
            "Stock ID": self.stock_id,
            "Drive Train": self.drivetrain,
            "Fuel Type": self.fuel_type,
            "Body": self.body,
            "Title": self.vin,
            "Condition": self.condition,
            "Accidents": self.accidents,
            "Owners": self.owners,
            "Comments": self.comments,
        }
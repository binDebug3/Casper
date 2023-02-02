from selenium.webdriver.common.by import By

class KSL_Detail(object):
    def __init__(self, driver, link):
        self.link = link.get_attribute('href')
        self.driver = driver
        link.click()
        self.year = ""
        self.make = ""
        self.model = ""
        self.trim = ""
        self.body = ""
        self.cab_type = ""
        self.bed = ""
        self.e_condition = ""
        self.i_condition = ""
        self.drive_type = ""
        self.dealer_licence = ""
        self.stock_id = ""
        self.transmission = ""
        self.liters = ""
        self.cylinders = ""
        self.fuel_type = ""
        self.doors = ""
        self.belts = ""
        self.mileage = ""
        self.vin = ""
        self.title = ""
        self.exterior = ""
        self.interior = ""
        self.comments = self.findComments()

        self.findAttributes()
        self.driver.back()

    def findAttributes(self):
        buttonClass = "seeMore"
        attPath = "//div[@class='top']/div/dl/dd"
        seeMore = self.driver.find_element(By.CLASS_NAME, buttonClass)
        if seeMore is not None:
            seeMore.click()
            "//div[@class='MuiGrid-root jss144']/p"
        attElems = self.driver.find_elements(By.XPATH, attPath)
        self.trim = attElems[0].text
        self.transmission = attElems[1].text
        self.engine = attElems[2].text
        self.doors = attElems[3].text
        self.stock_id = attElems[4].text
        self.exterior = attElems[5].text
        self.interior = attElems[6].text
        self.certified = attElems[7].text
        self.vin = attElems[8].text

    def findComments(self):
        commentPath = "//span/p"
        return self.driver.find_element(By.XPATH, commentPath).text

    def findFeatures(self):
        features = []
        featurePath = "//div[@class='feature-area']/ul/li"
        featureElems = self.driver.find_elements(By.XPATH, featurePath)
        for elem in featureElems:
            features.append(elem.text)
        return features

    # CONVERT TO STRING
    def __str__(self):
        """
        Convert Detail object to string
        :return: (string) Formatted string to display car data
        """
        output = str(self.link.get_attribute('href')) + \
            "\nYear: " + self.year + \
            "\nMake: " + self.make + \
            "\nModel: " + self.model + \
            "\nTrim: " + self.trim + \
            "\nBody: " + self.body + \
            "\nCabin Type: " + self.cab_type + \
            "\nTruck Bed: " + self.bed + \
            "\nExterior Condition: " + self.e_condition + \
            "\nInterior Condition: " + self.i_condition + \
            "\nDrive Type: " + self.drive_type + \
            "\nDealer Licence: " + self.dealer_licence + \
            "\nStock Number: " + self.stock_id + \
            "\nLiters: " + self.liters + \
            "\nCylinders: " + self.cylinders + \
            "\nFuel Type: " + self.fuel_type + \
            "\nDoors: " + self.doors + \
            "\nBelts: " + self.belts + \
            "\nMileage: " + self.mileage + \
            "\nVin: " + self.vin + \
            "\nTitle type: " + self.title + \
            "\nExterior Color: " + self.exterior + \
            "\nInterior Color: " + self.interior
        return output

    # CONVERT TO DICTIONARY FOR CSV
    def toDict(self):
        """
        Convert Detail object to dict
        :return: (dict) where keys are key details about the car and values are their values as strings
        """
        # missing year, make, model, and mileage because they are redundant
        return {
            "Link": str(self.link.get_attribute('href')),
            "Trim": self.trim,
            "Body": self.body,
            "Cabin Type": self.cab_type,
            "Truck Bed": self.bed,
            "Exterior Condition": self.e_condition,
            "Interior Condition": self.i_condition,
            "Drive Type": self.drive_type,
            "Dealer Licence": self.dealer_licence,
            "Stock Number": self.stock_id,
            "Liters": self.liters,
            "Cylinders": self.cylinders,
            "Fuel Type": self.fuel_type,
            "Doors": self.doors,
            "Belts": self.belts,
            "Vin": self.vin,
            "Title type": self.title,
            "Exterior Color": self.exterior,
            "Interior Color": self.interior
        }
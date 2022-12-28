from selenium.webdriver.common.by import By

class KSL_Detail(object):
    def __init__(self, driver, link):
        self.link = link.get_attribute('href')
        self.driver = driver
        link.click()
        self.date = ""
        self.city = ""
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
        output = str(self.link.get_attribute('href'))
        output += "\nExterior Color: " + self.exterior
        output += "\nInterior Color: " + self.interior
        output += "\nTransmission: " + self.transmission
        output += "\nTrim: " + self.trim
        output += "\nLink: " + str(self.link)
        output += "\nEngine: " + self.engine
        output += "\nCertified Pre-Owned: " + self.certified
        output += "\nDoors: " + self.doors
        output += "\nVin: " + self.vin
        output += "\nStock ID: " + self.stock_id
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
            "Certified Pre-Owned": self.certified,
            "Doors": self.doors,
            "Vin": self.vin,
            "Stock ID": self.stock_id,
        }
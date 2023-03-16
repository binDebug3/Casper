from selenium.webdriver.common.by import By

class CD_Detail(object):
    def __init__(self, driver, link):
        if driver is None:
            self.driver = "None"
            self.link = "None"
            self.trim = "None"
            self.exterior = "None"
            self.interior = "None"
            self.transmission = "None"
            self.engine = "None"
            self.certified = "None"
            self.doors = "None"
            self.vin = "None"
            self.stock_id = "None"
            self.comments = "None"
            self.features = "None"

        else:
            self.driver = driver
            self.link = str(link.get_attribute('href'))
            link.click()
            self.trim = ""
            self.exterior = ""
            self.interior = ""
            self.transmission = ""
            self.engine = ""
            self.certified = ""
            self.doors = ""
            self.vin = ""
            self.stock_id = ""
            self.comments = self.findComments()
            self.features = self.findFeatures()

            self.findAttributes()
            self.driver.back()


    def findAttributes(self):
        attPath = "//div[@class='top']/div/dl/dd"

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
        featurePath = "//div[@class='feature-area']/ul/li/span"

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
        output = "\nExterior Color: " + self.exterior
        output += "\nInterior Color: " + self.interior
        output += "\nTransmission: " + self.transmission
        output += "\nTrim: " + self.trim
        output += "\nLink: " + str(self.link)
        output += "\nEngine: " + self.engine
        output += "\nCertified Pre-Owned: " + self.certified
        output += "\nDoors: " + self.doors
        output += "\nVin: " + self.vin
        output += "\nStock ID: " + self.stock_id
        output += "\nFeatures: " + str(self.features)
        output += "\nComments: " + self.comments

        return output

    # CONVERT TO DICTIONARY FOR CSV
    def toDict(self):
        """
        Convert Detail object to dict
        :return: (dict) where keys are key details about the car and values are their values as strings
        """
        return {
            "Link": self.link,
            "Exterior Color": self.exterior,
            "Interior Color": self.interior,
            "Transmission": self.transmission,
            "Trim": self.trim,
            "Engine": self.engine,
            "Certified Pre-Owned": self.certified,
            "Doors": self.doors,
            "Vin": self.vin,
            "Stock ID": self.stock_id,
            "Features": str(self.features),
            "Comments": self.comments,
        }
import time

from selenium.webdriver.common.by import By
from selenium.common import NoSuchElementException, ElementClickInterceptedException
import Search


class CG_Detail(object):
    def __init__(self, driver, link):
        self.link = link.get_attribute('href')
        try:
            link.click()
        except ElementClickInterceptedException as ex:
            print("Click intercepted")
            print(ex.msg)
            time.sleep(1)
            print("Retrying link")
            link.click()
        self.owners = ""
        self.accidents = ""
        self.title = ""
        self.condition = ""
        self.drivetrain = ""
        self.fuel_type = ""
        self.body = ""
        # self.mileage = ""
        self.driver = driver
        self.trim = ""
        self.exterior = ""
        self.interior = ""
        self.transmission = ""
        self.engine = ""
        self.vin = ""
        self.stock_id = ""
        self.rental_use = ""
        self.doors = ""
        self.horse = ""
        self.tank = ""
        self.high_gas = ""
        self.city_gas = ""
        self.comb_gas = ""
        self.cargo = ""
        self.bLeg = ""
        self.fLeg = ""
        time.sleep(0.1)
        self.markDown = self.findMarkDown()
        self.deal = self.findDeal()
        self.comments = self.findDescriptions()
        self.damaged = Search.checkDamage(self.comments)
        self.safety, self.options = self.findSafetyOptions()

        # self.findAttributes()
        self.findOverview()
        self.driver.back()

    def findAttributes(self):
        attPath = "//div/ul[@class='dTIusl']/li/div[2]/p[2]"
        attElems = self.driver.find_elements(By.XPATH, attPath)
        length = len(attElems)
        # if 0 < length:
        #     self.mileage = attElems[0].text
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

    def findDeal(self):
        dealClass = "RJvEVf woFqWQ"
        try:
            dealElem = self.driver.find_element(By.CLASS_NAME, dealClass)
            return dealElem.text
        except NoSuchElementException as ex:
            print("Deal element not found")
            print(ex.msg)
            return "Not found"


    def findMarkDown(self):
        markDownPath = "//section[@class='_3TqHJ']/h3"
        pricePath = "//section[@class='_3TqHJ']"
        try:
            priceElem = self.driver.find_element(By.XPATH, pricePath)
            markElem = self.driver.find_element(By.XPATH, markDownPath)
            return priceElem.text + " " + markElem.text
        except NoSuchElementException as ex:
            print("Markdown element not found")
            print(ex.msg)
            time.sleep(300)
            return "Not found"


    def findDescriptions(self):
        descClass = "//section/div/div/p"
        descElem = self.driver.find_elements(By.XPATH, descClass)
        output = ""
        for elem in descElem:
            output += elem.text + "\n"
        return output

    def findOverview(self):
        features = {}
        featurePath = "//div/dl[@class='hP30qs']/dd"
        fNamePath = "//div/dl[@class='hP30qs']/dt"
        sectionClass = "sc-evZas geZswT"
        sectionElems = self.driver.find_elements(By.CLASS_NAME, sectionClass)[:6]
        print(f"Found {len(sectionElems)} sections")
        if len(sectionElems) == 0:
            time.sleep(180)
            quit()
        count = 0
        for section in sectionElems:
            featureElems = self.driver.find_elements(By.XPATH, featurePath)
            featureNames = self.driver.find_elements(By.XPATH, fNamePath)
            for i in range(len(featureElems)):
                features.update({featureNames[i].text.lower(): featureElems[i].text.lower()})
            section.click()
            print(f"Found {len(features)} after searching {count} sections in findOverview")

        # updateBasic = False
        for param in features.keys():
            val = features.get(param)
            if "trim" in param:
                self.trim = val
            elif "body" in param:
                self.body = val
            elif "exterior" in param:
                self.exterior = val
            elif "interior" in param:
                self.interior = val
            # elif "mileage" in param:
            #     self.mileage = val
            elif "condition" in param:
                self.condition = val
            elif "vin" in param:
                self.vin = val
            elif "stock" in param:
                self.stock_id = val
            elif "fuel type" in param:
                self.fuel_type = val
            elif "combined" in param:
                self.comb_gas = val
            elif "city" in param:
                self.city_gas = val
            elif "highway" in param:
                self.high_gas = val
            elif "tank" in param:
                self.tank = val
            elif "transmission" in param:
                self.transmission = val
            elif "drivetrain" in param:
                self.drivetrain = val
            elif "engine" in param:
                self.engine = val
            elif "horse" in param:
                self.horse = val
            elif "doors" in param:
                self.doors = val
            elif "front" in param:
                self.fLeg = val
            elif "back" in param:
                self.bLeg = val
            elif "cargo" in param:
                self.cargo = val

        return features

    def findHistory(self):
        historyClass = "sc-iJkHyd feZLPP"
        historyElems = self.driver.find_elements(By.CLASS_NAME, historyClass)
        title = historyElems[6]
        accidents = historyElems[7]
        owner = historyElems[8]
        if "clean" in title.lower():
            self.title = "Clean"
        else:
            self.title = "Not clean"
        self.accidents = accidents.split()[0]
        self.owners = owner.split()[0]
        if len(historyElems) > 9:
            self.rental_use = True
        else:
            self.rental_use = False


    def findSafetyOptions(self):
        safety = []
        options = []
        safetyPath = "//div/div/div/div/ul/li"
        safetyElems = self.driver.find_elements(By.XPATH, safetyPath)
        half = len(safetyElems) // 2
        for i, elem in enumerate(safetyElems):
            if elem.text is not None:
                if i < half:
                    safety.append(elem.text)
                else:
                    options.append(elem.text)
        return safety, options


    # CONVERT TO STRING
    def __str__(self):
        """
        Convert Detail object to string
        :return: (string) Formatted string to display car data
        """
        output = str(self.link)
        output += "\nDeal: " + self.deal
        output += "\nMark Down: " + self.markDown
        output += "\nTrim: " + self.trim
        output += "\nBody: " + self.body
        output += "\nExterior Color: " + self.exterior
        output += "\nInterior Color: " + self.interior
        output += "\nCondition: " + self.condition
        output += "\nVin: " + self.vin
        output += "\nStock ID: " + self.stock_id
        output += "\nFuel Type: " + self.fuel_type
        output += "\nCombined Gas Mileage: " + self.comb_gas
        output += "\nCity Gas Mileage: " + self.city_gas
        output += "\nHighway Gas Mileage: " + self.high_gas
        output += "\nTank Size: " + self.tank
        output += "\nTransmission: " + self.transmission
        output += "\nDrive Train: " + self.drivetrain
        output += "\nEngine: " + self.engine
        output += "\nHorse Power: " + self.horse
        output += "\nDoors: " + self.doors
        output += "\nFront Legroom: " + self.fLeg
        output += "\nBack Legroom: " + self.bLeg
        output += "\nCargo Size: " + self.cargo
        output += "\nTitle: " + self.title
        output += "\nAccidents: " + self.accidents
        output += "\nOwners: " + self.owners
        output += "\nRental Use: " + self.rental_use
        output += "\nSafety Features: " + str(self.safety)
        output += "\nAdditional Features: " + str(self.options)
        output += "\nComments: " + self.comments
        return output

    # CONVERT TO DICTIONARY FOR CSV
    def toDict(self):
        """
        Convert Detail object to dict
        :return: (dict) where keys are key details about the car and values are their values as strings
        """
        return {
            "Link": str(self.link),
            "Deal": self.deal,
            "Mark Down": self.markDown,
            "Trim: ": self.trim,
            "Body: ": self.body,
            "Exterior Color: ": self.exterior,
            "Interior Color: ": self.interior,
            "Condition: ": self.condition,
            "Vin: ": self.vin,
            "Stock ID: ": self.stock_id,
            "Drive Train: ": self.drivetrain,
            "Fuel Type: ": self.fuel_type,
            "Combined Gas Mileage: ": self.comb_gas,
            "City Gas Mileage: ": self.city_gas,
            "Highway Gas Mileage: ": self.high_gas,
            "Tank Size: ": self.tank,
            "Transmission: ": self.transmission,
            "Engine: ": self.engine,
            "Horse Power: ": self.horse,
            "Doors: ": self.doors,
            "Front Legroom: ": self.fLeg,
            "Back Legroom: ": self.bLeg,
            "Cargo Size: ": self.cargo,
            "Title: ": self.title,
            "Accidents: ": self.accidents,
            "Owners: ": self.owners,
            "Rental Use: ": self.rental_use,
            "Safety Features: ": str(self.safety),
            "Additional Features: ": str(self.options),
            "Comments: ": self.comments,
        }
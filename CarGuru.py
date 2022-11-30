import time
import math
import pandas as pd

import Car
import main
from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common import NoSuchElementException

class CarGuru(object):
    def __init__(self):
        p = main.p
        websites = {
            "AutoTrader": "https://www.autotrader.com/cars-for-sale/cars-under-" + p["maxPrice"] + "/" + p["city"] +
                          "-" + p["state"] + "-" + p["zipCode"] +
                          "?requestId=1819194850&dma=&transmissionCodes=AUT&searchRadius=" + p["radius"] +
                          "&priceRange=&location=&marketExtension=include&maxMileage=" + p["maxMiles"] +
                          "&isNewSearch=true&showAccelerateBanner=false&sortBy=relevance&numRecords=100",
            "CarGuru": "https://www.cargurus.com/Cars/inventorylisting/viewDetailsFilterViewInventoryListing.action?zip=" +
                        p["zipCode"] + "&inventorySearchWidgetType=PRICE&maxPrice=" + p["maxPrice"] +
                        "&showNegotiable=true&sortDir=ASC&sourceContext=usedPaidSearchNoZip&distance=" + p["radius"] +
                        "&minPrice=" + p["minPrice"] + "&sortType=DEAL_SCORE",
            "KSL": "https://cars.ksl.com/search/yearFrom/" + p["minYear"] + "/yearTo/" + str(p["currentYear"]) +
                   "/mileageFrom/0/mileageTo/" + p["altMax"] + "/priceFrom/" + p["minPrice"] + "/priceTo/" +
                   p["maxPrice"] + "/city/" + p["city"].capitalize() + "/state/" + p["state"].upper()}
        print(websites["CarGuru"])
        self.driver = webdriver.Chrome()
        self.driver.get(websites["CarGuru"])
        time.sleep(3)
        self.cars = []
        self.resCount = self.getCount()
        self.names = self.findNames()
        self.prices = self.findPrices()
        self.miles = self.findMiles()
        self.links = self.findLinks()
        # self.pages, self.pageElems = self.getPages()

    def getCount(self):
        resCountID = "eegHEr"
        try:
            results = self.driver.find_element(By.CLASS_NAME, resCountID).text.split()
            count = int(results[4].replace(",", ""))
            print(f"Found {count} cars")
            return count
        except (IndexError, NoSuchElementException):
            print("Waiting for page to load...")
            time.sleep(2)
            self.getCount()

    def getPages(self):
        # TODO implement getPages
        pages = []
        pageClass = ""
        pageElems = self.driver.find_elements(By.CLASS_NAME, pageClass)
        for page in pageElems:
            num = page.text
            if num.isdigit():
                pages.append(int(num))
        return pages, pageElems

    def findPrices(self):
        prices = []
        priceClass = "JzvPHo"
        priceElems = self.driver.find_elements(By.CLASS_NAME, priceClass)[4:]
        print("priceElems")
        print(len(priceElems))
        for elem in priceElems:
            prices.append(elem.text.replace(",", "").replace("$", "").split()[0])
        print(prices)
        return prices

    def findMiles(self):
        miles = []
        mileClass = "//div/p/span[2]"
        mileElems = self.driver.find_elements(By.XPATH, mileClass)[::2][4:]
        print("mileElems")
        print(len(mileElems))
        for elem in mileElems:
            stat = elem.text.replace(",", "").split()[0]
            # if int(stat) == 0:
            #     stat = main.p["altMax"]
            miles.append(stat)
        print(miles)
        return miles

    def findNames(self):
        names = []
        nameID = "vO42pn"
        nameElems = self.driver.find_elements(By.CLASS_NAME, nameID)[4:]
        print("nameElems")
        print(len(nameElems))
        for elem in nameElems:
            names.append(elem.text)
        print(names)
        return names

    def findBrand(self, nameList):
        brands = main.brands
        match = list(set(brands.keys()) & set(nameList))
        length = len(match)
        if length == 0:
            return "Not recognized"
        elif length > 1:
            return " ".join(match)
        else:
            return match[0]

    def findModel(self, nameList, brand):
        if brand != "Not recognized":
            index = nameList.index(brand)
            return " ".join(nameList[index + 1:])
        return "None"

    def findYear(self, nameList):
        for word in nameList:
            if word.isdigit():
                return int(word)
        return 0

    def findLinks(self):
        links = []
        linkPath = "//div[@class='MOfIEd XcutUU prRsnF']/a"
        linkElems = self.driver.find_elements(By.XPATH, linkPath)[4:]
        print("linkElems")
        # print(len(linkElems))
        for elem in linkElems:
            links.append(elem.get_attribute('href'))
        print(links)
        return links

    def getNewCars(self, garage):
        dfOld = pd.read_csv('CarGuru.csv')
        oldIDs = dfOld["Hash"].values.tolist()
        IDS = []
        for id in oldIDs:
            if isinstance(id, float) and not math.isnan(id):
                IDS.append(int(id))
            elif isinstance(id, int):
                IDS.append(id)
            elif isinstance(id, str) and id.isdigit():
                IDS.append(int(id))
        print(f"There are {len(IDS)} cars already in the table")
        newCars = []
        for car in garage:
            if car.id not in IDS:
                newCars.append(car)
        return newCars

    def toCSV(self, garage):
        columns = ["Make", "Model", "Score", "Price", "Year", "Mileage", "Date", "Source", "Link", "Hash"]
        df = pd.DataFrame([car.toDict() for car in garage], columns=columns)
        df.to_csv('CarGuru.csv', mode='a', index=False)
        self.exportCSV()
        print(f"Exported {len(garage)} cars to 'CarGuru.csv'")

    def exportCSV(self):
        df = pd.read_csv('CarGuru.csv')
        df = df.drop_duplicates(["Hash"])
        df = df.dropna()
        df = df.sort_values(["Score", "Price"], ascending=False)
        df.to_csv('CarGuru.csv', index=False, mode='w')

    def peruseCars(self):
        for i in range(len(self.names)):
            car = Car.Car()
            car.setName(self.names[i])
            car.setPrice(self.prices[i])
            car.setMiles(self.miles[i])
            car.setLink(self.links[i])
            car.setBrand(self.findBrand(car.nameList))
            car.setModel(self.findModel(car.nameList, car.brand))
            car.setYear(self.findYear(car.nameList))
            car.setSource("CarGuru")
            car.setScore()
            self.cars.append(car)
        if len(self.cars) > 0:
            self.toCSV(sorted(self.cars, key=lambda x: x.score)[::-1])


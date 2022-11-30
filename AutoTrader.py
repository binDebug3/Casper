import time

from Car import Car
import pandas as pd
from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from main import p, brands
import math

class AutoTrader(object):
    def __init__(self, site):
        websites = {
            "AutoTrader": "https://www.autotrader.com/cars-for-sale/cars-under-" + p["maxPrice"] + "/" + p["city"] +
                          "-" + p["state"] + "-" + p["zipCode"] +
                          "?requestId=1819194850&dma=&transmissionCodes=AUT&searchRadius=" + p["radius"] +
                          "&priceRange=&location=&marketExtension=include&maxMileage=" + p["maxMiles"] +
                          "&isNewSearch=true&showAccelerateBanner=false&sortBy=relevance&numRecords=100",
            "Cargurus": "https://www.cargurus.com/Cars/inventorylisting/viewDetailsFilterViewInventoryListing.action?zip=" +
                        p["zipCode"] + "&inventorySearchWidgetType=PRICE&maxPrice=" + p["maxPrice"] +
                        "&showNegotiable=true&sortDir=ASC&sourceContext=usedPaidSearchNoZip&distance=" + p["radius"] +
                        "&minPrice=" + p["minPrice"] + "&sortType=DEAL_SCORE",
            "KSL": "https://cars.ksl.com/search/yearFrom/" + p["minYear"] + "/yearTo/" + str(p["currentYear"]) +
                   "/mileageFrom/0/mileageTo/" + p["maxMiles"] + "/priceFrom/" + p["minPrice"] + "/priceTo/" +
                   p["maxPrice"] + "/city/" + p["city"] + "/state/" + p["state"].upper()}
        self.driver = webdriver.Chrome()
        self.driver.get(websites[site])
        self.cars = []
        self.resCount = self.getCount()
        self.names = self.findNames()
        self.prices = self.findPrices()
        self.miles = self.findMiles()
        self.links = self.findLinks()
        self.pages, self.pageElems = self.getPages()

    def getCount(self):
        resCountID = "results-text-container"
        results = self.driver.find_element(By.CLASS_NAME, resCountID).text
        results = results.split()
        count = results[0].split("-")
        try:
            print(f"Found {int(count[1]) - int(count[0]) + 1} cars")
            return int(count[1]) - int(count[0]) + 1
        except IndexError:
            print("Waiting for page to load...")
            time.sleep(2)
            self.getCount()

    def getPages(self):
        pages = []
        pageClass = "sr-only"
        pageElems = self.driver.find_elements(By.CLASS_NAME, pageClass)
        for page in pageElems:
            num = page.text
            if num.isdigit():
                pages.append(int(num))
        return pages, pageElems

    def findPrices(self):
        prices = []
        priceClass = "first-price"
        priceElems = self.driver.find_elements(By.CLASS_NAME, priceClass)
        for elem in priceElems:
            prices.append(elem.text.replace(",", ""))
        return prices

    def findMiles(self):
        miles = []
        mileClass = "item-card-specifications"
        mileElems = self.driver.find_elements(By.CLASS_NAME, mileClass)
        for elem in mileElems:
            miles.append(elem.text.replace(",", "").split()[0])
        return miles

    def findNames(self):
        names = []
        nameID = "text-size-sm-500"
        nameElems = self.driver.find_elements(By.CLASS_NAME, nameID)
        for elem in nameElems:
            names.append(elem.text)
        return names

    def findBrand(self, nameList):
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
        linkPath = "//div[@class='display-flex justify-content-between']/a"
        linkElems = self.driver.find_elements(By.XPATH, linkPath)
        for elem in linkElems:
            links.append(elem.get_attribute('href'))
        return links

    def getNewCars(self, garage):
        dfOld = pd.read_csv('autotrader.csv')
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
        df = pd.DataFrame([car.toDict() for car in garage])
        df.to_csv('autotrader.csv', mode='a', index=False)
        self.exportCSV()
        print(f"Exported {len(garage)} cars to 'autotrader.csv'")

    def exportCSV(self):
        df = pd.read_csv('autotrader.csv')
        df = df.drop_duplicates(["Hash"])
        df = df.dropna()
        df = df.sort_values(["Score", "Price"], ascending=False)
        df.to_csv('autotrader.csv', index=False, mode='w')

    def peruseCars(self):
        # print("Pages:", len(self.pageElems))
        # for j in range(len(self.pageElems)):
        #     self.resCount = self.getCount()
        for i in range(self.resCount):
            car = Car()
            car.setName(self.names[i + 2])
            car.setPrice(self.prices[i + 1])
            car.setMiles(self.miles[i])
            car.setLink(self.links[i + 1])
            car.setBrand(self.findBrand(car.nameList))
            car.setModel(self.findModel(car.nameList, car.brand))
            car.setYear(self.findYear(car.nameList))
            car.setSource("AutoTrader")
            car.setScore()
            self.cars.append(car)
        # thing = self.driver.find_element(By.CSS_SELECTOR, "[aria-label='Next Page']")
        # print(thing.text)
        # print(thing.get_attribute("href"))
        # thing.click()
        # time.sleep(2)
        self.toCSV(sorted(self.cars, key=lambda x: x.score)[::-1])


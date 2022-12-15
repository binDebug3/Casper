import Compresser
from Car import Car
import main

import time
import pandas as pd
import math

from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import urllib.request

class Search(object):
    def __init__(self, webName, website):
        # TODO UNUSED
        """
        Attempt at making a base search class. Each of the websites are distinct enough to disable any code reuse
        even though the process is very similar for each website
        :param webName:
        :param website:
        """
        self.website = website
        self.webName = webName
        self.driver = webdriver.Chrome()
        self.driver.get(website)
        self.cars = []
        self.searchBy = {}

        self.resCount = 0
        self.names = []
        self.prices = []
        self.miles = []
        self.links = []
        self.images = []
        # self.numPages, self.nextPage = [], []
        # self.resCount = self.getCount()
        # self.names = self.findNames()
        # self.prices = self.findPrices()
        # self.miles = self.findMiles()
        # self.links = self.findLinks()
        # self.images = self.findImages()
        # self.numPages, self.nextPage = self.getPages()

        self.compression = 40
        self.updateData = True

    def resetPage(self):
        self.driver.close()
        self.driver = webdriver.Chrome()
        self.driver.get(self.getNextPage())
        time.sleep(5)
        self.resCount = self.getCount(self.searchBy["count"])
        self.names = self.findNames(self.searchBy["names"])
        self.prices = self.findPrices(self.searchBy["prices"])
        self.miles = self.findMiles(self.searchBy["miles"])
        self.links = self.findLinks(self.searchBy["links"])
        # self.images = self.findImages()

    def getNextPage(self):
        nextPage = self.website
        index = -1
        while nextPage[index].isdigit():
            index -= 1
        index += 1
        currStart = nextPage[index:]
        newStart = str(int(currStart) + self.resCount)
        site = nextPage[:len(nextPage) + index] + newStart
        self.website = site
        return site

    def getCount(self, resCountID):
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

    def getPages(self, pageClass):
        # might not be implemented
        pageButtons = self.driver.find_element(By.XPATH, pageClass)
        text = pageButtons.text.split()
        if len(text) > 4:
            numPages = int(text[-3]) + 1
            nextPagePath = pageClass + "/li[" + str(numPages) + "]/a"
            nextPageButton = self.driver.find_element(By.XPATH, nextPagePath)
        else:
            numPages = 1
            nextPageButton = None
        return numPages, nextPageButton


    def findPrices(self, priceClass):
        prices = []
        priceElems = self.driver.find_elements(By.CLASS_NAME, priceClass)
        for elem in priceElems:
            prices.append(elem.text.replace(",", ""))
        return prices

    def findMiles(self, mileClass):
        miles = []
        mileElems = self.driver.find_elements(By.CLASS_NAME, mileClass)
        for elem in mileElems:
            miles.append(elem.text.replace(",", "").split()[0])
        return miles

    def findNames(self, nameID):
        names = []
        nameElems = self.driver.find_elements(By.CLASS_NAME, nameID)
        for elem in nameElems:
            names.append(elem.text)
        return names

    def findBrand(self, nameList):
        match = list(set(main.brands.keys()) & set(nameList))
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

    def findLinks(self, linkPath):
        links = []
        linkElems = self.driver.find_elements(By.XPATH, linkPath)
        for elem in linkElems:
            links.append(elem.get_attribute('href'))
        return links

    def findImages(self, imageClass):
        images = []
        imageElems = self.driver.find_elements(By.CLASS_NAME, imageClass)
        print("Number of images found:", len(imageElems))
        for elem in imageElems:
            src = elem.get_attribute('src')
            alt = "_".join(elem.get_attribute('alt').split())
            urllib.request.urlretrieve(src, alt + ".png")
            Compresser.compress_image(alt + ".png", self.compression)
            images.append(src)
        return images

    def setCompression(self, rate):
        self.compression = rate

    def updateBool(self, val=False):
        self.updateData = val

    def getNewCars(self, garage):
        dfOld = pd.read_csv(self.webName + '.csv')
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
        df.to_csv(self.webName + '.csv', mode='a', index=False)
        self.exportCSV()
        print(f"Exported {len(garage)} cars to {self.webName}.csv'")

    def exportCSV(self):
        df = pd.read_csv(self.webName + '.csv')
        df = df.drop_duplicates(["Hash"])
        df = df.dropna()
        df = df.sort_values(["Score", "Price"], ascending=False)
        df.to_csv(self.webName + '.csv', index=False, mode='w')

    def peruseCars(self):
        while self.resCount == 25:
            for i in range(self.resCount):
                car = Car()
                car.setName(self.names[i + 2])
                car.setPrice(self.prices[i + 1])
                car.setMiles(self.miles[i])
                car.setLink(self.links[i + 1])
                car.setBrand(self.findBrand(car.nameList))
                car.setModel(self.findModel(car.nameList, car.brand))
                car.setYear(self.findYear(car.nameList))
                car.setSource(self.webName)
                car.setScore()
                self.cars.append(car)
            self.resetPage()
        if self.updateData:
            self.toCSV(sorted(self.cars, key=lambda x: x.score)[::-1])

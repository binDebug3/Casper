from Car import Car

import pandas as pd
import math
from abc import abstractmethod, ABCMeta

class Search(metaclass=ABCMeta):
    def __init__(self):
        pass

    @property
    @abstractmethod
    def websites(self):
        pass

    @property
    @abstractmethod
    def driver(self):
        pass

    @property
    @abstractmethod
    def resCount(self):
        pass

    @property
    @abstractmethod
    def cars(self):
        pass

    @property
    @abstractmethod
    def names(self):
        pass

    @property
    @abstractmethod
    def prices(self):
        pass

    @property
    @abstractmethod
    def miles(self):
        pass

    @property
    @abstractmethod
    def links(self):
        pass

    @property
    @abstractmethod
    def images(self):
        pass

    @property
    @abstractmethod
    def compression(self):
        pass

    @property
    @abstractmethod
    def export(self):
        pass


    @abstractmethod
    def resetPage(self):
        pass

    @abstractmethod
    def getCount(self, resCountID):
        pass

    @abstractmethod
    def findPrices(self, priceClass):
        pass

    @abstractmethod
    def findMiles(self, mileClass):
        pass

    @abstractmethod
    def findNames(self, nameID):
        pass

    @abstractmethod
    def findBrand(self, nameList):
        pass

    @abstractmethod
    def findModel(self, nameList, brand):
        pass

    @abstractmethod
    def findYear(self, nameList):
        pass

    @abstractmethod
    def findLinks(self, linkPath):
        pass

    @abstractmethod
    def findImages(self, imageClass):
        pass

    def setCompression(self, rate):
        self.compression = rate

    def updateBool(self, val=False):
        self.updateData = val

    def getNewCars(self, garage):
        """
        NOT currently used
        Read all saved cars from Excel spreadsheet and compare it to the cars scraped to identify new cars.
        This is not the most efficient approach, and it fails to recognize matches if any of the parameters changed,
        for better or for worse
        :param garage:
        :return: newCars (list): list of car objects that were not already in the database
        """
        # read the csv and get a list of their hashed IDs woot woot
        dfOld = pd.read_csv('CarsDirect.csv')
        oldIDs = dfOld["Hash"].values.tolist()

        # compare each old ID to each new ID
        IDS = []
        for id in oldIDs:
            if isinstance(id, float) and not math.isnan(id):
                IDS.append(int(id))
            elif isinstance(id, int):
                IDS.append(id)
            elif isinstance(id, str) and id.isdigit():
                IDS.append(int(id))
        # visibility debugging print
        print(f"There are {len(IDS)} cars already in the table")

        # build list of car objects based on the list of IDs corresponding to new cars
        newCars = []
        for car in garage:
            if car.id not in IDS:
                newCars.append(car)
        return newCars

    def toCSV(self, garage):
        """
        Convert a list of Car objects to a CSV
        :param garage:
        :return:
        """
        # this is only useful when saving a new csv that does not already have columns
        columns = ["Make", "Model", "Score", "Price", "Year", "Mileage", "Date", "Source", "Link", "Image", "Hash"]

        # use Car's toDict method to build a new dataframe, save it, then call the export method
        df = pd.DataFrame([car.toDict() for car in garage])
        df.to_csv('CarsDirect.csv', mode='a', index=False)
        print(f"Found {df.shape[0]} new cars.")
        self.exportCSV()

    def exportCSV(self):
        """
        Clean database and export update version to overwrite the old version
        :param self
        :return:
        """
        # read the file, drop duplicates and null values, sort, then save file
        df = pd.read_csv('CarsDirect.csv')
        df = df.drop_duplicates(["Hash"])
        df = df[df.Make != "Make"]
        df.Score = df.Score.astype(float)
        df.Price = df.Price.astype(float)
        df = df.sort_values(["Score", "Price"], ascending=False)
        print(f"Exported {df.shape[0] - 1} cars to 'CarsDirect.csv'")
        df.to_csv('CarsDirect.csv', index=False, mode='w')

    def peruseCars(self, send=True):
        if not send:
            print("I will not update the CSV file on this round.")
            self.export = False
        # for each car on each page, build a Car object and set all of its attributes
        count = 0
        while self.resCount == 30 or count == 0:
            for i in range(len(self.names)):
                car = Car()
                car.setName(self.names[i])
                car.setPrice(self.prices[i])
                car.setMiles(self.miles[i])
                car.setLink(self.links[i])
                car.setImage(self.images[i])
                car.setBrand(self.findBrand(car.nameList))
                car.setModel(self.findModel(car.nameList, car.brand))
                car.setYear(self.findYear(car.nameList))
                car.setSource("CarsDirect")
                car.setScore()
                self.cars.append(car)
            # load the next page
            count = 1
            if self.resCount == 30:
                self.resetPage()
        # export new Car list to CSV
        if len(self.cars) > 0 and self.export:
            self.toCSV(sorted(self.cars, key=lambda x: x.score)[::-1])

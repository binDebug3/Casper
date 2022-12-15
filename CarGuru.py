import time
import math
import pandas as pd

import Car
import main
import Compresser

import urllib
from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.common import NoSuchElementException



class CarGuru(object):
    def __init__(self):
        """
        Initialize a CarGuru object. Opens the corresponding website and scrapes relevant data
            to build attribute lists.
        :param self
        Attributes:
                NOT IMPLEMENTED chrome_options  (object): arguments to send with the driver.get call
                websites (dict): website names matched to their link based on user preferences
                driver (object): selenium object that allows access to the DOM
                cars (list):    car objects created based on data found on the website
                resCount (int): result count, the number of results that appeared on the page
                names (list):   strings that contain the full title of the listing
                prices (list):  strings that represent the price of each car
                miles (list):   strings that represent the number of miles on each car
                links (list):   strings that link to the listing for each specific car, instead of the result page
                images (list):  strings that refer to the location and title of saved images for each car
                compression (list): rank to compress each image, 0 means do not compress
        :return:
        """
        websites = main.websites
        print("\n\nScanning CarGuru")
        print(websites["CarGuru"])
        self.driver = webdriver.Chrome()
        self.driver.get(websites["CarGuru"])
        time.sleep(3)
        self.setMileage()
        self.cars = []
        self.resCount = self.getCount()
        self.names = self.findNames()
        self.prices = self.findPrices()
        self.miles = self.findMiles()
        self.links = self.findLinks()
        self.images = self.findImages()
        # page number not currently necessary and not functional for this site
        # self.pages, self.pageElems = self.getPages()
        self.export = True

    def setExport(self, send):
        self.export = send

    def resetPage(self):
        """
        After website link has been updated and the driver has been closed, opens a new Chrome browser
            to display the next page. Updates all the AutoTrader attributes with the new data.
            This is not my best coding style, but it works for now.
        :param self
        :return:
        """
        self.resCount = self.getCount()
        self.names = self.findNames()
        self.prices = self.findPrices()
        self.miles = self.findMiles()
        self.links = self.findLinks()
        self.images = self.findImages()

    def getNextPage(self):
        nextClass = "jX_mq2"
        button = self.driver.find_elements(By.CLASS_NAME, nextClass)
        if len(button) <= 1:
            button[0].click()
        else:
            button[1].click()

    def getCount(self):
        """
        Find the number of search results on one page and update self.resCount with it
        :param self
        :return:
        """
        resCountID = "eegHEr"
        try:
            results = self.driver.find_element(By.CLASS_NAME, resCountID).text.split()
            count = int(results[2]) - int(results[0]) + 1
            # print(f"Found {count} cars")
            return count
        except (IndexError, NoSuchElementException):
            print("Waiting for page to load...")
            time.sleep(2)
            self.getCount()

    def getPages(self):
        # UNUSED
        """
        Count the number of total pages.
        NOT currently functional or necessary
        :param self
        :return: numPages (int): number of pages to scrape for a particular search
        :return: nextPageButton (list): list of button elements to click in order to switch pages
        """
        pages = []
        pageClass = ""
        pageElems = self.driver.find_elements(By.CLASS_NAME, pageClass)
        for page in pageElems:
            num = page.text
            if num.isdigit():
                pages.append(int(num))
        return pages, pageElems

    def findPrices(self):
        """
        Find the prices for each car
        :param self
        :return: prices (list): list of price strings
        """
        prices = []
        priceClass = "JzvPHo"
        # get a list of price elements and save the parsed text content
        priceElems = self.driver.find_elements(By.CLASS_NAME, priceClass)[4:]
        for elem in priceElems:
            prices.append(elem.text.replace(",", "").replace("$", "").split()[0])
        return prices

    def setMileage(self):
        sliderClass = "E9RuSU"
        barClass = "P6sai1"
        slideButton = self.driver.find_element(By.CLASS_NAME, sliderClass)
        slider = self.driver.find_element(By.CLASS_NAME, barClass)
        length = float(slider.size["width"])
        total = 310000
        offset = int(- (total - int(main.p["maxMiles"])) / total * length)
        move = ActionChains(self.driver)
        move.click_and_hold(slideButton).move_by_offset(offset, 0).release().perform()
        time.sleep(1)

    def findMiles(self):
        """
        Find the mileage for each car
        :param self
        :return: miles (list): list of mileage strings
        """
        miles = []
        mileClass = "//div/p/span[2]"
        # get a list of mileage elements and save the parsed text content
        mileElems = self.driver.find_elements(By.XPATH, mileClass)[::2][4:]
        for elem in mileElems:
            stat = elem.text.replace(",", "").split()[0]
            miles.append(stat)
        return miles

    def findNames(self):
        """
        Find the listing title for each car
            ex) 2017 Toyota Corolla
        :param self
        :return: names (list): list of name strings
        """
        names = []
        nameID = "vO42pn"
        # get a list of name elements and save the text content
        nameElems = self.driver.find_elements(By.CLASS_NAME, nameID)[4:]
        for elem in nameElems:
            names.append(elem.text)
        return names

    def findBrand(self, nameList):
        """
        Extract the brand of the car from the listing title
        :param nameList: name listing for the car split by spaces into a list
        :return: match (string): the brand of the car
        """
        # use list operator & to get all the words that match between
        # the set of brands and the words in the car's listing
        brands = main.brands
        match = list(set(brands.keys()) & set(nameList))
        length = len(match)

        # if none found, return 'Not Recognized', otherwise rebuild the string and return the brand
        if length == 0:
            return "Not recognized"
        elif length > 1:
            return " ".join(match)
        else:
            return match[0]

    def findModel(self, nameList, brand):
        """
        Extract the model of the car from the listing title
        :param nameList: name listing for the car split by spaces into a list
        :param brand: brand of the car
        :return:
        """
        if brand != "Not recognized":
            # get the index of the brand in the name list
            index = nameList.index(brand)
            # return the rest of the list following the brand
            return " ".join(nameList[index + 1:])
        return "None"

    def findYear(self, nameList):
        """
        Extract the year of the car from the listing title
        :param nameList: name listing for the car split by spaces into a list
        :return:
        """
        # return the first grouping of digits found in the name list
        for word in nameList:
            if word.isdigit():
                return int(word)
        return 0

    def findLinks(self):
        """
        Find the links to each car's specific information
        :param self
        :return: links (list): list of link strings
        """
        links = []
        linkPath = "//div[@class='MOfIEd XcutUU prRsnF']/a"
        # get the link elements and build a list of their href attributes
        linkElems = self.driver.find_elements(By.XPATH, linkPath)[4:]
        for elem in linkElems:
            links.append(elem.get_attribute('href'))
        return links

    def findImages(self):
        """
        Find the images for each car
        :param self
        :return: images (list): list of file folder location strings
        """
        # get a list of image elements
        images = []
        imageClass = "C6f2e2 bmTmAy"
        imageElems = self.driver.find_elements(By.XPATH, "//img[@class='C6f2e2 bmTmAy']")
        for elem in imageElems:
            # get the link to the element
            src = elem.get_attribute('src')
            # build a name for the image based on its alt text
            alt = "_".join(elem.get_attribute('alt').split())
            path = "Images/" + alt + ".png"
            # save the image
            urllib.request.urlretrieve(src, path)
            # compress with image with our custom compression algorithm woot woot
            try:
                Compresser.compress_image(path, 50)
                images.append(alt)
            except ValueError as error:
                print("Image '" + alt + ".png' did not download properly")
                print("More Details:")
                print(src)
                print(error)
                print()
                images.append("No image")
        return images

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
        dfOld = pd.read_csv('CarGuru.csv')
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
        df.to_csv('CarGuru.csv', mode='a', index=False)
        print(f"Found {df.shape[0]} new cars.")
        self.exportCSV()

        # visibility statement
        print(f"Exported {len(garage)} cars to 'CarGuru.csv'")

    def exportCSV(self):
        """
        Clean database and export update version to overwrite the old version
        :param self
        :return:
        """
        # read the file, drop duplicates and null values, sort, then save file
        df = pd.read_csv('CarGuru.csv')
        df = df.drop_duplicates(["Hash"])
        df = df[df.Make != "Make"]
        df.Score = df.Score.astype(float)
        df.Price = df.Price.astype(float)
        df = df.sort_values(["Score", "Price"], ascending=False)
        df.to_csv('CarGuru.csv', index=False, mode='w')

    def peruseCars(self, send=True):
        if not send:
            print("I will not update the CSV file on this round.")
            self.export = False
        # for each car on each page, build a Car object and set all of its attributes
        while self.resCount == 15:
            time.sleep(1)
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
                car.setImage(self.images[i])
                car.setScore()
                self.cars.append(car)
            # load the next page
            self.getNextPage()
            time.sleep(2)
            self.resetPage()
        # export new Car list to CSV
        if len(self.cars) > 0 and self.export:
            self.toCSV(sorted(self.cars, key=lambda x: x.score)[::-1])


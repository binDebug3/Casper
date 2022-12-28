import main
import Car
import Search

import time
import Compresser
import pandas as pd
import math

import urllib.request
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

class AutoTrader(object):
    def __init__(self):
        """
        Initialize an AutoTrader object. Opens the corresponding website and scrapes relevant data
            to build attribute lists.
        :param self
        Attributes:
                chrome_options  (object): arguments to send with the driver.get call
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
        # set chrome options arguments to configure chrome
        self.chrome_options = Options()
        # disable gpu (doesn't do what I want it to
        self.chrome_options.add_argument("--disable-gpu")
        # set full screen
        self.chrome_options.add_argument("--window-size=1920,1200")
        # disable extensions to help website load faster
        self.chrome_options.add_argument("--disable-extensions")
        self.driver = webdriver.Chrome(options=self.chrome_options)
        # self.driver = webdriver.Chrome()

        # open link
        print("\n\nScanning AutoTrader")
        self.website = main.websites["AutoTrader"]
        self.driver.get(self.website)
        time.sleep(5)
        print(self.website)
        # call methods that scrape the website to build parameter lists
        self.cars = []
        self.resCount = self.getCount()
        self.names = self.findNames()
        self.prices = self.findPrices()
        self.miles = self.findMiles()
        self.images = self.findImages()
        self.links = self.findLinks()

        # page number not currently necessary and not functional for this site
        # self.numPages, self.nextPage = self.getPages()

        self.compression = 50
        self.export = True

    def resetPage(self):
        """
        After website link has been updated and the driver has been closed, opens a new Chrome browser
            to display the next page. Updates all the AutoTrader attributes with the new data.
            This is not my best coding style, but it works for now.
        :param self
        :return:
        """
        self.driver.close()
        self.driver = webdriver.Chrome(options=self.chrome_options)
        # self.driver = webdriver.Chrome()
        self.driver.get(self.getNextPage())
        # wait for page to load
        time.sleep(3)
        self.resCount = self.getCount()
        self.names = self.findNames()
        self.prices = self.findPrices()
        self.miles = self.findMiles()
        self.links = self.findLinks()
        self.images = self.findImages()

    def getNextPage(self):
        """
        Open a new browser with a new link updated by the resetPage method
        :param self
        :return:
        """
        # get current link
        nextPage = self.website
        index = -1
        while nextPage[index].isdigit():
            index -= 1
        index += 1

        # find the next page number
        currStart = nextPage[index:]
        newStart = str(int(currStart) + self.resCount)

        # update website link
        site = nextPage[:len(nextPage) + index] + newStart
        self.website = site
        return site

    def getCount(self):
        """
        Find the number of search results on one page and update self.resCount with it
        :param self
        :return:
        """
        resCountID = "results-text-container"
        time.sleep(1)
        # get results text and parse it
        results = self.driver.find_element(By.CLASS_NAME, resCountID).text
        results = results.split()
        count = results[0].split("-")

        # catch page loading errors by giving the page more time to load
        try:
            return int(count[1]) - int(count[0]) + 1
        except IndexError:
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
        pageClass = "//*[@class='margin-horizontal-lg pagination']"
        # get a list of button elements that represent the number of pages
        pageButtons = self.driver.find_element(By.XPATH, pageClass)
        text = pageButtons.text.split()

        # if there are more than four pages, get all the page button elements
        if len(text) > 4:
            numPages = int(text[-3]) + 1
            nextPagePath = "//*[@class='margin-horizontal-lg pagination']/li[" + str(numPages) + "]/a"
            nextPageButton = self.driver.find_element(By.XPATH, nextPagePath)
        else:
            numPages = 1
            nextPageButton = None
        return numPages, nextPageButton


    def findPrices(self):
        """
        Find the prices for each car
        :param self
        :return: prices (list): list of price strings
        """
        # get a list of price elements and save the parsed text content
        prices = []
        priceClass = "first-price"
        priceElems = self.driver.find_elements(By.CLASS_NAME, priceClass)
        for elem in priceElems:
            prices.append(elem.text.replace(",", ""))
        return prices

    def findMiles(self):
        """
        Find the mileage for each car
        :param self
        :return: miles (list): list of mileage strings
        """
        # get a list of mileage elements and save the parsed text content
        miles = []
        mileClass = "item-card-specifications"
        mileElems = self.driver.find_elements(By.CLASS_NAME, mileClass)
        for elem in mileElems:
            miles.append(elem.text.replace(",", "").split()[0])
        return miles

    def findNames(self):
        """
        Find the listing title for each car
            ex) 2017 Toyota Corolla
        :param self
        :return: names (list): list of name strings
        """
        # get a list of name elements and save the text content
        names = []
        nameID = "text-size-sm-500"
        nameElems = self.driver.find_elements(By.CLASS_NAME, nameID)
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
        match = list(set(main.brands.keys()) & set(nameList))
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
        # get the link elements and build a list of their href attributes
        links = []
        linkPath = "//div[@class='display-flex justify-content-between']/a"
        linkElems = self.driver.find_elements(By.XPATH, linkPath)
        for elem in linkElems:
            carDetails = elem.get_attribute('href')
            links.append(carDetails)
            # self.driver.execute_script("window.open('about:blank','_blank');")
            # all_handles = self.driver.window_handles
            # self.driver.switch_to.window(all_handles[1])
            # self.driver.get(carDetails)
        return links

    def findImages(self):
        """
        Find the images for each car
        :param self
        :return: images (list): list of file folder location strings
        """
        # get a list of image elements
        images = []
        imageClass = "image-vertically-aligned"
        for i in range(1, self.resCount // 4 + 2):
            self.driver.execute_script("window.scrollTo(0, " + str(i*1000) + ")")
            time.sleep(0.2)
        imageElems = self.driver.find_elements(By.CLASS_NAME, imageClass)

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
            except (FileNotFoundError, ValueError) as error:
                print("Image '" + alt + "' did not load properly")
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
        dfOld = pd.read_csv('autotrader.csv')
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
        columns = ["Make", "Model", "Score", "Price", "Year", "Mileage", "Date", "Source", "Link", "Hash"]

        # use Car's toDict method to build a new dataframe, save it, then call the export method
        df = pd.DataFrame([car.toDict() for car in garage])
        df.to_csv('autotrader.csv', mode='a', index=False)
        print(f"Found {df.shape[0]} new cars.")
        self.exportCSV()

    def exportCSV(self):
        """
        Clean database and export update version to overwrite the old version
        :param self
        :return:
        """
        # read the file, drop duplicates and null values, sort, then save file
        df = pd.read_csv('autotrader.csv')
        df = df.drop_duplicates(["Hash"])
        df = df[df.Make != "Make"]
        df.Score = df.Score.astype(float)
        df.Price = df.Price.astype(float)
        df = df.sort_values(["Score", "Price"], ascending=False)
        print(f"Exported {df.shape[0] - 1} cars to 'autotrader.csv'")
        df.to_csv('autotrader.csv', index=False, mode='w')

    def peruseCars(self, send=True):
        if not send:
            print("I will not update the CSV file on this round.")
            self.export = False
        # for each car on each page, build a Car object and set all of its attributes
        while self.resCount == 25:
            for i in range(self.resCount):
                car = Car.Car()
                car.setName(self.names[i + 2])
                car.setPrice(self.prices[i + 1])
                car.setMiles(self.miles[i])
                car.setLink(self.links[i + 1])
                car.setBrand(self.findBrand(car.nameList))
                car.setModel(self.findModel(car.nameList, car.brand))
                car.setYear(self.findYear(car.nameList))
                car.setSource("AutoTrader")
                if i < len(self.images):
                    car.setImage(self.images[i])
                else:
                    car.setImage("Image not found")
                car.setScore()
                self.cars.append(car)
            # thing = self.driver.find_element(By.CSS_SELECTOR, "[aria-label='Next Page']")

            # load the next page
            self.resetPage()
        # export new Car list to CSV
        if len(self.cars) > 0 and self.export:
            self.toCSV(sorted(self.cars, key=lambda x: x.score)[::-1])


# ATTEMPTED AUTOTRADER OBJECT BASED ON A SEARCH SUPERCLASS. I DON'T THINK IT WILL WORK

# class AutoTrader2(Search):
#     def __init__(self):
#         self.webName = "AutoTrader"
#         self.website = "https://www.autotrader.com/cars-for-sale/cars-under-" + p["maxPrice"] + "/" + p["city"] + \
#                         "-" + p["state"] + "-" + p["zipCode"] + \
#                         "?requestId=1819194850&dma=&transmissionCodes=AUT&searchRadius=" + p["radius"] + \
#                         "&priceRange=&location=&marketExtension=include&maxMileage=" + p["maxMiles"] + \
#                         "&isNewSearch=true&showAccelerateBanner=false&sortBy=relevance&numRecords=25&firstRecord=0"
#         self.searchBy = {
#             "count": "results-text-container",
#             "prices": "first-price",
#             "miles": "item-card-specifications",
#             "names": "text-size-sm-500",
#             "links": "//div[@class='display-flex justify-content-between']/a"
#         }
#         super().__init__(self.webName, self.website)
#         self.resCount = self.getCount(self.searchBy["count"])
#         self.prices = self.findPrices(self.searchBy["prices"])
#         self.miles = self.findMiles(self.searchBy["miles"])
#         self.names = self.findNames(self.searchBy["names"])
#         self.links = self.findLinks(self.searchBy["links"])
#         # self.findImages("image-vertically-aligned")
#         self.updateBool()


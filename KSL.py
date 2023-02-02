import time
from selenium.webdriver import ActionChains

import Car
import main
import Compresser
import Search

import urllib.request
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

class KSL(object):
    def __init__(self, detailed=True):
        """
        Initialize a KSL object. Opens the corresponding website and scrapes relevant data
            to build attribute lists.
        :param self
        Attributes:
                NOT IMPLEMENTED chrome_options  (object): arguments to send with the driver.get call
                NOT IMPLEMENTED websites (dict): website names matched to their link based on user preferences
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
        self.website = main.websites["KSL"]
        self.driver = webdriver.Chrome(
            executable_path=r"C:\Users\dalli\PycharmProjects\CarMarket\Casper\chromedriver_win32\chromedriver.exe")
        self.driver.get(self.website)
        print("\n\nScanning KSL")
        print(self.website)
        time.sleep(5)
        self.cars = []
        self.detailed = detailed

        # result count not fully functional for this site
        # self.resCount = self.getCount()
        self.names = self.findNames()
        print("getting prices")
        self.prices = self.findPrices()
        print("done getting prices")
        self.miles = self.findMiles()
        self.compression = 50
        # self.images = self.findImages()
        self.links = self.findLinks()

        # page number not currently necessary and not functional for this site
        # self.pages, self.pageElems = self.getPages()

        self.retailer = "KSL"

    def resetPage(self):
        # might not be necessary if I can get selenium to click like it's supposed to
        raise NotImplemented("Reset page: Can't go on...")

    def getCount(self):
        """
        Find the number of search results on one page and update self.resCount with it
        :param self
        :return:
        """
        resCountID = "eFxiFS"
        try:
            results = self.driver.find_element(By.CLASS_NAME, resCountID).text
            results = results.split()
            print(f"Found {int(results[0])} cars")
            return int(results[0])
        except (IndexError, NoSuchElementException):
            print("Waiting for page to load...")
            time.sleep(2)
            self.getCount()

    def findPrices(self):
        """
        Find the prices for each car
        :param self
        :return: prices (list): list of price strings
        """
        prices = []
        priceClass = "eaOVFJ"
        # get a list of price elements and save the parsed text content
        priceElems = self.driver.find_elements(By.CLASS_NAME, priceClass)
        for elem in priceElems:
            prices.append(elem.text.replace(",", "").replace("$", ""))
        return prices

    def findMiles(self):
        """
        Find the mileage for each car
        :param self
        :return: miles (list): list of mileage strings
        """
        miles = []
        mileClass = "kMOSqH"
        # get a list of mileage elements and save the parsed text content
        mileElems = self.driver.find_elements(By.CLASS_NAME, mileClass)
        for elem in mileElems:
            stat = elem.text.replace(",", "").split()[0]
            if stat[0].isdigit() and int(stat) == 0:
                stat = main.p["altMax"]
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
        nameID = "listing-title"
        # get a list of name elements and save the text content
        nameElems = self.driver.find_elements(By.CLASS_NAME, nameID)
        for elem in nameElems:
            names.append(elem.text)
        return names

    def findLinks(self):
        """
        Find the links to each car's specific information
        :param self
        :return: links (list): list of link strings
        """
        links = []
        carDetails = []
        linkPath = "//div[@class='Listing__ListingInfoWrapper-sc-1v5k5vh-4 kEBiBz']/div/a"
        # get the link elements and build a list of their href attributes
        linkElems = self.driver.find_elements(By.XPATH, linkPath)
        for elem in linkElems:
            text = elem.text.split()
            if len(text) > 0 and text[0].isdigit():
                links.append(elem.get_attribute('href'))
                if self.detailed:
                    elem.click()
                    time.sleep(5)
                    contin = input("Continue?")
                    debot = self.driver.find_elements((By.XPATH, "//p[text()='Press & Hold']"))[3]
                    action = ActionChains(self.driver)
                    action.click_and_hold(debot)
                    action.perform()
                    print("Holding for 5 seconds")
                    time.sleep(5)
                    action.release(debot)
        return links

    def findImages(self):
        """
        Find the images for each car
        :param self
        :return: images (list): list of file folder location strings
        """
        # get a list of image elements
        images = []
        imageClass = "Listing__ListingImageAnchor-sc-1v5k5vh-1"
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

    def peruseCars(self):
        # for each car on each page, build a Car object and set all of its attributes
        for i in range(len(self.names)):
            try:
                car = Car.Car()
                car.setName(self.names[i])
                car.setPrice(self.prices[i])
                car.setMiles(self.miles[i])
                car.setLink(self.links[i])
                car.setBrand(Search.findBrand(car.nameList))
                car.setModel(Search.findModel(car.nameList, car.brand))
                car.setYear(Search.findYear(car.nameList))
                car.setSource(self.retailer)
                # car.setImage(self.images[i])
                car.setScore()
                self.cars.append(car)
            except IndexError as ex:
                print(ex)
                print(f"Index: {i}")
                print(f"Names length: {len(self.names)}")
                print(f"Prices length: {len(self.prices)}")
                print(f"Miles length: {len(self.miles)}")
                print(f"Links length: {len(self.links)}")
                print("Car:")
                print(car)
                print()

        # export new Car list to CSV
        if len(self.cars) > 0:
            Search.toCSV(self.retailer, sorted(self.cars, key=lambda x: x.score)[::-1])

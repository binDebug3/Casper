import time

import Search
import Car
import main
import Compresser

import urllib
from urllib.error import URLError
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common import NoSuchElementException, ElementClickInterceptedException, StaleElementReferenceException, \
    ElementNotInteractableException, InvalidSelectorException


class Carvana(object):
    def __init__(self, detailed=True):
        """
        Initialize a Carvana object. Opens the corresponding website and scrapes relevant data
            to build attribute lists.
        :param self
        Attributes:
                NOT IMPLEMENTED chrome_options  (object): arguments to send with the driver.get() call
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
        self.website = websites["Carvana"]
        print("\n\nScanning Carvana")
        print(self.website)

        # set chrome options arguments to configure chrome
        self.chrome_options = Options()
        # self.chrome_options.add_argument("--disable-gpu")
        # self.chrome_options.add_argument("--headless")
        # self.chrome_options.add_argument("--no-sandbox")
        # self.chrome_options.add_argument("--window-size=1420,1080")
        # set full screen
        self.chrome_options.add_argument("--window-size=1920,1200")
        self.chrome_options.add_argument("--disable-extensions")
        self.driver = webdriver.Chrome(options=self.chrome_options,
            executable_path=r"C:\Users\dalli\PycharmProjects\CarMarket\Casper\chromedriver_win32\chromedriver.exe")

        self.driver.get(self.website)
        time.sleep(2)

        wrongPage = True
        while wrongPage:
            try:
                self.setUpPage()
                wrongPage = False

            except IndexError as ex:
                print("\tAlert: Refreshing page because website B loaded")
                self.driver = webdriver.Chrome(options=self.chrome_options,
                                               executable_path=r"C:\Users\dalli\PycharmProjects\CarMarket\Casper\chromedriver_win32\chromedriver.exe")
                self.driver.get(self.website)

            time.sleep(2)

        self.cars = []
        self.detailed = detailed
        self.compression = 50
        count = 0
        self.getNextPage()

        try:
            self.names = self.findNames()
            self.resCount = len(self.names)
            self.prices = self.findPrices()
            self.miles = self.findMiles()
            self.images = self.findImages()

            print("looking for links")
            self.links = []

            count = 0
            while len(self.links) < len(self.prices):
                self.links, self.carDetails = self.findLinks()
                if count > 0:
                    print("Retrying link search attempt:", count)
                count += 1

        except StaleElementReferenceException as ex:
            time.sleep(2)
            count += 1
            print("Error on start up")
            print(ex.msg)
            print(f"Count: {count}")
            self.names = self.findNames()
            self.resCount = len(self.names)
            self.prices = self.findPrices()
            self.miles = self.findMiles()
            self.images = self.findImages()
            self.links, self.carDetails = self.findLinks()

        self.export = True
        self.retailer = "Carvana"


    def setUpPage(self):
        buttonClass = "fivNwy"
        priceInput = "//input[@class='DebouncedInput__Input-sc-10o1wzo-1 cONhZv']"
        mileInput = "//input[@class='DebouncedInput__Input-sc-10o1wzo-1 jcBsSA']"

        # PRICES
        # click on prices button
        priceButton = self.driver.find_elements(By.CLASS_NAME, buttonClass)
        priceButton = priceButton[0]
        priceButton.click()

        # switch from financed to prices
        financed = self.driver.find_elements(By.CLASS_NAME, "SwitchLabel-g8jqll-2")
        financed = financed[1]
        financed.click()

        # enter maximum price
        enterPrice = self.driver.find_elements(By.XPATH, priceInput)
        enterPrice = enterPrice[1]
        enterPrice.send_keys(main.p["maxPrice"])
        priceButton.click()

        # MILEAGE
        try:
            b = self.driver.find_elements(By.CLASS_NAME, buttonClass)
            c = b[3]
            c.click()
            d = self.driver.find_elements(By.XPATH, mileInput)
            e = d[3]
            e.send_keys(main.p["maxMiles"])
            time.sleep(0.1)
            c.click()

        except (InvalidSelectorException, ElementClickInterceptedException) as ex:
            print("\nMileage Error")
            print(ex.msg)

        except IndexError as ex:
            print("\nMileage Error")
            print(ex)

        self.website = str(self.driver.current_url)


    def setExport(self, send):
        self.export = send


    def resetPage(self):
        """
        After website link has been updated and the driver has been closed, opens a new Chrome browser
            to display the next page. Updates all the Carvana attributes with the new data.
            This is not my best coding style, but it works for now.
        :param self
        :return:
        """
        self.names = self.findNames()
        self.resCount = len(self.names)
        self.prices = self.findPrices()
        self.miles = self.findMiles()
        self.links = self.findLinks()
        self.images = self.findImages()


    def getNextPage(self):
        end = self.website[-1]

        if end.isdigit():
            update = int(end)
            update += 1
            self.website = self.website[:-1] + str(update)

        else:
            self.website += "&page=2"
        self.driver.close()
        self.driver = webdriver.Chrome(options=self.chrome_options,
                                       executable_path=r"C:\Users\dalli\PycharmProjects\CarMarket\Casper\chromedriver_win32\chromedriver.exe")

        self.driver.get(self.website)

        wrongPage = True
        while wrongPage:
            try:
                b = self.driver.find_elements(By.CLASS_NAME, "fivNwy")

                c = b[3]
                c.click()
                wrongPage = False

            except IndexError as ex:
                print(ex)
                print(f"\tAlert: Refreshing page {self.website[-1]} because website B loaded instead")
                self.driver = webdriver.Chrome(options=self.chrome_options,
                                               executable_path=r"C:\Users\dalli\PycharmProjects\CarMarket\Casper\chromedriver_win32\chromedriver.exe")

                print(self.website)
                self.driver.get(self.website)

            time.sleep(2)

        print("Page:", end)


    def findPrices(self):
        """
        Find the prices for each car
        :param self
        :return: prices (list): list of price strings
        """
        prices = []
        priceClass = "//div[@data-testid='price']"

        # get a list of price elements and save the parsed text content
        priceElems = self.driver.find_elements(By.XPATH, priceClass)

        for elem in priceElems:
            prices.append(elem.text.replace(",", "").replace("$", "").split()[0])

        return prices


    def findMiles(self):
        """
        Find the mileage for each car
        :param self
        :return: miles (list): list of mileage strings
        """
        miles = []
        milePath = "//div[@class='trim-mileage']/span[2]"

        # get a list of mileage elements and save the parsed text content
        mileElems = self.driver.find_elements(By.XPATH, milePath)

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
        nameClass = "make-model"

        try:
            # get a list of name elements and save the text content
            nameElems = self.driver.find_elements(By.CLASS_NAME, nameClass)
            for elem in nameElems:
                names.append(elem.text)
            return names

        except (IndexError, NoSuchElementException):
            print("Waiting for page to load...")
            time.sleep(2)
            self.findNames()


    def findLinks(self):
        """
        Find the links to each car's specific information
        :param self
        :return: links (list): list of link strings
        """
        links = []
        carDetails = []
        linkPath = "//div[@class='result-tile']/a"

        # get the link elements and build a list of their href attributes
        linkElems = self.driver.find_elements(By.XPATH, linkPath)
        print("\nLinks")

        for i, elem in enumerate(linkElems):
            links.append(elem.get_attribute('href'))
            print(i, "\t", elem.get_attribute('href'))

        if self.detailed:
            for i in range(len(links)):

                print(f"(Car {i}) Checking: {self.names[i]}")
                try:
                    linkElems[i].click()

                except ElementClickInterceptedException as ex:
                    break

        return links, carDetails


    def findImages(self):
        """
        Find the images for each car
        :param self
        :return: images (list): list of file folder location strings
        """
        # get a list of image elements
        images = []
        imagePath = "//picture[@class='vehicle-image']/img"
        imageElems = self.driver.find_elements(By.XPATH, imagePath)

        for elem in imageElems:
            # get the link to the element
            src = elem.get_attribute('src')

            # build a name for the image based on its alt text
            alt = "_".join(elem.get_attribute('alt').split())
            path = "Images/" + alt + ".png"

            # save the image
            try:
                urllib.request.urlretrieve(src, path)

            except URLError as ex:
                print("Error retrieving image")
                print(path)
                print(ex)

            # compress with image with our custom compression algorithm woot woot
            try:
                Compresser.compress_image(path, self.compression)
                images.append(alt)

            except (FileNotFoundError, ValueError, IndexError) as error:
                print("Image '" + alt + ".png' did not download properly")
                print("More Details:")
                print(src)
                print(error)
                print()
                images.append("No image")

        return images


    def peruseCars(self, send=True):
        if not send:
            print("I will not update the CSV file on this round.")
            self.export = False

        # for each car on each page, build a Car object and set all of its attributes
        while self.resCount == 21 and len(self.cars) < 100:
            time.sleep(0.5)

            for i in range(len(self.names)):
                car = Car.Car(self.detailed)
                car.setName(self.names[i])
                car.setPrice(self.prices[i])
                car.setMiles(self.miles[i])

                try:
                    car.setLink(self.links[i])

                except TypeError:
                    car.setLink(self.links[0][i])

                except IndexError as ex:
                    print("Error in car object construction")
                    print(ex)
                    print(f"\tIndex: {i}")
                    print("\tCar:", car.name)
                    print(f"\tNames length: {len(self.names)}")
                    print(f"\tPrices length: {len(self.prices)}")
                    print(f"\tMiles length: {len(self.miles)}")
                    print(f"\tLinks length: {len(self.links)}")
                    print("\t", self.website)
                    input("Press enter to continue:\n")

                car.setBrand(Search.findBrand(car.nameList))
                car.setModel(Search.findModel(car.nameList, car.brand))
                car.setYear(Search.findYear(car.nameList))
                car.setSource(self.retailer)
                car.setImage(self.images[i])
                car.setScore()

                if self.detailed:
                    car.setAddDetail(self.carDetails[i])
                self.cars.append(car)

            # load the next page
            self.getNextPage()
            time.sleep(1)
            self.resetPage()

        # export new Car list to CSV
        if len(self.cars) > 0 and self.export:
            Search.toCSV(self.retailer, sorted(self.cars, key=lambda x: x.score)[::-1])


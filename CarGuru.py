import time

import Search
import Car
import main
import Compresser
from Casper.CG_Detail import CG_Detail

import urllib
from urllib.error import URLError
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common import NoSuchElementException, ElementClickInterceptedException, StaleElementReferenceException


class CarGuru(object):
    def __init__(self, detailed=True):
        """
        Initialize a CarGuru object. Opens the corresponding website and scrapes relevant data
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
        print("\n\nScanning CarGuru")
        print(websites["CarGuru"])
        # set chrome options arguments to configure chrome
        self.chrome_options = Options()
        # self.chrome_options.add_argument("--disable-gpu")
        # self.chrome_options.add_argument("--headless")
        # self.chrome_options.add_argument("--no-sandbox")
        # self.chrome_options.add_argument("--window-size=1420,1080")
        # set full screen
        self.chrome_options.add_argument("--window-size=1920,1200")
        # disable extensions to help website load faster
        self.chrome_options.add_argument("--disable-extensions")
        self.driver = webdriver.Chrome(options=self.chrome_options,
            executable_path=r"C:\Users\dalli\PycharmProjects\CarMarket\Casper\chromedriver_win32\chromedriver.exe")
        self.driver.get(websites["CarGuru"])
        time.sleep(3)

        self.setMileage()
        self.cars = []
        self.detailed = detailed
        self.compression = 50
        count = 0
        try:
            self.resCount = self.getCount()
            self.names = self.findNames()
            self.prices = self.findPrices()
            self.miles = self.findMiles()
            self.images = self.findImages()
            self.links, self.carDetails = self.findLinks()
        except StaleElementReferenceException as ex:
            time.sleep(2)
            count += 1
            print(ex)
            print(count)
            self.resCount = self.getCount()
            self.names = self.findNames()
            self.prices = self.findPrices()
            self.miles = self.findMiles()
            self.images = self.findImages()
            self.links, self.carDetails = self.findLinks()
        # page number not currently necessary and not functional for this site
        # self.pages, self.pageElems = self.getPages()
        self.export = True
        self.retailer = "CarGuru"

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
        totalPixels = 330000
        offset = int(- (totalPixels - int(main.p["maxMiles"])) / totalPixels * length)
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

    def findLinks(self):
        """
        Find the links to each car's specific information
        :param self
        :return: links (list): list of link strings
        """
        links = []
        carDetails = []
        actions = ActionChains(self.driver)
        linkPath = "//div[@class='MOfIEd XcutUU prRsnF']/a"
        # get the link elements and build a list of their href attributes
        linkElems = self.driver.find_elements(By.XPATH, linkPath)[4:]
        for elem in linkElems:
            links.append(elem.get_attribute('href'))
        if self.detailed:
            for i in range(len(links)):
                print(f"(Car {i}) Checking: {self.names[i]}")
                try:
                    elem = self.driver.find_elements(By.XPATH, linkPath)[4+i]
                    actions.move_to_element(elem).perform()
                    time.sleep(0.5)
                    print(elem.get_attribute("href"))
                    visible = CG_Detail(self.driver, elem)
                    carDetails.append(visible)
                    print(visible)
                except ElementClickInterceptedException as ex:
                    print(f"Error searching car {i} - {self.names[i]}")
                    print(ex.msg)
                    carDetails.append(CG_Detail(None, None))
        return links, carDetails

    def findImages(self):
        """
        Find the images for each car
        :param self
        :return: images (list): list of file folder location strings
        """
        # get a list of image elements
        images = []
        imagePath = "//img[@class='C6f2e2 bmTmAy']"
        imageElems = self.driver.find_elements(By.XPATH, imagePath)
        for elem in imageElems:
            # get the link to the element
            src = elem.get_attribute('src')
            # build a name for the image based on its alt text
            alt = "_".join(elem.get_attribute('alt').split()).replace("\\", "").replace("/", "")
            path = "Images/" + alt + ".png"
            # save the image
            try:
                urllib.request.urlretrieve(src, path)
            except (URLError, FileNotFoundError) as ex:
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
        while self.resCount == 15 and len(self.cars) < 200:
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
                    print("Error")
                    print(ex)
                    print(f"Index: {i}")
                    print(f"Names length: {len(self.names)}")
                    print(f"Prices length: {len(self.prices)}")
                    print(f"Miles length: {len(self.miles)}")
                    print(f"Links length: {len(self.links)}")
                    print(f"Car: {car.name}")
                    print()
                    self.links, self.carDetails = self.findLinks()
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
            try:
                self.getNextPage()
                time.sleep(1)
                self.resetPage()
            except:
                self.resCount = 0
        # export new Car list to CSV
        if len(self.cars) > 0 and self.export:
            Search.toCSV(self.retailer, sorted(self.cars, key=lambda x: x.score)[::-1])


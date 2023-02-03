import AutoTrader
import KSL
import CarGuru
import CarsDirect
import Carvana
import Lowbook
from plyer import notification
from datetime import date
import os

# Hey! Meet Casper :)

# PARAMETERS
p = {
    "maxPrice": "15000",
    "minPrice": "8000",
    "maxMiles": "70000",
    "altMax": "70000",
    "minYear": "2010",
    "currentYear": 2023,
    "radius": "50",
    "city": "provo",
    "state": "ut",
    "zipCode": "84601",
    "used": True,

    "priceWeight": 1,
    "mileageWeight": 2,
    "yearWeight": 1,
    "makeWeight": 1,
}
fav = 1
med = 0.5
bad = 0
brands = {"toyota": fav, "honda": fav, "chevrolet": med, "ford": fav, "mercedes-benz": bad,
          "jeep": bad, "bmw": bad, "porsche": bad, "subaru": med, "nissan": med,
          "volkswagen": med, "lexus": med, "acura": med, "dodge": bad, "hyundai": med,
          "mazda": med, "tesla": fav, "kia": bad, "infiniti": med, "mitsubishi": bad,
          "mini": bad, "fiat": bad, "chrysler": bad, "buick": bad, "lincoln": bad, "audi": bad,
          "ram": bad, "scion": bad, "alfa": bad, "land": bad, "cadillac": bad, "smart": bad,
          "volvo": bad, "hummer": bad, "gmc": bad, "polaris": bad, "textron": bad, "harley": bad}
# encode carsdirect parameters
cdp = {"1050": "%600%600%6010%6014%60true%7C"}
cdm = {"50000": "%601%600%600%609%60true%7C",
       "none": ""}
cdy = {"0023": "%602%600%607%6030%60true%7C"}
websites = {
            "AutoTrader": "https://www.autotrader.com/cars-for-sale/cars-under-" + p["maxPrice"] + "/" + p["city"] +
                          "-" + p["state"] + "-" + p["zipCode"] +
                          "?requestId=1819194850&dma=&transmissionCodes=AUT&searchRadius=" + p["radius"] +
                          "&priceRange=&location=&marketExtension=include&maxMileage=" + p["maxMiles"] +
                          "&isNewSearch=true&showAccelerateBanner=false&sortBy=relevance&numRecords=25&firstRecord=0",
            "CarGuru": "https://www.cargurus.com/Cars/inventorylisting/viewDetailsFilterViewInventoryListing.action?zip=" +
                        p["zipCode"] + "&inventorySearchWidgetType=PRICE&maxPrice=" + p["maxPrice"] +
                        "&showNegotiable=true&sortDir=ASC&sourceContext=usedPaidSearchNoZip&distance=" + p["radius"] +
                        "&minPrice=" + p["minPrice"] + "&sortType=DEAL_SCORE",
            "KSL2": "https://cars.ksl.com/search/yearFrom/" + p["minYear"] + "/yearTo/" + str(p["currentYear"]) +
                   "/mileageFrom/0/mileageTo/" + p["maxMiles"] + "/priceFrom/" + p["minPrice"] + "/priceTo/" +
                   p["maxPrice"] + "/city/" + p["city"] + "/state/" + p["state"].upper(),
            "KSL": "https://cars.ksl.com/search/mileageTo/" + p["maxMiles"] + "/priceTo/" + p["maxPrice"] + "/yearFrom/" +
                    p["minYear"] + "/priceFrom/" + p["minPrice"],
            "CarsDirect": "https://www.carsdirect.com/used_cars/listings?dealerId=&sellerId=&active=&zipcode=" +
                          p["zipCode"] + "&distance=" + p["radius"] + "&qString=Price" + cdp["1050"] + "Year" +
                          cdy["0023"] + "Mileage" + cdm["50000"] +
                          "&keywords=&pageNum=1&sortColumn=Default&sortDirection=ASC&makeName=&modelName=",
            "Lowbook": "https://www.lowbooksales.com/used-cars?_gmod%5B0%5D=Dfe_Modules_VehiclePrice_Module&_gmod%5B1%5D=" +
                       "Dfe_Modules_CustomizePayment_Module&direction=desc&t=u&location[]=Lindon&" +
                       "priceto=" + p["maxPrice"] + "&mileageto=" + p["maxMiles"] + "&sf=sf_location",
            "Carvana": "https://www.carvana.com/cars",
}
detailed = False
selector = [6, 7]


if __name__ == "__main__":
    # Casper scrapes websites and opens their Excel file based on the selector list
    csv = 'start "excel.exe" "autotrader.csv"'

    if any(i in selector for i in [0, 1]):
        AutoTrader.AutoTrader().peruseCars()
    if any(i in selector for i in [0, 2]):
        KSL.KSL(detailed=False).peruseCars()
        csv = 'start "excel.exe" "ksl.csv"'
    if any(i in selector for i in [0, 3]):
        CarGuru.CarGuru(detailed=detailed).peruseCars()
        csv = 'start "excel.exe" "CarGuru.csv"'
    if any(i in selector for i in [0, 4]):
        CarsDirect.CarsDirect(detailed=detailed).peruseCars()
        csv = 'start "excel.exe" "CarsDirect.csv"'
        csv = 'start "excel.exe" "Detailed_CarsDirect.csv"'
    if any(i in selector for i in [0, 6]):
        Carvana.Carvana(detailed=detailed)
        # csv = 'start "excel.exe" "Carvana.csv"'
    if any(i in selector for i in [0, 7]):
        Lowbook.Lowbook(detailed=detailed)
        # csv = 'start "excel.exe" "Lowbook.csv"'

    # send a notification to the computer
    if len(selector) == 1:
        s = ""
    else:
        s = "s"
    notification.notify(
        title="Casper",
        message=f"Your data harvest for {len(selector)} retailer{s} on {date.today()} is done.",
        # display time
        timeout=10
    )

    # open the corresponding Excel file
    os.system(csv)

# list of things to do
# TODO test functionality on wider parameters and different parameters

# TODO NLP understand descriptions
# TODO make image classifier for cool cars

# small things
# TODO scrape lowbook
# TODO scrape carvana

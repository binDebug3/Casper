import AutoTrader
import KSL
import CarGuru

# Hey! Meet Casper :)

# PARAMETERS
p = {
    "maxPrice": "15000",
    "minPrice": "8000",
    "maxMiles": "45000",
    "altMax": "50000",
    "minYear": "2000",
    "currentYear": 2022,
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
          "jeep": med, "bmw": bad, "porsche": bad, "subaru": med, "nissan": med,
          "volkswagen": med, "lexus": med, "acura": med, "dodge": bad, "hyundai": med,
          "mazda": bad, "tesla": bad, "kia": bad, "infiniti": med, "mitsubishi": bad,
          "mini": bad, "fiat": bad, "chrysler": bad, "buick": med, "lincoln": bad, "audi": bad,
          "ram": bad, "scion": med}

if __name__ == "__main__":
    # AutoTrader.AutoTrader().peruseCars()
    # KSL.KSL().peruseCars()
    CarGuru.CarGuru().peruseCars()

# TODO scrape carsdirect
# TODO make the search class abstract

# TODO make script run automatically
# TODO make notification when good cars are found
# TODO scrape more data from each page
# TODO make image classifier for cool cars
# TODO scrape images
# TODO compress images
# TODO optimize code efficiency
# TODO test functionality on wider parameters and different parameters
# TODO NLP understand descriptions
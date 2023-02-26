import pandas as pd
import pickle
import datetime
import main
import math


def checkDamage(comment):
    keyWords = ['salvage', 'damage', 'broken', 'flood', ' riot', 'hail', 'stolen',
                'windstorm', 'tornado', ' fire', 'accident', 'broken', ' bent',
                ' flaw', 'busted', 'dinged', 'total loss', 'junked', 'rebuilt',
                'wrecked', 'reconstructed', 'branded title', 'insurance loss',
                'dysfunctional', 'maintenance problem', 'lemon',
                'odometer discrepancy', 'repairable', 'earthquake',
                'odometer rollback', 'water damage', 'recovered theft', 'buyback']
    for key in keyWords:
        if key in comment:
            return True
    return False


def findBrand(nameList):
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
    # elif length > 1:
    #     print("Length was greater than zero")
    #     print(nameList)
    #     print(length)
    #     print(match)
    #     return " ".join(match)
    else:
        return match[0]


def findModel(nameList, brand):
    """
    Extract the model of the car from the listing title
    :param nameList: name listing for the car split by spaces into a list
    :param brand: brand of the car
    :return:
    """
    if brand != "Not recognized":
        # get the index of the brand in the name list
        try:
            index = nameList.index(brand)
            # return the rest of the list following the brand
            return " ".join(nameList[index + 1:])
        except ValueError as ex:
            index = nameList.index(brand.split()[0])
            # return the rest of the list following the brand
            return " ".join(nameList[index + 1:])
    return "None"


def findYear(nameList):
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


def getNewCars(retailer, garage):
    """
    NOT currently used
    Read all saved cars from Excel spreadsheet and compare it to the cars scraped to identify new cars.
    This is not the most efficient approach, and it fails to recognize matches if any of the parameters changed,
    for better or for worse
    :param garage:
    :return: newCars (list): list of car objects that were not already in the database
    """
    # read the csv and get a list of their hashed IDs woot woot
    fileName = "Data/" + retailer + ".csv"
    dfOld = pd.read_csv(fileName)
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


def toCSV__OLD__(retailer, garage):
    """
    Convert a list of Car objects to a CSV
    :param retailer:
    :param garage:
    :return:
    """
    # this is only useful when saving a new csv that does not already have columns
    columns = ["Make", "Model", "Score", "Price", "Year", "Mileage", "Date", "OnSale", "Days",
               "Source", "Link", "Image", "Hash"]
    fileName = "Data/" + retailer + ".csv"

    dfOld = pd.read_csv(fileName)
    dfOld.OnSale = "False"

    # use Car's toDict method to build a new dataframe, save it, then call the export method
    df = pd.DataFrame([car.toDict() for car in garage])
    df.to_csv(fileName, mode='a', index=False)
    print(f"Found {df.shape[0]} new cars.")
    # exportCSV(retailer)

    # visibility statement
    print(f"Exported {len(garage)} cars to {fileName}")


def toCSV(retailer, garage):
    """
    Clean database and export update version to overwrite the old version
    :param garage: 
    :param retailer:
    :return:
    """
    # this is only useful when saving a new csv that does not already have columns
    columns = ["Make", "Model", "Score", "Price", "Year", "Mileage", "Date", "OnSale", "Days",
               "Source", "Link", "Image", "Hash"]
    # read the file and set OnSale to false
    fileName = "Data/" + retailer + ".csv"
    dfOld = pd.read_csv(fileName)
    dfOld.OnSale = "False"

    # use Car's toDict method to build a new dataframe with the new cars
    df = pd.DataFrame([car.toDict() for car in garage])
    df.to_csv("Data/New_CarGuru_011823.csv", index=False, mode='w')
    print(f"Found {df.shape[0]} new cars.")

    # append new cars to old cars
    df = pd.concat([dfOld, df])

    # drop hash duplicates so that OnSale=True remains
    df = df[df.Make != "Make"]
    df = df.sort_values(["OnSale", "Date"], ascending=False)
    df = df.drop_duplicates(["Hash"])

    # clean data frame
    df.Score = df.Score.astype(float)
    df.Price = df.Price.astype(float)
    df.Days = pd.to_numeric(df.Days)

    # increment the number of days since last update
    today = datetime.date.today()
    pickleName = "Data/last_update_" + retailer + ".pickle"

    # get the last update date
    try:
        last_update = pickle.load(open(pickleName, "rb"))
    except (OSError, IOError) as e:
        last_update = today
        pickle.dump(last_update, open(pickleName, "wb"))

    # update days on market if car is still on sale
    df.Days = df.apply(lambda x: x.Days + (today - last_update).days if x.OnSale == "True" else x.Days, axis=1)
    # df.Days = df.Days.add((today - last_update).days)

    # save the most recent update date (today)
    with open(pickleName, 'wb') as pickle_file:
        pickle.dump(today, pickle_file)

    # sort the dataframe and update the csv
    df = df.sort_values(["Days"], ascending=True)
    df = df.sort_values(["OnSale", "Score", "Price"], ascending=False)
    df.to_csv(fileName, index=False, mode='w')

def combine():
    df_a = pd.read_csv('Data/autotrader.csv')
    df_b = pd.read_csv('Data/ksl.csv')
    df_c = pd.read_csv('Data/Carvana.csv')
    df_d = pd.read_csv('Data/CarGuru.csv')
    df_e = pd.read_csv('Data/CarsDirect.csv')

    df_combined = pd.concat([df_a, df_b, df_c, df_d, df_e])
    df_combined = df_combined.sort_values(by=['Days'], ascending=True)
    df_combined = df_combined.sort_values(by=['OnSale', 'Score'], ascending=False)
    df_combined = df_combined.drop_duplicates(subset='Hash')

    df_combined.to_csv("Data/current_market.csv", index=False, mode='w')
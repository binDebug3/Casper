import os

import pytest
import Car
import pandas as pd

def test_score():
    df = pd.read_csv('Data/ksl.csv')
    originalLength = df.size
    for index, row in df.iterrows():
        car = Car.Car()
        car.setPrice(row["Price"])
        car.setMiles(row["Mileage"])
        car.setYear(row["Year"])
        car.setBrand(row["Make"])
        car.setScore()
        df.loc[index, "Score"] = car.score
        assert car.score > 0
    df.Score = df.Score.astype(float)
    df = df.sort_values(["Score", "Price"], ascending=False)
    df = df.drop_duplicates(["Year", "Make", "Model", "Price", "Mileage"])
    df.to_csv("Data/ksl.csv", mode='w', index=False)
    os.system('start "excel.exe" "ksl.csv"')

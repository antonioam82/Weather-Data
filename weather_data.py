from datetime import datetime
import matplotlib.pyplot as plt
from meteostat import Point, Daily, Monthly
from geopy.geocoders import Nominatim
import argparse

def main():
    parser = argparse.ArgumentParser(prog="WEATHER DATA 0.0",conflict_handler='resolve',
                                     description="Get wether metrics in command line")
    parser.add_argument('-reg','--region',help="Iinterest region")
    parser.add_argument('-ptn','--point',help="Coords")
    parser.add_argument('-dt','--data',choices=['tavg','tmin','tmax','prcp','snow','wdir','wspd','wpgt','pres','tsun'],help="Wheather metrics")
    parser.add_argument('-per','--periodicity',choices=['Daily','Monthly'],help="Periodicity for time series")
    parser.add_argument('-st','--start',help="Start date for time series")
    parser.add_argument('-e','--end',help="End date for time series")
    parser.add_argument('-plt','--plot',action='store_true',help="Show graph")

    args = parser.parse_args()


if __name__=='__main__':
    main()

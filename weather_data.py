from datetime import datetime
import matplotlib.pyplot as plt
from meteostat import Point, Daily, Monthly
from geopy.geocoders import Nominatim
from colorama import Fore, init, Style
import argparse

init()

now = datetime.now()
day = now.day
month = now.month
year = now.year

def main():
    parser = argparse.ArgumentParser(prog="WEATHER DATA 0.0",conflict_handler='resolve',
                                     description="Get wether metrics in command line")
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-reg','--region',type=set_reg_point,help="Interest region")
    group.add_argument('-ptn','--point',type=set_point,help="Coords")
    parser.add_argument('-dt','--data',choices=['tavg','tmin','tmax','prcp','snow','wdir','wspd','wpgt','pres','tsun'],help="Wheather metrics")
    parser.add_argument('-per','--periodicity',choices=['Daily','Monthly'],help="Periodicity for time series")
    parser.add_argument('-st','--start',type=check_dateformat,help="Start date for time series")
    parser.add_argument('-e','--end',default='{}/{}/{}'.format(year,month,day),type=check_dateformat,help="End date for time series")
    parser.add_argument('-plt','--plot',action='store_true',help="Show graph")
    parser.add_argument('-sv','--save',action='store_true',help="Save table")

    args = parser.parse_args()

    if not args.region and not args.point:
        parser.error(Fore.RED+Style.BRIGHT+"region or point is required."+Fore.RESET+Style.RESET_ALL)
    
    if args.end > args.start:
        parser.error(Fore.RED+Style.BRIGHT+"start date must be smaller than end date."+Fore.RESET+Style.RESET_ALL) 
    
    #print(args.start)
    #print(args.end)

def check_dateformat(val):
    try:
        date = datetime.strptime(val, '%Y/%m/%d')
        return date
    except Exception as e:
        raise argparse.ArgumentTypeError(Fore.RED+Style.BRIGHT+f"BAD DATE FORMAT: {str(e)}"+Fore.RESET+Style.RESET_ALL)

def set_reg_point(val):
    try:
        loc = Nominatim(user_agent="GetLoc")
        getLoc = loc.geocode(val)
        points = [getLoc.latitude,getLoc.longitude]
        print(points)
        return points
    except Exception as e:
        raise argparse.ArgumentTypeError(Fore.RED+Style.BRIGHT+str(e)+Fore.RESET+Style.RESET_ALL)

def set_point(val):
    try:
        vals = val.split("-")
        points = [vals[0],vals[1]]
        print(points)
        return points
    except Exception as e:
        raise argparse.ArgumentTypeError(Fore.RED+Style.BRIGHT+str(e)+Fore.RESET+Style.RESET_ALL)
        

if __name__=='__main__':
    main()
    
    

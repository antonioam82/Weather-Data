from datetime import datetime
import matplotlib.pyplot as plt
from meteostat import Point, Daily, Monthly
from geopy.geocoders import Nominatim
from colorama import Fore, init, Style
import pathlib
import argparse

init()

now = datetime.now()
day = now.day
month = now.month
year = now.year

dats = ['tavg','tmin','tmax','prcp','snow','wdir','wspd','wpgt','pres','tsun']

def main():
    parser = argparse.ArgumentParser(prog="WEATHER DATA 0.0",conflict_handler='resolve',
                                     description="Get wether metrics in command line")
    #group = parser.add_mutually_exclusive_group()
    parser.add_argument('-reg','--region',type=set_reg_point,help="Interest region")
    parser.add_argument('-long','--longitude',type=float,help="Coords")
    parser.add_argument('-lat','--latitude',type=float,help="Interest region")
    parser.add_argument('-dt','--data',type=set_data,help="Wheather metrics")
    parser.add_argument('-per','--periodicity',choices=['Daily','Monthly'],help="Periodicity for time series")
    parser.add_argument('-st','--start',type=check_dateformat,required=True,help="Start date for time series")
    parser.add_argument('-e','--end',default='{}/{}/{}'.format(year,month,day),type=check_dateformat,help="End date for time series")
    parser.add_argument('-plt','--plot',action='store_true',help="Show graph")
    parser.add_argument('-sv','--save',type=check_extension,help="Save table") #,action='store_true'

    args = parser.parse_args()

    if args.region:
        if args.longitude or args.latitude:
            parser.error(Fore.RED+Style.BRIGHT+"-lat/--latitude and -long/--longitude: not allowed with argument -reg/--region"+Fore.RESET+Style.RESET_ALL)
    else:
        if not args.longitude or not args.latitude:
            parser.error(Fore.RED+Style.BRIGHT+"region or point are required"+Fore.RESET+Style.RESET_ALL)
    
    if args.end < args.start:
        parser.error(Fore.RED+Style.BRIGHT+"start date must be smaller than end date."+Fore.RESET+Style.RESET_ALL)

    get_data(args)

def check_extension(val):
    extension = pathlib.Path(val).suffix
    if extension == ".txt" or extension == ".xlsx" or extension == ".csv":
        print('OK')
        return val
    else:
        raise argparse.ArgumentTypeError(Fore.RED+Style.BRIGHT+f"BAD FILE FORMAT: Format must be 'txt', 'xlsx' or 'csv'"+Fore.RESET+Style.RESET_ALL)

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

def set_data(vals):
    global dats
    choices = ['tavg','tmin','tmax','prcp','snow','wdir','wspd','wpgt','pres','tsun']
    dats = vals.split(",")
    for i in dats:
        if i not in choices:
            raise argparse.ArgumentTypeError(Fore.RED+Style.BRIGHT+"BAD CHOICE"+Fore.RESET+Style.RESET_ALL)
            break

def set_point(val):
    try:
        vals = val.split("-")
        points = [vals[0],vals[1]]
        print(points)
        return points
    except Exception as e:
        raise argparse.ArgumentTypeError(Fore.RED+Style.BRIGHT+str(e)+Fore.RESET+Style.RESET_ALL)

def get_data(args):
    try:
        if not args.region:
            region = Point(args.latitude, args.longitude)
            #print(region)
        else:
            region = Point(args.region[0], args.region[1])
        data = Daily(region, args.start, args.end)
        data = data.fetch()
        print("\n"+Fore.GREEN)
        print(data[dats])
        print("\n"+Fore.RESET)

        if args.plot:
            data.plot(y=dats)
            plt.show()
            
    except Exception as e:
        print(Fore.RED+Style.BRIGHT+str(e)+Fore.RESET+Style.RESET_ALL)

if __name__=='__main__':
    main()
    
    
    
    
    

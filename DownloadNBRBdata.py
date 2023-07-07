import sys
import argparse
import time
import requests
import json
from enum import Enum
from datetime import datetime
import traceback

class Currency(Enum):
    USD = 'USD'
    EUR = 'EUR'

def SaveToJson(data:list, currency:Currency, startYear:int, endYear:int):
    with open(f"./{currency.value}-{startYear}-{endYear}.json", 'w') as output_file:
        jsondata = json.dumps(data, indent=4)
        output_file.write(jsondata)

# establishing session
s = requests.Session() 
s.headers.update({'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'})

def download_data(session, url):
    request = session.get(url)
    return request.text

def download_currency_data(curId:int, year:int)->list:
    data = []

    time.sleep(0.3)
    url1 = "https://api.nbrb.by/exrates/rates/dynamics/{0}?startdate={1}-01-01&enddate={1}-06-30"
    fdata = download_data(s, url1.format(curId, year))
    data += json.loads(fdata)

    time.sleep(0.4)
    url2 = "https://api.nbrb.by/exrates/rates/dynamics/{0}?startdate={1}-07-01&enddate={1}-12-31"
    fdata = download_data(s, url2.format(curId, year))
    data += json.loads(fdata)
    
    print(f"for {len(data)} days")
    return data

def DownloadUsdData(startYear:int, endYear:int)->list:
    data = []
    currency = Currency.USD.value
    
    id = 145
    for year in range(startYear, 2022):
        print(f"{currency}({id}) for {year} was downloaded")
        data += download_currency_data(id, year)        

    id = 431
    for year in range(2021, endYear+1):
        print(f"{currency}({id}) for {year} was downloaded")
        data += download_currency_data(id, year)

    return data

def DownloadEurData(startYear:int, endYear:int)->list:
    data = []
    currency = Currency.EUR.value
    
    id = 19
    for year in range(startYear, 2017):
        print(f"{currency}({id}) for {year} was downloaded")
        data += download_currency_data(id, year)        

    id = 292
    for year in range(2016, 2022):
        print(f"{currency}({id}) for {year} was downloaded")
        data += download_currency_data(id, year)        

    id = 451
    for year in range(2021, endYear+1):
        print(f"{currency}({id}) for {year} was downloaded")
        data += download_currency_data(id, year)

    return data

def main() -> int:

    print(sys.argv)

    parser = argparse.ArgumentParser(description="BSU Salary")
    parser.add_argument('-USD', '--USD', action='store_true', help="Get Data for USD currency")
    parser.add_argument('-EUR', '--EUR', action='store_true', help="Get Data for EUR currency")

    args = parser.parse_args()

    startYear = 2000
    endYear = 2023

    try:
        print(args)

        if args.USD:
            SaveToJson(DownloadUsdData(startYear,endYear), Currency.USD, startYear,endYear)           

        if args.EUR:
            SaveToJson(DownloadEurData(startYear,endYear), Currency.EUR, startYear,endYear)

    except Exception as error:
        print()
        print("ERROR:")
        traceback.print_exception(error)
        return -1

    return 0

if __name__ == '__main__':
    sys.exit(main())
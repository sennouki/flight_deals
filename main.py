import os

from google_sheets import GoogleSheets
from flight_searcher import FlightSearcher
from sms_client import Sms

sms = Sms()
my_sheets = GoogleSheets(url=os.getenv("SHEETS_URL"))
my_sheets.iata_code_to_sheets()
flight_searcher = FlightSearcher()
flight_searcher.find_flights()

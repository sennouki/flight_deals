import os
import datetime as dt
import requests

from google_sheets import GoogleSheets
from sms_client import Sms

account_sid = YOUR_ACCOUNT_SID
auth_token = YOUR_AUTH_TOKEN

sms = Sms()
now = dt.datetime.now().date().strftime("%d/%m/%Y")
six_months = dt.datetime.now() + dt.timedelta(days=30 * 6)
six_months = six_months.strftime("%d/%m/%Y")
data_manager = GoogleSheets(url=os.getenv("SHEETS_URL"))


class FlightSearcher:

    def find_flights(self):
        # create an empty list to store all flight data
        all_flights_data = []
        # create a headers dictionary with the API key
        headers = {
                "apikey": os.getenv("KIWI_API")
            }
        # get the list of cities from the data manager
        datas = data_manager.get_data()
        # iterate over the cities
        for cities in datas["prices"]:
            # create the parameters for the API request
            params = {
                "fly_from": "ATH",
                "fly_to": cities["iataCode"],
                "date_from": now,
                "date_to": six_months,
                "curr": "EUR",
                "max_stopovers": 0,
                "nights_in_dst_from": 7,
                "nights_in_dst_to": 28,
                "flight_type": "round",
                "one_for_city": 1,
            }

            # make the API request
            response = requests.get(url="https://api.tequila.kiwi.com/v2/search", headers=headers, params=params)
            # raise an exception if the request is not successful
            response.raise_for_status()
            # get the flight data from the response, or an empty list if the data key is not present
            flights_data = response.json().get("data", [])
            # check if the flight data list is not empty
            if flights_data:
                # print the flight data for each flight
                for flight in flights_data:
                    print(f'{flight["cityTo"]} από €{flight["price"]}! Για να το κλείσεις πάτα εδώ: {flight["deep_link"]}')
                    # send sms if the price of the flight is lower than the lowest price in sheets
                    if int(flight["price"]) < int(cities["lowestPrice"]):
                        sms.send_sms(message=f"Low alert price! Tickets to {flight['cityTo']} only for €{flight['price']}!")
                # add the flight data to the all_flights_data list
                all_flights_data.extend(flights_data)

            else:
                # if flight data is empty, print a message
                print(f"Δεν βρέθηκε εισιτήριο για το {cities['city']}")
        return all_flights_data

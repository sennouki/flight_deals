import os
import requests


class GoogleSheets:
    def __init__(self, url):
        self.iata_code = None
        self.data = None
        self.url = url

    def get_data(self):
        """
        Makes a GET request to the provided URL and returns the response in JSON format.
        Raises an error if the request is not successful.
        """
        response = requests.get(url=self.url)
        response.raise_for_status()
        data = response.json()
        return data

    @staticmethod
    def iata_code_finder(data):
        """
        Iterates through the data and finds the IATA code for each city using the KIWI API.
        Returns the data with the IATA code added for each city.
        """
        for cities in data["prices"]:
            params = {
                "term": (cities["city"])
            }
            headers = {
                "apikey": os.getenv("KIWI_API")
            }
            response = requests.get(url=os.getenv("KIWI_URL"), params=params, headers=headers)
            response.raise_for_status()
            final_data = response.json()
            cities["iataCode"] = (final_data["locations"][0]["code"])
            iata_code = {
                "price": {
                    "iataCode": cities["iataCode"],
                    "id": (cities["id"])
                }
            }
            print(iata_code)
        return data

    def iata_code_to_sheets(self):
        """
        Retrieves the data, finds the IATA code for each city, and updates the Google Sheets document
        with the IATA code for each city.
        """
        self.data = self.iata_code_finder(data=self.get_data())
        for item in self.data["prices"]:
            iata_code = {
                "price": {
                    "iataCode": item["iataCode"],
                    "id": item["id"]
                }
            }
            rp = requests.put(url=f"{os.getenv('SHEETS_URL')}/{item['id']}", json=iata_code)
            rp.raise_for_status()
            print(rp.status_code)

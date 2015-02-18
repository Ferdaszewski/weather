"""Module to get and store weather data."""
import datetime
import json
import os
import pytz
import requests

# Forecast.io API key
API_KEY = os.environ["FORECASTIO_API"]


class Forecast(object):
    """Forecast data for a specific location and time"""
    def __init__(self, lat, lng, time=None, units='auto'):
        self.lat = lat
        self.lng = lng
        self.units = units
        self.time = time
        self.headers, self.data = self._get_data()

    def _get_data(self):
        """Get JSON data from forecast.io"""
        if self.time is None:
            url = "https://api.forecast.io/forecast/%s/%s,%s" % (
                API_KEY, self.lat, self.lng)
        else:
            # Time in ISO format without microseconds
            url_time = self.time.replace(microsecond=0).isoformat()

            url = "https://api.forecast.io/forecast/%s/%s,%s,%s" % (
                API_KEY, self.lat, self.lng, url_time)

        response = requests.get(url, params={'units': self.units})
        return response.headers, response.json()

if __name__ == '__main__':
    # Portland, OR
    lat = 45.52
    lng = -122.681944

    # Test, save JSON to local file and print HTTP response
    test_forecast = Forecast(lat, lng)
    print test_forecast.headers
    with open('data-dump.json', 'w') as f:
        json.dump(test_forecast.data, f, indent=2)

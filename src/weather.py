"""Module to get and store weather data."""
import datetime
import os
import pygal
import pytz
import requests

# Forecast.io API key
API_KEY = os.environ["FORECASTIO_API"]


class Forecast(object):
    """Forecast data for a specific location and time"""
    def __init__(self, lat, lng, time=None, units='auto'):
        self.lat = lat
        self.lng = lng
        self.data = {}
        self.units = units
        self.time = time

    def get_data(self):
        """Get JSON data from forecast.io"""
        if self.time is None:
            url = "https://api.forecast.io/forecast/%s/%s,%s" % (
                API_KEY, self.lat, self.lng)
        else:
            # Time in ISO format without microseconds
            url_time = self.time.replace(microsecond=0).isoformat()

            url = "https://api.forecast.io/forecast/%s/%s,%s,%s" % (
                API_KEY, self.lat, self.lng, url_time)

        return requests.get(url, params={'units': self.units})


def svg_line_chart(line_data):
    """Returns an svg lines chart from a list of tuples
    ('line name', [line, data])
    """
    line_chart = pygal.Line()
    for line in line_data:
        line_chart.add(line[0], line[1])

    # For testing write to file
    line_chart.render_to_file('line_chart.svg')

    return line_chart


def json_line(json, name, data_block='hourly'):
    """Generate a list of data points from the json data file for name
    and return a tuple: ('name', [the, list]).
    """
    try:
        data = json[data_block]['data']
    except IndexError as error:
        print "Error. JSON data does not have %s data block." % data_block
        print error
        return None

    try:
        line_data = [block[name] for block in data]
    except IndexError as error:
        print "Error. JSON data bock %s does not have %s key." % (
            data_block, name)
        print error
        return None

    return (name, line_data)


if __name__ == '__main__':
    # Portland, OR
    lat = 45.52
    lng = -122.681944

    forecast_json = Forecast(lat, lng).get_data().json()

    line_names = ['cloudCover', 'precipProbability']
    line_data = []
    for line_name in line_names:
        line_data.append(json_line(forecast_json, line_name))

    svg_line_chart(line_data)

#-*- coding: utf-8 -*-

"""A weather dashboard web app."""
import codecs
from datetime import datetime
from datetime import timedelta
import jinja2
import pytz
import re

import locsearch
import weatherdata


class Location(object):
    """Location of the weather forecast."""
    def __init__(self):
        self.lat_lng = None
        self.name = None

    def search(self, search_term):
        """Search for the latitude and longitude of the search_term and
        sets the object attributes to that location.

        Returns boolean indicating success of the search.
        """

        # Term needs to be in Unicode
        if not isinstance(search_term, unicode):
            try:
                search_term = unicode(search_term, 'utf-8')
            except TypeError:
                raise TypeError("Cannot convert %r to unicode." % search_term)

        # Validate search_term, no empty strings or None
        try:
            search_list = search_term.split(',')
            search_list = [i.strip() for i in search_list if i.strip()]
            if len(search_list) == 0 or len(search_list) > 2:
                raise AttributeError
        except AttributeError:
            raise TypeError("Not a valid search term: %r" % search_term)

        # Zip-code-like string (i.e. five digits)
        if len(search_list) == 1 and re.match(r'^\d{5}$', search_list[0]):
            result, place = locsearch.zip_search(search_list[0])
        # Search for the city
        else:
            result, place = locsearch.city_search(search_list)

        self.lat_lng = result
        self.name = place
        return result is not None


class Weather(object):
    """Weather forecast for a location."""
    def __init__(self, location):
        """Args:
                location is a Location object.
        """
        self.location = location
        self.forecast = {}

    def get_forecast(self, time=None):
        """Get the forecast for location, with the option to define a
        past or future datetime.datetime. Default None is now.
        """
        temp_forecast = weatherdata.Forecast(*self.location.lat_lng)
        self.forecast = temp_forecast.data


class Webpage(object):
    """Webpage that displays the weather information.

    Args: forecast is a Weather object.
    """
    def __init__(self, weather):
        self.forecast = weather.forecast
        self.name = weather.location.name

    def _get_data_list(self, data_key, time_frame='hourly'):
        """Returns list of elements of the data_key from forecast in the
        time_frame.
        """
        try:
            data_block = self.forecast[time_frame]['data']
        except IndexError:
            print "Error. No weather data for hourly time frame."
        try:
            data_list = [chunk[data_key] for chunk in data_block]
        except IndexError:
            print "Error. JSON data bock %s does not have %s key."
        return data_list

    def _utc_to_loc(self, dt_list, loc_tz):
        """Helper method to convert a list of Unix timestamps to the
        loc_tz timezone and round to the nearest hour and return it.
        """
        # Convert from a Unix timestamp to a datetime object
        utc_tz = pytz.utc
        dt_list = [datetime.utcfromtimestamp(dt).replace(tzinfo=utc_tz)
                   for dt in dt_list]

        # Localize and normalize datetime to forecast timezone
        dt_list = [loc_tz.normalize(utc_dt.astimezone(loc_tz))
                   for utc_dt in dt_list]

        # Round to the nearest hour (3600 seconds)
        hour = 3600
        for idx, dt_loc in enumerate(dt_list):
            # Remove timezone for math to work
            dt_loc = dt_loc.replace(tzinfo=None)

            # Round naive time to nearest hour
            seconds = (dt_loc - dt_loc.min).seconds
            rounding = (seconds+hour/2) // hour * hour
            dt_loc += timedelta(0, rounding-seconds, -dt_loc.microsecond)

            # Add timezone back in
            dt_list[idx] = dt_loc.replace(tzinfo=loc_tz)

        return dt_list

    def render_page(self):
        """Renders the webpage using the forecast data and returns the
        html as a string.
        """
        # Collect data for template
        temp_data = {
            'place_name': self.name,
            'alert_text': None,
            'alert_url': None,
            'daily_desc': self.forecast['hourly']['summary'],
            'current_temp': int(round(
                                self.forecast['currently']['temperature'])),
            'data_temp': None,
            'data_cloud': None,
            'data_wind': None,
            'data_precip': None,
            'sunset': None,
            'sunrise': None
        }

        # Set alert data if present
        try:
            temp_data['alert_text'] = self.forecast['alerts'][0]['title']
            temp_data['alert_url'] = self.forecast['alerts'][0]['uri']
        except KeyError:
            print "No alert currently for: ", temp_data['place_name']

        # Set list data
        key_list = [
            ('data_temp', 'temperature'),
            ('data_cloud', 'cloudCover'),
            ('data_wind', 'windSpeed'),
            ('data_precip', 'precipProbability')
            ]
        for loc_key, data_key in key_list:
            temp_data[loc_key] = ','.join([str(item) for item in
                                          self._get_data_list(data_key)])

        # Range of hours in the chart, localized to forecast timezone
        loc_tz = pytz.timezone(self.forecast['timezone'])
        dt_range = self._get_data_list('time')
        dt_range = self._utc_to_loc(dt_range, loc_tz)

        # Sunset and sunrise, localized to forecast timezone
        sunrise_dt = self._get_data_list('sunriseTime', time_frame='daily')
        sunrise_dt = self._utc_to_loc(sunrise_dt, loc_tz)
        sunset_dt = self._get_data_list('sunsetTime', time_frame='daily')
        sunset_dt = self._utc_to_loc(sunset_dt, loc_tz)

        # Trim past sunsets/rises
        first_hour = dt_range[0]
        if sunrise_dt[0] < first_hour:
            del sunrise_dt[0]
        if sunset_dt[0] < first_hour:
            del sunset_dt[0]

        # Find out if first hour is day or night
        if sunrise_dt[0] < sunset_dt[0]:
            night_hour = 1
        else:
            night_hour = 0

        # Create hourly binary night list (day = 0 night =1)
        night = []
        for hour in dt_range:
            if hour == sunrise_dt[0]:
                night_hour = 0
                del sunrise_dt[0]
            elif hour == sunset_dt[0]:
                night_hour = 1
                del sunset_dt[0]
            night.append(night_hour)
        temp_data['night'] = ','.join([str(item) for item in night])

        # Render html
        env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates/'))
        template = env.get_template('index-template.html')
        return template.render(temp_data)


if __name__ == '__main__':
    # Temporary test of the search functionality
    # tests = [
    #     u"98502",
    #     u"12345",
    #     u"00000",
    #     u"01010",
    #     u"zipcode",
    #     u"abcde",
    #     u"apple",
    #     u"099999",
    #     u"123j22",
    #     "this is a string",
    #     u"Not a City Name?",
    #     u"Los Angeles",
    #     u"los angeles, ca",
    #     u"Springfield",
    #     u"Springfield, OR",
    #     u"Tokyo",
    #     u"PoRtLand",
    #     u"PDX",
    #     u"Paris",
    #     u"Paris, France",
    #     u"Paris, TX",
    #     u"Olympia",
    #     u"London",
    #     u"London, United Kingdom",
    #     u"djibuti",
    #     u"Ho Chi Minh City",
    #     u"Thành phố Hồ Chí Minh",
    #     "上海市",
    #     "Dinas a Sir Caerdydd",
    #     "São Tomé",
    #     "boring",
    #     "Batman",
    #     "1770",
    #     "El Pueblo de Nuestra Señora la Reina de los Ángeles de Porciúncula",
    #     u"岡崎市",
    #     "秋田",
    #     "Akita"
    # # ]

    # for test in tests:
    #     print "=" * 100
    #     print "Searching for: ", test
    #     new_location = Location()
    #     if new_location.search(test):
    #         print new_location.lat_lng
    #         print new_location.name
    #     else:
    #         print new_location.name
    #     print "=" * 100

    # Temp test for search to forecast
    # tests = [
    #     "pdx"
    # ]

    # for test in tests:
    #     temp_loc = Location()
    #     print "=" * 100
    #     print "Forecast for: " + test
    #     if temp_loc.search(test):
    #         Weather(temp_loc).get_forecast()
    #     else:
    #         print "%s not found." % test
    #         print "Possible matches: "
    #         print temp_loc.name
    #     print '=' * 100

    # Temp test from search to forecast to svg
    search_term = "pdx"
    temp_loc = Location()
    temp_loc.search(search_term)
    temp_weather = Weather(temp_loc)
    temp_weather.get_forecast()
    temp_webpage = Webpage(temp_weather)
    html = temp_webpage.render_page()

    # Write html to file
    with codecs.open('../web/index.html', 'w', 'utf_8') as fpt:
        fpt.write(html)

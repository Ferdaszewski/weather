#-*- coding: utf-8 -*-

"""A weather dashboard web app."""
import codecs
import jinja2
import re

import locsearch
import svg
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

    def get_forcast(self, time=None):
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

    def _get_data_list(self, data_key):
        """Returns a string joined with ',' of elements of the data_key
        from forecast.
        """
        try:
            data_block = self.forecast['hourly']['data']
        except IndexError:
            print "Error. No weather data for hourly time frame."
        try:
            data_list = [chunk[data_key] for chunk in data_block]
        except IndexError:
            print "Error. JSON data bock %s does not have %s key."
        return ','.join([str(item) for item in data_list])

    def render_page(self):
        """Renders the webpage using the forecast data and writes the
        html file to disk.
        """
        # Collect data for template
        temp_data = {
            'place_name': self.name,
            'alert_text': None,
            'alert_url': None,
            'daily_desc': self.forecast['hourly']['summary'],
            'current_temp': int(round(self.forecast['currently']['temperature'])),
            'data_temp': None,
            'data_cloud': None,
            'data_wind': None,
            'data_precip': None
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
            temp_data[loc_key] = self._get_data_list(data_key)

        # Render html
        env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates/'))
        template = env.get_template('index-template.html')
        html = template.render(temp_data)
        with codecs.open('../web/index.html', 'w', 'utf_8') as fpt:
            fpt.write(html)


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
    #         Weather(temp_loc).get_forcast()
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
    temp_weather.get_forcast()
    temp_webpage = Webpage(temp_weather)
    temp_webpage.render_page()

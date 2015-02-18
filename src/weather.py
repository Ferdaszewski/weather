#-*- coding: utf-8 -*-

"""A weather dashboard web app."""
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

    def get_forcast(self, time=None):
        """Get the forecast for location, with the option to define a
        past or future datetime.datetime. Default None is now.
        """
        temp_forecast = weatherdata.Forecast(*self.location.lat_lng)
        self.forecast = temp_forecast.data
        print self.location.name
        print temp_forecast.headers
        print self.forecast


class Chart(object):
    """A SVG chart."""
    pass


class webpage():
    """Webpage."""
    pass

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

    # Temp test for search to forecast to svg
    tests = [
    "batman"
    ]

    for test in tests:
        temp_loc = Location()
        print "=" * 100
        print "Forecast for: " + test
        if temp_loc.search(test):
            Weather(temp_loc).get_forcast()
        else:
            print "%s not found." % test
            print "Possible matches: "
            print temp_loc.name
        print '=' * 100

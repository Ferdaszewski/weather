"""A weather dashboard web app."""
import re

import locsearch


class Location(object):
    """Location of the weather forecast."""
    def __init__(self):
        self.lat = None
        self.lng = None

    def search(self, search_term):
        """Search for the latitude and longitude of the search_term.
        Returns location (latitude, longitude), otherwise None.
        """

        # Term needs to be in Unicode
        if not isinstance(search_term, unicode):
            try:
                search_term = unicode(search_term, 'utf-8')
            except TypeError:
                print "Cannot convert %r to unicode." % search_term
                return None, None

        # Validate search_term, no empty strings or None
        try:
            search_list = search_term.split(',')
            search_list = [i.strip() for i in search_list if i.strip()]
            if len(search_list) == 0 or len(search_list) > 2:
                raise AttributeError
        except AttributeError:
            return None, None

        # Only one zip-code-like string (i.e. five digits)
        if len(search_list) == 1 and re.match(r'^\d{5}$', search_list[0]):
            return locsearch.zip_search(search_list[0])
        else:
            return locsearch.city_search(search_list)

class Weather(object):
    """Weather forecast for a location."""
    def __init__(self, location):
        """Args:
                location is a Location object.
        """
        self.location = location


class Chart(object):
    """A SVG chart."""
    pass


class webpage():
    """Webpage."""
    pass

if __name__ == '__main__':
    test_search_db = dbsearch()

    # Zip-code Tests
    tests = [
        u"98502",
        u"12345",
        u"00000",
        u"01010",
        u"zipcode",
        u"abcde",
        u"apple",
        u"099999",
        u"123j22",
        "this is a string",
        123,
        [],
        u"bla, ba, bla, ab",
        u"",
        u"  \t\n  ",
        u"  ,  \t,\n,  \t\n,   , ,,,,,,    ",
        u"Not a City Name?",
        u"Los Angeles",
        u"los angeles, ca",
        u"los angles, ca, united states",
        u"Springfield",
        u"Springfield, OR",
        u"Tokyo",
        u"PoRtLand",
        u"PDX",
        u"Paris",
        u"Paris, France",
        u"Paris, TX",
        u"Olympia",
        u"London",
        u"London, United Kingdom",
        u"djibuti",
        u"Ho Chi Minh City",
        u"Thành phố Hồ Chí Minh",
        "上海市",
        "Dinas a Sir Caerdydd",
        "São Tomé",
        "boring",
        "batman",
        "1770",
        "El Pueblo de Nuestra Señora la Reina de los Ángeles de Porciúncula",
        u"岡崎市",
        "秋田",
        "Akita"
    ]

    for test in tests:
        print "=" * 100
        print "Searching for: ", test
        result, city = test_search_db.search(test)
        print result
        print city
        print "=" * 100

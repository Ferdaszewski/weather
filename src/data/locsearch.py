"""Module to search for a location's longitude and latitude. Currently
Search is limited to:
1) US Postal Codes (5 digits only)
2) City[[, "2 char US state"] XOR [, "country name"]]
"""
import datetime
from peewee import *
import re

import locdb


class dbsearch(object):
    """Search algorithm."""
    def __init__(self):
        self.search_list = []

    def search(self, search_term):
        """Search for the latitude and longitude of the search_term.
        Returns location (latitude, longitude), otherwise None.
        """

        # Validate search_term, no empty strings or None
        try:
            self.search_list = search_term.split(',')
            self.search_list = [i.strip() for i in self.search_list
                                if i.strip()]
            if len(self.search_list) == 0 or len(self.search_list) > 2:
                raise AttributeError
        except AttributeError:
            return None

        # Only one zip-code-like string (i.e. five digits)
        locdb.db.connect()
        if len(self.search_list) == 1 and re.match(r'^\d{5}$',
                                                   self.search_list[0]):
            return zip_search(self.search_list[0])
        else:
            return city_search(self.search_list)
        db.close()


def zip_search(term):
    """Search the UsZip database for the postal code. Return
    the latitude and longitude if found, None otherwise.
    """
    try:
        result = locdb.UsZip.get(postal_code=term)
    except locdb.UsZip.DoesNotExist as e:
        print e
        return None
    return result.latitude, result.longitude


def city_search(term_list):
    """Search the City database and return the latitude and longitude
    if only one city found, otherwise None.
    """
    # TODO: make search more dynamic. Currently limited to:
    # City[, "2 char US state"] OR [, "country name"]

    # Query database for city name
    city_query = locdb.City.select().where(
        fn.lower(locdb.City.name) == term_list[0].lower()).dicts()

    num_cities = city_query.count()
    if num_cities == 0:
        # Broad search of alternate names for cities
        city_query = locdb.City.select().where(
            fn.lower(locdb.City.alternatenames).contains(
                term_list[0].lower())).dicts()
        num_cities = city_query.count()
        if num_cities == 0:
            print "No matches after alternate city name search."
            return None

    # One city found, no additional search needed
    if num_cities == 1:
        return city_query[0]['latitude'], city_query[0]['longitude']

    if len(term_list) != 2:
        print "To many matches and no state or country for:", term_list
        print "Possible cities:\n"
        for city in city_query:
            print city
        return None

    city_query_list = []

    # US city search
    if len(term_list[1]) == 2:
        for city in city_query:

            # Add city to new query list if states match
            if city['admin1'].lower() == term_list[1].lower():
                city_query_list.append(city)

    # International city search
    elif len(term_list[1]) > 2:
        for city in city_query:

            # Add city to new query list if country name matches
            if city['country_name'].lower() == term_list[1].lower():
                city_query_list.append(city)

    # Check new city_query_list
    if len(city_query_list) == 1:
        return city_query_list[0]['latitude'], city_query[0]['longitude']
    elif len(city_query_list) == 0:
        print "No match found after country/state search for: ", term_list
    else:
        print "To many possible matches after country/state search."
        print "Possible cities:\n"
        for city in city_query_list:
            print city
    return None


if __name__ == '__main__':
    test_search_db = dbsearch()

    # Zip-code Tests
    # tests = [
    #     "98502",
    #     "12345",
    #     "00000",
    #     "01010",
    #     "zipcode",
    #     "abcde",
    #     "a",
    #     "0",
    #     "1",
    #     "099999",
    #     "123j22"
    # ]

    # City name tests
    tests = [
        "bla, ba, bla, ab",
        "",
        "  \t\n  ",
        "  ,  \t,\n,  \t\n,   , ,,,,,,    ",
        "Not a City Name?",
        "Los Angeles",
        "los angeles, ca",
        "los angles, ca, united states",
        "Springfield",
        "Springfield, OR",
        "Tokyo",
        "PoRtLand",
        "PDX",
        "Paris",
        "Paris, France",
        "Paris, TX",
        "Olympia",
        "London",
        "London, United Kingdom",
        "djibuti"
    ]
    for test in tests:
        print "=" * len(test)
        print "Searching for: ", test
        print test_search_db.search(test)
        print "=" * len(test)

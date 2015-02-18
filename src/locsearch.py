"""Module to search for a location's longitude and latitude. Currently
Search is limited to:
1) US Postal Codes (5 digits only)
1) City
2) City[[, "2 char US state"] OR [, "country name"]]
"""
from peewee import *

import locdb


def zip_search(term):
    """Search the UsZip database for the postal code. Return
    the latitude and longitude if found, None otherwise.
    """
    locdb.db.connect()
    try:
        result = locdb.UsZip.get(postal_code=term)
    except locdb.UsZip.DoesNotExist:
        print "Postal Code %s not found." % term
        return None, None
    else:
        return ((result.latitude, result.longitude),
                ', '.join((result.place_name,
                          result.admin1_name,
                          'United States')
                          )
                )
    finally:
        locdb.db.close()


def city_search(term_list):
    """Search the City database for the city.

    Args:
        term_list: List of utf-8 encoded unicode strings.

    Returns a tuple:
        When City is found, returns the tuple:
            (latitude, longitude), "City Name, [state] OR [country]"

        No matches found, returns the tuple:
            None, None

        When multiple matches are found, returns the tuple:
            None, ["City Name, [state] OR [country]", ...]
    """
    # TODO: make search more dynamic/forgiving.

    locdb.db.connect()
    try:
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
                return None, None
    finally:
        locdb.db.close()

    # One city found, no additional search needed
    if num_cities == 1:
        return ((city_query[0]['latitude'], city_query[0]['longitude']),
                ', '.join((city_query[0]['name'],
                          city_query[0]['admin1'],
                          city_query[0]['country_name'])
                          )
                )

    if len(term_list) != 2:
        return_cities = [', '.join((city['name'],
                                   city['admin1'],
                                   city['country_name'])
                                   )
                         for num, city in enumerate(city_query) if num < 10
                         ]
        return None, return_cities

    city_q_list = []

    # US city search
    if len(term_list[1]) == 2:
        # Add city to new query list if states match
        for city in city_query:
            if city['admin1'].lower() == term_list[1].lower():
                city_q_list.append(city)

    # International city search
    elif len(term_list[1]) > 2:
        # Add city to new query list if country name matches
        for city in city_query:
            if city['country_name'].lower() == term_list[1].lower():
                city_q_list.append(city)

    # Check new city_q_list
    if len(city_q_list) == 1:
        return ((city_q_list[0]['latitude'], city_q_list[0]['longitude']),
                ', '.join((city_q_list[0]['name'],
                          city_q_list[0]['admin1'],
                          city_q_list[0]['country_name'])
                          )
                )
    elif len(city_q_list) == 0:
        return None, None
    else:
        return_cities = [', '.join((city['name'],
                                   city['admin1'],
                                   city['country_name'])
                                   )
                         for num, city in enumerate(city_q_list) if num < 10
                         ]
        return None, return_cities

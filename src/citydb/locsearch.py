"""Module to search for a locations longitude and latitude."""
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
        Returns location (latitude, longitude), otherwise returns a
        list of possible matches or None.
        """

        # Validate search_term, no empty strings or None
        try:
            self.search_list = search_term.split(',')
            self.search_list = [i.strip() for i in self.search_list
                                if i.strip()]
            if not self.search_list:
                raise AttributeError
        except AttributeError:
            return None

        # Only one zip-code-like string (i.e. five digits)
        if len(self.search_list) == 1 and re.match(r'^\d{5}$', self.search_list[0]):
            return zip_search(self.search_list[0])
        else:
            # search city db
            pass


def zip_search(term):
    """Search the UsZip database for the postal code. Returns
    the latitude and longitude if found, None otherwise."""
    with locdb.db.connect():
        try:
            result = locdb.UsZip.get(postal_code=term)
        except locdb.UsZip.DoesNotExist as e:
            print e
            return None
        return result.latitude, result.longitude


if __name__ == '__main__':
    temp = dbsearch()

    tests = [
        "98502",
        "12345",
        "00000",
        "01010",
        "zipcode",
        "abcde",
        "a",
        "0",
        "1",
        "099999",
        "123j22"
    ]
    for test in tests:
        print temp.search(test)
        
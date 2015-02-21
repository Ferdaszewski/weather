"""Module to manage a local SQLite database with latitude and longitude
of bot international cities and US postal codes.
"""
import codecs
import csv
import datetime
from peewee import *
import sys

# Constants
DATE_FORMAT = '%Y-%m-%d'
CITY_DATA_FILE = 'data-sources/geonames/cities5000.txt'
COUNTRY_DATA_FILE = 'data-sources/geonames/countryInfo.txt'
ZIP_DATA_FILE = 'data-sources/uszip/US.txt'
USZIP_KEYS = (
    'country_code',
    'postal_code',
    'place_name',
    'admin1_name',
    'admin1_code',
    'admin2_name',
    'admin2_code',
    'admin3_name',
    'admin3_code',
    'latitude',
    'longitude',
    'accuracy'
    )
GEONAME_KEYS = (
    'geonameid',
    'name',
    'asciiname',
    'alternatenames',
    'latitude',
    'longitude',
    'feature_class',
    'feature_code',
    'country_code',
    'cc2',
    'admin1',
    'admin2',
    'admin3',
    'admin4',
    'population',
    'elevation',
    'dem',
    'timezone',
    'modification_date'
    )

# Use SqliteDatabase
db = SqliteDatabase('location_data.db')


class UsZip(Model):
    """Database model to hold us zipcode information."""
    country_code = CharField(max_length=2)

    # While US codes are integers, other country postal codes are not.
    # Note: US postal codes are not guaranteed to be unique.
    postal_code = CharField(max_length=5, index=True)
    place_name = CharField(max_length=180)
    admin1_name = CharField(max_length=100, null=True)
    admin1_code = CharField(max_length=20, null=True)
    admin2_name = CharField(max_length=100, null=True)
    admin2_code = CharField(max_length=20, null=True)
    admin3_name = CharField(max_length=100, null=True)
    admin3_code = CharField(max_length=20, null=True)
    latitude = FloatField()
    longitude = FloatField()
    accuracy = CharField(null=True)

    class Meta:
        database = db

class City(Model):
    """Database model to hold city geo information."""
    geonameid = IntegerField(primary_key=True, unique=True)
    name = CharField(max_length=200)
    asciiname = CharField(max_length=200, null=True)
    alternatenames = TextField(null=True)
    latitude = FloatField()
    longitude = FloatField()
    feature_class = CharField(max_length=1)
    feature_code = CharField(max_length=10)
    country_code = CharField(max_length=2)

    # Not in source data, added from countryInfo.txt
    country_code3 = CharField(max_length=3, null=True)
    country_name = CharField(max_length=200, null=True)

    cc2 = CharField(max_length=60, null=True)
    admin1 = CharField(max_length=20, null=True)
    admin2 = CharField(max_length=80, null=True)
    admin3 = CharField(max_length=20, null=True)
    admin4 = CharField(max_length=20, null=True)
    population = IntegerField()
    elevation = IntegerField(null=True)
    dem = IntegerField(null=True)
    timezone = CharField(max_length=40)
    modification_date = DateField()

    class Meta:
        database = db


def unicode_csv_reader(unicode_csv_data, **kwargs):
    """csv.py doesn't do Unicode; encode temporarily as UTF-8.
    Source: Python documentation.
    """
    csv_reader = csv.reader(utf_8_encoder(unicode_csv_data), **kwargs)
    for row in csv_reader:
        # decode UTF-8 back to Unicode, cell by cell:
        yield [unicode(cell, 'utf-8') for cell in row]


def utf_8_encoder(unicode_csv_data):
    """Decode UTF-8 back to Unicode.
    Source: Python documentation.
    """
    for line in unicode_csv_data:
        yield line.encode('utf-8')


def load_file(file_name, data_keys):
    """Load tab-delimited text file into a list of dicts."""

    # Avoid field limit (131072) _csv error by expanding size limit
    csv.field_size_limit(sys.maxsize)

    with codecs.open(file_name, 'r', 'utf_8') as data_file:
        # Double quote char in alternative names field not escape char
        reader = unicode_csv_reader(data_file, delimiter="\t",
                                    quoting=csv.QUOTE_NONE)
        cities = []
        num_cities = 0
        for row in reader:

            # Fixes PeeWee error with '' for ints.
            row = [i if i != '' else None for i in row]

            # Dict for each row, list
            cities.append(dict(zip(data_keys, row)))
            num_cities += 1
    print "%d rows loaded from %s" % (num_cities, file_name)
    return cities


def load_db(data, table):
    """Load data into the database table. data is list of rows (dict).
    Each dict is a new row in the db.
    """
    # Insert rows 500 at a time
    # 1000 per time suggestion from peewee documentation fails:
    # "too many terms in compound SELECT"
    with db.transaction():
        for idx in range(0, len(data), 500):
            table.insert_many(data[idx:idx+500]).execute()
    print "%d cities loaded into database." % table.select().count()


def create_tables():
    """Small helper function to delete existing tables and create new
    tables in the database.
    """
    db.connect()
    City.drop_table(fail_silently=True)
    UsZip.drop_table(fail_silently=True)
    db.create_tables([City, UsZip], safe=True)
    db.close()


def add_city_data(city_list):
    """Changes modification_date to datetime.date and adds country name
    and ISO3 country code.
    """
    # Change string to datetime.date
    for city in city_list:
        city['modification_date'] = datetime.datetime.strptime(
            city['modification_date'], DATE_FORMAT).date()

    # Load country name info into a dict of dicts
    co_name_data = {}
    with codecs.open(COUNTRY_DATA_FILE, 'r', 'utf-8') as data_file:
        for line in data_file:
            line_list = line.split('\t')
            if line_list[0][0] != '#':
                co_name_data[line_list[0]] = {
                    "country_code3": line_list[1],
                    "country_name": line_list[4]
                }

    # Load country name data into each country/row
    for city in city_list:
        city.update(co_name_data[city['country_code']])

    return city_list


if __name__ == '__main__':
    db.connect()
    create_tables()

    # Load city geo info
    city_list = load_file(CITY_DATA_FILE, GEONAME_KEYS)
    load_db(add_city_data(city_list), City)

    # Load postal code info
    load_db(load_file(ZIP_DATA_FILE, USZIP_KEYS), UsZip)

    db.close()

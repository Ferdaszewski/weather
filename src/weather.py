"""A weather dashboard web app."""

class Location(object):
    """Location of the weather forecast."""
    pass


class Weather(object):
    """Weather forecast for the location."""
    def __init__(self, location):
        """Args:
                location is a Location object.
        """
        self.location = location


def render_svg(weather_data):
    """Renders the svg elements for the webpage."""
    pass


def render_webpage():
    """Renders the webpage."""
    pass

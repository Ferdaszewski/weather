#!/usr/bin/env python

"""Routes for a weather dashboard web application."""
import bottle
import socket

from weather import Weather, Location, Webpage


@bottle.route('/', method=['GET', 'POST'])
def do_weather():
    """Search for location and get current weather. Post used so search
    term can be Unicode.
    """
    post_search = bottle.request.forms.get('search_term')
    if post_search:
        search_term = post_search
    else:
        search_term = "Portland, OR"

    # Find the location
    location = Location()
    try:
        location.search(search_term)
    except TypeError:
        print "Search term error."

    # Get weather info for location
    weather = Weather(location)
    weather.get_forecast()

    return Webpage(weather).render_page()


@bottle.route('/assets/<filepath:path>')
def server_static(filepath):
    """Static website assets."""
    return bottle.static_file(filepath, root='../web/assets')

if __name__ == '__main__':
    # Local development server.
    bottle.run(host='0.0.0.0', port=8080, debug=True, reloader=True)

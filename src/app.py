"""Routes for a weather dashboard web application."""
import bottle

from weather import Weather, Location, Webpage


@bottle.route('/')
@bottle.post('/')
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
    location.search(search_term)

    # Get weather info for location
    weather = Weather(location)
    weather.get_forecast()

    return Webpage(weather).render_page()


@bottle.route('/assets/<filepath:path>')
def server_static(filepath):
    """Static website assets."""
    return bottle.static_file(filepath, root='../web/assets')

# Development server
bottle.run(host='localhost', port=8080, debug=True, reloader=True)

"""Routes for a weather dashboard web application."""
import bottle

from weather import Weather, Location, Webpage


@bottle.route('/')
@bottle.post('/')
@bottle.route('/<url_search>')
def do_weather(url_search="Portland, OR"):
    post_search = bottle.request.forms.get('search_term')
    if post_search:
        search_term = post_search
    else:
        search_term = url_search

    # Find the location
    location = Location()
    location.search(search_term)

    # Get weather info for location
    weather = Weather(location)
    weather.get_forecast()

    return Webpage(weather).render_page()


@bottle.route('/assets/<filepath:path>')
def server_static(filepath):
    return bottle.static_file(filepath, root='../web/assets')

bottle.run(host='localhost', port=8080, debug=True, reloader=True)

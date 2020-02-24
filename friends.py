import urllib.request
import urllib.parse
import urllib.error
import twurl
import json
import ssl
import folium
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

geolocator = Nominatim(user_agent="specify_your_app_name_here", timeout=100)
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=0.1, max_retries=1)


def getting_json(username):
    TWITTER_URL = 'https://api.twitter.com/1.1/friends/list.json'

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    while True:
        url = twurl.augment(TWITTER_URL,
                            {'screen_name': username, 'count': '25'})
        print('Retrieving', url)
        connection = urllib.request.urlopen(url, context=ctx)
        data = connection.read().decode()

        js = json.loads(data)
        return js


def getting_locations(json_dict):
    locations_dict = {}
    for user in json_dict['users']:
        if user['location'] != '':
            locations_dict[user['location']] = user['screen_name']
    return locations_dict


def re_locations(locations_dict):
    points = []
    for loc in locations_dict:
        location = geolocator.geocode(loc)
        if location is not None:
            points.append(
                (loc, locations_dict[loc],
                 location.latitude, location.longitude))
    return points


def marking_locations(location_list: list):
    fg_friends = folium.FeatureGroup(name="Friends")

    for loc in location_list:
        fg_friends.add_child(folium.Marker(
            location=[loc[2], loc[3]], popup=loc[1]+', in '+loc[0], icon = folium.Icon(color='green', icon='heart')))
    return fg_friends


def main(username):
    mapp = folium.Map(location=[1, 1], zoom_start=1.5)
    js = getting_json(username)
    location_dict = getting_locations(js)
    points_list = re_locations(location_dict)
    marking = marking_locations(points_list)
    mapp.add_child(marking)
    mapp.add_child(folium.LayerControl())
    mapp.save('mysite/templates/map.html')
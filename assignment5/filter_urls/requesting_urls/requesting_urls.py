import requests as req
from os import path

"""
Sends a get reguest with an url and optional parameters and optionally saves the html to a .txt

Args: A valid URL-string, optional parameters and an optional filename

Returns: The text-element of the get-request
"""
def get_html(url, params=None, output=None):
    r = req.get(url, params=params)
    if output != None:
        f = open(output, "w")
        f.write(r.url)
        f.write(r.text)
        f.close()
    return r.text

"""
studio_ghibli = get_html("https://en.wikipedia.org/wiki/Studio_Ghibli", output="studio_ghibli.txt")
star_wars = get_html("https://en.wikipedia.org/wiki/Star_Wars", output="star_wars")
dungeons_and_dragons = get_html("https://en.wikipedia.org/wiki/Dungeons_%26_Dragons", output="dungeons_and_dragons.txt")
main_info = get_html("https://en.wikipedia.org/w/index.php", {"title":"Main_Page", "action":"info"}, "main_info.txt")
hurricane_gonzalo = get_html("https://en.wikipedia.org/w/index.php", {"title":"Hurricane Gonzalo", "oldid":"983056166"}, "hurricane_gonzalo.txt")
"""

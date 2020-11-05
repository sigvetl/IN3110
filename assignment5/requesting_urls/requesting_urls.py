import requests as req
from os import path


def get_html(url, params=None, output=None):
    """
    Sends a get reguest with an url and optional parameters and optionally saves the html to a .txt

    Args:
        url (string): A valid URL-string
        params (dict): optional parameters to get request
        filename (string): optional name of file
    Returns:
        text: The text-element of the get-request
    """
    r = req.get(url, params=params)

    assert r.status_code == 200

    if output != None:
        f = open(output, "w")
        f.write(r.url)
        f.write(r.text)
        f.close()
    return r.text

"""
studio_ghibli = get_html("https://en.wikipedia.org/wiki/Studio_Ghibli", output="studio_ghibli.txt")
star_wars = get_html("https://en.wikipedia.org/wiki/Star_Wars", output="star_wars.txt")
dungeons_and_dragons = get_html("https://en.wikipedia.org/wiki/Dungeons_%26_Dragons", output="dungeons_and_dragons.txt")
main_info = get_html("https://en.wikipedia.org/w/index.php", {"title":"Main_Page", "action":"info"}, "main_info.txt")
hurricane_gonzalo = get_html("https://en.wikipedia.org/w/index.php", {"title":"Hurricane Gonzalo", "oldid":"983056166"}, "hurricane_gonzalo.txt")
"""

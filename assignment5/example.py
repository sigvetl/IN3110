#import the module
import requests as req
from os import path
#grabbing the content of https://en.wikipedia.org/wiki/URL
resp = req.get("https://github.uio.no/IN3110/IN3110-sigvetl/blob/master/README.md")
#get () method returns a response object
print(resp.text)
print(resp.status_code)
print(resp.encoding)

#<!DOCTYPE html>
#<html class=”client=nojs” lang=”en” dir=”ltr”> <head>
#<meta charset=”UTF=8”/>
#<title >URL = Wikipedia</title >
#shortened for the purpose of viewing


def get_html(url, params=None, output=None):
    r = req.get(url, params=params)
    if output != None:
        f = open(output, "w")
        f.write(r.url)
        f.write(r.text)
        f.close()
    return r

get_html("https://en.wikipedia.org/wiki/Studio_Ghibli")
get_html("https://en.wikipedia.org/wiki/Star_Wars")
get_html("https://en.wikipedia.org/wiki/Dungeons_%26_Dragons")
a = get_html("https://en.wikipedia.org/w/index.php", {"title":"Main_Page", "action":"info"})
print(a.url)
get_html("https://en.wikipedia.org/w/index.php", {"title":"Hurricane Gonzalo", "oldid":"983056166"}, "Gonzalo.txt")

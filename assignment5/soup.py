from bs4 import BeautifulSoup
import requests as req
url = "https://en.wikipedia.org/wiki/List of soups"
# request url as we have already learned = yeah!
request = req.get(url)
soup = BeautifulSoup(request.text, "html.parser")
#check the t i t l e of the wikipedia page
print(soup.title)
# get the soup table
soup_table = soup.find('table', {"class":'wikitable_sortable'})

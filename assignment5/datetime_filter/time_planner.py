from bs4 import BeautifulSoup
import re
from dateutil import parser
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
from requesting_urls.requesting_urls import get_html


def get_captions(captions):
    """
    Matches the event-keys with the event-values

    Args:
        captions (resultset): A resultset containing the poption-tag
    Returns:
        dictionary: discipline event keys and values
    """
    count = 0
    dict = {}
    for e in captions[0]:
        if count % 2 == 0:
            key = re.findall("([A-Z]{2})", e)
        elif count % 2 == 1:
            value = re.findall(">(.*)<", str(e))
            dict[key[0]] = value[0]
        count +=1
    return dict


def extract_events(url):
    """
    Fetches the table, indexes the list of events and writes all events to a file using markdown

    Args:
        url (string): url to extract the ski-events from
    """
    html = get_html(url)
    document = BeautifulSoup(html, "lxml")
    table = document.find("table", {"class" : 'wikitable plainrowheaders'})
    captions = table.find_all("caption")
    disciplines = get_captions(captions)
    #e = discipline.find_all("a")
    rows = table.find_all("tr")

    f = open("betting_slip_empty.md", "w")
    f.write("\n" + "BETTING SLIP" + "\n\n")
    f.write("Name:" + "\n\n")
    f.write("DATE | VENUE | DISCIPLINE | Who wins?\n")
    f.write("--- | --- | --- | ---\n")

    slip = []
    for row in rows[1:]:
        cells = row.find_all(["td", "th"])
        cells_text = [cell.get_text(strip=True) for cell in cells]
        #filter non-events
        if len(cells_text) > 5:
            date = cells_text[2]
            #if venue is empty keep previous
            if len(cells_text) == 9:
                venue = cells_text[3]
                discipline = cells_text[4]
            else:
                discipline = cells_text[3]
            slip.append([date, venue, discipline])

    for row in slip:
        date_regex = "(\d[^]].*\d)"
        row[0] = re.findall(date_regex, row[0])[0]
        row[0] = parser.parse(row[0])
        discipline_regex = "([A-Z]{2})"
        row[2] = re.findall(discipline_regex, row[2])[0]
        #sub with dict
        for key in disciplines:
            if key == row[2]:
                row[2] = disciplines[key]
        f.write(row[0].strftime("%d/%m/%Y") + " | " + row[1] + " | " + row[2] + " | \n")
    f.close()


#table = format_table(url)
url2020 = "https://en.wikipedia.org/wiki/2020%E2%80%9321_FIS_Alpine_Ski_World_Cup"
url2019 = "https://en.wikipedia.org/wiki/2019%E2%80%9320_FIS_Alpine_Ski_World_Cup"
extract_events(url2020)
extract_events(url2019)

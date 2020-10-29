from bs4 import BeautifulSoup
import re
from requesting_urls.requesting_urls import get_html
from dateutil import parser

def format_table(url):
    # request url as we have already learned = yeah!
    html = get_html(url)
    document = BeautifulSoup(html.text, "html.parser")
    #check the t i t l e of the wikipedia page
    #print(document.title)
    # get the soup table
    table = document.find("table", {"class" : 'wikitable plainrowheaders'})
    #print(table.find("th").get_text())

    rows = table.find_all("tr")
    return rows

def extract_events(table):
    #date in date-format
    #venue
    #discipline
    #who wins?
    f = open("betting_slip_empty.md", "w")
    f.write("DATE | VENUE | DISCIPLINE | Who wins?\n")
    f.write("--- | --- | --- | ---\n")
    slip = []
    for row in table[1:]:
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
        discipline_regex = "([A-Z][A-Z])"
        row[2] = re.findall(discipline_regex, row[2])[0]
        f.write(row[0].strftime("%d/%m/%Y") + " | " + row[1] + " | " + row[2] + " | \n")
    f.close()


#table = format_table(url)
url2020 = "https://en.wikipedia.org/wiki/2020%E2%80%9321_FIS_Alpine_Ski_World_Cup"
url2019 = "https://en.wikipedia.org/wiki/2019%E2%80%9320_FIS_Alpine_Ski_World_Cup"
extract_events(format_table(url2020))
extract_events(format_table(url2019))

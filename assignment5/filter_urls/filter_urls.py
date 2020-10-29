import re
from requesting_urls.requesting_urls import get_html


"""
Splitting a HTML documents into a list of URLs that are contained in the document

Args: A HTML string

Returns: A list of all found URLs found in the HTML-string
"""
def find_urls(html_doc, baseurl):
    #find all starting with <a followed by any number of characters and eventually href="
    #capture a group that does not contain " or # before ending capture when coming to a " or #
    regex = "<a .*?href=\"([^\"#]+)[\"|#]"
    matches = re.findall(regex, html_doc)
    print(len(matches))
    list = []
    #adding prefix to relative URLs
    for e in matches:
        if e[0] == '/' and e[1] == '/':
            #hardcoded https
            e = "https:" + e
            list.append(e)
        elif e[0] == '/' and e[1] != '/':
            e = baseurl + e
            list.append(e)
        else:
            list.append(e)
    return list

#does not filter links not starting with but containing cowikipedia.org
def find_articles(html_string, baseurl, name):
    urls = find_urls(html_string, baseurl)
    regex = "(https://.*\.wikipedia.org[^:]*$)"
    matches = []
    for links in urls:
        if re.findall(regex, links):
            matches.append(links)
    #matches = [re.findall(regex, links) for links in list_of_links]
    #matches = [match != [] for match in matches]
    write_to_file(matches, name)
    return matches

def write_to_file(list_of_links, name):
    f = open(name, "w")
    for link in list_of_links:
        f.write(link + "\n")
    f.close()

nobel_prize = get_html("https://en.wikipedia.org/wiki/Nobel_Prize")
bundesliga = get_html("https://en.wikipedia.org/wiki/Bundesliga")
fis = get_html("https://en.wikipedia.org/wiki/2019%E2%80%9320_FIS_Alpine_Ski_ World_Cup")
nobel_articles = find_articles(nobel_prize, "https://en.wikipedia.org", 'nobel_prize.txt')
bundes_articles = find_articles(bundesliga, "https://en.wikipedia.org", 'bundesliga.txt')
fis_articles = find_articles(fis, "https://en.wikipedia.org", 'fis.txt')
#for e in a:
#    print(e)

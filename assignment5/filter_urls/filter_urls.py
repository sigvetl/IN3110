import re
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
from requesting_urls.requesting_urls import get_html

def find_urls(html_doc, baseurl):
    """
    Splitting a HTML documents into a list of URLs that are contained in the document

    Args:
        html_doc (string): A HTML string
        baseurl (string): the base of the URL
    Returns:
        array: A list of all found URLs found in the HTML-string
    """
    #find all starting with <a followed by any number of characters and eventually href="
    #capture a group that does not contain " or # before ending capture when coming to a " or #
    regex = "<a .*?href=\"([^\"#]+)[\"|#]"
    matches = re.findall(regex, html_doc)
    protocol = re.findall("(https:|http:)", baseurl)[0]

    for e in range(len(matches)):
        r1 = (re.sub(r'(^\/[^\/].*)', baseurl + r'\g<1>', matches[e]))
        r2 = (re.sub(r'(^\/\/.*)', protocol + r'\g<1>', matches[e]))
        #can probably be intertwined using '((^\/[^\/].*)|(^\/\/.*))'

        if (r1 != matches[e]):
            matches[e] = r1
        elif(r2 != matches[e]):
            matches[e] = r2

    return matches


def find_articles(html_string, baseurl, name):
    """
    Searches through a list of URLs and filters out the ones not matched by the regex.
    Does not filter links not starting with but containing wikipedia.org

    Args:
        html_string (string): A HTML string
        baseurl (string) the base of the URL
        name (string): the name of the file to write links to
    Returns:
        array: The list of Wikipedia-articles
    """
    urls = find_urls(html_string, baseurl)
    regex = "(https://.*\.wikipedia.org[^:]*$)"
    matches = []
    for links in urls:
        if re.findall(regex, links):
            matches.append(links)
    write_to_file(matches, name)
    return matches


def write_to_file(list_of_links, name):
    """
    Writes the list of links to the specified filename
    Args:
        list_of_links (array): A list of links
        name (string): a filename
    """
    f = open(name, "w")
    for link in list_of_links:
        f.write(link + "\n")
    f.close()

"""
nobel_prize = get_html("https://en.wikipedia.org/wiki/Nobel_Prize")
bundesliga = get_html("https://en.wikipedia.org/wiki/Bundesliga")
fis = get_html("https://en.wikipedia.org/wiki/2019%E2%80%9320_FIS_Alpine_Ski_ World_Cup")
nobel_articles = find_articles(nobel_prize, "https://en.wikipedia.org", 'nobel_prize.txt')
bundes_articles = find_articles(bundesliga, "https://en.wikipedia.org", 'bundesliga.txt')
fis_articles = find_articles(fis, "https://en.wikipedia.org", 'fis.txt')
"""

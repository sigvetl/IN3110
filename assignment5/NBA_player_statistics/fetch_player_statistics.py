import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
from requesting_urls.requesting_urls import get_html
from bs4 import BeautifulSoup
import re
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import time

def extract_teams(URL):
    """
    Fetches data from bracket, ectracts team-name and url for teams that appeared in
    the conference semifinals

    Args:
        URL (string): url of 2020 NBA
    Returns:
        array: 2d list with pairs of team names and URL for wikipedia entry of team
    """
    html = get_html("https://en.wikipedia.org/wiki/2020_NBA_playoffs")
    baseurl = "https://en.wikipedia.org"
    document = BeautifulSoup(html, "lxml")
    header = document.find("span",{"class":"mw-headline","id":"Bracket"})
    table = header.find_next("table")
    rows = table.find_all("tr")

    bracket = []
    for row in rows[4:-3]:
        cells = row.find_all(["td"])
        links = row.find_all("a")
        if links != []:
            links = links[0].get("href")
        cells_text = [cell.get_text(strip=True) for cell in cells]
        cells_text.append(baseurl + str(links))
        bracket.append(cells_text)

    bracket2 = []
    for previous, current, next in zip(bracket, bracket[1:], bracket[2:]):
        if len(current) == 3 and current[1] == "":
            regex = "[a-zA-Z\s]+"
            team = re.findall(regex, previous[3])[0]
            link = previous[-1]
            bracket2.append([team, link])
            team = re.findall(regex, next[3])[0]
            link = next[-1]
            bracket2.append([team, link])

    return bracket2


def get_player_links(teams):
    """
    Searches through the table entry for each team containing the active players
    and appends all active players and their URLs to a list

    Args:
       teams (array): List of team-URL pairs
    Returns:
        array: 3d list containing team-name and player-URL pairs
    """
    baseurl = "https://en.wikipedia.org"

    player_urls = []
    for i in range(len(teams)):
        html = get_html(teams[i][1])
        document = BeautifulSoup(html, "lxml")
        table = document.find("table", {"class" : 'toccolours'})
        next_table = table.find_next("table")
        rows = table.find_all("tr")
        liste = []
        team = []
        team.append(teams[i][0])

        for row in rows:
            cells = row.find_all(["td"])
            celler = [cell for cell in cells]
            liste.append(celler)
        for row in liste[4:]:
            pair = []
            #link = row[2].get("href")
            links = row[2].find_all("a")
            name = links[0].get("title")
            lenke = links[0].get("href")
            pair.append(name)
            pair.append(baseurl + str(lenke))
            team.append(pair)
        player_urls.append(team)

    return player_urls

def get_player_stats(player_urls):
    """
    Extracts player points, rebound and blocks from each players 2019-20 regular
    season stats. Time consuming function. Tried using threads to speed it up, but i believe
    the bottlenecks are the get-request

    Args:
        player_urls (array): 3d list containing team-name and player-URL pairs
    Returns:
        array: 3d list containing team-name and [player-name, stats]
    """
    player_stats = []
    for i in range(len(player_urls)):
        teamlist = []
        teamlist.append(player_urls[i][0])
        for j in range(len(player_urls[i])-1):
            html = get_html(player_urls[i][j+1][1])
            document = BeautifulSoup(html, "lxml")
            table = document.find("table", class_="wikitable sortable")
            if table != None:
                rows = table.find_all("tr")
                for row in rows[-3:-1]:
                    cells = row.find_all(["td"])
                    celle = [cell.get_text(strip=True) for cell in cells]
                    if celle != []:
                        if celle[0][3] == '9':
                            #midlertidig
                            if celle[11] == '-':
                                celle[11] = '0'
                            if celle[12] == '-':
                                celle[12] = '0'
                            celle[12] = re.findall("([0-9.]+)", celle[12])[0]
                            teamlist.append([player_urls[i][j+1][0], float(celle[8]), float(celle[11]), float(celle[12])])
        player_stats.append(teamlist)
    return player_stats
        #RPG = 8, BPG = 11, PPG = 12


def filter_top_3(url):
    """
    Driver function. Calls submethods and sorts and extracts 3 best players
    Sends this list to function that creates plots

    Args:
        url (array.pyi): 3d list containing team-name and [player-name, stats]

    Return:
        array: Sorted 2d list containing player objects
                for top 3 players for each team
    """
    team_urls = extract_teams(url)
    player_urls = get_player_links(team_urls)
    player_stats = get_player_stats(player_urls)
    best_players = []
    for i in range(len(player_stats)):
        sorted_list = sorted(player_stats[i][1:], key=lambda x: x[3], reverse=True)
        player_list = [Player(player_stats[i][0], sorted_list[j][0], sorted_list[j][3], sorted_list[j][2], sorted_list[j][1]) for j in range(3)]
        best_players.append(player_list)

    bar_plot(best_players, 'ppg')
    bar_plot(best_players, 'bpg')
    bar_plot(best_players, 'rpg')
    return best_players

class Player():
    """
    Player class to store information of a NBA player in a clear way.

    Attributes:
        team_name (str): Name of team the player belongs to.
        player_name (str): Name of the player.
        ppg (float): Player's score in points per game category.
        bpg (float): Player's score in blocks per game category.
        rpg (float): Player's score in rebounds per game category.
    """

    def __init__(self, team, player_name, ppg, bpg, rpg):
        """
        Initiates class instance.
        Args:
            team (str): Name of team the player belongs to.
            player_name (str): Name of the player.
            ppg (float): Player's score in points per game category.
            bpg (float): Player's score in blocks per game category.
            rpg (float): Player's score in rebounds per game category.
        """
        self.team_name = team
        self.player_name = player_name
        self.ppg = ppg
        self.bpg = bpg
        self.rpg = rpg

def bar_plot(best_players, key):
    """
    Creates a list for the stat to be plotted for each team and plots the data grouped by team

    Args:
        best_players (array): 2d list of 3 best player-objects for each team,
        type (string): the abbrievation to be concatenated with the title
    """

    tick_vals = []  # need to store x values for bars for xticks to work
    tick_labels = []  # need to store bar labels for xticks to work

    for i, team in enumerate(best_players):
        x = np.linspace(i+1, i+2, 3) + i  # x values for plotting
        # scores: get scores from each Player class object's attribute:
        scores = [getattr(player, key) for player in team]
        # names: get names from each Player class object's attribute:
        names = [player.player_name for player in team]
        #print("Plotting " + names + " with " + scores + " at index " + x)
        plt.bar(x, scores, 0.3, label=team[0].team_name)
        tick_vals.extend(x.tolist())  # add x values to list
        tick_labels.extend(names)  # add player names to list

    plt.xticks(tick_vals, tick_labels, rotation='vertical')
    plt.subplots_adjust(bottom=0.2)  # tweak spacing to prevent clipping of tick-labels
    plt.ylabel(key)
    plt.title(f"{key} in RS(19-20) for top 3 players of conference semifinalists")
    plt.legend()
    plt.gcf().set_size_inches(12.8, 9.6)
    plt.savefig(f"players_over_{key}.png")
    plt.clf()

url = "https://en.wikipedia.org/wiki/2020_NBA_playoffs"
if __name__ == "__main__":
    best_players = filter_top_3(url)

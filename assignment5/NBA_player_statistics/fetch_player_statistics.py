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
        array: Sorted 3d list containing team-name and [player-name, stats]
                for top 3 players for each team
    """
    team_urls = extract_teams(url)
    player_urls = get_player_links(team_urls)
    player_stats = get_player_stats(player_urls)
    all = []
    for i in range(len(player_stats)):
        sorted_list = sorted(player_stats[i][1:], key=lambda x: x[3], reverse=True)
        all.append([player_stats[i][0], sorted_list[0], sorted_list[1], sorted_list[2]])

    bar_plot(all, 3, 'Points per game', 'PPG', 'players_over_ppg.png')
    bar_plot(all, 2, 'Blocks per game', 'BPG', 'players_over_bpg.png')
    bar_plot(all, 1, 'Rebounds per game', 'RPG', 'players_over_rpg.png')
    return all



def bar_plot(best_players, index, title, type, file):
    """
    Creates a list for the stat to be plotted for each team and plots the data grouped by team
    I struggled with the player-ticks and have set the teamlabels as ticks in

    Args:
        best_players (array): 3d list of 3 best players for each team,
        index (int): the index that fetches the right column
        title (string): title of the y-axis,
        type (string): the abbrievation to be concatenated with the title
        file (string): filename for storage of the file
    """
    teamlabels = []
    playerlabels = []
    team1 = []
    team2 = []
    team3 = []
    team4 = []
    team5 = []
    team6 = []
    team7 = []
    team8 = []
    for i in range(len(best_players)):
        teamlabels.append(best_players[i][0])
        for j in range(len(best_players[i])-1):
            playerlabels.append(best_players[i][j+1][0])

    for i in range(len(best_players[0])-1):
        team1.append(best_players[0][i+1][index])
        team2.append(best_players[1][i+1][index])
        team3.append(best_players[2][i+1][index])
        team4.append(best_players[3][i+1][index])
        team5.append(best_players[4][i+1][index])
        team6.append(best_players[5][i+1][index])
        team7.append(best_players[6][i+1][index])
        team8.append(best_players[7][i+1][index])

    x = np.arange(len(teamlabels))  # the label locations
    width = 0.25  # distance between bars
    widthbar = 0.2 #width of bars

    fig, ax = plt.subplots()
    rects1 = ax.bar([0-width, 0, 0+width], team1, widthbar, label=best_players[0][0])
    rects2 = ax.bar([1-width, 1, 1+width], team2, widthbar, label=best_players[1][0])
    rects3 = ax.bar([2-width, 2, 2+width], team3, widthbar, label=best_players[2][0])
    rects4 = ax.bar([3-width, 3, 3+width], team4, widthbar, label=best_players[3][0])
    rects5 = ax.bar([4-width, 4, 4+width], team5, widthbar, label=best_players[4][0])
    rects6 = ax.bar([5-width, 5, 5+width], team6, widthbar, label=best_players[5][0])
    rects7 = ax.bar([6-width, 6, 6+width], team7, widthbar, label=best_players[6][0])
    rects8 = ax.bar([7-width, 7, 7+width], team8, widthbar, label=best_players[7][0])

    ax.set(xlim=(-0.5, 10.5))
    ax.set_ylabel(title)
    ax.set_title(type +' in RS(19-20) for top 3 players of conference semifinalists')
    ax.set_xticks(x)
    ax.tick_params(labelrotation=90)
    ax.set_xticklabels(teamlabels)
    ax.legend()

    def autolabel(rects):
        """Attach a text label above each bar in *rects*, displaying its height."""
        for rect in rects:
            height = rect.get_height()
            ax.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() /2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')

    autolabel(rects1)
    autolabel(rects2)
    autolabel(rects3)
    autolabel(rects4)
    autolabel(rects5)
    autolabel(rects6)
    autolabel(rects7)
    autolabel(rects8)

    fig.tight_layout()

    plt.savefig(file)

    plt.show()


url = "https://en.wikipedia.org/wiki/2020_NBA_playoffs"
best_players = filter_top_3(url)

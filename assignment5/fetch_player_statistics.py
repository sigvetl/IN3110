from requesting_urls.requesting_urls import get_html
from bs4 import BeautifulSoup
import re
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

#returns list with team-url pairs
def extract_teams():
    html = get_html("https://en.wikipedia.org/wiki/2020_NBA_playoffs")
    baseurl = "https://en.wikipedia.org"
    document = BeautifulSoup(html.text, "lxml")
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
        #link = links.get("href")
        cells_text.append(baseurl + str(links))
        bracket.append(cells_text)
        #print(cells_text)
    bracket2 = []
    for previous, current, next in zip(bracket, bracket[1:], bracket[2:]):
        if len(current) == 3 and current[1] == "":
            #if e[2][0] == "W" or e[2][0] == "E":
            regex = "[a-zA-Z\s]+"
            team = re.findall(regex, previous[3])[0]
            link = previous[-1]
            bracket2.append([team, link])
            team = re.findall(regex, next[3])[0]
            link = next[-1]
            bracket2.append([team, link])

    return bracket2

#Includes player name as a pair with link
def get_player_links(teams):
    baseurl = "https://en.wikipedia.org"
    player_urls = []
    for i in range(len(teams)):
        html = get_html(teams[i][1])
        document = BeautifulSoup(html.text, "lxml")
        print(document.title)
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
    player_stats = []
    for i in range(len(player_urls)):
        print(i)
        teamlist = []
        teamlist.append(player_urls[i][0])
        for j in range(len(player_urls[i])-1):
            html = get_html(player_urls[i][j+1][1])
            document = BeautifulSoup(html.text, "lxml")
            print(document.title)
            table = document.find("table", class_="wikitable sortable")
            if table != None:
                rows = table.find_all("tr")
                for row in rows[-3:-1]:
                    cells = row.find_all(["td"])
                    celle = [cell.get_text(strip=True) for cell in cells]
                    #liste.append(celler)
                    if celle != []:
                        if celle[0][3] == '9':
                            #midlertidig
                            #strip player name for (basketball)
                            #not necessary
                            if celle[11] == '-':
                                celle[11] = '0'
                            if celle[12] == '-':
                                celle[12] = '0'
                            celle[12] = re.findall("([0-9.]+)", celle[12])[0]
                            teamlist.append([player_urls[i][j+1][0], float(celle[8]), float(celle[11]), float(celle[12])])
        player_stats.append(teamlist)
    print(player_stats)
    return player_stats
        #RPG = 8, BPG = 11, PPG = 12


def filter_top_3(player_stats):
    all = []
    for i in range(len(player_stats)):
        sorted_list = sorted(player_stats[i][1:], key=lambda x: x[3], reverse=True)
        #print(sorted_list[0])
        all.append([player_stats[i][0], sorted_list[0], sorted_list[1], sorted_list[2]])
    return all

def arrange_data(best_players):
    teamlabels = []
    playerlabels = []
    ppg = []
    bpg = []
    rpg = []
    for i in range(len(best_players)):
        teamlabels.append(best_players[i][0])
        for j in range(len(best_players[i])-1):
            playerlabels.append(best_players[i][j+1][0])
            ppg.append(best_players[i][j+1][3])
            bpg.append(best_players[i][j+1][2])
            rpg.append(best_players[i][j+1][1])
    title = "in RS(19-20) for top 3 players of conference semifinalists"
    simple_bar(playerlabels, ppg, "Points per game", title)
    simple_bar(playerlabels, rpg, "Rebounds per game", title)
    simple_bar(playerlabels, bpg, "Blocks per game", title)

def simple_bar(playerlabels, data, y, title):
    X = np.arange(len(playerlabels))
    fig, ax = plt.subplots()
    ax.bar(playerlabels, data)
    ax.set_ylabel(y)
    ax.set_title(title)
    ax.set_xticklabels(X)
    ax.tick_params(labelrotation=90)
    ax.set_xticklabels(playerlabels)
    fig.tight_layout()
    plt.title(title)
    plt.show()

def bar_plot(best_players):
    teamlabels = []
    playerlabels = []
    player1 = []
    player2 = []
    player3 = []
    for i in range(len(best_players)):
        teamlabels.append(best_players[i][0])
        for j in range(len(best_players[i])-1):
            playerlabels.append(best_players[i][j+1][0])
        player1.append(best_players[i][1][3])
        player2.append(best_players[i][2][3])
        player3.append(best_players[i][3][3])
    #men_means = [20, 34, 30, 35, 27]
    #women_means = [25, 32, 34, 20, 25]
    print(playerlabels)
    x = np.arange(len(playerlabels))  # the label locations
    print(x)
    width = 0.25  # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width, player1, width, label='player1')
    rects2 = ax.bar(x, player2, width, label='player2')
    rects3 = ax.bar(x + width, player3, width, label='player3')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Points per game')
    ax.set_title('PPG in RS(19-20) for top 3 players of conference semifinalists')
    ax.set_xticks(x)
    #ax.set_xticks(xx)
    ax.tick_params(labelrotation=90)
    ax.set_xticklabels(playerlabels)
    ax.legend()

    """
    def autolabel(rects):
        Attach a text label above each bar in *rects*, displaying its height.
        for rect in rects:
            height = rect.get_height()
            ax.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() /2, height),
                        xytext=(0, 30),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')


    autolabel(rects1)
    autolabel(rects2)
    autolabel(rects3)
    """
    fig.tight_layout()

    plt.show()



#teams = extract_teams()
#print(teams)
#player_urls = get_player_links(teams)
#print(player_urls)
player_urls = [['Milwaukee', ['Giannis Antetokounmpo', 'https://en.wikipedia.org/wiki/Giannis_Antetokounmpo'], ['Thanasis Antetokounmpo', 'https://en.wikipedia.org/wiki/Thanasis_Antetokounmpo'], ['Eric Bledsoe', 'https://en.wikipedia.org/wiki/Eric_Bledsoe'], ['Sterling Brown (basketball)', 'https://en.wikipedia.org/wiki/Sterling_Brown_(basketball)'], ['Pat Connaughton', 'https://en.wikipedia.org/wiki/Pat_Connaughton'], ['Donte DiVincenzo', 'https://en.wikipedia.org/wiki/Donte_DiVincenzo'], ['George Hill (basketball)', 'https://en.wikipedia.org/wiki/George_Hill_(basketball)'], ['Ersan İlyasova', 'https://en.wikipedia.org/wiki/Ersan_%C4%B0lyasova'], ['Kyle Korver', 'https://en.wikipedia.org/wiki/Kyle_Korver'], ['Brook Lopez', 'https://en.wikipedia.org/wiki/Brook_Lopez'], ['Robin Lopez', 'https://en.wikipedia.org/wiki/Robin_Lopez'], ['Frank Mason III', 'https://en.wikipedia.org/wiki/Frank_Mason_III'], ['Wesley Matthews', 'https://en.wikipedia.org/wiki/Wesley_Matthews'], ['Khris Middleton', 'https://en.wikipedia.org/wiki/Khris_Middleton'], ['Cameron Reynolds', 'https://en.wikipedia.org/wiki/Cameron_Reynolds'], ['Marvin Williams', 'https://en.wikipedia.org/wiki/Marvin_Williams'], ['D. J. Wilson', 'https://en.wikipedia.org/wiki/D._J._Wilson']], ['Miami', ['Bam Adebayo', 'https://en.wikipedia.org/wiki/Bam_Adebayo'], ['Kyle Alexander', 'https://en.wikipedia.org/wiki/Kyle_Alexander'], ['Jimmy Butler', 'https://en.wikipedia.org/wiki/Jimmy_Butler'], ['Jae Crowder', 'https://en.wikipedia.org/wiki/Jae_Crowder'], ['Goran Dragić', 'https://en.wikipedia.org/wiki/Goran_Dragi%C4%87'], ['Udonis Haslem', 'https://en.wikipedia.org/wiki/Udonis_Haslem'], ['Tyler Herro', 'https://en.wikipedia.org/wiki/Tyler_Herro'], ['Solomon Hill (basketball)', 'https://en.wikipedia.org/wiki/Solomon_Hill_(basketball)'], ['Andre Iguodala', 'https://en.wikipedia.org/wiki/Andre_Iguodala'], ['Derrick Jones Jr.', 'https://en.wikipedia.org/wiki/Derrick_Jones_Jr.'], ['Meyers Leonard', 'https://en.wikipedia.org/wiki/Meyers_Leonard'], ['Kendrick Nunn', 'https://en.wikipedia.org/wiki/Kendrick_Nunn'], ['KZ Okpala', 'https://en.wikipedia.org/wiki/KZ_Okpala'], ['Kelly Olynyk', 'https://en.wikipedia.org/wiki/Kelly_Olynyk'], ['Duncan Robinson (basketball)', 'https://en.wikipedia.org/wiki/Duncan_Robinson_(basketball)'], ['Chris Silva', 'https://en.wikipedia.org/wiki/Chris_Silva'], ['Gabe Vincent', 'https://en.wikipedia.org/wiki/Gabe_Vincent']], ['Boston', ['Jaylen Brown', 'https://en.wikipedia.org/wiki/Jaylen_Brown'], ['Carsen Edwards', 'https://en.wikipedia.org/wiki/Carsen_Edwards'], ['Tacko Fall', 'https://en.wikipedia.org/wiki/Tacko_Fall'], ['Javonte Green', 'https://en.wikipedia.org/wiki/Javonte_Green'], ['Gordon Hayward', 'https://en.wikipedia.org/wiki/Gordon_Hayward'], ['Enes Kanter', 'https://en.wikipedia.org/wiki/Enes_Kanter'], ['Romeo Langford', 'https://en.wikipedia.org/wiki/Romeo_Langford'], ['Semi Ojeleye', 'https://en.wikipedia.org/wiki/Semi_Ojeleye'], ['Vincent Poirier', 'https://en.wikipedia.org/wiki/Vincent_Poirier'], ['Marcus Smart', 'https://en.wikipedia.org/wiki/Marcus_Smart'], ['Jayson Tatum', 'https://en.wikipedia.org/wiki/Jayson_Tatum'], ['Daniel Theis', 'https://en.wikipedia.org/wiki/Daniel_Theis'], ['Kemba Walker', 'https://en.wikipedia.org/wiki/Kemba_Walker'], ['Brad Wanamaker', 'https://en.wikipedia.org/wiki/Brad_Wanamaker'], ['Tremont Waters', 'https://en.wikipedia.org/wiki/Tremont_Waters'], ['Grant Williams (basketball)', 'https://en.wikipedia.org/wiki/Grant_Williams_(basketball)'], ['Robert Williams (basketball)', 'https://en.wikipedia.org/wiki/Robert_Williams_(basketball)']], ['Toronto', ['OG Anunoby', 'https://en.wikipedia.org/wiki/OG_Anunoby'], ['Chris Boucher (basketball)', 'https://en.wikipedia.org/wiki/Chris_Boucher_(basketball)'], ['Oshae Brissett', 'https://en.wikipedia.org/wiki/Oshae_Brissett'], ['Terence Davis', 'https://en.wikipedia.org/wiki/Terence_Davis'], ['Marc Gasol', 'https://en.wikipedia.org/wiki/Marc_Gasol'], ['Dewan Hernandez', 'https://en.wikipedia.org/wiki/Dewan_Hernandez'], ['Rondae Hollis-Jefferson', 'https://en.wikipedia.org/wiki/Rondae_Hollis-Jefferson'], ['Serge Ibaka', 'https://en.wikipedia.org/wiki/Serge_Ibaka'], ['Stanley Johnson (basketball)', 'https://en.wikipedia.org/wiki/Stanley_Johnson_(basketball)'], ['Kyle Lowry', 'https://en.wikipedia.org/wiki/Kyle_Lowry'], ['Patrick McCaw', 'https://en.wikipedia.org/wiki/Patrick_McCaw'], ['Malcolm Miller (basketball)', 'https://en.wikipedia.org/wiki/Malcolm_Miller_(basketball)'], ['Norman Powell', 'https://en.wikipedia.org/wiki/Norman_Powell'], ['Pascal Siakam', 'https://en.wikipedia.org/wiki/Pascal_Siakam'], ['Matt Thomas (basketball)', 'https://en.wikipedia.org/wiki/Matt_Thomas_(basketball)'], ['Fred VanVleet', 'https://en.wikipedia.org/wiki/Fred_VanVleet'], ['Paul Watson (basketball)', 'https://en.wikipedia.org/wiki/Paul_Watson_(basketball)']], ['LA Lakers', ['Kostas Antetokounmpo', 'https://en.wikipedia.org/wiki/Kostas_Antetokounmpo'], ['Avery Bradley', 'https://en.wikipedia.org/wiki/Avery_Bradley'], ['Devontae Cacok', 'https://en.wikipedia.org/wiki/Devontae_Cacok'], ['Kentavious Caldwell-Pope', 'https://en.wikipedia.org/wiki/Kentavious_Caldwell-Pope'], ['Alex Caruso', 'https://en.wikipedia.org/wiki/Alex_Caruso'], ['Quinn Cook', 'https://en.wikipedia.org/wiki/Quinn_Cook'], ['Anthony Davis', 'https://en.wikipedia.org/wiki/Anthony_Davis'], ['Jared Dudley', 'https://en.wikipedia.org/wiki/Jared_Dudley'], ['Danny Green (basketball)', 'https://en.wikipedia.org/wiki/Danny_Green_(basketball)'], ['Talen Horton-Tucker', 'https://en.wikipedia.org/wiki/Talen_Horton-Tucker'], ['Dwight Howard', 'https://en.wikipedia.org/wiki/Dwight_Howard'], ['LeBron James', 'https://en.wikipedia.org/wiki/LeBron_James'], ['Kyle Kuzma', 'https://en.wikipedia.org/wiki/Kyle_Kuzma'], ['JaVale McGee', 'https://en.wikipedia.org/wiki/JaVale_McGee'], ['Markieff Morris', 'https://en.wikipedia.org/wiki/Markieff_Morris'], ['Rajon Rondo', 'https://en.wikipedia.org/wiki/Rajon_Rondo'], ['J. R. Smith', 'https://en.wikipedia.org/wiki/J._R._Smith'], ['Dion Waiters', 'https://en.wikipedia.org/wiki/Dion_Waiters']], ['Houston', ['Bruno Caboclo', 'https://en.wikipedia.org/wiki/Bruno_Caboclo'], ['DeMarre Carroll', 'https://en.wikipedia.org/wiki/DeMarre_Carroll'], ['Tyson Chandler', 'https://en.wikipedia.org/wiki/Tyson_Chandler'], ['Chris Clemons (basketball)', 'https://en.wikipedia.org/wiki/Chris_Clemons_(basketball)'], ['Robert Covington', 'https://en.wikipedia.org/wiki/Robert_Covington'], ['Michael Frazier II', 'https://en.wikipedia.org/wiki/Michael_Frazier_II'], ['Eric Gordon', 'https://en.wikipedia.org/wiki/Eric_Gordon'], ['Jeff Green (basketball)', 'https://en.wikipedia.org/wiki/Jeff_Green_(basketball)'], ['James Harden', 'https://en.wikipedia.org/wiki/James_Harden'], ['Danuel House', 'https://en.wikipedia.org/wiki/Danuel_House'], ['Luc Mbah a Moute', 'https://en.wikipedia.org/wiki/Luc_Mbah_a_Moute'], ['Ben McLemore', 'https://en.wikipedia.org/wiki/Ben_McLemore'], ['David Nwaba', 'https://en.wikipedia.org/wiki/David_Nwaba'], ['Austin Rivers', 'https://en.wikipedia.org/wiki/Austin_Rivers'], ['Thabo Sefolosha', 'https://en.wikipedia.org/wiki/Thabo_Sefolosha'], ['P. J. Tucker', 'https://en.wikipedia.org/wiki/P._J._Tucker'], ['Russell Westbrook', 'https://en.wikipedia.org/wiki/Russell_Westbrook']], ['Denver', ['Will Barton', 'https://en.wikipedia.org/wiki/Will_Barton'], ['Keita Bates-Diop', 'https://en.wikipedia.org/wiki/Keita_Bates-Diop'], ['Bol Bol', 'https://en.wikipedia.org/wiki/Bol_Bol'], ['Vlatko Čančar', 'https://en.wikipedia.org/wiki/Vlatko_%C4%8Can%C4%8Dar'], ['Tyler Cook', 'https://en.wikipedia.org/wiki/Tyler_Cook'], ['Torrey Craig', 'https://en.wikipedia.org/wiki/Torrey_Craig'], ['Troy Daniels', 'https://en.wikipedia.org/wiki/Troy_Daniels'], ['PJ Dozier', 'https://en.wikipedia.org/wiki/PJ_Dozier'], ['Jerami Grant', 'https://en.wikipedia.org/wiki/Jerami_Grant'], ['Gary Harris', 'https://en.wikipedia.org/wiki/Gary_Harris'], ['Nikola Jokić', 'https://en.wikipedia.org/wiki/Nikola_Joki%C4%87'], ['Paul Millsap', 'https://en.wikipedia.org/wiki/Paul_Millsap'], ['Monté Morris', 'https://en.wikipedia.org/wiki/Mont%C3%A9_Morris'], ['Jamal Murray', 'https://en.wikipedia.org/wiki/Jamal_Murray'], ['Mason Plumlee', 'https://en.wikipedia.org/wiki/Mason_Plumlee'], ['Michael Porter Jr.', 'https://en.wikipedia.org/wiki/Michael_Porter_Jr.'], ['Noah Vonleh', 'https://en.wikipedia.org/wiki/Noah_Vonleh']], ['LA Clippers', ['Patrick Beverley', 'https://en.wikipedia.org/wiki/Patrick_Beverley'], ['Amir Coffey', 'https://en.wikipedia.org/wiki/Amir_Coffey'], ['Paul George', 'https://en.wikipedia.org/wiki/Paul_George'], ['JaMychal Green', 'https://en.wikipedia.org/wiki/JaMychal_Green'], ['Montrezl Harrell', 'https://en.wikipedia.org/wiki/Montrezl_Harrell'], ['Reggie Jackson (basketball, born 1990)', 'https://en.wikipedia.org/wiki/Reggie_Jackson_(basketball,_born_1990)'], ['Mfiondu Kabengele', 'https://en.wikipedia.org/wiki/Mfiondu_Kabengele'], ['Kawhi Leonard', 'https://en.wikipedia.org/wiki/Kawhi_Leonard'], ['Terance Mann', 'https://en.wikipedia.org/wiki/Terance_Mann'], ['Rodney McGruder', 'https://en.wikipedia.org/wiki/Rodney_McGruder'], ['Marcus Morris', 'https://en.wikipedia.org/wiki/Marcus_Morris'], ['Johnathan Motley', 'https://en.wikipedia.org/wiki/Johnathan_Motley'], ['Joakim Noah', 'https://en.wikipedia.org/wiki/Joakim_Noah'], ['Patrick Patterson (basketball)', 'https://en.wikipedia.org/wiki/Patrick_Patterson_(basketball)'], ['Landry Shamet', 'https://en.wikipedia.org/wiki/Landry_Shamet'], ['Lou Williams', 'https://en.wikipedia.org/wiki/Lou_Williams'], ['Ivica Zubac', 'https://en.wikipedia.org/wiki/Ivica_Zubac']]]

#player_stats = get_player_stats(player_urls)
#print(player_stats)
player_stats = [['Milwaukee', ['Giannis Antetokounmpo', 13.6, 1.0, 29.5], ['Thanasis Antetokounmpo', 1.2, 0.1, 2.8], ['Eric Bledsoe', 4.6, 0.4, 14.9], ['Pat Connaughton', 4.2, 0.5, 5.4], ['Donte DiVincenzo', 4.8, 0.3, 9.2], ['George Hill (basketball)', 3.0, 0.1, 9.4], ['Ersan İlyasova', 4.8, 0.3, 6.6], ['Kyle Korver', 2.1, 0.2, 6.7], ['Brook Lopez', 4.6, 2.4, 12.0], ['Robin Lopez', 2.4, 0.7, 5.4], ['Wesley Matthews', 2.5, 0.1, 7.4], ['Khris Middleton', 6.2, 0.1, 20.9], ['Marvin Williams', 2.7, 0.5, 6.7], ['Marvin Williams', 4.4, 0.5, 4.0], ['D. J. Wilson', 2.5, 0.1, 3.6]], ['Miami', ['Bam Adebayo', 10.2, 1.3, 15.9], ['Kyle Alexander', 1.5, 0.0, 1.0], ['Jimmy Butler', 6.7, 0.6, 19.9], ['Jae Crowder', 6.2, 0.3, 9.9], ['Jae Crowder', 5.4, 0.5, 11.9], ['Goran Dragić', 3.2, 0.2, 16.2], ['Udonis Haslem', 4.0, 0.0, 3.0], ['Solomon Hill (basketball)', 3.0, 0.1, 5.7], ['Solomon Hill (basketball)', 1.9, 0.5, 4.5], ['Andre Iguodala', 3.7, 1.0, 4.6], ['Meyers Leonard', 5.1, 0.3, 6.1], ['Kendrick Nunn', 2.7, 0.2, 15.3], ['KZ Okpala', 1.0, 0.2, 1.4], ['Kelly Olynyk', 4.6, 0.3, 8.2], ['Duncan Robinson (basketball)', 3.2, 0.3, 13.5], ['Chris Silva', 2.9, 0.5, 3.0], ['Gabe Vincent', 0.6, 0.0, 2.4]], ['Boston', ['Jaylen Brown', 6.4, 0.4, 20.3], ['Carsen Edwards', 1.3, 0.1, 3.3], ['Tacko Fall', 2.1, 0.6, 3.3], ['Javonte Green', 1.9, 0.2, 3.4], ['Gordon Hayward', 6.7, 0.4, 17.5], ['Enes Kanter', 7.4, 0.7, 8.1], ['Semi Ojeleye', 2.1, 0.1, 3.4], ['Jayson Tatum', 7.0, 0.9, 23.4], ['Daniel Theis', 6.6, 1.3, 9.2], ['Kemba Walker', 3.9, 0.5, 20.4], ['Brad Wanamaker', 2.0, 0.2, 6.9], ['Grant Williams (basketball)', 2.6, 0.5, 3.4]], ['Toronto', ['OG Anunoby', 5.3, 0.7, 10.6], ['Chris Boucher (basketball)', 4.5, 1.0, 6.6], ['Terence Davis', 3.3, 0.2, 7.5], ['Marc Gasol', 6.3, 0.9, 7.5], ['Dewan Hernandez', 1.8, 0.0, 2.8], ['Dewan Hernandez', 9.1, 1.8, 13.7], ['Rondae Hollis-Jefferson', 4.7, 0.4, 7.0], ['Serge Ibaka', 8.2, 0.8, 15.4], ['Stanley Johnson (basketball)', 1.5, 0.2, 2.4], ['Kyle Lowry', 5.0, 0.4, 19.4], ['Patrick McCaw', 2.3, 0.1, 4.6], ['Norman Powell', 3.7, 0.4, 16.0], ['Pascal Siakam', 7.3, 0.9, 22.9], ['Fred VanVleet', 3.8, 0.3, 17.6]], ['LA Lakers', ['Kostas Antetokounmpo', 0.6, 0.0, 1.4], ['Avery Bradley', 2.3, 0.1, 8.6], ['Devontae Cacok', 5.0, 0.0, 6.0], ['Kentavious Caldwell-Pope', 2.1, 0.2, 9.3], ['Alex Caruso', 1.9, 0.3, 5.5], ['Quinn Cook', 1.2, 0.0, 5.1], ['Anthony Davis', 9.3, 2.3, 26.1], ['Jared Dudley', 1.2, 0.1, 1.5], ['Danny Green (basketball)', 3.3, 0.5, 8.0], ['Talen Horton-Tucker', 1.2, 0.2, 5.7], ['Dwight Howard', 7.3, 1.1, 7.5], ['LeBron James', 7.8, 0.5, 25.3], ['Kyle Kuzma', 4.5, 0.4, 12.8], ['JaVale McGee', 5.7, 1.4, 6.6], ['Markieff Morris', 3.9, 0.3, 11.0], ['Markieff Morris', 3.2, 0.4, 5.3], ['Rajon Rondo', 3.0, 0.0, 7.1], ['J. R. Smith', 0.8, 0.0, 2.8], ['Dion Waiters', 3.7, 0.7, 9.3], ['Dion Waiters', 1.9, 0.6, 11.9]], ['Houston', ['Bruno Caboclo', 2.0, 0.5, 2.8], ['Bruno Caboclo', 2.0, 0.6, 3.5], ['DeMarre Carroll', 2.1, 0.1, 2.2], ['DeMarre Carroll', 2.7, 0.3, 6.0], ['Tyson Chandler', 2.5, 0.3, 1.3], ['Chris Clemons (basketball)', 0.9, 0.1, 4.9], ['Robert Covington', 6.0, 0.9, 12.8], ['Robert Covington', 8.0, 2.2, 11.6], ['Michael Frazier II', 0.8, 0.0, 2.1], ['Eric Gordon', 2.0, 0.3, 14.4], ['Jeff Green (basketball)', 2.7, 0.3, 7.8], ['Jeff Green (basketball)', 2.9, 0.5, 12.2], ['James Harden', 6.6, 0.9, 34.3], ['Danuel House', 4.2, 0.5, 10.5], ['Luc Mbah a Moute', 0.7, 0.0, 1.7], ['Ben McLemore', 2.2, 0.2, 10.1], ['David Nwaba', 2.3, 0.6, 5.2], ['Austin Rivers', 2.6, 0.1, 8.8], ['Thabo Sefolosha', 2.3, 0.3, 2.2], ['P. J. Tucker', 6.6, 0.5, 6.9], ['Russell Westbrook', 7.9, 0.4, 27.2]], ['Denver', ['Will Barton', 6.3, 0.5, 15.1], ['Keita Bates-Diop', 3.0, 0.5, 6.8], ['Keita Bates-Diop', 2.4, 0.6, 5.4], ['Vlatko Čančar', 0.7, 0.1, 1.2], ['Tyler Cook', 0.9, 0.0, 1.7], ['Tyler Cook', 2.0, 0.0, 2.0], ['Torrey Craig', 3.3, 0.6, 5.4], ['Troy Daniels', 1.1, 0.1, 4.2], ['Troy Daniels', 1.0, 0.0, 4.3], ['PJ Dozier', 1.9, 0.2, 5.8], ['Jerami Grant', 3.5, 0.8, 12.0], ['Gary Harris', 2.9, 0.3, 10.4], ['Nikola Jokić', 9.7, 0.6, 19.9], ['Paul Millsap', 5.7, 0.6, 11.6], ['Monté Morris', 1.9, 0.2, 9.0], ['Jamal Murray', 4.0, 0.3, 18.5], ['Mason Plumlee', 5.2, 0.6, 7.2], ['Michael Porter Jr.', 4.7, 0.5, 9.3], ['Noah Vonleh', 4.0, 0.2, 4.1], ['Noah Vonleh', 1.1, 0.0, 1.9]], ['LA Clippers', ['Patrick Beverley', 5.2, 0.5, 7.9], ['Paul George', 5.2, 0.4, 21.5], ['JaMychal Green', 6.2, 0.4, 6.8], ['Montrezl Harrell', 7.1, 1.1, 18.6], ['Reggie Jackson (basketball, born 1990)', 2.9, 0.1, 14.9], ['Reggie Jackson (basketball, born 1990)', 3.0, 0.2, 9.5], ['Kawhi Leonard', 7.1, 0.6, 27.1], ['Marcus Morris', 5.4, 0.4, 19.6], ['Marcus Morris', 4.1, 0.7, 10.1], ['Joakim Noah', 3.2, 0.2, 2.8], ['Patrick Patterson (basketball)', 2.6, 0.1, 4.9], ['Landry Shamet', 1.9, 0.2, 9.3], ['Lou Williams', 3.1, 0.2, 18.2], ['Ivica Zubac', 7.5, 0.9, 8.3]]]
[['Milwaukee', ['Giannis Antetokounmpo', 13.6, 1.0, 29.5], ['Thanasis Antetokounmpo', 1.2, 0.1, 2.8], ['Eric Bledsoe', 4.6, 0.4, 14.9], ['Pat Connaughton', 4.2, 0.5, 5.4], ['Donte DiVincenzo', 4.8, 0.3, 9.2], ['George Hill (basketball)', 3.0, 0.1, 9.4], ['Ersan İlyasova', 4.8, 0.3, 6.6], ['Kyle Korver', 2.1, 0.2, 6.7], ['Brook Lopez', 4.6, 2.4, 12.0], ['Robin Lopez', 2.4, 0.7, 5.4], ['Wesley Matthews', 2.5, 0.1, 7.4], ['Khris Middleton', 6.2, 0.1, 20.9], ['Marvin Williams', 2.7, 0.5, 6.7], ['Marvin Williams', 4.4, 0.5, 4.0], ['D. J. Wilson', 2.5, 0.1, 3.6]], ['Miami', ['Bam Adebayo', 10.2, 1.3, 15.9], ['Kyle Alexander', 1.5, 0.0, 1.0], ['Jimmy Butler', 6.7, 0.6, 19.9], ['Jae Crowder', 6.2, 0.3, 9.9], ['Jae Crowder', 5.4, 0.5, 11.9], ['Goran Dragić', 3.2, 0.2, 16.2], ['Udonis Haslem', 4.0, 0.0, 3.0], ['Solomon Hill (basketball)', 3.0, 0.1, 5.7], ['Solomon Hill (basketball)', 1.9, 0.5, 4.5], ['Andre Iguodala', 3.7, 1.0, 4.6], ['Meyers Leonard', 5.1, 0.3, 6.1], ['Kendrick Nunn', 2.7, 0.2, 15.3], ['KZ Okpala', 1.0, 0.2, 1.4], ['Kelly Olynyk', 4.6, 0.3, 8.2], ['Duncan Robinson (basketball)', 3.2, 0.3, 13.5], ['Chris Silva', 2.9, 0.5, 3.0], ['Gabe Vincent', 0.6, 0.0, 2.4]], ['Boston', ['Jaylen Brown', 6.4, 0.4, 20.3], ['Carsen Edwards', 1.3, 0.1, 3.3], ['Tacko Fall', 2.1, 0.6, 3.3], ['Javonte Green', 1.9, 0.2, 3.4], ['Gordon Hayward', 6.7, 0.4, 17.5], ['Enes Kanter', 7.4, 0.7, 8.1], ['Semi Ojeleye', 2.1, 0.1, 3.4], ['Jayson Tatum', 7.0, 0.9, 23.4], ['Daniel Theis', 6.6, 1.3, 9.2], ['Kemba Walker', 3.9, 0.5, 20.4], ['Brad Wanamaker', 2.0, 0.2, 6.9], ['Grant Williams (basketball)', 2.6, 0.5, 3.4]], ['Toronto', ['OG Anunoby', 5.3, 0.7, 10.6], ['Chris Boucher (basketball)', 4.5, 1.0, 6.6], ['Terence Davis', 3.3, 0.2, 7.5], ['Marc Gasol', 6.3, 0.9, 7.5], ['Dewan Hernandez', 1.8, 0.0, 2.8], ['Dewan Hernandez', 9.1, 1.8, 13.7], ['Rondae Hollis-Jefferson', 4.7, 0.4, 7.0], ['Serge Ibaka', 8.2, 0.8, 15.4], ['Stanley Johnson (basketball)', 1.5, 0.2, 2.4], ['Kyle Lowry', 5.0, 0.4, 19.4], ['Patrick McCaw', 2.3, 0.1, 4.6], ['Norman Powell', 3.7, 0.4, 16.0], ['Pascal Siakam', 7.3, 0.9, 22.9], ['Fred VanVleet', 3.8, 0.3, 17.6]], ['LA Lakers', ['Kostas Antetokounmpo', 0.6, 0.0, 1.4], ['Avery Bradley', 2.3, 0.1, 8.6], ['Devontae Cacok', 5.0, 0.0, 6.0], ['Kentavious Caldwell-Pope', 2.1, 0.2, 9.3], ['Alex Caruso', 1.9, 0.3, 5.5], ['Quinn Cook', 1.2, 0.0, 5.1], ['Anthony Davis', 9.3, 2.3, 26.1], ['Jared Dudley', 1.2, 0.1, 1.5], ['Danny Green (basketball)', 3.3, 0.5, 8.0], ['Talen Horton-Tucker', 1.2, 0.2, 5.7], ['Dwight Howard', 7.3, 1.1, 7.5], ['LeBron James', 7.8, 0.5, 25.3], ['Kyle Kuzma', 4.5, 0.4, 12.8], ['JaVale McGee', 5.7, 1.4, 6.6], ['Markieff Morris', 3.9, 0.3, 11.0], ['Markieff Morris', 3.2, 0.4, 5.3], ['Rajon Rondo', 3.0, 0.0, 7.1], ['J. R. Smith', 0.8, 0.0, 2.8], ['Dion Waiters', 3.7, 0.7, 9.3], ['Dion Waiters', 1.9, 0.6, 11.9]], ['Houston', ['Bruno Caboclo', 2.0, 0.5, 2.8], ['Bruno Caboclo', 2.0, 0.6, 3.5], ['DeMarre Carroll', 2.1, 0.1, 2.2], ['DeMarre Carroll', 2.7, 0.3, 6.0], ['Tyson Chandler', 2.5, 0.3, 1.3], ['Chris Clemons (basketball)', 0.9, 0.1, 4.9], ['Robert Covington', 6.0, 0.9, 12.8], ['Robert Covington', 8.0, 2.2, 11.6], ['Michael Frazier II', 0.8, 0.0, 2.1], ['Eric Gordon', 2.0, 0.3, 14.4], ['Jeff Green (basketball)', 2.7, 0.3, 7.8], ['Jeff Green (basketball)', 2.9, 0.5, 12.2], ['James Harden', 6.6, 0.9, 34.3], ['Danuel House', 4.2, 0.5, 10.5], ['Luc Mbah a Moute', 0.7, 0.0, 1.7], ['Ben McLemore', 2.2, 0.2, 10.1], ['David Nwaba', 2.3, 0.6, 5.2], ['Austin Rivers', 2.6, 0.1, 8.8], ['Thabo Sefolosha', 2.3, 0.3, 2.2], ['P. J. Tucker', 6.6, 0.5, 6.9], ['Russell Westbrook', 7.9, 0.4, 27.2]], ['Denver', ['Will Barton', 6.3, 0.5, 15.1], ['Keita Bates-Diop', 3.0, 0.5, 6.8], ['Keita Bates-Diop', 2.4, 0.6, 5.4], ['Vlatko Čančar', 0.7, 0.1, 1.2], ['Tyler Cook', 0.9, 0.0, 1.7], ['Tyler Cook', 2.0, 0.0, 2.0], ['Torrey Craig', 3.3, 0.6, 5.4], ['Troy Daniels', 1.1, 0.1, 4.2], ['Troy Daniels', 1.0, 0.0, 4.3], ['PJ Dozier', 1.9, 0.2, 5.8], ['Jerami Grant', 3.5, 0.8, 12.0], ['Gary Harris', 2.9, 0.3, 10.4], ['Nikola Jokić', 9.7, 0.6, 19.9], ['Paul Millsap', 5.7, 0.6, 11.6], ['Monté Morris', 1.9, 0.2, 9.0], ['Jamal Murray', 4.0, 0.3, 18.5], ['Mason Plumlee', 5.2, 0.6, 7.2], ['Michael Porter Jr.', 4.7, 0.5, 9.3], ['Noah Vonleh', 4.0, 0.2, 4.1], ['Noah Vonleh', 1.1, 0.0, 1.9]], ['LA Clippers', ['Patrick Beverley', 5.2, 0.5, 7.9], ['Paul George', 5.2, 0.4, 21.5], ['JaMychal Green', 6.2, 0.4, 6.8], ['Montrezl Harrell', 7.1, 1.1, 18.6], ['Reggie Jackson (basketball, born 1990)', 2.9, 0.1, 14.9], ['Reggie Jackson (basketball, born 1990)', 3.0, 0.2, 9.5], ['Kawhi Leonard', 7.1, 0.6, 27.1], ['Marcus Morris', 5.4, 0.4, 19.6], ['Marcus Morris', 4.1, 0.7, 10.1], ['Joakim Noah', 3.2, 0.2, 2.8], ['Patrick Patterson (basketball)', 2.6, 0.1, 4.9], ['Landry Shamet', 1.9, 0.2, 9.3], ['Lou Williams', 3.1, 0.2, 18.2], ['Ivica Zubac', 7.5, 0.9, 8.3]]]

#best_players = filter_top_3(player_stats)

best_players = [['Milwaukee', ['Giannis Antetokounmpo', 13.6, 1.0, 29.5], ['Khris Middleton', 6.2, 0.1, 20.9], ['Eric Bledsoe', 4.6, 0.4, 14.9]], ['Miami', ['Jimmy Butler', 6.7, 0.6, 19.9], ['Goran Dragić', 3.2, 0.2, 16.2], ['Bam Adebayo', 10.2, 1.3, 15.9]], ['Boston', ['Jayson Tatum', 7.0, 0.9, 23.4], ['Kemba Walker', 3.9, 0.5, 20.4], ['Jaylen Brown', 6.4, 0.4, 20.3]], ['Toronto', ['Pascal Siakam', 7.3, 0.9, 22.9], ['Kyle Lowry', 5.0, 0.4, 19.4], ['Fred VanVleet', 3.8, 0.3, 17.6]], ['LA Lakers', ['Anthony Davis', 9.3, 2.3, 26.1], ['LeBron James', 7.8, 0.5, 25.3], ['Kyle Kuzma', 4.5, 0.4, 12.8]], ['Houston', ['James Harden', 6.6, 0.9, 34.3], ['Russell Westbrook', 7.9, 0.4, 27.2], ['Eric Gordon', 2.0, 0.3, 14.4]], ['Denver', ['Nikola Jokić', 9.7, 0.6, 19.9], ['Jamal Murray', 4.0, 0.3, 18.5], ['Will Barton', 6.3, 0.5, 15.1]], ['LA Clippers', ['Kawhi Leonard', 7.1, 0.6, 27.1], ['Paul George', 5.2, 0.4, 21.5], ['Marcus Morris', 5.4, 0.4, 19.6]]]
#print(best_players[0][1])
arrange_data(best_players)

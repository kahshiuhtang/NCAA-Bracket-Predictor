from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
def dataScraperRating(years = [2022]):
    # loop through each year
    result = []
    for y in years:
        # NCAA season to scrape
        year = y
        # URL to scrape
        url = f"https://www.sports-reference.com/cbb/seasons/{year}-standings.html#standings_aac"
        # collect HTML data
        html = urlopen(url)
        
        # create beautiful soup object from HTML
        soup = BeautifulSoup(html, features="lxml")
        print(soup)
        # use getText()to extract the headers into a list
        titles = [th.getText() for th in soup.findAll('tr', limit=100)[1].findAll('th') if th.getText() != '\xa0']
        # first, find only column headers
        headers = titles[1:titles.index("Notes")+1]
        # then, exclude first set of column headers (duplicated)
        titles = titles[titles.index("Notes")+1:]
        print(headers)
         # next, grab all data from rows (avoid first row)
        rows = soup.findAll('tr')[1:]
        team_stats = [[td.getText() for td in rows[i].findAll('td') if td.getText() != '']
                    for i in range(len(rows))]
        team_stats = [e for e in team_stats if e != []]
        team_stats = [e[0:10] + [''.join(e[10:len(e)-1])] + [e[len(e)-1]] for e in team_stats if e != [] and type(e[0]) == str and e[0] != '-' and len(e) < 15]
        print(team_stats)
        basic_stats = pd.DataFrame(team_stats, columns = headers)
        basic_stats["Year"] = [y for ele in basic_stats["SRS"]]
        temp_col = basic_stats.pop('Year')
        basic_stats.insert(0, 'Year', temp_col)
        result.append(basic_stats)
    return result
result1 = dataScraperRating()
df1 = pd.concat(result1)
df1.to_csv("ConferenceStandings.csv")
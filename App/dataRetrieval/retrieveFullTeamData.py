from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd

def dataScraperBasic(years = [2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021,2022]):
    # loop through each year
    result = []
    for y in years:
        # NCAA season to scrape
        year = y
        # URL to scrape
        url1 = f"https://www.sports-reference.com/cbb/seasons/{year}-school-stats.html#basic_school_stats"
        url2 = f"https://www.sports-reference.com/cbb/seasons/{year}-opponent-stats.html#basic_opp_stats"
        # collect HTML data
        html1 = urlopen(url1)
        html2 = urlopen(url2)
        
        # create beautiful soup object from HTML
        soup1 = BeautifulSoup(html1, features="lxml")
        soup2 = BeautifulSoup(html2, features="lxml")
        
        # use getText()to extract the headers into a list
        titles = [th.getText() for th in soup1.findAll('tr', limit=2)[1].findAll('th') if th.getText() != '\xa0']
        
        # first, find only column headers
        headers = titles[1:titles.index("PF")+1]
        
        # then, exclude first set of column headers (duplicated)
        titles = titles[titles.index("PF")+1:]

         # next, grab all data from rows (avoid first row)
        rows1 = soup1.findAll('tr')[1:]
        rows2 = soup2.findAll('tr')[1:]
        team_stats1 = [[td.getText() for td in rows1[i].findAll('td') if td.getText() != '']
                    for i in range(len(rows1))]
        team_stats2 = [[td.getText() for td in rows2[i].findAll('td') if td.getText() != '']
                    for i in range(len(rows2))]
        team_stats1 = [e for e in team_stats1 if e != []]
        team_stats2 = [e for e in team_stats2 if e != []]
        basic_stats1 = pd.DataFrame(team_stats1, columns = headers)
        basic_stats2 = pd.DataFrame(team_stats2, columns = headers)
        basic_stats1["Tourn."] = ["Y" if "NCAA" in ele else "N" for ele in basic_stats1["School"]]
        # remove NCAA from team names
        basic_stats1["School"] = [ele.replace('NCAA', '') for ele in basic_stats1["School"]]
        #final_df = final_df.append(basic_stats)
        basic_stats2 = basic_stats2.drop(basic_stats2.columns[[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]], axis = 1)
        basic_stats = pd.concat([basic_stats1, basic_stats2], axis = 1, join='inner')
        basic_stats["Year"] = [y for ele in basic_stats1["School"]]
        temp_col = basic_stats.pop('Year')
        basic_stats.insert(0, 'Year', temp_col)
        result.append(basic_stats)
    return result
def dataScraperAdvanced(years = [2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021,2022]):
    # loop through each year
    result = []
    for y in years:
        # NCAA season to scrape
        year = y
        # URL to scrape
        url1 = f"https://www.sports-reference.com/cbb/seasons/{year}-advanced-school-stats.html#adv_school_stats"
        url2 = f"https://www.sports-reference.com/cbb/seasons/{year}-advanced-opponent-stats.html#adv_opp_stats"
         # collect HTML data
        html1 = urlopen(url1)
        html2 = urlopen(url2)
        
        # create beautiful soup object from HTML
        soup1 = BeautifulSoup(html1, features="lxml")
        soup2 = BeautifulSoup(html2, features="lxml")
        
        # use getText()to extract the headers into a list
        titles = [th.getText() for th in soup1.findAll('tr', limit=2)[1].findAll('th') if th.getText() != '\xa0']
        
        # first, find only column headers
        headers = titles[1:titles.index("FT/FGA")+1]
        
        # then, exclude first set of column headers (duplicated)
        titles = titles[titles.index("FT/FGA")+1:]

         # next, grab all data from rows (avoid first row)
        rows1 = soup1.findAll('tr')[1:]
        rows2 = soup2.findAll('tr')[1:]
        team_stats1 = [[td.getText() for td in rows1[i].findAll('td') if td.getText() != '']
                    for i in range(len(rows1))]
        team_stats2 = [[td.getText() for td in rows2[i].findAll('td') if td.getText() != '']
                    for i in range(len(rows2))]
        team_stats1 = [e for e in team_stats1 if e != []]
        team_stats2 = [e for e in team_stats2 if e != []]
        basic_stats1 = pd.DataFrame(team_stats1, columns = headers)
        basic_stats2 = pd.DataFrame(team_stats2, columns = headers)
        basic_stats1 = basic_stats1.drop(basic_stats1.columns[[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]], axis = 1)
        basic_stats2 = basic_stats2.drop(basic_stats2.columns[[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]], axis = 1)
        basic_stats = pd.concat([basic_stats1, basic_stats2], axis = 1, join='inner')
        result.append(basic_stats)
    return result

result1 = dataScraperBasic()
result2 = dataScraperAdvanced()
df1 = pd.concat(result1)
df2 = pd.concat(result2)
result = pd.concat([df1, df2], axis=1)
result = result.drop(result.columns[[0,52]], axis = 1)
result.to_csv("Final_Data.csv")


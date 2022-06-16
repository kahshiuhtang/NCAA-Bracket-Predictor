from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd

def dataScraperBasic(years = [2000]):
    # loop through each year
    result = []
    for y in years:
        # NCAA season to scrape
        year = y
        # URL to scrape
        url1 = f"https://www.sports-reference.com/cbb/seasons/{year}-school-stats.html#basic_school_stats"
        # collect HTML data
        html1 = urlopen(url1)
        
        # create beautiful soup object from HTML
        soup1 = BeautifulSoup(html1, features="lxml")
        
        # use getText()to extract the headers into a list
        titles = [th.getText() for th in soup1.findAll('tr', limit=2)[1].findAll('th') if th.getText() != '\xa0']
        
        # first, find only column headers
        headers = titles[1:titles.index("PF")+1]
        #headers.pop(9)
        #headers.pop(9)
        #headers.pop(21)
        #print(headers)
        
        # then, exclude first set of column headers (duplicated)
        titles = titles[titles.index("PF")+1:]

         # next, grab all data from rows (avoid first row)
        rows1 = soup1.findAll('tr')[1:]
        team_stats1 = [[td.getText() for td in rows1[i].findAll('td') if td.getText() != '']
                    for i in range(len(rows1))]
        team_stats1 = [e for e in team_stats1 if e != []]
        basic_stats1 = pd.DataFrame(team_stats1, columns = headers)
        basic_stats1["Tourn."] = ["Y" if "NCAA" in ele else "N" for ele in basic_stats1["School"]]
        # remove NCAA from team names
        basic_stats1["School"] = [ele.replace('NCAA', '') for ele in basic_stats1["School"]]
        #final_df = final_df.append(basic_stats)
        basic_stats1["Year"] = [y for ele in basic_stats1["School"]]
        temp_col = basic_stats1.pop('Year')
        basic_stats1.insert(0, 'Year', temp_col)
        result.append(basic_stats1)
    return result
def dataScraperAdvanced(years = [2000]):
    # loop through each year
    result = []
    for y in years:
        # NCAA season to scrape
        year = y
        # URL to scrape
        url1 = f"https://www.sports-reference.com/cbb/seasons/{year}-advanced-school-stats.html#adv_school_stats"
         # collect HTML data
        html1 = urlopen(url1)
        
        # create beautiful soup object from HTML
        soup1 = BeautifulSoup(html1, features="lxml")
        
        # use getText()to extract the headers into a list
        titles = [th.getText() for th in soup1.findAll('tr', limit=2)[1].findAll('th') if th.getText() != '\xa0']
        
        # first, find only column headers
        headers = titles[1:titles.index("FT/FGA")+1]
        print(year)
        # then, exclude first set of column headers (duplicated)
        titles = titles[titles.index("FT/FGA")+1:]

         # next, grab all data from rows (avoid first row)
        rows1 = soup1.findAll('tr')[1:]
        team_stats1 = [[td.getText() for td in rows1[i].findAll('td') if td.getText() != '']
                    for i in range(len(rows1))]
        team_stats1 = [e for e in team_stats1 if e != []]
        basic_stats1 = pd.DataFrame(team_stats1, columns = headers)
        basic_stats1 = basic_stats1.drop(basic_stats1.columns[[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]], axis = 1)
        result.append(basic_stats1)
    return result

result1 = dataScraperBasic()
result2 = dataScraperAdvanced()
df1 = pd.concat(result1)
df2 = pd.concat(result2)
result = pd.concat([df1, df2], axis=1)
#result = result.drop(result.columns[[0,52]], axis = 1)
result.to_csv("Final_Data1995.csv")


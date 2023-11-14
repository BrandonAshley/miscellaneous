import requests
import pandas as pd
from bs4 import BeautifulSoup

# Step 1: Extract links to all Premier League table CSV files
url = 'https://www.football-data.co.uk/englandm.php'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')
csv_links = []
for link in soup.find_all('a', href=True):
    if link.text == 'Premier League' and link['href'].startswith('mmz'):
        csv_link = 'https://www.football-data.co.uk/' + link['href']
        csv_links.append(csv_link)

# Step 2: Download and merge the first 7 CSV files
dfs = []
for csv_link in csv_links[:10]:
    response = requests.get(csv_link)
    filename = csv_link.split('/')[-1].split('.')[0] + '.csv'
    with open(filename, 'wb') as f:
        f.write(response.content)
    df = pd.read_csv(filename)
    dfs.append(df)
merged_df = pd.concat(dfs, ignore_index=True)


df_Before_drop=merged_df


print(merged_df.head())

nan_counts = merged_df.isna().sum()

# Calculate the percentage of NaN values in each column
nan_percents = nan_counts / len(merged_df) * 100

# Print the columns with more than 90% NaN values
cols_to_drop = nan_percents[nan_percents > 20].index.tolist()
print(f"Columns to drop: {cols_to_drop}")

# Drop the columns with more than 90% NaN values
merged_df.drop(columns=cols_to_drop, inplace=True)

# Check how many NaN values still remain
print(f"Number of NaN values remaining: {merged_df.isna().sum().sum()}")


merged_df.to_csv('PremierLeague.csv')


import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from scipy.stats import trim_mean

df_original=pd.read_csv('PremierLeague.csv')
df=df_original.copy()

df.dropna(thresh=df.shape[1]*0.5, inplace=True)


# convert date column to datetime format
df['Date'] = pd.to_datetime(df['Date'], dayfirst=True,format='mixed')
#df['Date'] = pd.to_datetime(df['Date'])


# format date string to desired format
#f['Date'] = df['Date'].dt.strftime('%d/%m/%Y')
#df=df.set_index('Date')

#print(df.columns)

#Average of the odds
df["HomeOdds"]=df[['B365H','BWH','IWH','PSH','WHH','VCH','PSCH']].mean(axis=1)
df["DrawOdds"]=df[['B365D','BWD','IWD','PSD','WHD','VCD','PSCD']].mean(axis=1)
df["AwayOdds"]=df[['B365A','BWA','IWA','PSA','WHA','VCA','PSCA']].mean(axis=1)
    
df=df.drop(columns=['B365H', 'B365D', 'B365A', 'BWH', 'BWD', 'BWA', 'IWH',
'IWD', 'IWA', 'PSH', 'PSD', 'PSA', 'WHH', 'WHD', 'WHA', 'VCH', 'VCD',
'VCA', 'PSCH', 'PSCD', 'PSCA'])

le = LabelEncoder()
df['Referee'] = le.fit_transform(df['Referee'])

df['Results'] = df.apply(lambda row: row['AwayTeam'] if row['FTR'] == 'A' else (row['HomeTeam'] if row['FTR'] == 'H' else 'Draw'), axis=1)

df['Halftime_result'] = df.apply(lambda row: row['AwayTeam'] if row['HTR'] == 'A' else (row['HomeTeam'] if row['HTR'] == 'H' else 'Draw'), axis=1)

df=df.drop(columns=['Unnamed: 0', 'Div','FTR','HTR'])#


team_perf = pd.concat([
    df.groupby(['HomeTeam', 'AwayTeam'])['FTHG'].mean().reset_index().rename(columns={'`FTHG': 'HomeGoals'}),
    df.groupby(['AwayTeam', 'HomeTeam'])['FTAG'].mean().reset_index().rename(columns={'FTAG': 'AwayGoals'}),
    
    df.groupby(['HomeTeam', 'AwayTeam'])['HS'].mean().reset_index().rename(columns={'HS': 'HomeShots'}),
    df.groupby(['AwayTeam', 'HomeTeam'])['AS'].mean().reset_index().rename(columns={'AS': 'AwayShots'}),
    
    df.groupby(['HomeTeam', 'AwayTeam'])['HST'].mean().reset_index().rename(columns={'HST': 'HomeShotsTarget'}),
    df.groupby(['AwayTeam', 'HomeTeam'])['AST'].mean().reset_index().rename(columns={'AST': 'AwayShotsTarget'}),
    
    df.groupby(['HomeTeam', 'AwayTeam'])['HF'].mean().reset_index().rename(columns={'HF': 'HomeFouls'}),
    df.groupby(['AwayTeam', 'HomeTeam'])['AF'].mean().reset_index().rename(columns={'AF': 'AwayFouls'}),
    
    df.groupby(['HomeTeam', 'AwayTeam'])['HC'].mean().reset_index().rename(columns={'HC': 'HomeCorners'}),
    df.groupby(['AwayTeam', 'HomeTeam'])['AC'].mean().reset_index().rename(columns={'AC': 'AwayCorners'}),
    
    df.groupby(['HomeTeam', 'AwayTeam'])['HC'].mean().reset_index().rename(columns={'HC': 'HomeCorners'}),
    df.groupby(['AwayTeam', 'HomeTeam'])['AC'].mean().reset_index().rename(columns={'AC': 'AwayCorners'}),
    
    df.groupby(['HomeTeam', 'AwayTeam'])['HY'].mean().reset_index().rename(columns={'HY': 'HomeYellows'}),
    df.groupby(['AwayTeam', 'HomeTeam'])['AY'].mean().reset_index().rename(columns={'AY': 'AwayYellows'}),
    
    df.groupby(['HomeTeam', 'AwayTeam'])['HomeOdds'].mean().reset_index(),
    df.groupby(['AwayTeam', 'HomeTeam'])['DrawOdds'].mean().reset_index(),
    df.groupby(['AwayTeam', 'HomeTeam'])['AwayOdds'].mean().reset_index()
    


])

grouped = team_perf.groupby(['HomeTeam', 'AwayTeam']).sum()
grouped = grouped.reset_index()


test=grouped[(grouped['HomeTeam'].str.contains('Man United') & grouped['AwayTeam'].str.contains('Liverpool')) |                 (grouped['AwayTeam'].str.contains('Man United')& grouped['HomeTeam'].str.contains('Liverpool'))]


#Every teams results
df_matches=df
df_matches=df_matches.reset_index()

def create_team_dataframe(team_name, df_matches):
    # Get all matches where the team played as either HomeTeam or AwayTeam
    team_matches = df_matches[(df_matches['HomeTeam'] == team_name) | (df_matches['AwayTeam'] == team_name)]
    
    # If no matches found, return an empty DataFrame
    if len(team_matches) == 0:
        return pd.DataFrame()
    
    # Create a new column to indicate if the team was Home or Away
    team_matches['Venue'] = np.where(team_matches['HomeTeam'] == team_name, 'Home', 'Away')
    
    
    # Set the index to be the date of the match
    team_matches.set_index('Date', inplace=True)
    
    # Return the new DataFrame
    return team_matches

team_dataframes = {}
for team in df['HomeTeam'].unique():
    team_df = create_team_dataframe(team, df_matches)
    if not team_df.empty:
        team_dataframes[team] = team_df
        
for team in df['AwayTeam'].unique():
    team_df = create_team_dataframe(team, df_matches)
    if not team_df.empty and team not in team_dataframes:
        team_dataframes[team] = team_df

all_teams_df = pd.concat(team_dataframes.values(), keys=team_dataframes.keys())

all_teams_df.reset_index(inplace=True)
all_teams_df.set_index(['level_0', 'Date'], inplace=True)

all_teams_df['Team']=np.where(all_teams_df['Venue']=='Home', all_teams_df['HomeTeam'], all_teams_df['AwayTeam'])
col_team=all_teams_df.pop('Team')
all_teams_df.insert(1,'Team',col_team)



team_dfs = {team_name: all_teams_df[all_teams_df['Team'] == team_name] for team_name in all_teams_df['Team'].unique()}
all_teams_df.reset_index(inplace=True)
def transform_row(row):
    if row["Team"] == row["HomeTeam"]:
        return {
            "Date":row["Date"],
            "Team": row["Team"],
            "Opponent": row["AwayTeam"],
            "Venue": row["Venue"],
            "TeamGoal": row["FTHG"],
            "TeamHalfTimeGoal": row["HTHG"],
            "TeamShots": row["HS"],
            "TeamOnTarget": row["HST"],
            "TeamFouls": row["HF"],
            "TeamCleanSheets": int(row["FTAG"] == 0),
            "TeamYellow": row["HY"],
            "TeamRed": row["HR"],
            "TeamWinOdds": row["HomeOdds"],
            "OpponentGoal": row["FTAG"],
            "OpponentGoalHalfTimeGoal": row["HTAG"],
            "OpponentGoalShots": row["AS"],
            "OpponentGoalOnTarget": row["AST"],
            "OpponentGoalFouls": row["AF"],
            "OpponentGoalCleanSheets": int(row["FTHG"] == 0),
            "OpponentGoalYellow": row["AY"],
            "OpponentGoalRed": row["AR"],
            "OpponentGoalWinOdds": row["AwayOdds"],
            "Results": row["Results"],
            "Halftime_result": row["Halftime_result"],
            "Referee": row["Referee"],
            "DrawOdds":row["DrawOdds"]
        }
    elif row["Team"] == row["AwayTeam"]:
        return {
            "Date":row["Date"],
            "Team": row["Team"],
            "Opponent": row["HomeTeam"],
            "Venue": row["Venue"],
            "TeamGoal": row["FTAG"],
            "TeamHalfTimeGoal": row["HTAG"],
            "TeamShots": row["AS"],
            "TeamOnTarget": row["AST"],
            "TeamFouls": row["AF"],
            "TeamCleanSheets": int(row["FTHG"] == 0),
            "TeamYellow": row["AY"],
            "TeamRed": row["AR"],
            "TeamWinOdds": row["AwayOdds"],
            "OpponentGoal": row["FTHG"],
            "OpponentGoalHalfTimeGoal": row["HTHG"],
            "OpponentGoalShots": row["HS"],
            "OpponentGoalOnTarget": row["HST"],
            "OpponentGoalFouls": row["HF"],
            "OpponentGoalCleanSheets": int(row["FTAG"] == 0),
            "OpponentGoalYellow": row["HY"],
            "OpponentGoalRed": row["HR"],
            "OpponentGoalWinOdds": row["HomeOdds"],
            "Results": row["Results"],
            "Halftime_result": row["Halftime_result"],
            "Referee": row["Referee"],
            "DrawOdds":row["DrawOdds"]
        }
    else:
        # This row doesn't involve the target team, so we don't need to transform it
        return row.to_dict()



new_rows = all_teams_df.apply(transform_row, axis=1)
new_df = pd.DataFrame(new_rows.tolist())


all_teams_df.set_index(['level_0', 'Date'], inplace=True)
#new_df.set_index(['Date'], inplace=True)

print(new_df.columns)
Df_form_all=new_df.copy()


# Set the trim percentage
trim_perc = 0.2

# Define a function to calculate the trimmed mean
def rolling_trimmed_mean(series):
    return trim_mean(series, trim_perc)



#FORM LAST 5 games

# Sort the All_teams_df dataframe by date in ascending order
Df_form_all = Df_form_all.sort_values(by='Date')


cols = ['TeamGoal', 'TeamHalfTimeGoal', 'TeamShots', 'TeamOnTarget', 'TeamFouls', 
        'TeamCleanSheets', 'TeamYellow', 'TeamRed', 'TeamWinOdds', 'OpponentGoal', 
        'OpponentGoalHalfTimeGoal', 'OpponentGoalShots', 'OpponentGoalOnTarget', 
        'OpponentGoalFouls', 'OpponentGoalCleanSheets', 'OpponentGoalYellow', 
        'OpponentGoalRed', 'OpponentGoalWinOdds']

# Create a new dataframe to store the form columns
form_last_5_df = pd.DataFrame(columns=['Date', 'Team'] + [f'{col}_Form_last_5' for col in cols] )

# Loop through each team in the dataframe
for team in Df_form_all['Team'].unique():
    # Select only the rows for the current team and sort by date in ascending order
    team_df = Df_form_all.loc[Df_form_all['Team'] == team].sort_values(by='Date')

    # Loop through each column and calculate the rolling mean for the last 5 games and last 3 games vs opponent
    for col in cols:
        # Calculate the rolling mean and shift the values by 1 so that the current game is not included in the calculation
        # team_df[f'{col}_Form'] = team_df[col].rolling(window=5, min_periods=1).mean().shift(1)
        
        team_df[f'{col}_Form_last_5'] = team_df[col].rolling(window=5, min_periods=1).apply(rolling_trimmed_mean, raw=True).shift(1)


    # Add the team dataframe to the form dataframe
    form_last_5_df = pd.concat([form_last_5_df, team_df[['Date', 'Team'] + [f'{col}_Form_last_5' for col in cols]]])
    form_last_5_df = form_last_5_df.fillna(method='bfill')

# Merge the form dataframe with the All_teams_df dataframe on date and team columns
Df_form_all = Df_form_all.merge(form_last_5_df, on=['Date', 'Team'])



#Last 3 against Opponent

cols = ['TeamGoal', 'TeamHalfTimeGoal', 'TeamShots', 'TeamOnTarget', 'TeamFouls', 
        'TeamCleanSheets', 'TeamYellow', 'TeamRed', 'TeamWinOdds', 'OpponentGoal', 
        'OpponentGoalHalfTimeGoal', 'OpponentGoalShots', 'OpponentGoalOnTarget', 
        'OpponentGoalFouls', 'OpponentGoalCleanSheets', 'OpponentGoalYellow', 
        'OpponentGoalRed', 'OpponentGoalWinOdds']

# Create a new dataframe to store the form columns
form_last_3_opponent_df = pd.DataFrame(columns=['Date', 'Team', 'Opponent'] + [f'{col}_vs_Opponent_Form_3' for col in cols])

# Loop through each team in the dataframe
for team in Df_form_all['Team'].unique():
    # Select only the rows for the current team and sort by date in ascending order
    team_df = Df_form_all.loc[Df_form_all['Team'] == team].sort_values(by='Date')

    # Loop through each opponent for the current team and calculate the rolling mean for the last 5 games against that opponent
    for opponent in team_df['Opponent'].unique():
        # Select only the rows for the current opponent and sort by date in ascending order
        opponent_df = team_df.loc[team_df['Opponent'] == opponent].sort_values(by='Date')
        
        # Loop through each column and calculate the rolling mean for the last 5 games against the current opponent
        for col in cols:
            # Calculate the rolling mean and shift the values by 1 so that the current game is not included in the calculation
            opponent_df[f'{col}_vs_Opponent_Form_3'] = opponent_df[col].rolling(window=3, min_periods=1).mean().shift(1)

        # Add the opponent dataframe to the form dataframe
        form_last_3_opponent_df = pd.concat([form_last_3_opponent_df, opponent_df[['Date', 'Team', 'Opponent'] + [f'{col}_vs_Opponent_Form_3' for col in cols]]])
        form_last_3_opponent_df = form_last_3_opponent_df.fillna(method='bfill')

# Merge the form dataframe with the All_teams_df dataframe on date, team, and opponent columns
Df_form_all = Df_form_all.merge(form_last_3_opponent_df, on=['Date', 'Team', 'Opponent'])




#Venue form
cols = ['TeamGoal', 'TeamHalfTimeGoal', 'TeamShots', 'TeamOnTarget', 'TeamFouls', 
        'TeamCleanSheets', 'TeamYellow', 'TeamRed', 'TeamWinOdds', 'OpponentGoal', 
        'OpponentGoalHalfTimeGoal', 'OpponentGoalShots', 'OpponentGoalOnTarget', 
        'OpponentGoalFouls', 'OpponentGoalCleanSheets', 'OpponentGoalYellow', 
        'OpponentGoalRed', 'OpponentGoalWinOdds']

# Create a new dataframe to store the form columns
form_last_5_venue_df = pd.DataFrame(columns=['Date', 'Team', 'Venue'] + [f'{col}_Form_venue_5' for col in cols])

# Loop through each team in the dataframe
for team in Df_form_all['Team'].unique():
    # Select only the rows for the current team and sort by date in ascending order
    team_df = Df_form_all.loc[Df_form_all['Team'] == team].sort_values(by='Date')

    # Loop through each column and calculate the rolling mean for the last 5 games
    for col in cols:
        # Calculate the rolling mean and shift the values by 1 so that the current game is not included in the calculation
        team_df[f'{col}_Form_venue_5'] = team_df.groupby('Venue', group_keys=False)[col].apply(lambda x: x.rolling(window=5, min_periods=1).mean().shift(1))

    # Add the team dataframe to the form dataframe
    form_last_5_venue_df = pd.concat([form_last_5_venue_df, team_df[['Date', 'Team', 'Venue'] + [f'{col}_Form_venue_5' for col in cols]]])
    form_last_5_venue_df = form_last_5_venue_df.fillna(method='bfill')

# Merge the form dataframe with the All_teams_df dataframe on date and team columns
Df_form_all = Df_form_all.merge(form_last_5_venue_df, on=['Date', 'Team', 'Venue'])






test2=Df_form_all[(Df_form_all['Team'].str.contains('Man United') & Df_form_all['Opponent'].str.contains('Liverpool')) |                 (Df_form_all['Opponent'].str.contains('Man United')& Df_form_all['Team'].str.contains('Liverpool'))]

print(Df_form_all.columns)

Df_form_all.to_csv('PremierLeague_mathes_Increase_data.csv')














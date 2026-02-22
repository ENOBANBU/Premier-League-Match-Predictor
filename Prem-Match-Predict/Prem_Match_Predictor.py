import requests
import pandas as pd

# ==========================================
# CONFIGURATION
# ==========================================
api_key = "api_key"  # <--- PASTE YOUR KEY HERE

# CHANGE: We use the 'topscorer' endpoint instead of 'player'
# This allows us to get data by League, without needing a Team ID
base_url = "http://api.isportsapi.com/sport/football/match"

# ==========================================
# FETCH DATA
# ==========================================
print("Fetching Match Results...")

params = {
    "api_key": api_key,
    "leagueId": "1639",  # Premier League
    "seasonId": "5555", # 23/24 Season
} 

try:
    response = requests.get(base_url, params=params)
    data = response.json()

    if data.get('code') == 0:
        print("SUCCESS! Data received.")
        
        # Convert to DataFrame
        # The API puts the list inside a 'data' key
        df = pd.DataFrame(data['data'])
        df=df[df['status'] == 'Finished']
        df=df.sort_values("matchTime",ascending=False)

        teamOne = input("Enter Team 1 Name: ")
        if teamOne == df['Arsenal']:
            print("fetching data for Arsenal")
            team_id = 19
        def calculate_form(team_id, matches):
            points = 0
            gd = 0

            for index, row in matches.iterrows():
                if row['homeTeamId'] == team_id:
                    scored = row['homeScore']
                    conceded = row['awayScore']
                else:
                    scored = row['awayScore']
                    conceded = row['homeScore']

                if scored > conceded:
                    points += 3
                elif scored == conceded:
                    points += 1

                gd += (scored - conceded)

            return points, gd
        




        #teamTwo = input("Enter Team 2 Name: ")





        # Show the data
        if not df.empty:
            # Select clean columns
            # usually: playerName, teamName, goals, assists
            # Line 39 replacement:
            #cols = [c for c in ['playerName', 'teamName', 'score', 'goals', 'assists'] if c in df.columns]
            #print(df[cols].head(10))
            
            # Save it
            df.to_csv("prem_top_scorers.csv", index=False)
            print("\nSaved to 'prem_top_scorers.csv'")
        else:
            print("No players found in the list.")
            
    else:
        print("API Error:", data.get('message'))

except Exception as e:
    print("Connection failed:", e)

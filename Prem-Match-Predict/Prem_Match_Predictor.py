import requests
import pandas as pd

# ==========================================
# CONFIGURATION
# ==========================================
api_key = "DDOSUavdwzi9UFHa"  # <--- PASTE YOUR KEY HERE

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
    "seasonId": "5555", # 25/26 Season
} 

try:
    response = requests.get(base_url, params=params)
    data = response.json()

    if data.get('code') == 0:
        print("SUCCESS! Data received.")
        
        # Convert to DataFrame
        # The API puts the list inside a 'data' key
        df = pd.DataFrame(data['data'])
        #Completed matches only, sorted by most recent
        df=df[df['status'] == 'Finished']
        df=df.sort_values("matchTime",ascending=False)

        def last_n_matches(team_id, df, n=5):
            # Filter matches where the team is either home or away
            team_matches = df[(df['homeTeamId'] == team_id) | (df['awayTeamId'] == team_id)]
            # Sort by match time and get the last n matches
            last_matches = team_matches.sort_values('matchTime', ascending=False).head(n)
            return last_matches
        
        # Function to calculate form (points and goal difference) for a team based on recent matches
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

        teamOne = input("Enter Team 1 Name: ")

        # We check the team name against the DataFrame to find the corresponding team ID. This is a bit clunky, but it works for now. We can optimize this later by creating a mapping of team names to IDs.
        if teamOne == df['Arsenal'].iloc[0]:
            print("fetching data for Arsenal")
            team_id = 19
            last_n_matches(team_id, df, n=5)
            calculate_form(team_id, df)
        elif teamOne == df['AFC Bournemouth'].iloc[0]:
            print("fetching data for AFC Bournemouth")
            team_id = 348    
            last_n_matches(team_id, df, n=5)
            calculate_form(team_id, df)
        elif teamOne == df['Aston Villa'].iloc[0]:      
            print("fetching data for Aston Villa")
            team_id = 20    
            last_n_matches(team_id, df, n=5)
            calculate_form(team_id, df)
        elif teamOne == df['Brentford'].iloc[0]:
            print("fetching data for Brentford")
            team_id = 365    
            last_n_matches(team_id, df)
            calculate_form(team_id, df)
        elif teamOne == df['Brighton & Hove Albion'].iloc[0]:
            print("fetching data for Brighton & Hove Albion")
            team_id = 60    
            last_n_matches(team_id, df, n=5)
            calculate_form(team_id, df)
        elif teamOne == df['Burnley'].iloc[0]:
            print("fetching data for Burnley")
            team_id = 46    
            last_n_matches(team_id, df, n=5)
            calculate_form(team_id, df)
        elif teamOne == df['Chelsea'].iloc[0]:
            print("fetching data for Chelsea")
            team_id = 24    
            last_n_matches(team_id, df, n=5)
            calculate_form(team_id, df)
        elif teamOne == df['Crystal Palace']:
            print("fetching data for Crystal Palace")
            team_id = 35    
            last_n_matches(team_id, df, n=5)
            calculate_form(team_id, df)
        elif teamOne == df['Everton']:
            print("fetching data for Everton")
            team_id = 31  
            last_n_matches(team_id, df, n=5)  
            calculate_form(team_id, df)
        elif teamOne == df['Fulham']:
            print("fetching data for Fulham")
            team_id = 29    
            last_n_matches(team_id, df, n=5)
            calculate_form(team_id, df)
        elif teamOne == df['Leeds United']:
            print("fetching data for Leeds United")
            team_id = 56    
            last_n_matches(team_id, df, n=5)
            calculate_form(team_id, df)
        elif teamOne == df['Liverpool']:
            print("fetching data for Liverpool")
            team_id = 25    
            last_n_matches(team_id, df, n=5)
            calculate_form(team_id, df) 
        elif teamOne == df['Manchester City']:
            print("fetching data for Manchester City")
            team_id = 26    
            last_n_matches(team_id, df, n=5)
            calculate_form(team_id, df)
        elif teamOne == df['Manchester United']:
            print("fetching data for Manchester United")
            team_id = 27    
            last_n_matches(team_id, df, n=5)
            calculate_form(team_id, df)
        elif teamOne == df['Newcastle United']: 
            print("fetching data for Newcastle United")
            team_id = 28    
            last_n_matches(team_id, df, n=5)
            calculate_form(team_id, df)
        elif teamOne == df['Nottingham Forest']:
            print("fetching data for Nottingham Forest")
            team_id = 49    
            last_n_matches(team_id, df, n=5)
            calculate_form(team_id, df)
        elif teamOne == df['Sunderland A.F.C']:
            print("fetching data for Sunderland A.F.C")
            team_id = 65    
            last_n_matches(team_id, df, n=5)
            calculate_form(team_id, df)
        elif teamOne == df['Tottenham']:
            print("fetching data for Tottenham")
            team_id = 33
            last_n_matches(team_id, df, n=5)    
            calculate_form(team_id, df)
        elif teamOne == df['West Ham United']:
            print("fetching data for West Ham United")
            team_id = 62    
            last_n_matches(team_id, df, n=5)
            calculate_form(team_id, df)
        elif teamOne == df['Wolverhampton Wanderers']:
            print("fetching data for Wolverhampton Wanderers")
            team_id = 52    
            last_n_matches(team_id, df, n=5)
            calculate_form(team_id, df)
        else:
            print("Team not found. Please check the name and try again.")

        teamTwo = input("Enter Team 2 Name: ")
        
        # We repeat the same process for Team 2, but we can optimize this by creating a mapping of team names to IDs instead of using multiple if-elif statements. For now, we'll keep it simple and use the same structure.
        if teamTwo == df['Arsenal']:
            print("fetching data for Arsenal")
            team_id = 19
            last_n_matches(team_id, df, n=5)
            calculate_form(team_id, df)
        elif teamTwo == df['AFC Bournemouth']:
            print("fetching data for AFC Bournemouth")
            team_id = 348    
            last_n_matches(team_id, df, n=5)
            calculate_form(team_id, df)
        elif teamTwo == df['Aston Villa']:      
            print("fetching data for Aston Villa")
            team_id = 20    
            last_n_matches(team_id, df, n=5)
            calculate_form(team_id, df)
        elif teamTwo == df['Brentford']:
            print("fetching data for Brentford")
            team_id = 365    
            last_n_matches(team_id, df, n=5)
            calculate_form(team_id, df)
        elif teamTwo == df['Brighton & Hove Albion']:
            print("fetching data for Brighton & Hove Albion")
            team_id = 60    
            last_n_matches(team_id, df, n=5)
            calculate_form(team_id, df)
        elif teamTwo == df['Burnley']:
            print("fetching data for Burnley")
            team_id = 46    
            last_n_matches(team_id, df, n=5)
            calculate_form(team_id, df)
        elif teamTwo == df['Chelsea']:
            print("fetching data for Chelsea")
            team_id = 24    
            last_n_matches(team_id, df, n=5)
            calculate_form(team_id, df)
        elif teamTwo == df['Crystal Palace']:
            print("fetching data for Crystal Palace")
            team_id = 35    
            last_n_matches(team_id, df, n=5)
            calculate_form(team_id, df)
        elif teamTwo == df['Everton']:
            print("fetching data for Everton")
            team_id = 31    
            last_n_matches(team_id, df, n=5)
            calculate_form(team_id, df)
        elif teamTwo == df['Fulham']:
            print("fetching data for Fulham")
            team_id = 29    
            last_n_matches(team_id, df, n=5)
            calculate_form(team_id, df)
        elif teamTwo == df['Leeds United']:
            print("fetching data for Leeds United")
            team_id = 56    
            last_n_matches(team_id, df, n=5)
            calculate_form(team_id, df)
        elif teamTwo == df['Liverpool']:
            print("fetching data for Liverpool")
            team_id = 25    
            last_n_matches(team_id, df, n=5)
            calculate_form(team_id, df) 
        elif teamTwo == df['Manchester City']:
            print("fetching data for Manchester City")
            team_id = 26    
            last_n_matches(team_id, df, n=5)
            calculate_form(team_id, df)
        elif teamTwo == df['Manchester United']:
            print("fetching data for Manchester United")
            team_id = 27    
            last_n_matches(team_id, df, n=5)
            calculate_form(team_id, df)
        elif teamTwo == df['Newcastle United']: 
            print("fetching data for Newcastle United")
            team_id = 28    
            last_n_matches(team_id, df, n=5)
            calculate_form(team_id, df)
        elif teamTwo == df['Nottingham Forest']:
            print("fetching data for Nottingham Forest")
            team_id = 49    
            last_n_matches(team_id, df, n=5)
            calculate_form(team_id, df)
        elif teamTwo == df['Sunderland A.F.C']:
            print("fetching data for Sunderland A.F.C")
            team_id = 65    
            last_n_matches(team_id, df, n=5)
            calculate_form(team_id, df)
        elif teamTwo == df['Tottenham']:
            print("fetching data for Tottenham")
            team_id = 33
            last_n_matches(team_id, df, n=5)
            calculate_form(team_id, df)
        elif teamTwo == df['West Ham United']:
            print("fetching data for West Ham United")
            team_id = 62    
            last_n_matches(team_id, df, n=5)
            calculate_form(team_id, df)
        elif teamTwo == df['Wolverhampton Wanderers']:
            print("fetching data for Wolverhampton Wanderers")
            team_id = 52    
            last_n_matches(team_id, df, n=5)
            calculate_form(team_id, df)
        else:
            print("Team not found. Please check the name and try again.")

    #make a head to head that compare each teams last 5 matches and calculate the points and goal difference for each team. This will give us an idea of the current form of each team, which can be a useful predictor for the match outcome.

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

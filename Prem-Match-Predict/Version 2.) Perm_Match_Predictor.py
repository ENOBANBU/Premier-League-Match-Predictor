import requests
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
#Same idea of Code, though, more efficient using Machine Learning and RandomForestClassification
API_KEY = "YOUR_KEY_HERE"
BASE_URL = "http://api.isportsapi.com/sport/football/match"

# Mapping team names to their API IDs
TEAM_MAP = {
    "Arsenal": 19, "AFC Bournemouth": 348, "Aston Villa": 20, "Brentford": 365,
    "Brighton & Hove Albion": 60, "Burnley": 46, "Chelsea": 24, "Crystal Palace": 35,
    "Everton": 31, "Fulham": 29, "Leeds United": 56, "Liverpool": 25,
    "Manchester City": 26, "Manchester United": 27, "Newcastle United": 28,
    "Nottingham Forest": 49, "Sunderland A.F.C": 65, "Tottenham": 33,
    "West Ham United": 62, "Wolverhampton Wanderers": 52
}

# 2. HELPER FUNCTIONS
def last_n_matches(team_id, df, n=5):
    team_matches = df[(df['homeTeamId'] == team_id) | (df['awayTeamId'] == team_id)]
    return team_matches.sort_values('matchTime', ascending=False).head(n)

def calculate_form(team_id, matches):
    points, gd = 0, 0
    for _, row in matches.iterrows():
        if row['homeTeamId'] == team_id:
            scored, conceded = row['homeScore'], row['awayScore']
        else:
            scored, conceded = row['awayScore'], row['homeScore']
        
        if scored > conceded: points += 3
        elif scored == conceded: points += 1
        gd += (scored - conceded)
    return points, gd

# 3. DATA FETCHING
print("Fetching Match Results...")
params = {"api_key": API_KEY, "leagueId": "1639", "seasonId": "5555"}

try:
    response = requests.get(BASE_URL, params=params)
    data = response.json()

    if data.get('code') != 0:
        print("API Error:", data.get('message'))
        exit()

    df = pd.DataFrame(data['data'])
    df = df[df['status'] == 'Finished']
    df['matchTime'] = pd.to_numeric(df['matchTime']) # Ensure time is numeric for comparison
    df = df.sort_values("matchTime", ascending=False)

    # 4. ML DATA PREPARATION
    features, targets = [], []

    for _, row in df.iterrows():
        past_matches = df[df['matchTime'] < row['matchTime']]
        h_m = last_n_matches(row['homeTeamId'], past_matches)
        a_m = last_n_matches(row['awayTeamId'], past_matches)

        if len(h_m) >= 3 and len(a_m) >= 3:
            h_pts, h_gd = calculate_form(row['homeTeamId'], h_m)
            a_pts, a_gd = calculate_form(row['awayTeamId'], a_m)
            
            features.append([h_pts, h_gd, a_pts, a_gd])
            
            if row['homeScore'] > row['awayScore']: targets.append(1) # Home Win
            elif row['homeScore'] == row['awayScore']: targets.append(0) # Draw
            else: targets.append(2) # Away Win

    # 5. TRAINING
    X_train, X_test, y_train, y_test = train_test_split(features, targets, test_size=0.2)
    model = RandomForestClassifier(n_estimators=100)
    model.fit(X_train, y_train)
    print(f"Model Trained. Accuracy: {model.score(X_test, y_test) * 100:.2f}%")

    # 6. USER INTERFACE (PREDICTION)
    print("\n--- PREMIER LEAGUE PREDICTOR ---")
    t1_name = input("Enter Home Team: ")
    t2_name = input("Enter Away Team: ")

    if t1_name in TEAM_MAP and t2_name in TEAM_MAP:
        h_id, a_id = TEAM_MAP[t1_name], TEAM_MAP[t2_name]
        
        h_pts, h_gd = calculate_form(h_id, last_n_matches(h_id, df))
        a_pts, a_gd = calculate_form(a_id, last_n_matches(a_id, df))
        
        pred = model.predict([[h_pts, h_gd, a_pts, a_gd]])
        res_map = {1: "HOME WIN", 0: "DRAW", 2: "AWAY WIN"}
        
        print(f"\nPREDICTION for {t1_name} vs {t2_name}: {res_map[pred[0]]}")
    else:
        print("One of the teams was not found. Check spelling!")

except Exception as e:
    print("An error occurred:", e)

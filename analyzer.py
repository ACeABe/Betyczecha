import pandas as pd
import os
import matplotlib.pyplot as plt
from datetime import datetime

DATA_PATH = 'data/matches.csv'
PICKS_DIR = 'data/picks'

def fetch_latest_matches():
    os.makedirs('data', exist_ok=True)
    matches = [
        {"date": "2025-05-27", "team_home": "Team A", "team_away": "Team G", "result": "W", "odds": 1.85},
        {"date": "2025-05-21", "team_home": "Team A", "team_away": "Team H", "result": "L", "odds": 2.10},
    ]
    df_new = pd.DataFrame(matches)
    if os.path.exists(DATA_PATH):
        df_old = pd.read_csv(DATA_PATH)
        df_all = pd.concat([df_new, df_old], ignore_index=True).drop_duplicates()
    else:
        df_all = df_new
    df_all.to_csv(DATA_PATH, index=False)

def analyze_matches():
    try:
        df = pd.read_csv(DATA_PATH)
        df = df.sort_values('date', ascending=False)
        team = df.iloc[0]['team_home']
        recent = df[df['team_home'] == team].head(5)
        wins = (recent['result'] == 'W').sum()
        avg_odds = recent['odds'].mean()
        if wins >= 3:
            return f"Rekomendacja: {team} w dobrej formie (wygrane: {wins}/5, średnie kursy: {avg_odds:.2f})"
        else:
            return f"Odradzamy typowanie na {team} (tylko {wins}/5 zwycięstw, średnie kursy: {avg_odds:.2f})"
    except Exception as e:
        return f"Błąd analizy: {str(e)}"

def get_recent_matches_plot():
    try:
        df = pd.read_csv(DATA_PATH)
        team = df.iloc[0]['team_home']
        recent = df[df['team_home'] == team].head(5)
        results = recent['result'].map({'W': 1, 'L': 0})
        dates = pd.to_datetime(recent['date']).dt.strftime('%d.%m')
        plt.figure(figsize=(6, 3))
        plt.plot(dates[::-1], results[::-1], marker='o', linestyle='-', color='blue')
        plt.ylim(-0.1, 1.1)
        plt.yticks([0, 1], ['Porażka', 'Wygrana'])
        plt.title(f'Forma drużyny: {team}')
        plt.tight_layout()
        os.makedirs('static', exist_ok=True)
        plt.savefig('static/form_chart.png')
        plt.close()
    except Exception as e:
        print(f"Błąd tworzenia wykresu: {e}")

def save_user_pick(username, team, date, odds, pick):
    os.makedirs(PICKS_DIR, exist_ok=True)
    filepath = os.path.join(PICKS_DIR, f'{username}_picks.csv')
    new_entry = pd.DataFrame([{'user': username, 'date': date, 'team': team, 'odds': odds, 'pick': pick}])
    if os.path.exists(filepath):
        df = pd.read_csv(filepath)
        df = pd.concat([df, new_entry], ignore_index=True)
    else:
        df = new_entry
    df.to_csv(filepath, index=False)

def export_user_picks(username):
    filepath = os.path.join(PICKS_DIR, f'{username}_picks.csv')
    export_path = os.path.join(PICKS_DIR, f'{username}_export.xlsx')
    if os.path.exists(filepath):
        df = pd.read_csv(filepath)
        df.to_excel(export_path, index=False)
    return export_path

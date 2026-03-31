# mlb_2026_game_logs.py
import statsapi
import pandas as pd
from datetime import datetime

print("🚀 925Sports - Starting full 2026 MLB game logs pull...")

all_rows = []

# Get all 30 MLB teams for 2026
teams = statsapi.get('teams', {'sportId': 1, 'season': 2026})['teams']

for team in teams:
    team_id = team['id']
    team_name = team['name']
    
    print(f"Processing team: {team_name}")
    
    # Get roster
    roster = statsapi.get('team_roster', {'teamId': team_id, 'season': 2026})['roster']
    
    for player in roster:
        player_id = player['person']['id']
        player_name = player['person']['fullName']
        
        # Hitting game logs
        try:
            hitting_data = statsapi.player_stats(player_id, group="hitting", type="gameLog", season=2026)
            splits = hitting_data.get('stats', [{}])[0].get('splits', [])
            for game in splits:
                stat = game.get('stat', {})
                all_rows.append({
                    'Player': player_name,
                    'Team': team_name,
                    'Type': 'Hitting',
                    'Date': game.get('date'),
                    'Opponent': game.get('opponent', {}).get('abbreviation', 'N/A'),
                    'AB': stat.get('atBats'),
                    'R': stat.get('runs'),
                    'H': stat.get('hits'),
                    '2B': stat.get('doubles'),
                    '3B': stat.get('triples'),
                    'HR': stat.get('homeRuns'),
                    'RBI': stat.get('rbi'),
                    'BB': stat.get('baseOnBalls'),
                    'SO': stat.get('strikeOuts'),
                    'SB': stat.get('stolenBases'),
                    'AVG': stat.get('avg'),
                    'OBP': stat.get('obp'),
                    'SLG': stat.get('slg'),
                    'OPS': stat.get('ops'),
                })
        except:
            pass

        # Pitching game logs
        try:
            pitching_data = statsapi.player_stats(player_id, group="pitching", type="gameLog", season=2026)
            splits = pitching_data.get('stats', [{}])[0].get('splits', [])
            for game in splits:
                stat = game.get('stat', {})
                all_rows.append({
                    'Player': player_name,
                    'Team': team_name,
                    'Type': 'Pitching',
                    'Date': game.get('date'),
                    'Opponent': game.get('opponent', {}).get('abbreviation', 'N/A'),
                    'IP': stat.get('inningsPitched'),
                    'H': stat.get('hits'),
                    'R': stat.get('runs'),
                    'ER': stat.get('earnedRuns'),
                    'BB': stat.get('baseOnBalls'),
                    'SO': stat.get('strikeOuts'),
                    'HR': stat.get('homeRuns'),
                    'ERA': stat.get('era'),
                    'WHIP': stat.get('whip'),
                })
        except:
            pass

# Create DataFrame, sort newest games first, and save
df = pd.DataFrame(all_rows)

if not df.empty and 'Date' in df.columns:
    df = df.sort_values(by=['Date', 'Player'], ascending=[False, True])

filename = f"mlb_2026_game_logs_{datetime.now().strftime('%Y%m%d')}.csv"
df.to_csv(filename, index=False)

print(f"✅ Done! Saved {len(df):,} rows to {filename}")
print(f"Total unique players: {len(df['Player'].unique()) if not df.empty else 0}")

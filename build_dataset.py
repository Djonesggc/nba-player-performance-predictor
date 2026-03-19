from nba_api.stats.static import players
from nba_api.stats.endpoints import playergamelog
import pandas as pd
import time

player_names = [
    "LeBron James",
    "Stephen Curry",
    "Nikola Jokic",
    "Jayson Tatum",
    "Luka Doncic"
]

season = "2024-25"
all_rows = []

for player_name in player_names:
    try:
        found_players = players.find_players_by_full_name(player_name)
        if not found_players:
            print(f"Player not found: {player_name}")
            continue

        player_id = found_players[0]["id"]
        print(f"Pulling data for {player_name}...")

        gamelog = playergamelog.PlayerGameLog(
            player_id=player_id,
            season=season,
            season_type_all_star="Regular Season"
        )

        df = gamelog.get_data_frames()[0]

        if df.empty or len(df) < 6:
            print(f"Not enough data for {player_name}")
            continue

        df = df.copy()

        df["HOME"] = df["MATCHUP"].apply(lambda x: 0 if "@" in x else 1)

        for i in range(5, len(df)):
            previous_5 = df.iloc[i-5:i]

            row = {
                "player_name": player_name,
                "opponent": df.iloc[i]["MATCHUP"].split()[-1],
                "home": df.iloc[i]["HOME"],
                "minutes": float(df.iloc[i]["MIN"]),
                "avg_points_last5": previous_5["PTS"].mean(),
                "avg_rebounds_last5": previous_5["REB"].mean(),
                "avg_assists_last5": previous_5["AST"].mean(),
                "points": df.iloc[i]["PTS"],
                "rebounds": df.iloc[i]["REB"],
                "assists": df.iloc[i]["AST"]
            }

            all_rows.append(row)

        time.sleep(1)

    except Exception as e:
        print(f"Error with {player_name}: {e}")

dataset = pd.DataFrame(all_rows)
dataset.to_csv("nba_pra_data.csv", index=False)

print("Dataset saved as nba_pra_data.csv")
print(dataset.head())
print(f"Total rows: {len(dataset)}")
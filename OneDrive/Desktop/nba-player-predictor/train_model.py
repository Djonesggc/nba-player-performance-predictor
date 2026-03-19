import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib
import math

# Load dataset
df = pd.read_csv("nba_pra_data.csv")

# Features
X = df[["home", "minutes", "avg_points_last5", "avg_rebounds_last5", "avg_assists_last5"]]

# Targets
y_points = df["points"]
y_rebounds = df["rebounds"]
y_assists = df["assists"]

# Split data
X_train, X_test, y_points_train, y_points_test = train_test_split(
    X, y_points, test_size=0.2, random_state=42
)

_, _, y_rebounds_train, y_rebounds_test = train_test_split(
    X, y_rebounds, test_size=0.2, random_state=42
)

_, _, y_assists_train, y_assists_test = train_test_split(
    X, y_assists, test_size=0.2, random_state=42
)

# Train 3 models
points_model = RandomForestRegressor(random_state=42)
rebounds_model = RandomForestRegressor(random_state=42)
assists_model = RandomForestRegressor(random_state=42)

points_model.fit(X_train, y_points_train)
rebounds_model.fit(X_train, y_rebounds_train)
assists_model.fit(X_train, y_assists_train)

# Predictions
points_preds = points_model.predict(X_test)
rebounds_preds = rebounds_model.predict(X_test)
assists_preds = assists_model.predict(X_test)

# Evaluation function
def print_metrics(name, y_true, y_pred):
    mae = mean_absolute_error(y_true, y_pred)
    rmse = math.sqrt(mean_squared_error(y_true, y_pred))
    r2 = r2_score(y_true, y_pred)

    print(f"{name} Model")
    print("MAE:", round(mae, 2))
    print("RMSE:", round(rmse, 2))
    print("R²:", round(r2, 2))
    print()

print_metrics("Points", y_points_test, points_preds)
print_metrics("Rebounds", y_rebounds_test, rebounds_preds)
print_metrics("Assists", y_assists_test, assists_preds)

# Save models
joblib.dump(points_model, "points_model.pkl")
joblib.dump(rebounds_model, "rebounds_model.pkl")
joblib.dump(assists_model, "assists_model.pkl")

print("Models saved successfully.")
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import joblib
import matplotlib.pyplot as plt


# Load dataset
df = pd.read_csv("final_gold_data.csv")


# Features & target
X = df[['SPX', 'USO', 'SLV', 'EUR_USD']]
y = df['GLD']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Scaling
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Save scaler
joblib.dump(scaler, "scaler.joblib")

# Model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train_scaled, y_train)

# Prediction
y_pred = model.predict(X_test_scaled)

# Evaluation
print("MAE:", mean_absolute_error(y_test, y_pred))
print("R2 Score:", r2_score(y_test, y_pred))
print(df.shape)
print(df.select_dtypes(include=['number']).corr())
# Save model
joblib.dump(model, "model.joblib")


#feature importance
importance = model.feature_importances_
features = X.columns

plt.bar(features, importance)
plt.title("Feature Importance")
plt.show()
import os
os.environ['OMP_NUM_THREADS'] = '1'

import json
import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import Ridge, LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score, mean_squared_error

def train_and_export():
    print("Loading historical dataset final_gold_data.csv...")
    df = pd.read_csv("final_gold_data.csv")
    
    # Feature matrix and target
    feature_cols = ['SPX', 'USO', 'SLV', 'EUR_USD']
    X = df[feature_cols]
    y = df['GLD']

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.15, random_state=42
    )

    # Standard Scaler
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # 1. Primary Model: Random Forest Regressor
    print("Training Random Forest Regressor...")
    rf_model = RandomForestRegressor(n_estimators=100, max_depth=16, random_state=42, n_jobs=1)
    rf_model.fit(X_train_scaled, y_train)

    rf_pred = rf_model.predict(X_test_scaled)
    rf_mae = mean_absolute_error(y_test, rf_pred)
    rf_r2 = r2_score(y_test, rf_pred)
    rf_rmse = np.sqrt(mean_squared_error(y_test, rf_pred))
    print(f"Random Forest -> R2: {rf_r2:.4f}, MAE: {rf_mae:.2f}, RMSE: {rf_rmse:.2f}")

    # 2. Ensemble Model 2: Ridge Regression
    print("Training Ridge Regression for consensus...")
    ridge_model = Ridge(alpha=1.0)
    ridge_model.fit(X_train_scaled, y_train)
    ridge_pred = ridge_model.predict(X_test_scaled)
    ridge_r2 = r2_score(y_test, ridge_pred)

    # 3. Linear Regression for pure client-side fast coefficients
    lin_model = LinearRegression()
    lin_model.fit(X_train_scaled, y_train)

    # Save scaler and models with compression
    joblib.dump(scaler, "scaler.joblib", compress=3)
    joblib.dump(rf_model, "model.joblib", compress=3)
    print("Saved scaler.joblib and model.joblib (compressed).")

    # Feature importances
    importances = rf_model.feature_importances_.tolist()
    feature_importance_dict = {col: round(imp * 100, 2) for col, imp in zip(feature_cols, importances)}

    # Correlation Matrix
    numeric_df = df.select_dtypes(include=[np.number])
    corr_matrix = numeric_df.corr().round(4).to_dict()

    # Latest record for baseline
    latest_row = df.iloc[-1].to_dict()

    # Export Model Metadata for Offline Client-side & API consensus
    meta = {
        "model_name": "Antigravity AI Gold Intelligence Ensemble",
        "version": "2.0.0",
        "features": feature_cols,
        "scaler": {
            "mean": scaler.mean_.tolist(),
            "scale": scaler.scale_.tolist(),
            "var": scaler.var_.tolist()
        },
        "metrics": {
            "random_forest": {
                "r2_score": round(rf_r2, 4),
                "mae": round(rf_mae, 2),
                "rmse": round(rf_rmse, 2),
                "accuracy_pct": round(rf_r2 * 100, 2)
            },
            "ridge": {
                "r2_score": round(ridge_r2, 4)
            }
        },
        "feature_importance_pct": feature_importance_dict,
        "offline_linear_weights": {
            "coef": lin_model.coef_.tolist(),
            "intercept": float(lin_model.intercept_)
        },
        "correlation_matrix": corr_matrix,
        "dataset_summary": {
            "total_records": len(df),
            "start_date": str(df['Date'].iloc[0]),
            "end_date": str(df['Date'].iloc[-1]),
            "gld_min": float(df['GLD'].min()),
            "gld_max": float(df['GLD'].max()),
            "gld_mean": round(float(df['GLD'].mean()), 2)
        },
        "latest_baseline": {
            "Date": str(latest_row.get("Date", "")),
            "GLD": float(latest_row.get("GLD", 4629.9)),
            "SPX": float(latest_row.get("SPX", 7230.1)),
            "USO": float(latest_row.get("USO", 101.9)),
            "SLV": float(latest_row.get("SLV", 75.9)),
            "EUR_USD": float(latest_row.get("EUR_USD", 1.17))
        }
    }

    with open("model_meta.json", "w") as f:
        json.dump(meta, f, indent=2)

    print("Exported model_meta.json successfully!")
    return meta

if __name__ == "__main__":
    train_and_export()
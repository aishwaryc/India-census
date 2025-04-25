import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.multioutput import MultiOutputRegressor
from sklearn.ensemble import RandomForestRegressor
import joblib
import os

# Load original census dataset
csv_path = 'models/india-districts-census-2011.csv'
if not os.path.exists(csv_path):
    raise FileNotFoundError(f"CSV not found: {csv_path}")
df = pd.read_csv(csv_path)

# Basic cleaning
df.drop_duplicates(inplace=True)
required_columns = ['Population', 'Male', 'Female']
for col in ['Urban_population', 'Rural_population']:
    if col not in df.columns:
        df[col] = df['Population'] * 0.5  # Fill missing with 50/50 split assumption
required_columns += ['Urban_population', 'Rural_population']
df = df.dropna(subset=required_columns)

# Create derived features
df['Population_Under_18'] = df['Population'] * 0.35  # mock assumption

# Aggregate metrics
metrics_df = pd.DataFrame({
    'Total_Population': [df['Population'].sum()],
    'Male_Population': [df['Male'].sum()],
    'Female_Population': [df['Female'].sum()],
    'Urban_Population': [df['Urban_population'].sum()],
    'Rural_Population': [df['Rural_population'].sum()],
    'Population_Under_18': [df['Population_Under_18'].sum()]
}, index=[2011])

# Prepare training data (extrapolate to more years)
years = np.arange(2001, 2031)
years_df = pd.DataFrame(index=years)
for col in metrics_df.columns:
    slope = 0.012  # mock growth rate
    base = metrics_df.loc[2011, col]
    years_df[col] = base * (1 + slope) ** (years - 2011)

# Train model
X = years_df.index.values.reshape(-1,1)
Y = years_df.values
scaler = StandardScaler().fit(X)
X_scaled = scaler.transform(X)
model = MultiOutputRegressor(RandomForestRegressor(random_state=42)).fit(X_scaled, Y)

# Save everything
os.makedirs('models', exist_ok=True)
joblib.dump(model, 'models/pop_model.joblib')
joblib.dump(scaler, 'models/scaler.joblib')
years_df.to_pickle('models/yearly_metrics.pkl')
print('Model, scaler, and yearly metrics saved.')
import pandas as pd
import numpy as np
import statsmodels.api as sm

# Read the CSV file
df = pd.read_csv('brief_search_for_conf_meta_analysis_lidar_to_sar_optical.csv')

# Filter out rows where R² is 'Not reported' or 'Not explicitly stated'
df = df[~df['R²'].isin(['Not reported', 'Not explicitly stated'])]

# Convert R² to float
df['R²'] = df['R²'].astype(float)

# Transform R² to Fisher’s Z scores
df['z'] = 0.5 * np.log((1 + df['R²']) / (1 - df['R²']))

# Assume variance for Z scores (since sample sizes are not available, use a constant)
# In practice, var_z = 1 / (n - 3), but here we use 0.1 as placeholder
df['var_z'] = 0.1

# Create method dummy: 1 for Machine Learning, 0 for Regression
df['method_ml'] = df['Method'].apply(lambda x: 1 if 'regression' not in x.lower() else 0)

# Create dummies for Forest Type
forest_dummies = pd.get_dummies(df['Forest Type'], prefix='forest', drop_first=True)

# Combine moderators
moderators = pd.concat([df[['method_ml']], forest_dummies], axis=1)

# Add constant for intercept
X = sm.add_constant(moderators).astype(float)

# Fit weighted least squares (fixed effects approximation)
weights = 1 / df['var_z'].values
model = sm.WLS(df['z'].values, X, weights=weights)
result = model.fit()

# Calculate Q statistic for heterogeneity
residuals = result.resid
Q = np.sum(weights * residuals**2)
df_q = len(df) - len(result.params)
I2 = max(0, (Q - df_q) / Q * 100) if Q > 0 else 0

# Print results
print("Meta-Regression Results (Fixed Effects Approximation):")
print(result.summary())
print(f"\nHeterogeneity:")
print(f"Q statistic: {Q:.4f}")
print(f"Degrees of freedom: {df_q}")
print(f"I²: {I2:.2f}%")

# Interpretation
print("\nInterpretation:")
print("Reported R² values were transformed to Fisher’s Z scores to stabilize variance and enable cross-study comparisons.")
print("A weighted least squares model was employed as an approximation to account for heterogeneity.")
print("The analysis compares the performance of machine learning-based models versus traditional regression approaches, as well as differences in model accuracy across forest types.")
print("Positive coefficient for method_ml indicates Machine Learning has higher R² (in Z scale).")
print("Coefficients for forest types are relative to the reference category.")
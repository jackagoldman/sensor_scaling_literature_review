import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Set style to mimic ggplot
sns.set_style('whitegrid')
sns.set_palette('Set2')

# Read the CSV file
df = pd.read_csv('brief_search_for_conf_meta_analysis_lidar_to_sar_optical.csv')

# Filter out rows where R² is 'Not reported' or 'Not explicitly stated'
df = df[~df['R²'].isin(['Not reported', 'Not explicitly stated'])]

# Convert R² to float
df['R²'] = df['R²'].astype(float)

# Group method into 'Regression' or 'Machine learning'
df['method_group'] = df['Method'].apply(lambda x: 'Regression' if 'regression' in x.lower() else 'Machine learning')

# Function to categorize target source
def categorize_target(target):
    has_sar = 'SAR' in target
    has_landsat = 'Landsat' in target
    if has_sar and has_landsat:
        return 'Landsat/SAR'
    elif has_sar:
        return 'SAR'
    elif has_landsat:
        return 'Landsat'
    else:
        return 'Other'

df['target_source_group'] = df['Target Source'].apply(categorize_target)

# Remove rows where target_source_group is 'Other'
df = df[df['target_source_group'] != 'Other']

# Create boxplots
fig, axes = plt.subplots(1, 2, figsize=(10, 5))

# Boxplot 1: R² by target source
sns.boxplot(data=df, x='target_source_group', y='R²', hue='target_source_group', ax=axes[0], palette='Set2', legend=False)
axes[0].set_title('R² by Target Source')
axes[0].set_xlabel('Target Source')
axes[0].text(-0.1, 1.05, 'a)', transform=axes[0].transAxes, fontsize=12, fontweight='bold', va='top', ha='right')

# Add sample sizes for target source
categories_ts = sorted(df['target_source_group'].unique())
for i, cat in enumerate(categories_ts):
    subset = df[df['target_source_group'] == cat]
    n = len(subset)
    y_pos = subset['R²'].max() + 0.05
    axes[0].text(i, y_pos, f'n={n}', ha='center', va='bottom', fontsize=10)

# Adjust ylim to include sample size text
max_r2 = df['R²'].max()
axes[0].set_ylim(axes[0].get_ylim()[0], max_r2 + 0.1)

# Boxplot 2: R² by method
sns.boxplot(data=df, x='method_group', y='R²', hue='method_group', ax=axes[1], palette='Set2', legend=False)
axes[1].set_title('R² by Method')
axes[1].set_xlabel('Method')
axes[1].text(-0.1, 1.05, 'b)', transform=axes[1].transAxes, fontsize=12, fontweight='bold', va='top', ha='right')

# Add sample sizes for method
categories_m = sorted(df['method_group'].unique())
for i, cat in enumerate(categories_m):
    subset = df[df['method_group'] == cat]
    n = len(subset)
    y_pos = subset['R²'].max() + 0.05
    axes[1].text(i, y_pos, f'n={n}', ha='center', va='bottom', fontsize=10)

# Adjust ylim to include sample size text
axes[1].set_ylim(axes[1].get_ylim()[0], max_r2 + 0.1)

plt.tight_layout()
plt.savefig('boxplots.png', dpi=300)
plt.show()
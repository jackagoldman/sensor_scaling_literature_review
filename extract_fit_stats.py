import pandas as pd
import re

# Read the Web of Science data file
df = pd.read_csv('wos_search_refined_11-16-25.txt', sep='\t')

# Keywords for forest types
forest_keywords = ['boreal', 'temperate', 'coniferous']

# Filter rows where the abstract contains any of the forest keywords (case-insensitive) but NOT 'tropical'
contains_forest = df['AB'].str.contains('|'.join(forest_keywords), case=False, na=False)
no_tropical = ~df['AB'].str.contains('tropical', case=False, na=False)
filtered_articles = df[contains_forest & no_tropical]

# Fit statistics patterns
patterns = {
    'R²': r'(?:R-2|R2|R[²])\s*[:=]\s*([0-9.]+)',
    'RMSE': r'RMSE\s*[:=]\s*([0-9.]+)',
    'MAE': r'MAE\s*[:=]\s*([0-9.]+)',
    'Correlation': r'correlation\s*[:=]\s*([0-9.]+)',
    'Accuracy': r'accuracy\s*[:=]\s*([0-9.]+)',
    'Precision': r'precision\s*[:=]\s*([0-9.]+)',
    'Recall': r'recall\s*[:=]\s*([0-9.]+)',
    'F1': r'F1\s*[:=]\s*([0-9.]+)'
}

# Function to extract fit statistics from abstract
def extract_fit_stats(abstract):
    if pd.isna(abstract):
        return {}
    stats = {}
    for stat, pattern in patterns.items():
        matches = re.findall(pattern, abstract, re.IGNORECASE)
        if matches:
            stats[stat] = matches  # list of values
    return stats

# Model types keywords
model_keywords = [
    'random forest', 'support vector machine', 'svm', 'neural network', 'linear regression',
    'k-nearest neighbor', 'knn', 'k-nn', 'gradient boosting', 'decision tree',
    'regression', 'machine learning', 'geostatistical', 'kriging', 'allometric'
]

# Function to extract model types from abstract
def extract_models(abstract):
    if pd.isna(abstract):
        return []
    abstract_lower = abstract.lower()
    models = [kw for kw in model_keywords if kw in abstract_lower]
    return list(set(models))  # unique

# Collect data for dataframe
data = []
for idx, row in filtered_articles.iterrows():
    title = row['TI']
    abstract = row['AB']
    stats = extract_fit_stats(abstract)
    models = extract_models(abstract)
    if stats:  # only if mentioned
        data.append({
            'Title': title,
            'Fit Statistics': stats,
            'Model Types': models
        })

# Create dataframe
df_stats = pd.DataFrame(data)

# Print the dataframe
print("Dataframe of articles with extracted fit statistics:")
print(df_stats)

# Save to CSV
df_stats.to_csv('fit_statistics_dataframe.csv', index=False)
print("\nDataframe saved to 'fit_statistics_dataframe.csv'")

# Also, expand for better view
expanded_data = []
for item in data:
    title = item['Title']
    for stat, values in item['Fit Statistics'].items():
        for value in values:
            expanded_data.append({
                'Title': title,
                'Statistic': stat,
                'Value': value
            })

df_expanded = pd.DataFrame(expanded_data)
print("\nExpanded dataframe (one row per statistic-value pair):")
print(df_expanded.head(20))  # show first 20

# Save expanded
df_expanded.to_csv('fit_statistics_expanded.csv', index=False)
print("Expanded dataframe saved to 'fit_statistics_expanded.csv'")

# Convert to RIS format for Zotero import
def to_ris(row):
    ris = []
    ris.append("TY  - JOUR")  # Assuming all are journal articles
    
    # Title
    if pd.notna(row['TI']):
        ris.append(f"TI  - {row['TI']}")
    
    # Authors - split by semicolon
    if pd.notna(row['AU']):
        authors = row['AU'].split('; ')
        for au in authors:
            ris.append(f"AU  - {au.strip()}")
    
    # Publication Year
    if pd.notna(row['PY']):
        ris.append(f"PY  - {int(row['PY'])}")
    
    # Journal
    if pd.notna(row['SO']):
        ris.append(f"JO  - {row['SO']}")
    
    # Volume
    if pd.notna(row['VL']):
        ris.append(f"VL  - {row['VL']}")
    
    # Issue
    if pd.notna(row['IS']):
        ris.append(f"IS  - {row['IS']}")
    
    # Pages
    if pd.notna(row['BP']) and pd.notna(row['EP']):
        ris.append(f"SP  - {row['BP']}")
        ris.append(f"EP  - {row['EP']}")
    elif pd.notna(row['BP']):
        ris.append(f"SP  - {row['BP']}")
    
    # DOI
    if pd.notna(row['DI']):
        ris.append(f"DO  - {row['DI']}")
    
    # Abstract
    if pd.notna(row['AB']):
        ris.append(f"AB  - {row['AB']}")
    
    # Keywords (from DE - Keywords)
    if pd.notna(row['DE']):
        keywords = row['DE'].split('; ')
        for kw in keywords:
            ris.append(f"KW  - {kw.strip()}")
    
    ris.append("ER  - ")
    ris.append("")
    
    return "\n".join(ris)

# Generate RIS content for all articles
ris_content = ""
for idx, row in df.iterrows():
    ris_content += to_ris(row)

# Save to file
with open('wos_references.ris', 'w', encoding='utf-8') as f:
    f.write(ris_content)

print("RIS file saved as 'wos_references.ris'")
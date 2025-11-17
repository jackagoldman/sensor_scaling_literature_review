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

# Fit statistics keywords (case-insensitive)
fit_keywords = ['r2', 'r²', 'rmse', 'mae', 'r-squared', 'correlation', 'accuracy', 'precision', 'recall', 'f1']

# Function to check if abstract contains any fit statistic
def mentions_fit_stats(abstract):
    if pd.isna(abstract):
        return False
    abstract_lower = abstract.lower()
    return any(keyword in abstract_lower for keyword in fit_keywords)

# Process each article
results = []
for idx, row in filtered_articles.iterrows():
    title = row['TI']
    abstract = row['AB']
    has_fit_stats = mentions_fit_stats(abstract)
    results.append((title, has_fit_stats))

# Print results
print("Articles mentioning fit statistics (R², RMSE, MAE, etc.) in the abstract:")
mentioning = []
not_mentioning = []
for title, has in results:
    if has:
        print(f"Yes: {title}")
        mentioning.append(title)
    else:
        print(f"No: {title}")
        not_mentioning.append(title)

print(f"\nTotal articles mentioning fit statistics: {len(mentioning)}")
print(f"Total articles not mentioning fit statistics: {len(not_mentioning)}")

# Save to file
with open('fit_statistics_check.txt', 'w') as f:
    f.write("Articles mentioning fit statistics (R², RMSE, MAE, etc.) in the abstract:\n\n")
    f.write("Mentioning:\n")
    for title in mentioning:
        f.write(f"- {title}\n")
    f.write(f"\nTotal mentioning: {len(mentioning)}\n\n")
    f.write("Not mentioning:\n")
    for title in not_mentioning:
        f.write(f"- {title}\n")
    f.write(f"\nTotal not mentioning: {len(not_mentioning)}\n")

print("Results saved to 'fit_statistics_check.txt'")
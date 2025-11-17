import pandas as pd

# Read the Web of Science data file
df = pd.read_csv('wos_search_refined_11-16-25.txt', sep='\t')

# Keywords for forest types
forest_keywords = ['boreal', 'temperate', 'coniferous']

# Filter rows where the abstract contains any of the forest keywords (case-insensitive) but NOT 'tropical'
# First, contains any forest keyword
contains_forest = df['AB'].str.contains('|'.join(forest_keywords), case=False, na=False)
# Does not contain 'tropical'
no_tropical = ~df['AB'].str.contains('tropical', case=False, na=False)

# Combine filters
filtered_articles = df[contains_forest & no_tropical]

# Extract the titles
titles = filtered_articles['TI'].tolist()

# Print the list of titles
print("Articles mentioning 'boreal', 'temperate', or 'coniferous' in the abstract (excluding those with 'tropical'):")
for i, title in enumerate(titles, 1):
    print(f"{i}. {title}")

print(f"\nTotal articles: {len(titles)}")

# Optionally, save to a file
with open('articles_forest_types_no_tropical.txt', 'w') as f:
    f.write("Articles mentioning 'boreal', 'temperate', or 'coniferous' in the abstract (excluding those with 'tropical'):\n")
    for i, title in enumerate(titles, 1):
        f.write(f"{i}. {title}\n")
    f.write(f"\nTotal articles: {len(titles)}")

print("List saved to 'articles_forest_types_no_tropical.txt'")
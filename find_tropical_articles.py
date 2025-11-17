import pandas as pd

# Read the Web of Science data file
df = pd.read_csv('wos_search_refined_11-16-25.txt', sep='\t')

# Filter rows where the abstract contains 'tropical' (case-insensitive)
tropical_articles = df[df['AB'].str.contains('tropical', case=False, na=False)]

# Extract the titles
titles = tropical_articles['TI'].tolist()

# Print the list of titles
print("Articles with 'tropical' in the abstract:")
for i, title in enumerate(titles, 1):
    print(f"{i}. {title}")

print(f"\nTotal articles found: {len(titles)}")

# Optionally, save to a file
with open('tropical_articles.txt', 'w') as f:
    f.write("Articles with 'tropical' in the abstract:\n")
    for i, title in enumerate(titles, 1):
        f.write(f"{i}. {title}\n")
    f.write(f"\nTotal articles found: {len(titles)}")

print("Titles saved to 'tropical_articles.txt'")
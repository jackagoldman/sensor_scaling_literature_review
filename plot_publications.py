import pandas as pd
import matplotlib.pyplot as plt

# Read the Web of Science data file
df = pd.read_csv('wos_search_refined_11-16-25.txt', sep='\t')

# Extract the publication year column
years = df['PY']

# Count the number of publications per year
counts = years.value_counts().sort_index()

# Create a bar plot
plt.figure(figsize=(10, 6))
plt.bar(counts.index, counts.values, color='skyblue')
plt.xlabel('Year')
plt.ylabel('Number of Publications')
plt.title('Number of Publications per Year')
plt.xticks(counts.index, rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Save the plot as an image file
plt.savefig('publications_per_year.png', dpi=300, bbox_inches='tight')

# Display the plot
plt.show()
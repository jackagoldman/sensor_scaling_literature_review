import pandas as pd
import matplotlib.pyplot as plt

# Read the Web of Science data file
df = pd.read_csv('wos_search_refined_11-16-25.txt', sep='\t')

# Extract abstracts, drop NaN
abstracts = df['AB'].dropna()

# Initialize counters
categories = {
    'Boreal only': 0,
    'Temperate only': 0,
    'Coniferous only': 0,
    'Combinations': 0
}

# Keywords
keywords = ['boreal', 'temperate', 'coniferous']

# Process each abstract
for abstract in abstracts:
    abstract_lower = abstract.lower()
    mentions = {kw: kw in abstract_lower for kw in keywords}
    
    mentioned = [kw for kw, present in mentions.items() if present]
    
    if len(mentioned) == 1:
        if 'boreal' in mentioned:
            categories['Boreal only'] += 1
        elif 'temperate' in mentioned:
            categories['Temperate only'] += 1
        elif 'coniferous' in mentioned:
            categories['Coniferous only'] += 1
    elif len(mentioned) > 1:
        categories['Combinations'] += 1

# Print the counts
print("Counts of studies mentioning forest types:")
for cat, count in categories.items():
    print(f"{cat}: {count}")

# Plot the bar chart
plt.figure(figsize=(8, 6))
bars = plt.bar(categories.keys(), categories.values(), color=['blue', 'green', 'red', 'purple'])
plt.xlabel('Categories')
plt.ylabel('Number of Studies')
plt.title('Number of Studies Mentioning Forest Type Combinations')
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Add sample sizes on top of bars
for bar, count in zip(bars, categories.values()):
    plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5, str(count), ha='center', va='bottom')

# Save the plot
plt.savefig('forest_type_categories.png', dpi=300, bbox_inches='tight')

# Display the plot
plt.show()
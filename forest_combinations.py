import pandas as pd
import re

# Read the Web of Science data file
df = pd.read_csv('wos_search_refined_11-16-25.txt', sep='\t')

# Extract abstracts, drop NaN
abstracts = df['AB'].dropna()

# Set to store unique combinations
combinations = set()

# Process each abstract
for abstract in abstracts:
    # Convert to lowercase for case-insensitive matching
    abstract = abstract.lower()
    # Find all matches of 1-3 words followed by "forest"
    matches = re.findall(r'\b(\w+(?:\s+\w+){0,2})\s+forest\b', abstract)
    for match in matches:
        # Add the full phrase including "forest"
        combinations.add(match + ' forest')

# Sort the combinations for better readability
sorted_combinations = sorted(combinations)

# Print the list of combinations
print("List of all possible word combinations found in the abstracts:")
for combo in sorted_combinations:
    print(combo)

# Optionally, save to a file
with open('forest_combinations.txt', 'w') as f:
    f.write("List of all possible word combinations found in the abstracts:\n")
    for combo in sorted_combinations:
        f.write(combo + '\n')

print(f"\nTotal unique combinations: {len(sorted_combinations)}")
print("Combinations saved to 'forest_combinations.txt'")
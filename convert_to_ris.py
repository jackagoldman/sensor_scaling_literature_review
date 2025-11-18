import pandas as pd

# Read the Web of Science data file
df = pd.read_csv('wos_search_refined_11-16-25.txt', sep='\t')

# Function to convert to RIS format
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

# Generate RIS content
ris_content = ""
for idx, row in df.iterrows():
    ris_content += to_ris(row)

# Save to file
with open('wos_references.ris', 'w', encoding='utf-8') as f:
    f.write(ris_content)

print("RIS file saved as 'wos_references.ris'")
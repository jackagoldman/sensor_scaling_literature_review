import pandas as pd
import requests
import time
import re
import json

# Function to extract information using local LLM via Ollama
def extract_info(title, abstract):
    prompt = f"""
    Analyze the following paper title and abstract. Extract the following information if available:
    - Forest type (e.g., boreal, temperate, tropical, coniferous, deciduous, mixed)
    - Region (e.g., country, continent, specific location)
    - Scale (e.g., plot, stand, landscape, regional, global)
    - Statistical method (e.g., linear regression, random forest, SVM, neural network)
    - R² values (list all reported R² or coefficient of determination)
    - RMSE values (list all reported RMSE or root mean square error)

    Title: {title}
    Abstract: {abstract}

    Output in JSON format:
    {{
        "forest_type": "string or list",
        "region": "string",
        "scale": "string",
        "statistical_method": "string or list",
        "r2_values": [list of floats],
        "rmse_values": [list of floats]
    }}
    If not available, use null or empty list.
    """
    try:
        response = requests.post('http://localhost:11434/api/generate', json={
            "model": "llama3.2",  # or your chosen model
            "prompt": prompt,
            "stream": False
        })
        result = response.json()['response'].strip()
        # Assuming the model outputs JSON, parse it
        return json.loads(result)
    except Exception as e:
        print(f"Error: {e}")
        return None

# Read the TSV file
df = pd.read_csv('/Users/jgoldman/git/sensor_scaling_literature_review/wos_search_refined_11-16-25.txt', sep='\t', encoding='utf-8')

# Initialize list for results
results = []

# Process each paper
for idx, row in df.iterrows():
    title = row.get('TI', '')
    abstract = row.get('AB', '')
    doi = row.get('DI', '')
    
    if pd.isna(abstract) or abstract == '':
        continue  # Skip if no abstract
    
    info = extract_info(title, abstract)
    if info:
        info['title'] = title
        info['doi'] = doi
        results.append(info)
    
    time.sleep(1)  # Rate limit

# Convert to DataFrame
output_df = pd.DataFrame(results)

# Save to CSV
output_df.to_csv('/Users/jgoldman/git/sensor_scaling_literature_review/extracted_data.csv', index=False)

print("Extraction complete. Data saved to extracted_data.csv")
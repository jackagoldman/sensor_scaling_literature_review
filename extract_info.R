# Load necessary libraries
library(httr)
library(jsonlite)
library(dplyr)
library(readr)

# Function to extract information using local LLM via Ollama
extract_info <- function(title, abstract) {
  prompt <- paste0(
    "Analyze the following paper title and abstract. Extract the following information if available:\n",
    "- Forest type (e.g., boreal, temperate, tropical, coniferous, deciduous, mixed)\n",
    "- Region (e.g., country, continent, specific location)\n",
    "- Scale (e.g., plot, stand, landscape, regional, global)\n",
    "- Statistical method (e.g., linear regression, random forest, SVM, neural network)\n",
    "- R² values (list all reported R² or coefficient of determination)\n",
    "- RMSE values (list all reported RMSE or root mean square error)\n\n",
    "Title: ", title, "\n",
    "Abstract: ", abstract, "\n\n",
    "Output in JSON format:\n",
    "{\n",
    "  \"forest_type\": \"string or list\",\n",
    "  \"region\": \"string\",\n",
    "  \"scale\": \"string\",\n",
    "  \"statistical_method\": \"string or list\",\n",
    "  \"r2_values\": [list of floats],\n",
    "  \"rmse_values\": [list of floats]\n",
    "}\n",
    "If not available, use null or empty list."
  )
  
  response <- POST(
    url = "http://localhost:11434/api/generate",
    body = toJSON(list(
      model = "llama3.2",  # or your chosen model
      prompt = prompt,
      stream = FALSE
    ), auto_unbox = TRUE),
    encode = "json"
  )
  
  if (status_code(response) == 200) {
    result <- content(response, "text")
    result_json <- fromJSON(result)
    return(result_json$response)
  } else {
    cat("Error:", status_code(response), "\n")
    return(NULL)
  }
}

# Read the TSV file
df <- read_tsv('/Users/jgoldman/git/sensor_scaling_literature_review/wos_search_refined_11-16-25.txt')

# Initialize list for results
results <- list()

# Process each paper
for (i in 1:nrow(df)) {
  title <- df$TI[i]
  abstract <- df$AB[i]
  doi <- df$DI[i]
  
  if (is.na(abstract) || abstract == "") next
  
  info_json <- extract_info(title, abstract)
  if (!is.null(info_json)) {
    info <- fromJSON(info_json)
    info$title <- title
    info$doi <- doi
    results <- append(results, list(info))
  }
  
  Sys.sleep(1)  # Rate limit
}

# Convert to DataFrame
output_df <- bind_rows(results)

# Save to CSV
write_csv(output_df, '/Users/jgoldman/git/sensor_scaling_literature_review/extracted_data_r.csv')

print("Extraction complete. Data saved to extracted_data_r.csv")
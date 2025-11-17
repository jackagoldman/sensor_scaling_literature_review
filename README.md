# sensor_scaling_literature_review

This repository contains a literature review on sensor scaling for aboveground biomass estimation from airborne lidar to optical satellite and radar data.

## Setup

1. Install Ollama: https://ollama.ai/
2. Pull a model: `ollama pull llama3.2` (or another model capable of JSON output)

## Extraction

Run the Python or R script to extract information from abstracts using a local LLM.

- Python: `python extract_info.py`
- R: `Rscript extract_info.R`

This will create `extracted_data.csv` or `extracted_data_r.csv` with extracted fields: forest_type, region, scale, statistical_method, r2_values, rmse_values.

## Meta-Analysis

After extraction, run the meta-analysis in R:

`Rscript meta_analysis.R`

This performs regression analysis on R² and RMSE as functions of the predictors.

Note: The scripts assume the LLM outputs valid JSON. You may need to adjust the prompt or parsing for better results.
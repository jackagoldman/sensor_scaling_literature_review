# Meta-analysis script in R

# Load libraries
library(metafor)
library(dplyr)
library(readr)

# Read the extracted data
df <- read_csv('extracted_data.csv')

# Assuming r2_values is a column with lists, but since CSV, perhaps it's string, need to parse
# For simplicity, assume we have columns: forest_type, region, scale, statistical_method, r2, rmse
# Where r2 is the main R² value, rmse the main RMSE

# Clean data: remove NAs, etc.
df_clean <- df %>%
  filter(!is.na(r2) & !is.na(rmse)) %>%
  mutate(
    forest_type = as.factor(forest_type),
    region = as.factor(region),
    scale = as.factor(scale),
    statistical_method = as.factor(statistical_method)
  )

# For meta-analysis, since it's not effect sizes, but regression on metrics
# Perhaps use lm or something, but for meta, if we have variances, but here no.
# Since it's not traditional meta-analysis, just regression.

# Fit a linear model for R²
model_r2 <- lm(r2 ~ forest_type + region + scale + statistical_method, data = df_clean)

# Summary
summary(model_r2)

# Similarly for RMSE
model_rmse <- lm(rmse ~ forest_type + region + scale + statistical_method, data = df_clean)
summary(model_rmse)

# If using metafor for mixed effects, but since no yi, vi, perhaps not.
# For meta-regression, need effect sizes.

# Perhaps treat each paper as a study, with r2 as yi, but variance unknown.
# Can assume variance or use rma.uni with known variances if available.

# For simplicity, the lm is fine.
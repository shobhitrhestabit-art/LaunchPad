# Day 1 — Exploratory Data Analysis Report

## Dataset Overview
- Rows: 1345
- Columns: 37
- Dataset cleaned using automated pipeline

## Missing Values
- No missing values present after preprocessing
- Confirmed using missing value heatmap

## Feature Distributions
- Numeric features show varied distributions
- Some toxicity-related features exhibit skewness
- Categorical feature: gender

## Correlation Analysis
- Strong correlations observed among toxicity and pharmacokinetic features
- Clinical indicators such as serum_creatinine and blood_urea show meaningful relationships

## Target Distribution
- Target variable: nephrotoxic_label
- Distribution inspected for class imbalance
- Potential imbalance handling to be considered in later stages

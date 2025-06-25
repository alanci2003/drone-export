# Drone Export Analytics

This project processes, visualizes, and explores Taiwan’s drone export data using a clean and modular Python stack.

---

## 🗂 Project Structure

drone-export/
├── app.py # Gradio app for interactive charts
├── preprocess_drone_exports.py # Step 2: Clean and transform raw CSV
├── plot_01_to_06.py # Step 3: Generates 6 export data plots
├── assets/ # Output folder for cleaned CSVs and images
├── sample_raw.csv # Example Big5-encoded export CSV
├── requirements.txt
└── README.md

---

## ✅ Step-by-Step Workflow

### ✅ Step 1: Place Raw Data

Save your Big5-encoded CSV from Taiwan Customs (e.g., `sample_raw.csv`) in the project root.

### ✅ Step 2: Clean the Data

```bash
python preprocess_drone_exports.py
```

This command:
- Translates `國家` (country) column to English using deep-translator.
- Converts 民國年 (ROC calendar) dates to Gregorian.
- Converts export values (`美元(千元)`) to full USD.
- Adds `yyyy/mm` and `qtr` fields.
- Saves the cleaned UTF‑8 CSV under `assets/`.

The output file will be named `assets/Drone_export_cleaned_YYYYMMDD.csv`.

### ✅ Step 3: Launch the Dashboard

Run the Gradio app to visualize and download plots:

```bash
python app.py
```

---

## 📦 Features
- Upload Big5-encoded customs data
- Translate country names to English
- Convert ROC dates to Gregorian ``yyyy/mm`` and map to quarters
- Scale export value from thousands of USD to actual amount
- Group low-volume countries as ``Other`` for readability
- Download the cleaned CSV and all generated charts

## 📊 Visualizations
This app automatically generates six types of drone export visualizations:
1. **Drone Unit Counts** — Total drones exported by quarter and destination country (stacked bar).
2. **Drone Unit Share (%)** — Percentage share of drones exported to each country per quarter.
3. **Export Value ($K)** — Export value (in thousands of USD) by country and quarter.
4. **Export Value Share (%)** — Proportion of export value per country per quarter.
5. **2023H2 vs 2024H2 Comparison** — Unit share and export value share across two half-year periods.
6. **2023H2 vs 2025Q1 Comparison** — Unit share, value share, unit count, and value count across three periods.

All plots are downloadable as high-resolution PNGs and the underlying data is also exported as CSVs.

## 🚀 How to Use

### On Hugging Face Space
1. Visit the space at `https://huggingface.co/spaces/<your-username>/drone-export-dashboard`
2. Upload the raw CSV file.
3. Click **"Process"** to generate charts and download links.

### Run Locally
```bash
git clone https://huggingface.co/spaces/<your-username>/drone-export-dashboard
cd drone-export-dashboard
pip install -r requirements.txt
python app.py
```

## Project Structure
```
├── app.py
├── preprocess_drone_exports.py
├── plot_01_to_06.py
├── assets/
├── requirements.txt
└── README.md
```

## Dependencies
- gradio>=4.0
- pandas
- matplotlib
- numpy
- pydantic<2.0
- deep-translator

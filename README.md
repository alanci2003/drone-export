# Drone Export Dashboard

This project provides a simple Gradio interface for processing drone export data. Upload a raw CSV file encoded in Big5 and the app will preprocess the data, generate six visualizations, and allow you to download the resulting files.

## 📦 Features
- Upload Big5-encoded customs data
- Translate country names to English
- Convert ROC dates to Gregorian ``yyyy/mm`` and map to quarters
- Scale export value from thousands of USD to actual amount
- Group low-volume countries as ``Other`` for readability
- Download the cleaned CSV and all generated charts

Run the application with:

```bash
pip install -r requirements.txt
python app.py
```

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
- gradio
- pandas
- matplotlib
- numpy
- googletrans==4.0.0-rc1

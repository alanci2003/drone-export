from __future__ import annotations

from datetime import datetime
from pathlib import Path
from time import sleep

import pandas as pd
from deep_translator import GoogleTranslator


def safe_translate(text: str, translator, retries=3, delay=1) -> str:
    """Try to translate text with retries; fallback to original if failed."""
    for _ in range(retries):
        try:
            translated = translator.translate(text)
            if translated and translated != text:
                return translated
        except Exception:
            pass
        sleep(delay)
    return text


def clean_data(input_path: str | Path, output_dir: str | Path = "assets") -> Path:
    """Clean raw drone export CSV data."""
    input_path = Path(input_path)
    output_dir = Path(output_dir)

    # Step 1: Read CSV with Big5 encoding
    df = pd.read_csv(input_path, encoding="big5")

    # Step 2: Translate country names with manual override
    translator = GoogleTranslator(source="auto", target="en")
    manual_map = {
        "美國": "United States",
        "瓜地馬拉": "Guatemala",
        "貝里斯": "Belize",
        "聖露西亞": "Saint Lucia",
        "英國": "United Kingdom",
        "南韓": "South Korea",
        "德國": "Germany",
        "羅馬尼亞": "Romania",
        "波蘭": "Poland",
        "奧地利": "Austria",
        "紐西蘭": "New Zealand",
        "中國大陸": "China"
    }

    unique_countries = df["國家"].dropna().unique()
    translated_countries = {
        tw: manual_map.get(tw, safe_translate(tw, translator))
        for tw in unique_countries
    }
    df["country"] = df["國家"].map(translated_countries)

    # Optional debug: list untranslated entries
    for orig, eng in translated_countries.items():
        if orig == eng and orig not in manual_map:
            print(f"⚠️ Possibly untranslated: {orig}")

    # Step 3: Convert ROC date to yyyy/mm and quarter
    def parse_roc_date(roc_str: str) -> tuple[str, str]:
        try:
            year, month = roc_str.replace("年", "/").replace("月", "").split("/")
            year = int(year) + 1911
            month = int(month)
            return f"{year}/{month}", f"{year} Q{((month - 1)//3) + 1}"
        except Exception:
            return "", ""

    df["yyyy/mm"], df["qtr"] = zip(*df["日期"].map(parse_roc_date))

    # Step 4: Convert USD from thousands to actual amount
    df["US$ amount"] = df["美元(千元)"].fillna(0) * 1000

    # Step 5: Rename columns
    df.rename(columns={
        "貨品號列": "HS code",
        "中文貨名": "中文貨名",
        "英文貨名": "detail",
        "美元(千元)": "美元(千元)",
        "數量(限11碼貨品)": "Quanity",
        "數量單位": "數量單位",
    }, inplace=True)

    # Step 6: Reorder columns
    final_cols = [
        "進出口別", "日期", "yyyy/mm", "qtr", "country",
        "HS code", "中文貨名", "detail", "美元(千元)",
        "US$ amount", "Quanity", "數量單位"
    ]
    df_final = df[final_cols]

    # Step 7: Export
    today_str = datetime.today().strftime("%Y%m%d")
    output_dir.mkdir(exist_ok=True)
    output_filename = f"Drone_export_cleaned_{today_str}.csv"
    output_path = output_dir / output_filename
    df_final.to_csv(output_path, index=False, encoding="utf-8-sig")

    print(f"✅ Exported to {output_path}")
    return output_path


if __name__ == "__main__":
    sample_input = "sample_raw.csv"
    clean_data(sample_input, "assets")

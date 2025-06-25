from __future__ import annotations

from datetime import datetime
from pathlib import Path

import pandas as pd
from deep_translator import GoogleTranslator


def clean_data(input_path: str | Path, output_dir: str | Path = "assets") -> Path:
    """Clean raw drone export CSV data.

    Parameters
    ----------
    input_path : str | Path
        Path to the raw CSV encoded in Big5.
    output_dir : str | Path, optional
        Directory to save the cleaned CSV, by default "assets".

    Returns
    -------
    Path
        Path to the cleaned CSV written to ``output_dir``.
    """
    input_path = Path(input_path)
    output_dir = Path(output_dir)

    # Step 1: Read CSV with Big5 encoding
    df = pd.read_csv(input_path, encoding="big5")

    # Step 2: Translate country names using Deep Translator
    translator = GoogleTranslator(source="auto", target="en")
    unique_countries = df["國家"].unique()
    translated_countries = {
        tw: translator.translate(tw)
        for tw in unique_countries
    }
    df["country"] = df["國家"].map(translated_countries)

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

    # Step 5: Rename columns for consistency
    df.rename(columns={
        "貨品號列": "HS code",
        "中文貨名": "中文貨名",
        "英文貨名": "detail",
        "美元(千元)": "美元(千元)",
        "數量(限11碼貨品)": "Quanity",
        "數量單位": "數量單位",
    }, inplace=True)

    # Step 6: Reorder and select final columns
    final_cols = [
        "進出口別", "日期", "yyyy/mm", "qtr", "country",
        "HS code", "中文貨名", "detail", "美元(千元)",
        "US$ amount", "Quanity", "數量單位"
    ]
    df_final = df[final_cols]

    # Step 7: Export to CSV with today's date
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

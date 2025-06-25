import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import os
from datetime import datetime


def load_and_group(df, value_col, threshold=5):
    df[value_col] = pd.to_numeric(df[value_col], errors="coerce")
    grouped = df.groupby(["qtr", "country"])[value_col].sum().reset_index()
    country_totals = grouped.groupby("country")[value_col].sum()
    rare = country_totals[country_totals < threshold].index
    grouped["country_grouped"] = grouped["country"].apply(lambda x: "Other" if x in rare else x)
    final = grouped.groupby(["qtr", "country_grouped"])[value_col].sum().reset_index()
    pivot = final.pivot(index="qtr", columns="country_grouped", values=value_col).fillna(0)
    ordered_cols = pivot.sum().sort_values(ascending=False).index.tolist()
    pivot = pivot[ordered_cols]
    colors = cm.get_cmap("tab20", len(ordered_cols))(np.arange(len(ordered_cols)))
    return pivot, colors


def plot_and_save(df, colors, title, ylabel, filename, label_thresh, fmt="{val}", yfmt=None):
    fig, ax = plt.subplots(figsize=(12, 6))
    df.plot(kind="bar", stacked=True, ax=ax, color=colors)
    for i, (idx, row) in enumerate(df.iterrows()):
        cumulative = 0
        for j, val in enumerate(row):
            if val > label_thresh:
                ax.text(i, cumulative + val / 2, fmt.format(val=val), ha="center", va="center", fontsize=8)
            cumulative += val
    ax.set_title(title)
    ax.set_ylabel(ylabel)
    ax.set_xlabel("Quarter")
    ax.legend(title="Country", bbox_to_anchor=(1.05, 1), loc='upper left')
    if yfmt:
        ax.yaxis.set_major_formatter(yfmt)
    plt.tight_layout()
    return fig, ax


def save_outputs(fig, df, prefix, output_dir):
    date_str = datetime.today().strftime("%Y%m%d")
    png_path = os.path.join(output_dir, f"{prefix}_{date_str}.png")
    csv_path = os.path.join(output_dir, f"{prefix}_{date_str}.csv")
    fig.savefig(png_path, dpi=300)
    df.to_csv(csv_path)
    plt.close(fig)
    return png_path, csv_path


def plot_01(cleaned_csv_path: str, output_dir: str) -> tuple[str, str]:
    df = pd.read_csv(cleaned_csv_path)
    pivot, colors = load_and_group(df, "Quanity")
    fig, ax = plot_and_save(pivot, colors, "Quarterly Drone Exports by Destination Country",
                            "Number of Drones Exported", "01_Drone_Export_Counts", label_thresh=10,
                            fmt="{val:.0f}")
    return save_outputs(fig, pivot.astype(int), "01_Drone_Export_Counts", output_dir)


def plot_02(cleaned_csv_path: str, output_dir: str) -> tuple[str, str]:
    df = pd.read_csv(cleaned_csv_path)
    pivot, colors = load_and_group(df, "Quanity")
    percent = pivot.div(pivot.sum(axis=1), axis=0) * 100
    fig, ax = plot_and_save(percent, colors, "Quarterly Drone Export Share by Destination Country",
                            "Percentage of Quarter Total (%)", "02_Drone_Export_Percent", label_thresh=1.5,
                            fmt="{val:.1f}%")
    return save_outputs(fig, percent.round(2), "02_Drone_Export_Percent", output_dir)


def plot_03(cleaned_csv_path: str, output_dir: str) -> tuple[str, str]:
    df = pd.read_csv(cleaned_csv_path)
    pivot, colors = load_and_group(df, "美元(千元)")
    fig, ax = plot_and_save(pivot, colors, "Quarterly Drone Export Value by Destination Country",
                            "Export Value (in Thousand USD)", "03_Drone_Export_Value", label_thresh=20,
                            fmt="${val:.0f}K")
    return save_outputs(fig, (pivot * 1000).astype(int), "03_Drone_Export_Value", output_dir)


def plot_04(cleaned_csv_path: str, output_dir: str) -> tuple[str, str]:
    df = pd.read_csv(cleaned_csv_path)
    pivot, colors = load_and_group(df, "美元(千元)")
    percent = pivot.div(pivot.sum(axis=1), axis=0) * 100
    fig, ax = plot_and_save(percent, colors, "Quarterly Drone Export Value Share by Country",
                            "Percentage of Export Value (%)", "04_Drone_Export_Value_Pct", label_thresh=1.5,
                            fmt="{val:.1f}%")
    return save_outputs(fig, percent.round(2), "04_Drone_Export_Value_Pct", output_dir)


def plot_05(cleaned_csv_path: str, output_dir: str) -> tuple[list[str], list[str]]:
    df = pd.read_csv(cleaned_csv_path)
    df["Quanity"] = pd.to_numeric(df["Quanity"], errors="coerce")
    df["美元(千元)"] = pd.to_numeric(df["美元(千元)"], errors="coerce")
    df["period"] = df["qtr"].map({"2023 Q3": "2023 H2", "2023 Q4": "2023 H2", "2024 Q3": "2024 H2", "2024 Q4": "2024 H2"})
    df = df[df["period"].notna()]
    qty = df.groupby(["period", "country"])["Quanity"].sum().reset_index()
    usd = df.groupby(["period", "country"])["美元(千元)"].sum().reset_index()
    qty_pivot, colors = load_and_group(qty, "Quanity")
    usd_pivot, _ = load_and_group(usd, "美元(千元)")
    qty_pct = qty_pivot.div(qty_pivot.sum(axis=1), axis=0) * 100
    usd_pct = usd_pivot.div(usd_pivot.sum(axis=1), axis=0) * 100

    f1, _ = plot_and_save(qty_pct, colors, "Drone Unit Share: 2023H2 vs 2024H2", "% of Total Units",
                          "05_Unit_Share", 2.5, fmt="{val:.1f}%")
    f2, _ = plot_and_save(usd_pct, colors, "Export Value Share: 2023H2 vs 2024H2", "% of Export Value",
                          "05_Value_Share", 2.5, fmt="{val:.1f}%")
    p1, c1 = save_outputs(f1, qty_pct.round(2), "05_Unit_Share", output_dir)
    p2, c2 = save_outputs(f2, usd_pct.round(2), "05_Value_Share", output_dir)
    return [p1, p2], [c1, c2]


def plot_06(cleaned_csv_path: str, output_dir: str) -> tuple[list[str], list[str]]:
    df = pd.read_csv(cleaned_csv_path)
    df["Quanity"] = pd.to_numeric(df["Quanity"], errors="coerce")
    df["美元(千元)"] = pd.to_numeric(df["美元(千元)"], errors="coerce")
    df["period"] = df["qtr"].map({
        "2023 Q3": "2023 H2", "2023 Q4": "2023 H2",
        "2024 Q3": "2024 H2", "2024 Q4": "2024 H2",
        "2025 Q1": "2025 Q1"
    })
    df = df[df["period"].notna()]
    qty = df.groupby(["period", "country"])["Quanity"].sum().reset_index()
    usd = df.groupby(["period", "country"])["美元(千元)"].sum().reset_index()
    qty_pivot, colors = load_and_group(qty, "Quanity")
    usd_pivot, _ = load_and_group(usd, "美元(千元)")
    qty_pct = qty_pivot.div(qty_pivot.sum(axis=1), axis=0) * 100
    usd_pct = usd_pivot.div(usd_pivot.sum(axis=1), axis=0) * 100

    f1, _ = plot_and_save(qty_pct, colors, "Unit Share: 2023H2 vs 2025Q1", "% of Total Units",
                          "06_Unit_Share", 2.5, fmt="{val:.1f}%")
    f2, _ = plot_and_save(usd_pct, colors, "Value Share: 2023H2 vs 2025Q1", "% of Export Value",
                          "06_Value_Share", 2, fmt="{val:.1f}%")
    f3, _ = plot_and_save(qty_pivot, colors, "Unit Count: 2023H2 vs 2025Q1", "Units", "06_Unit_Count",
                          15, fmt="{val:.0f}")
    f4, _ = plot_and_save(usd_pivot, colors, "Export Value ($K): 2023H2 vs 2025Q1", "Value in $K",
                          "06_Value_Count", 30, fmt="${val:.0f}K")

    p1, c1 = save_outputs(f1, qty_pct.round(2), "06_Unit_Share", output_dir)
    p2, c2 = save_outputs(f2, usd_pct.round(2), "06_Value_Share", output_dir)
    p3, c3 = save_outputs(f3, qty_pivot.astype(int), "06_Unit_Count", output_dir)
    p4, c4 = save_outputs(f4, (usd_pivot * 1000).astype(int), "06_Value_Count", output_dir)
    return [p1, p2, p3, p4], [c1, c2, c3, c4]

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import os
from datetime import datetime

def load_and_group(df, value_col, time_col="qtr", threshold=5):
    df[value_col] = pd.to_numeric(df[value_col], errors="coerce")
    grouped = df.groupby([time_col, "country"])[value_col].sum().reset_index()
    country_totals = grouped.groupby("country")[value_col].sum()
    rare = country_totals[country_totals < threshold].index
    grouped["country_grouped"] = grouped["country"].apply(lambda x: "Other" if x in rare else x)
    final = grouped.groupby([time_col, "country_grouped"])[value_col].sum().reset_index()
    pivot = final.pivot(index=time_col, columns="country_grouped", values=value_col).fillna(0)
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
    ax.annotate(f"Generated on {datetime.today().strftime('%Y-%m-%d')}",
                xy=(1.0, -0.15), xycoords='axes fraction',
                ha='right', fontsize=9, style='italic')
    plt.tight_layout()
    return fig, ax

def save_outputs(fig, df, prefix, output_dir):
    date_str = datetime.today().strftime("%Y%m%d")
    png_path = os.path.join(output_dir, f"{prefix}_{date_str}.png")
    csv_path = os.path.join(output_dir, f"{prefix}_{date_str}.csv")
    fig.savefig(png_path, dpi=300)
    df.to_csv(csv_path)
    plt.close(fig)
    return [png_path], [csv_path]

# Helper for plots with and without Hong Kong
def generate_dual_plots(cleaned_csv_path, output_dir, plotting_func, prefix):
    df = pd.read_csv(cleaned_csv_path)

    # Ensure consistent comparison
    df["country"] = df["country"].astype(str).str.strip()
    df_excl = df[~df["country"].str.lower().eq("hongkong")]

    # Plot with full data
    all_result = plotting_func(df, output_dir, prefix)
    # Plot excluding Hongkong
    excl_result = plotting_func(df_excl, output_dir, f"{prefix}_excl_HK")

    return all_result[0] + excl_result[0], all_result[1] + excl_result[1]


# Individual plot generators below (adjusted to work with dual plot helper)
def plot_01(cleaned_csv_path: str, output_dir: str):
    def _plot(df, outdir, tag):
        pivot, colors = load_and_group(df, "Quanity")
        fig, ax = plot_and_save(pivot, colors, f"Quarterly Drone Exports by Country ({tag})",
                                "Number of Drones Exported", tag, label_thresh=10, fmt="{val:.0f}")
        return save_outputs(fig, pivot.astype(int), tag, outdir)
    return generate_dual_plots(cleaned_csv_path, output_dir, _plot, "01_Drone_Export_Counts")

def plot_02(cleaned_csv_path: str, output_dir: str):
    def _plot(df, outdir, tag):
        pivot, colors = load_and_group(df, "Quanity")
        percent = pivot.div(pivot.sum(axis=1), axis=0) * 100
        fig, ax = plot_and_save(percent, colors, f"Quarterly Drone Export Share by Country ({tag})",
                                "Percentage of Quarter Total (%)", tag, label_thresh=1.5, fmt="{val:.1f}%")
        return save_outputs(fig, percent.round(2), tag, outdir)
    return generate_dual_plots(cleaned_csv_path, output_dir, _plot, "02_Drone_Export_Percent")

def plot_03(cleaned_csv_path: str, output_dir: str):
    def _plot(df, outdir, tag):
        pivot, colors = load_and_group(df, "美元(千元)")
        fig, ax = plot_and_save(pivot, colors, f"Quarterly Drone Export Value by Country ({tag})",
                                "Export Value (in Thousand USD)", tag, label_thresh=20, fmt="${val:.0f}K")
        return save_outputs(fig, (pivot * 1000).astype(int), tag, outdir)
    return generate_dual_plots(cleaned_csv_path, output_dir, _plot, "03_Drone_Export_Value")

def plot_04(cleaned_csv_path: str, output_dir: str):
    def _plot(df, outdir, tag):
        pivot, colors = load_and_group(df, "美元(千元)")
        percent = pivot.div(pivot.sum(axis=1), axis=0) * 100
        fig, ax = plot_and_save(percent, colors, f"Quarterly Drone Export Value Share by Country ({tag})",
                                "Percentage of Export Value (%)", tag, label_thresh=1.5, fmt="{val:.1f}%")
        return save_outputs(fig, percent.round(2), tag, outdir)
    return generate_dual_plots(cleaned_csv_path, output_dir, _plot, "04_Drone_Export_Value_Pct")

def plot_05(cleaned_csv_path: str, output_dir: str):
    def _plot(df, outdir, tag):
        df["Quanity"] = pd.to_numeric(df["Quanity"], errors="coerce")
        df["美元(千元)"] = pd.to_numeric(df["美元(千元)"], errors="coerce")
        df["period"] = df["qtr"].map({"2023 Q3": "2023 H2", "2023 Q4": "2023 H2",
                                        "2024 Q3": "2024 H2", "2024 Q4": "2024 H2"})
        df = df[df["period"].notna()]
        qty = df.groupby(["period", "country"])["Quanity"].sum().reset_index()
        usd = df.groupby(["period", "country"])["美元(千元)"].sum().reset_index()

        qty_pivot, colors = load_and_group(qty, "Quanity", time_col="period")
        usd_pivot, _ = load_and_group(usd, "美元(千元)", time_col="period")
        qty_pct = qty_pivot.div(qty_pivot.sum(axis=1), axis=0) * 100
        usd_pct = usd_pivot.div(usd_pivot.sum(axis=1), axis=0) * 100

        f1, _ = plot_and_save(qty_pct, colors, f"Drone Unit Share: 2023H2 vs 2024H2 ({tag})", "% of Total Units",
                              f"{tag}_Unit_Share", 2.5, fmt="{val:.1f}%")
        f2, _ = plot_and_save(usd_pct, colors, f"Export Value Share: 2023H2 vs 2024H2 ({tag})", "% of Export Value",
                              f"{tag}_Value_Share", 2.5, fmt="{val:.1f}%")
        p1, c1 = save_outputs(f1, qty_pct.round(2), f"{tag}_Unit_Share", outdir)
        p2, c2 = save_outputs(f2, usd_pct.round(2), f"{tag}_Value_Share", outdir)
        return p1 + p2, c1 + c2

    return generate_dual_plots(cleaned_csv_path, output_dir, _plot, "05")

def plot_06(cleaned_csv_path: str, output_dir: str):
    def _plot(df, outdir, tag):
        df["Quanity"] = pd.to_numeric(df["Quanity"], errors="coerce")
        df["美元(千元)"] = pd.to_numeric(df["美元(千元)"], errors="coerce")
        df["period"] = df["qtr"].map({"2023 Q3": "2023 H2", "2023 Q4": "2023 H2",
                                        "2024 Q3": "2024 H2", "2024 Q4": "2024 H2",
                                        "2025 Q1": "2025 Q1"})
        df = df[df["period"].notna()]
        qty = df.groupby(["period", "country"])["Quanity"].sum().reset_index()
        usd = df.groupby(["period", "country"])["美元(千元)"].sum().reset_index()

        qty_pivot, colors = load_and_group(qty, "Quanity", time_col="period")
        usd_pivot, _ = load_and_group(usd, "美元(千元)", time_col="period")
        qty_pct = qty_pivot.div(qty_pivot.sum(axis=1), axis=0) * 100
        usd_pct = usd_pivot.div(usd_pivot.sum(axis=1), axis=0) * 100

        f1, _ = plot_and_save(qty_pct, colors, f"Unit Share: 2023H2 vs 2025Q1 ({tag})", "% of Total Units",
                              f"{tag}_Unit_Share", 2.5, fmt="{val:.1f}%")
        f2, _ = plot_and_save(usd_pct, colors, f"Value Share: 2023H2 vs 2025Q1 ({tag})", "% of Export Value",
                              f"{tag}_Value_Share", 2, fmt="{val:.1f}%")
        f3, _ = plot_and_save(qty_pivot, colors, f"Unit Count: 2023H2 vs 2025Q1 ({tag})", "Units",
                              f"{tag}_Unit_Count", 15, fmt="{val:.0f}")
        f4, _ = plot_and_save(usd_pivot, colors, f"Export Value ($K): 2023H2 vs 2025Q1 ({tag})", "Value in $K",
                              f"{tag}_Value_Count", 30, fmt="${val:.0f}K")

        p1, c1 = save_outputs(f1, qty_pct.round(2), f"{tag}_Unit_Share", outdir)
        p2, c2 = save_outputs(f2, usd_pct.round(2), f"{tag}_Value_Share", outdir)
        p3, c3 = save_outputs(f3, qty_pivot.astype(int), f"{tag}_Unit_Count", outdir)
        p4, c4 = save_outputs(f4, (usd_pivot * 1000).astype(int), f"{tag}_Value_Count", outdir)
        return p1 + p2 + p3 + p4, c1 + c2 + c3 + c4

    return generate_dual_plots(cleaned_csv_path, output_dir, _plot, "06")

from pathlib import Path
import gradio as gr
from plot_01_to_06 import plot_01, plot_02, plot_03, plot_04, plot_05, plot_06
from preprocess_drone_exports import clean_data

ASSETS_DIR = Path("assets")

def process_file(file_obj):
    cleaned_csv = clean_data(file_obj.name, ASSETS_DIR)

    # Ensure all outputs are proper tuples/lists
    p1, c1 = plot_01(cleaned_csv, ASSETS_DIR)
    p2, c2 = plot_02(cleaned_csv, ASSETS_DIR)
    p3, c3 = plot_03(cleaned_csv, ASSETS_DIR)
    p4, c4 = plot_04(cleaned_csv, ASSETS_DIR)
    p5_list, c5_list = plot_05(cleaned_csv, ASSETS_DIR)
    p6_list, c6_list = plot_06(cleaned_csv, ASSETS_DIR)

    return (
        *p1, *c1,
        *p2, *c2,
        *p3, *c3,
        *p4, *c4,
        *p5_list, *c5_list,
        *p6_list, *c6_list
    )

with gr.Blocks(title="Drone Export Data Visualizer") as app:
    gr.Markdown("## 📦 Drone Export Data Cleaner and Visualizer")

    gr.Markdown("""
        **📝 Expected Raw Data Format (Big5-encoded CSV):**
        - 國家: Country name (in Traditional Chinese)
        - 日期: Date in ROC format (e.g., "113年3月")
        - 貨品號列: HS Code
        - 中文貨名: Product name (Chinese)
        - 英文貨名: Product name (English)
        - 美元(千元): Export value in thousands of USD
        - 數量(限11碼貨品): Quantity exported
        - 數量單位: Unit of measurement
    """)

    with gr.Row():
        file_input = gr.File(label="Upload raw CSV (Big5-encoded export data)", file_types=[".csv"])
        submit_btn = gr.Button("Submit & Visualize")

    with gr.Tabs():
        with gr.Tab("📊 Export Count"):
            img1 = gr.Image(label="Plot 01: Drone Export Counts by Quarter")
            csv1 = gr.File(label="CSV: Export Counts")
            img1b = gr.Image(label="Plot 01 (Excl. HK)")
            csv1b = gr.File(label="CSV: Export Counts (Excl. HK)")

        with gr.Tab("📊 Export Count Share"):
            img2 = gr.Image(label="Plot 02: Export Count Share by Country")
            csv2 = gr.File(label="CSV: Count Share")
            img2b = gr.Image(label="Plot 02 (Excl. HK)")
            csv2b = gr.File(label="CSV: Count Share (Excl. HK)")

        with gr.Tab("💰 Export Value"):
            img3 = gr.Image(label="Plot 03: Export Value by Quarter")
            csv3 = gr.File(label="CSV: Value")
            img3b = gr.Image(label="Plot 03 (Excl. HK)")
            csv3b = gr.File(label="CSV: Value (Excl. HK)")

        with gr.Tab("💰 Export Value Share"):
            img4 = gr.Image(label="Plot 04: Export Value Share by Country")
            csv4 = gr.File(label="CSV: Value Share")
            img4b = gr.Image(label="Plot 04 (Excl. HK)")
            csv4b = gr.File(label="CSV: Value Share (Excl. HK)")

        with gr.Tab("📈 H2 Comparison (2023 vs 2024)"):
            img5a = gr.Image(label="Plot 05A: Unit Share")
            csv5a = gr.File(label="CSV: Unit Share")
            img5ab = gr.Image(label="Plot 05A (Excl. HK)")
            csv5ab = gr.File(label="CSV: Unit Share (Excl. HK)")
            img5b = gr.Image(label="Plot 05B: Value Share")
            csv5b = gr.File(label="CSV: Value Share")
            img5bb = gr.Image(label="Plot 05B (Excl. HK)")
            csv5bb = gr.File(label="CSV: Value Share (Excl. HK)")

        with gr.Tab("📈 H2 vs Q1 Comparison (2023H2 vs 2025Q1)"):
            img6a = gr.Image(label="Plot 06A: Unit Share")
            csv6a = gr.File(label="CSV: Unit Share")
            img6ab = gr.Image(label="Plot 06A (Excl. HK)")
            csv6ab = gr.File(label="CSV: Unit Share (Excl. HK)")
            img6b = gr.Image(label="Plot 06B: Value Share")
            csv6b = gr.File(label="CSV: Value Share")
            img6bb = gr.Image(label="Plot 06B (Excl. HK)")
            csv6bb = gr.File(label="CSV: Value Share (Excl. HK)")
            img6c = gr.Image(label="Plot 06C: Unit Count")
            csv6c = gr.File(label="CSV: Unit Count")
            img6cb = gr.Image(label="Plot 06C (Excl. HK)")
            csv6cb = gr.File(label="CSV: Unit Count (Excl. HK)")
            img6d = gr.Image(label="Plot 06D: Value Count")
            csv6d = gr.File(label="CSV: Value Count")
            img6db = gr.Image(label="Plot 06D (Excl. HK)")
            csv6db = gr.File(label="CSV: Value Count (Excl. HK)")

    submit_btn.click(
        fn=process_file,
        inputs=[file_input],
        outputs=[
            img1, csv1, img1b, csv1b,
            img2, csv2, img2b, csv2b,
            img3, csv3, img3b, csv3b,
            img4, csv4, img4b, csv4b,
            img5a, csv5a, img5ab, csv5ab,
            img5b, csv5b, img5bb, csv5bb,
            img6a, csv6a, img6ab, csv6ab,
            img6b, csv6b, img6bb, csv6bb,
            img6c, csv6c, img6cb, csv6cb,
            img6d, csv6d, img6db, csv6db
        ]
    )

if __name__ == "__main__":
    app.launch()

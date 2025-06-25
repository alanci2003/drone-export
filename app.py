from __future__ import annotations

from pathlib import Path

import gradio as gr

from preprocess_drone_exports import clean_data
from plot_01_to_06 import (
    plot_01,
    plot_02,
    plot_03,
    plot_04,
    plot_05,
    plot_06,
)

ASSETS_DIR = Path('assets')


def cleanup_assets():
    if ASSETS_DIR.exists():
        for p in ASSETS_DIR.iterdir():
            if p.is_file():
                p.unlink()
    ASSETS_DIR.mkdir(exist_ok=True)


def process_file(file):
    cleanup_assets()
    clean_csv = clean_data(file.name, ASSETS_DIR)
    p1, c1 = plot_01(clean_csv, ASSETS_DIR)
    p2, c2 = plot_02(clean_csv, ASSETS_DIR)
    p3, c3 = plot_03(clean_csv, ASSETS_DIR)
    p4, c4 = plot_04(clean_csv, ASSETS_DIR)
    p5_list, c5_list = plot_05(clean_csv, ASSETS_DIR)
    p6_list, c6_list = plot_06(clean_csv, ASSETS_DIR)
    return (
        clean_csv,
        p1, c1,
        p2, c2,
        p3, c3,
        p4, c4,
        p5_list[0], c5_list[0],
        p5_list[1], c5_list[1],
        p6_list[0], c6_list[0],
        p6_list[1], c6_list[1],
        p6_list[2], c6_list[2],
        p6_list[3], c6_list[3],
    )


with gr.Blocks() as app:
    gr.Markdown("# Drone Export Analytics")
    with gr.Row():
        uploader = gr.File(label="Upload raw CSV")
        process_btn = gr.Button("Process")
    clean_csv_output = gr.File(label="Cleaned CSV")

    with gr.Tabs():
        with gr.Tab("01 - Unit Count"):
            img1 = gr.Image()
            csv1 = gr.File(label="Download CSV")
        with gr.Tab("02 - Unit Share"):
            img2 = gr.Image()
            csv2 = gr.File(label="Download CSV")
        with gr.Tab("03 - Export Value"):
            img3 = gr.Image()
            csv3 = gr.File(label="Download CSV")
        with gr.Tab("04 - Value Share"):
            img4 = gr.Image()
            csv4 = gr.File(label="Download CSV")
        with gr.Tab("05 - 2023H2 vs 2024H2"):
            img5a = gr.Image()
            csv5a = gr.File(label="Download CSV")
            img5b = gr.Image()
            csv5b = gr.File(label="Download CSV")
        with gr.Tab("06 - 2023H2 vs 2025Q1"):
            img6a = gr.Image()
            csv6a = gr.File(label="Download CSV")
            img6b = gr.Image()
            csv6b = gr.File(label="Download CSV")
            img6c = gr.Image()
            csv6c = gr.File(label="Download CSV")
            img6d = gr.Image()
            csv6d = gr.File(label="Download CSV")

    process_btn.click(
        fn=process_file,
        inputs=uploader,
        outputs=[
            clean_csv_output,
            img1, csv1,
            img2, csv2,
            img3, csv3,
            img4, csv4,
            img5a, csv5a, img5b, csv5b,
            img6a, csv6a, img6b, csv6b, img6c, csv6c, img6d, csv6d,
        ],
    )

if __name__ == "__main__":
    app.launch()

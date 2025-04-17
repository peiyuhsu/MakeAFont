import sys
from pathlib import Path
from pdf2image import convert_from_path
from PIL import Image

if len(sys.argv) < 2:
    print("❗請提供 PDF 檔案名稱，例如：python3 cut_chars_indexed.py myfile.pdf")
    sys.exit(1)

INPUT_PDF = sys.argv[1]
OUTPUT_DIR = Path(f"output/{Path(INPUT_PDF).stem}")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 格線參數（v9）
grid_rows = 7
grid_cols = 5
cell_width = 340
cell_height = 340
padding_x = 70
padding_y = 70
offset_x = 235
offset_y = 210

def extract_and_index(img: Image.Image, page_index: int):
    count = 0
    for row in range(grid_rows):
        for col in range(grid_cols):
            left = offset_x + col * (cell_width + padding_x)
            upper = offset_y + row * (cell_height + padding_y)
            right = left + cell_width
            lower = upper + cell_height
            cropped = img.crop((left, upper, right, lower))
            filename = f"page{page_index:02d}_idx{count:02d}.png"
            cropped.save(OUTPUT_DIR / filename)
            count += 1

def main():
    images = convert_from_path(INPUT_PDF, dpi=300)
    for i, img in enumerate(images):
        extract_and_index(img, i)
    print(f"✅ 已儲存切割圖片至：{OUTPUT_DIR.resolve()}")

if __name__ == "__main__":
    main()
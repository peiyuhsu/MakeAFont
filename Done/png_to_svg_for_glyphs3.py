#!/usr/bin/env python3
"""
批次將PNG檔案轉換為Glyphs 3相容的SVG檔案
需要安裝以下套件：
- pip install pillow potrace svgpathtools numpy
"""

import os
import sys
import glob
from PIL import Image
import potrace
import numpy as np
from svgpathtools import parse_path, wsvg, Path, Line
import re

# 設定
INPUT_DIR = './'  # 輸入目錄，包含PNG檔案
OUTPUT_DIR = './svg_output/'  # 輸出目錄
THRESHOLD = 128  # 二值化閥值 (0-255)
TURDSIZE = 2  # potrace參數：忽略小於此大小的區域
ALPHAMAX = 1.0  # potrace參數：角度閥值
OPTTOLERANCE = 0.2  # potrace參數：最佳化誤差
SCALE = 1.0  # 縮放比例

# 確保輸出目錄存在
os.makedirs(OUTPUT_DIR, exist_ok=True)

def bitmap_to_potrace_bitmap(bitmap):
    """將numpy陣列轉換為potrace可接受的bitmap格式"""
    potrace_bitmap = potrace.Bitmap(bitmap.shape[1], bitmap.shape[0])
    for y in range(bitmap.shape[0]):
        for x in range(bitmap.shape[1]):
            potrace_bitmap.put(x, y, bitmap[y, x])
    return potrace_bitmap

def bitmap_to_svg_path(bitmap, name='path', optimize=True):
    """將bitmap轉換為SVG路徑"""
    bm = bitmap_to_potrace_bitmap(bitmap)
    
    # potrace設定
    param = potrace.Param()
    param.turdsize = TURDSIZE
    param.alphamax = ALPHAMAX
    param.opttolerance = OPTTOLERANCE
    param.optimize = optimize
    
    # 進行路徑追蹤
    plist = bm.trace(param)
    
    # 生成SVG路徑
    svg_paths = []
    path_data = ""
    
    # 處理所有輪廓
    for curve in plist.curves:
        segments = curve.segments
        if not segments:
            continue
            
        # 開始路徑
        start = segments[0].start_point
        path_data += f"M {start.x} {start.y} "
        
        # 繪製所有段落
        for segment in segments:
            if segment.is_corner:
                c = segment.c
                path_data += f"L {c.x} {c.y} "
                end = segment.end_point
                path_data += f"L {end.x} {end.y} "
            else:
                c1, c2 = segment.c1, segment.c2
                end = segment.end_point
                path_data += f"C {c1.x} {c1.y} {c2.x} {c2.y} {end.x} {end.y} "
        
        # 閉合路徑
        path_data += "Z "
    
    # 返回SVG路徑數據
    return path_data

def invert_coordinates(path_data, height):
    """反轉Y座標 (Glyphs使用不同的座標系統)"""
    path = parse_path(path_data)
    transformed_path = Path()
    
    for segment in path:
        if isinstance(segment, Line):
            # 簡單地反轉Y座標
            start = complex(segment.start.real, height - segment.start.imag)
            end = complex(segment.end.real, height - segment.end.imag)
            transformed_path.append(Line(start, end))
        else:
            # 對於其他類型的段落，也需要反轉控制點
            start = complex(segment.start.real, height - segment.start.imag)
            end = complex(segment.end.real, height - segment.end.imag)
            
            if hasattr(segment, 'control1'):
                control1 = complex(segment.control1.real, height - segment.control1.imag)
            else:
                control1 = None
                
            if hasattr(segment, 'control2'):
                control2 = complex(segment.control2.real, height - segment.control2.imag)
            else:
                control2 = None
                
            # 創建相同類型的新段落但Y座標已翻轉
            new_segment = segment.__class__(start, end, control1, control2)
            transformed_path.append(new_segment)
    
    return transformed_path.d()

def extract_unicode_from_filename(filename):
    """從檔名提取Unicode編碼"""
    match = re.search(r'uni([0-9A-F]{4,6})\.png$', filename)
    if match:
        return match.group(1)
    return None

def create_svg_for_glyphs(path_data, width, height, unicode_hex, output_file):
    """建立適合Glyphs 3的SVG檔案"""
    # 調整座標系，Glyphs使用左下角為原點
    # 反轉Y座標
    transformed_path = invert_coordinates(path_data, height)
    
    # 創建SVG檔案
    svg_content = f"""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
    <g id="glyph{unicode_hex}">
        <path d="{transformed_path}" fill="black" />
    </g>
</svg>"""
    
    # 寫入檔案
    with open(output_file, 'w') as f:
        f.write(svg_content)

def preprocess_image(image_path):
    """預處理圖像：載入、轉灰階、二值化"""
    # 載入圖像
    image = Image.open(image_path)
    
    # 轉換為灰階
    if image.mode != 'L':
        image = image.convert('L')
    
    # 二值化處理
    image_array = np.array(image)
    binary_image = (image_array < THRESHOLD).astype(np.uint8)
    
    return binary_image, image.width, image.height

def process_png_file(png_file):
    """處理單一PNG檔案並轉換為SVG"""
    try:
        # 提取Unicode碼
        unicode_hex = extract_unicode_from_filename(os.path.basename(png_file))
        if not unicode_hex:
            print(f"警告：無法從檔名提取Unicode碼：{png_file}")
            # 使用檔名作為輸出
            output_name = os.path.splitext(os.path.basename(png_file))[0]
        else:
            output_name = f"uni{unicode_hex}"
        
        # 預處理圖像
        binary_image, width, height = preprocess_image(png_file)
        
        # 轉換為SVG路徑
        path_data = bitmap_to_svg_path(binary_image)
        
        # 輸出檔案路徑
        output_file = os.path.join(OUTPUT_DIR, f"{output_name}.svg")
        
        # 建立SVG檔案
        create_svg_for_glyphs(path_data, width, height, unicode_hex or "unknown", output_file)
        
        print(f"已轉換：{png_file} -> {output_file}")
        return True
    
    except Exception as e:
        print(f"錯誤處理檔案 {png_file}: {str(e)}")
        return False

def batch_process():
    """批次處理所有PNG檔案"""
    # 找出所有PNG檔案
    png_files = glob.glob(os.path.join(INPUT_DIR, "*.png"))
    
    if not png_files:
        print(f"在目錄 {INPUT_DIR} 中未找到PNG檔案")
        return
    
    print(f"找到 {len(png_files)} 個PNG檔案，開始處理...")
    
    success_count = 0
    for png_file in png_files:
        if process_png_file(png_file):
            success_count += 1
    
    print(f"完成！成功轉換 {success_count}/{len(png_files)} 個檔案到 {OUTPUT_DIR}")

if __name__ == "__main__":
    batch_process()

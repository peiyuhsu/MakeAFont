# Glyphs 3 SVG匯入指南

## SVG檔案結構要求

要成功導入Glyphs 3的SVG檔案應符合以下條件：

1. **單一路徑**：每個字符最好由單一路徑組成，或組織成適當的路徑群組
2. **座標系統**：Glyphs 3使用從左下角開始的座標系統，與標準SVG不同
3. **路徑方向**：外部路徑應為順時針方向，內部路徑（如「o」中的洞）應為逆時針方向
4. **閉合路徑**：所有路徑應正確閉合
5. **路徑ID**：建議使用`glyph`加Unicode碼作為ID
6. **填充屬性**：路徑應有正確的填充屬性（通常為黑色填充）

## 批次匯入SVG到Glyphs 3

### 方法一：拖放操作

1. 啟動Glyphs 3應用程式
2. 建立新字體檔案或開啟現有檔案
3. 在Finder/檔案總管中選擇多個SVG檔案
4. 將選擇的檔案拖曳到Glyphs 3視窗中

Glyphs將嘗試根據檔案名稱自動匹配字符。

### 方法二：使用腳本匯入

Glyphs 3支援Python腳本，您可以使用以下步驟：

1. 在Glyphs 3中選擇「Script」>「Open Scripts Folder」
2. 將以下腳本保存為`ImportSVGFolder.py`：

```python
# ImportSVGFolder.py
# 批次從文件夾導入SVG到Glyphs
# 菜單項: File > Import > SVG Folder

import os
import re
from GlyphsApp import Glyphs, GSGlyph

def run(sender):
    font = Glyphs.font
    if not font:
        Glyphs.showNotification("錯誤", "請先開啟一個字體檔案")
        return
    
    # 選擇文件夾
    folder = Glyphs.chooseFolder()
    if not folder:
        return
        
    count = 0
    for filename in os.listdir(folder):
        if not filename.lower().endswith(".svg"):
            continue
            
        # 從檔名提取Unicode
        match = re.search(r'uni([0-9A-F]{4,6})\.svg$', filename)
        if match:
            unicode_hex = match.group(1)
            
            # 建立字符
            glyph_name = Glyphs.niceGlyphName(chr(int(unicode_hex, 16)))
            
            # 檢查字符是否已存在
            glyph = font.glyphs[glyph_name]
            if not glyph:
                glyph = GSGlyph()
                glyph.name = glyph_name
                glyph.unicode = unicode_hex
                font.glyphs.append(glyph)
            
            # 匯入SVG
            filepath = os.path.join(folder, filename)
            try:
                glyph.importSVG_firstMasterOnly_(filepath)
                count += 1
            except Exception as e:
                Glyphs.showNotification("錯誤", f"無法匯入 {filename}: {str(e)}")
    
    Glyphs.showNotification("匯入完成", f"成功匯入 {count} 個SVG檔案")

```

3. 重新啟動Glyphs 3
4. 在菜單中選擇「File > Import > SVG Folder」
5. 選擇包含SVG檔案的文件夾

### 方法三：使用命令列工具

Glyphs 3提供命令列工具，可用於批次處理：

```bash
/Applications/Glyphs\ 3.app/Contents/MacOS/Glyphs -NSDocumentRevisionsDebugMode YES batch-import-svg /path/to/svgs /path/to/output.glyphs
```

## 匯入後的處理

匯入SVG後，可能需要進行以下調整：

1. **調整大小和位置**：使用Glyphs的Transform工具調整字符大小和位置
2. **調整基線**：檢查並調整字符的基線位置
3. **路徑最佳化**：使用「Path > Tidy up Paths」功能精簡路徑
4. **路徑方向**：使用「Path > Correct Path Direction」修正路徑方向
5. **設置字符寬度**：確保每個字符有正確的寬度設置

## 常見問題

### SVG未顯示或不完整

- 檢查SVG檔案是否有效（可在瀏覽器中打開確認）
- 確保路徑座標系統正確
- 確認是否有路徑超出邊界

### 字符定位問題

- SVG應使用與Glyphs相容的座標系統（左下角為原點）
- 調整字符的垂直對齊和基線

### 複雜SVG的處理

對於非常複雜的SVG，可以考慮：

1. 在Illustrator或Inkscape中簡化路徑
2. 使用SVGO工具最佳化SVG
3. 手動編輯SVG檔案，簡化路徑數據
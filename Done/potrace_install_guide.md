# 安裝必要套件指南

要使用PNG轉SVG腳本，您需要安裝以下Python套件和依賴庫。

## 1. 安裝Python與pip

確保您已經安裝了Python 3.6或更高版本，可以通過以下命令檢查：

```bash
python --version
```

## 2. 安裝所需的Python套件

```bash
pip install pillow numpy svgpathtools potrace
```

### 在Windows上安裝potrace可能需要額外步驟

如果在Windows上安裝`potrace`套件時遇到問題，可以嘗試以下方法：

1. 安裝Visual C++ Build Tools：
   - 下載並安裝[Visual Studio Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
   - 選擇安裝「C++ build tools」組件

2. 使用預編譯的wheel：
   ```bash
   pip install --find-links=https://github.com/tatarize/potrace-wheels/releases/tag/v1.16 potrace
   ```

## 3. 安裝Potrace命令列工具（可選，但推薦）

腳本內部使用的是Python的potrace綁定，但安裝原始的Potrace命令列工具可以提供更多功能和備選方案。

### 在Windows上：
1. 下載[Potrace for Windows](http://potrace.sourceforge.net/#downloading)
2. 解壓縮並將可執行檔案路徑添加到系統PATH

### 在macOS上：
```bash
brew install potrace
```

### 在Linux上：
```bash
# Debian/Ubuntu
sudo apt-get install potrace

# Fedora
sudo dnf install potrace

# Arch Linux
sudo pacman -S potrace
```

## 4. 其他可能有用的工具

- **Inkscape**: 開源向量圖編輯器，可用於手動調整SVG
- **SVGO**: SVG優化工具
  ```bash
  npm install -g svgo
  ```

## 安裝驗證

成功安裝後，您可以運行以下Python代碼測試是否一切正常：

```python
import PIL
import numpy
import svgpathtools
import potrace

print("所有依賴項已成功安裝！")
```

若無錯誤訊息，表示安裝成功，可以開始使用轉換腳本。
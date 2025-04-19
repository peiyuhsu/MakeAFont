import os

# 從 list_ext_symbols.txt 讀取所有符號名稱
with open('list_ext_symbols.txt', 'r', encoding='utf-8') as f:
    symbol_names = [line.strip() for line in f if line.strip()]

# 確保沒有任何換行符或特殊字元
symbol_names = [name.strip('\r\n\t ') for name in symbol_names]

# 生成頁面索引，從 page00_idx00 到 page09_idx22
page_idx_files = []
for page in range(10):  # 從 page00 到 page09
    max_idx = 22 if page == 9 else 34  # page09 只到 idx22
    for idx in range(max_idx + 1):  # +1 是為了包含最後一個索引
        page_idx_files.append(f"page{page:02d}_idx{idx:02d}.png")

# 確認數量和範圍
total_files = len(page_idx_files)
print(f"從 list_ext_symbols.txt 讀取了 {len(symbol_names)} 個符號名稱")
print(f"生成了 {total_files} 個頁面索引 (從 page00_idx00 到 page09_idx22)")

# 建立重命名對照表
rename_pairs = []
for i, symbol in enumerate(symbol_names):
    if i < len(page_idx_files):
        old_name = page_idx_files[i]
        new_name = f"{symbol}.png"
        rename_pairs.append((old_name, new_name))

# 檢查是否有足夠的頁面索引映射所有符號名稱
if len(symbol_names) > len(page_idx_files):
    print(f"警告：還有 {len(symbol_names) - len(page_idx_files)} 個符號名稱未映射")

# 執行重命名操作
print(f"將重命名 {len(rename_pairs)} 個檔案")
print(f"第一個映射: {rename_pairs[0][0]} → {rename_pairs[0][1]}")
print(f"最後一個映射: {rename_pairs[-1][0]} → {rename_pairs[-1][1]}")

# 完整對照表（選擇性打印）
print("\n===== 檔案重命名對照表 =====")
for i, (old, new) in enumerate(rename_pairs):
    print(f"{i+1:3d}. {old} → {new}")

# 實際執行重命名
for old_name, new_name in rename_pairs:
    if os.path.exists(old_name):
        os.rename(old_name, new_name)
        print(f"✔ {old_name} → {new_name}")
    else:
        print(f"⚠ 找不到檔案：{old_name}")

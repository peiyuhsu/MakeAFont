import os

def main():
    # 從 list_ext_naming.txt 讀取所有 Unicode 編碼
    try:
        with open('list_ext_naming.txt', 'r', encoding='utf-8') as f:
            unicode_codes = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print("錯誤：找不到 list_ext_naming.txt 檔案")
        return
    except Exception as e:
        print(f"讀取檔案時發生錯誤：{e}")
        return

    # 生成頁面索引，從 page00_idx00 到 page17_idx22
    page_idx_files = []
    for page in range(18):  # 從 page00 到 page17
        max_idx = 22 if page == 17 else 34  # page17 只到 idx22
        for idx in range(max_idx + 1):  # +1 是為了包含最後一個索引
            page_idx_files.append(f"page{page:02d}_idx{idx:02d}.png")

    # 確認數量和範圍
    print(f"從 list_ext_naming.txt 讀取了 {len(unicode_codes)} 個 Unicode 編碼")
    print(f"生成了 {len(page_idx_files)} 個頁面索引 (從 page00_idx00 到 page17_idx22)")
    
    # 建立重命名對照表
    mapping_table = []
    for i, code in enumerate(unicode_codes):
        if i < len(page_idx_files):
            old_name = page_idx_files[i]
            new_name = f"{code}.png"
            mapping_table.append((old_name, new_name))
    
    # 打印完整對照表
    print("\n===== 檔案重命名對照表 =====")
    for i, (old, new) in enumerate(mapping_table):
        print(f"{i+1:3d}. {old} → {new}")
    
    # 詢問用戶是否執行重命名
    while True:
        choice = input("\n請確認是否執行重命名操作？(Y/N): ").strip().upper()
        if choice == 'Y':
            # 執行重命名操作
            success_count = 0
            missing_count = 0
            for old_name, new_name in mapping_table:
                if os.path.exists(old_name):
                    try:
                        os.rename(old_name, new_name)
                        print(f"✔ {old_name} → {new_name}")
                        success_count += 1
                    except Exception as e:
                        print(f"✘ 重命名失敗 {old_name}：{e}")
                else:
                    print(f"⚠ 找不到檔案：{old_name}")
                    missing_count += 1
            
            # 打印執行結果統計
            print(f"\n重命名完成！成功：{success_count}，找不到：{missing_count}")
            break
        elif choice == 'N':
            print("已取消重命名操作。")
            break
        else:
            print("無效的輸入，請輸入 Y 或 N。")

if __name__ == "__main__":
    main()

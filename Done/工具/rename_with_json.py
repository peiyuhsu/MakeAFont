import json
from pathlib import Path

INPUT_DIR = Path("output/list_base_batch1_done")   # 圖片來源資料夾
JSON_FILE = "校對後.json"
RENAME_DIR = INPUT_DIR / "renamed"
RENAME_DIR.mkdir(parents=True, exist_ok=True)

def char_to_unicode_name(char):
    return f"uni{ord(char):04X}"

def main():
    with open(JSON_FILE, "r", encoding="utf-8") as f:
        items = json.load(f)

    for item in items:
        char = item.get("char")
        index = item.get("index")
        if not char or len(char) != 1:
            print(f"⚠️ 無效字元，跳過：{item}")
            continue

        src = INPUT_DIR / f"{index}.png"
        dst = RENAME_DIR / f"{char_to_unicode_name(char)}.png"
        if not src.exists():
            print(f"❗ 找不到檔案：{src}")
            continue

        src.rename(dst)
        print(f"✅ 重新命名：{src.name} → {dst.name}")

    print(f"\n🎉 所有圖片已重新命名至：{RENAME_DIR.resolve()}")

if __name__ == "__main__":
    main()
    
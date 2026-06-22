import json
import os

input_path = r"c:\laragon\www\kbli\kbli_2025.json"
output_dir = r"c:\laragon\www\kbli"

if not os.path.exists(input_path):
    print(f"Error: {input_path} not found.")
    exit(1)

with open(input_path, 'r', encoding='utf-8') as f:
    items = json.load(f)

kategori_list = []
golongan_pokok_list = []
golongan_list = []
subgolongan_list = []
kelompok_list = []

current_category = None

for item in items:
    level = item["level"]
    code = item["code"]
    title = item["title"]
    desc = item["description"]
    
    if level == "Category":
        current_category = code
        kategori_list.append({
            "code": code,
            "title": title,
            "description": desc
        })
    elif level == "Golongan Pokok":
        golongan_pokok_list.append({
            "code": code,
            "title": title,
            "description": desc,
            "kategori_code": current_category
        })
    elif level == "Golongan":
        parent = code[:-1] # 3 digits -> 2 digits
        golongan_list.append({
            "code": code,
            "title": title,
            "description": desc,
            "golongan_pokok_code": parent
        })
    elif level == "Subgolongan":
        parent = code[:-1] # 4 digits -> 3 digits
        subgolongan_list.append({
            "code": code,
            "title": title,
            "description": desc,
            "golongan_code": parent
        })
    elif level == "Kelompok":
        parent = code[:-1] # 5 digits -> 4 digits
        kelompok_list.append({
            "code": code,
            "title": title,
            "description": desc,
            "subgolongan_code": parent
        })

# Save files
files = {
    "01_kategori.json": kategori_list,
    "02_golongan_pokok.json": golongan_pokok_list,
    "03_golongan.json": golongan_list,
    "04_subgolongan.json": subgolongan_list,
    "05_kelompok.json": kelompok_list
}

# Clean old unnumbered files if they exist
old_files = ["kategori.json", "golongan_pokok.json", "golongan.json", "subgolongan.json", "kelompok.json"]
for old_file in old_files:
    old_path = os.path.join(output_dir, old_file)
    if os.path.exists(old_path):
        os.remove(old_path)
        print(f"Removed old file: {old_path}")

for filename, data in files.items():
    path = os.path.join(output_dir, filename)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Saved {len(data)} items to {path}")


import pypdf
import re
import json
import os

pdf_path = r"c:\laragon\www\kbli\klasifikasi-baku-lapangan-usaha-indonesia--kbli--2025-.pdf"
output_path = r"c:\laragon\www\kbli\kbli_2025.json"

if not os.path.exists(pdf_path):
    print(f"Error: {pdf_path} not found.")
    exit(1)

reader = pypdf.PdfReader(pdf_path)
total_pages = len(reader.pages)
print(f"Total Pages: {total_pages}")

def clean_page(page_text):
    lines = [line.strip() for line in page_text.split('\n') if line.strip()]
    if not lines:
        return []
    
    # Drop first line (header)
    lines_cleaned = lines[1:]
    
    # Drop last line (footer URL)
    if lines_cleaned and ("bps.go.id" in lines_cleaned[-1].lower()):
        lines_cleaned = lines_cleaned[:-1]
        
    final_lines = []
    for l in lines_cleaned:
        if "bps.go.id" in l.lower():
            continue
        if "klasifikasi baku lapangan" in l.lower():
            continue
        final_lines.append(l)
    return final_lines

all_lines = []

# Range of pages containing detailed classification: 247 to 1040 (0-indexed: 246 to 1039)
start_page = 246
end_page = 1040 # exclusive, meaning page 1040 (idx 1039) is included

for idx in range(start_page, min(end_page, total_pages)):
    page_text = reader.pages[idx].extract_text()
    if page_text:
        all_lines.extend(clean_page(page_text))

items = []
current_item = None

# Matches A or 2-5 digits followed by title
code_regex = re.compile(r'^([A-V]|\d{2,5})\s+([A-Z0-9\s,\-\(\)/&’\.\+\*:;\"\'!_]+)$')

for line in all_lines:
    match = code_regex.match(line)
    if match:
        if current_item:
            items.append(current_item)
        code = match.group(1)
        title = match.group(2).strip()
        current_item = {
            "code": code,
            "title": title,
            "description": "",
            "level": "Category" if len(code) == 1 else ["Golongan Pokok", "Golongan", "Subgolongan", "Kelompok"][len(code)-2]
        }
    else:
        if current_item:
            # We want to check if this line is continuation of a multi-line title.
            # Conditions for title continuation:
            # 1. The line is in all uppercase.
            # 2. The description has not started yet.
            # 3. The line doesn't start with standard description prefixes.
            is_desc_start = any(line.startswith(prefix) for prefix in [
                "Kategori ini", "Golongan pokok ini", "Golongan ini", 
                "Subgolongan ini", "Kelompok ini", "Mencakup", "Tidak mencakup",
                "Lihat kelompok", "Lihat subgolongan", "Lihat golongan"
            ])
            
            if not is_desc_start and current_item["description"] == "" and line.isupper() and len(line) > 3:
                current_item["title"] += " " + line
            else:
                if current_item["description"]:
                    current_item["description"] += " " + line
                else:
                    current_item["description"] = line

if current_item:
    items.append(current_item)

# Save to JSON
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(items, f, ensure_ascii=False, indent=2)

print(f"Parsing complete. Saved {len(items)} items to {output_path}")

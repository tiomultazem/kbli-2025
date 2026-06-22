import sqlite3
import json
import os

db_path = r"c:\laragon\www\kbli\kbli_2025.db"
json_dir = r"c:\laragon\www\kbli"

# Hapus DB lama jika ada agar bersih
if os.path.exists(db_path):
    os.remove(db_path)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Aktifkan foreign key support di SQLite
cursor.execute("PRAGMA foreign_keys = ON;")

# 1. Buat Tabel
cursor.execute("""
CREATE TABLE kategori (
    code TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT
);
""")

cursor.execute("""
CREATE TABLE golongan_pokok (
    code TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    kategori_code TEXT,
    FOREIGN KEY (kategori_code) REFERENCES kategori(code) ON DELETE SET NULL
);
""")

cursor.execute("""
CREATE TABLE golongan (
    code TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    golongan_pokok_code TEXT,
    FOREIGN KEY (golongan_pokok_code) REFERENCES golongan_pokok(code) ON DELETE SET NULL
);
""")

cursor.execute("""
CREATE TABLE subgolongan (
    code TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    golongan_code TEXT,
    FOREIGN KEY (golongan_code) REFERENCES golongan(code) ON DELETE SET NULL
);
""")

cursor.execute("""
CREATE TABLE kelompok (
    code TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    subgolongan_code TEXT,
    FOREIGN KEY (subgolongan_code) REFERENCES subgolongan(code) ON DELETE SET NULL
);
""")

conn.commit()

# 2. Impor Data dari JSON
files = [
    {
        "name": "01_kategori.json",
        "table": "kategori",
        "query": "INSERT INTO kategori (code, title, description) VALUES (?, ?, ?)",
        "fields": ["code", "title", "description"]
    },
    {
        "name": "02_golongan_pokok.json",
        "table": "golongan_pokok",
        "query": "INSERT INTO golongan_pokok (code, title, description, kategori_code) VALUES (?, ?, ?, ?)",
        "fields": ["code", "title", "description", "kategori_code"]
    },
    {
        "name": "03_golongan.json",
        "table": "golongan",
        "query": "INSERT INTO golongan (code, title, description, golongan_pokok_code) VALUES (?, ?, ?, ?)",
        "fields": ["code", "title", "description", "golongan_pokok_code"]
    },
    {
        "name": "04_subgolongan.json",
        "table": "subgolongan",
        "query": "INSERT INTO subgolongan (code, title, description, golongan_code) VALUES (?, ?, ?, ?)",
        "fields": ["code", "title", "description", "golongan_code"]
    },
    {
        "name": "05_kelompok.json",
        "table": "kelompok",
        "query": "INSERT INTO kelompok (code, title, description, subgolongan_code) VALUES (?, ?, ?, ?)",
        "fields": ["code", "title", "description", "subgolongan_code"]
    }
]

for f_info in files:
    file_path = os.path.join(json_dir, f_info["name"])
    if not os.path.exists(file_path):
        print(f"Warning: {f_info['name']} not found, skipping.")
        continue
    
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"Importing {len(data)} items into '{f_info['table']}' table...")
    
    insert_data = []
    for item in data:
        row = []
        for field in f_info["fields"]:
            row.append(item.get(field))
        insert_data.append(row)
        
    cursor.executemany(f_info["query"], insert_data)
    conn.commit()

conn.close()
print(f"Success! SQLite database generated at: {db_path}")

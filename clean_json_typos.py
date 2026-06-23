import json
import re
import os

input_path = r"c:\laragon\www\kbli\kbli_2025.json"

if not os.path.exists(input_path):
    print("Error: kbli_2025.json tidak ditemukan.")
    exit(1)

with open(input_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Daftar pola typo yang umum dalam dataset KBLI 2025 hasil ekstraksi PDF BPS.
# Kita petakan kata terpecah ke kata yang benar.
typo_map = {
    r"\bseb\s+agai\b": "sebagai",
    r"\blau\s+t\b": "laut",
    r"\btam\s+bang\b": "tambang",
    r"\bbesa\s+r\b": "besar",
    r"\bberm\s+otor\b": "bermotor",
    r"\bant\s+ara\b": "antara",
    r"\bole\s+h\b": "oleh",
    r"\brepa\s+rasi\b": "reparasi",
    r"\bde\s+ngan\b": "dengan",
    r"\bsos\s+ial\b": "sosial",
    r"\bla\s+han\b": "lahan",
    r"\bkegi\s+atan\b": "kegiatan",
    r"\btang\s+ga\b": "tangga",
    r"\bke\s+rtas\b": "kertas",
    r"\bolah\s+raga\b": "olahraga",
    r"\bbara\s+ng\b": "barang",
    r"\blaha\s+n\b": "lahan",
    r"\bsal\s+uran\b": "saluran",
    r"\bmine\s+ral\b": "mineral",
    r"\bja\s+mu\b": "jamu",
    r"\bumu\s+m\b": "umum",
    r"\bdi\s+ri\b": "diri",
    r"\bter\s+sebut\b": "tersebut",
    r"\bpe\s+nga\s+was\s+an\b": "pengawasan",
    r"\bjas\s+a\b": "jasa",
    r"\bba\s+rang\b": "barang",
    r"\bda\s+lam\b": "dalam",
    r"\bdi\s+la\s+ku\s+kan\b": "dilakukan",
    r"\bbu\s+kan\b": "bukan",
    r"\bpenye\s+diaan\b": "penyediaan",
    r"\bwa\s+ter\b": "water",
    r"\bpenye\s+dia\b": "penyedia",
    r"\bpenyewa\s+an\b": "penyewaan",
    r"\bpem\s+bangunan\b": "pembangunan",
    r"\bpem\s+buatan\b": "pembuatan",
    r"\bpe\s+masangan\b": "pemasangan",
    r"\bpe\s+masaran\b": "pemasaran",
    r"\bper\s+dagangan\b": "perdagangan",
    r"\bper\s+alatan\b": "peralatan",
    r"\bper\s+baikan\b": "perbaikan",
    r"\bper\s+siapan\b": "persiapan",
    r"\bper\s+tambangan\b": "pertambangan",
    r"\bper\s+kebunan\b": "perkebunan",
    r"\bpe\s+ternakan\b": "peternakan",
    r"\bper\s+ikanan\b": "perikanan",
    r"\bper\s+jalanan\b": "perjalanan",
    r"\bper\s+awatan\b": "perawatan",
    r"\bpe\s+merintahan\b": "pemerintahan",
    r"\bper\s+tahanan\b": "pertahanan",
    r"\bpen\s+didikan\b": "pendidikan",
    r"\bke\s+sehatan\b": "kesehatan",
    r"\bke\s+senian\b": "kesenian",
    r"\bre\s+kreasi\b": "rekreasi",
    r"\bor\s+ganisasi\b": "organisasi",
    r"\bper\s+orangan\b": "perorangan",
    r"\bin\s+ternasional\b": "internasional",
    r"\bper\s+tanian\b": "pertanian",
    r"\bke\s+hutanan\b": "kehutanan",
    r"\bpenye\s+liputan\b": "penyeliputan",
    r"\bpenye\s+lidikan\b": "penyelidikan",
    r"\bpeng\s+upasan\b": "pengupasan",
    r"\bpenyi\s+apan\b": "penyiapan",
    r"\bpem\s+bersihan\b": "pembersihan",
    r"\bpeng\s+eringan\b": "pengeringan",
    r"\bbene\s+fisiasi\b": "benefisiasi",
    r"\bkon\s+sentrasi\b": "konsentrasi",
    r"\bpen\s+cairan\b": "pencairan",
    r"\bkla\s+sifikasi\b": "klasifikasi",
    r"\bgo\s+longan\b": "golongan",
    r"\bsub\s+golongan\b": "subgolongan",
    r"\bpen\s+carian\b": "pencarian",
    r"\bper\s+gantian\b": "pergantian",
    r"\bpen\s+dukung\b": "pendukung",
    r"\bpe\s+layanan\b": "pelayanan",
    r"\bpenyega\s+ran\b": "penyegaran",
    r"\bpenyal\s+uran\b": "penyaluran",
    r"\bpemelihara\s+an\b": "pemeliharaan",
    r"\bpen\s+dapatan\b": "pendapatan",
    r"\bper\s+tunjukan\b": "pertunjukan",
    r"\bper\s+judian\b": "perjudian",
    r"\bper\s+taruhan\b": "pertaruhan",
    r"\bper\s+lindungan\b": "perlindungan",
    r"\bper\s+usahaan\b": "perusahaan",
    r"\bper\s+temuan\b": "pertemuan",
    r"\bper\s+mukiman\b": "permukiman",
    r"\bper\s+ekonomian\b": "perekonomian",
    r"\bper\s+undang\b": "perundang",
    r"\bper\s+nyataan\b": "pernyataan",
    r"\bper\s+bedaan\b": "perbedaan",
    r"\bper\s+batasan\b": "perbatasan",
    r"\bper\s+setujuan\b": "persetujuan",
    r"\bper\s+kembangan\b": "perkembangan",
    r"\bper\s+kiran\b": "perkiran",
    r"\bper\s+mintaan\b": "permintaan",
    r"\bper\s+tumbuhan\b": "pertumbuhan",
    r"\bper\s+tandingan\b": "pertandingan",
    r"\bper\s+kelahian\b": "perkelahian",
    r"\bper\s+temenan\b": "pertemenan",
    r"\bper\s+sekutuan\b": "persekutuan",
    r"\bper\s+janjian\b": "perjanjian",
    r"\bper\s+buatan\b": "perbuatan",
    r"\bper\s+aturan\b": "peraturan",
    r"\bper\s+soalan\b": "persoalan",
    r"\bper\s+asaan\b": "perasaan",
    r"\bper\s+bandingan\b": "perbandingan",
    r"\bper\s+sepuluhan\b": "persepuluhan",
    r"\bper\s+hitungan\b": "perhitungan",
    r"\bair\s+lau\s+t\b": "air laut",
    r"\bair\s+ba\s+s\b": "air basah",
    r"\bsaline\s+wa\s+ter\b": "saline water",
    r"\bper\s+wira\b": "perwira",
    r"\bper\s+to\s+lo\s+ngan\b": "pertolongan",
    r"\bkon\s+struksi\b": "konstruksi",
    r"\bin\s+dustri\b": "industri",
    r"\beks\s+traksi\b": "ekstraksi",
    r"\ba\s+suransi\b": "asuransi",
    r"\bpro\s+fesional\b": "profesional",
    r"\bad\s+ministrasi\b": "administrasi",
    r"\bja\s+minan\b": "jaminan",
    r"\bpe\s+nyeliputan\b": "penyeliputan",
    r"\bpe\s+nyelidikan\b": "penyelidikan"
}

modified_count = 0

for item in data:
    orig_title = item.get("title", "")
    orig_desc = item.get("description", "")
    
    title = orig_title
    desc = orig_desc
    
    for pattern, replacement in typo_map.items():
        title = re.sub(pattern, replacement, title, flags=re.IGNORECASE)
        desc = re.sub(pattern, replacement, desc, flags=re.IGNORECASE)
        
    if title != orig_title or desc != orig_desc:
        item["title"] = title
        item["description"] = desc
        modified_count += 1

# Tulis kembali ke kbli_2025.json
with open(input_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Selesai! Memperbaiki {modified_count} item di dalam {input_path}")

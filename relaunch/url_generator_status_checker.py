"""
Shopify URL Generator & Status Checker – Multilingual

Author: Antonio Blago
Date: 2025-05-17

Description:
This script loads product, page, and blog data from Shopify export files,
generates complete multilingual URLs, checks their HTTP status,
and exports everything to an Excel file for further processing (e.g., redirects).

Optional: It also generates a .txt export for Screaming Frog.
"""

import pandas as pd
from pathlib import Path
import requests

# ─────────────── Settings ─────────────── #
DATA_DIR = Path(__file__).resolve().parent / "import_data" / "shop_data"
DOMAIN_URL = "https://example-shop.com"
LANGUAGES = ["", "/de"]  # "" = default language (e.g., en); add more like "/fr", "/it" if needed

FILE_MAP = {
    "products": ("/products/", "product"),
    "custom_collections": ("/collections/", "collection"),
    "smart_collections": ("/collections/", "collection"),
    "pages": ("/pages/", "page"),
    "blog_posts": ("/blogs/news/", "blog_post")  # optionally adjust blog handle
}

frames_all = []

print("📁 Found CSV files:")
for file in DATA_DIR.glob("*.csv"):
    print("–", file.name)

# ─────────────── Process each CSV ─────────────── #
for file in DATA_DIR.glob("*.csv"):
    filename = file.name.lower()

    for key, (prefix, content_type) in FILE_MAP.items():
        if key in filename:
            try:
                df = pd.read_csv(file)
                if "Handle" not in df.columns:
                    print(f"⚠️ 'Handle' column missing in: {file.name}")
                    break

                df = df.dropna(subset=["Handle"])
                df["Handle"] = df["Handle"].astype(str).str.strip()

                for lang in LANGUAGES:
                    df_lang = pd.DataFrame({
                        "path": lang + prefix + df["Handle"],
                        "type": content_type,
                        "lang": lang.strip("/") or "default"
                    })
                    frames_all.append(df_lang)

                print(f"✅ Processed: {file.name} ({len(df)} entries)")

            except Exception as e:
                print(f"❌ Error in {file.name}: {e}")
            break  # only process the first matching file type per file

# ─────────────── Merge & Enrich ─────────────── #
if not frames_all:
    raise ValueError("❌ No valid Shopify files found.")

df_all = pd.concat(frames_all, ignore_index=True)
df_all["url"] = DOMAIN_URL + df_all["path"]
df_all["slug"] = df_all["path"].str.strip("/")

# ─────────────── HTTP Status Check ─────────────── #
print("\n🌐 Checking HTTP status codes...")
def check_status(url):
    try:
        response = requests.head(url, timeout=5, allow_redirects=True)
        return response.status_code
    except Exception as e:
        return str(e)

df_all["http_status"] = df_all["url"].apply(check_status)

# ─────────────── Excel Export ─────────────── #
output_file = DATA_DIR / "shop_urls_multilang_checked.xlsx"
df_all.to_excel(output_file, index=False)
print(f"\n📦 Export with HTTP status completed: {output_file}")

# ─────────────── Screaming Frog Export ─────────────── #
screamingfrog_path = DATA_DIR / "shop_urls_for_screamingfrog.txt"
df_all["url"].to_csv(screamingfrog_path, index=False, header=False)
print(f"📤 Exported URLs for Screaming Frog: {screamingfrog_path}")

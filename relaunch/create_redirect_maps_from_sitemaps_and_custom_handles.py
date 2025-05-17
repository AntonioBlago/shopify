import pandas as pd
import requests
from urllib.parse import urljoin
from xml.etree import ElementTree as ET
import os

# === CONFIGURATION ===
excel_path = r"./redirect_mapping_input.xlsx"         # Path to Excel file with mapping info
output_dir = r"./redirect_exports"                    # Directory to save output CSV files
sitemap_index_url = "https://yourshop.com/sitemap.xml"  # Main sitemap index of the original domain
old_domain = "https://yourshop.com"                   # Used to clean old sitemap URLs

# Dictionary of international shops with associated language slugs
dict_of_shops = {
    "https://it.yourshop.com": ["/it/", "/it-it/", "/fr-it/", "/de-it/", "/en-it/"],
    "https://fr.yourshop.com": ["/fr/", "/fr-fr/", "/de-fr/", "/it-fr/", "/en-fr/"]
}

# Function to validate a source URL (customizable if needed)
def is_source_url_valid(source_path, *args, **kwargs):
    return True

# Parse sitemap index and filter by language slug and type fragment
def parse_sitemap_index_filtered(slugs):
    urls = set()
    selected_sitemaps = []

    valid_fragments = [
        "sitemap_products_",
        "sitemap_pages_",
        "sitemap_collections_",
        "sitemap_blogs_"
    ]

    try:
        response = requests.get(sitemap_index_url, timeout=10)
        if response.status_code == 200:
            tree = ET.fromstring(response.content)
            ns = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}

            for sitemap in tree.findall('ns:sitemap', ns):
                loc = sitemap.find('ns:loc', ns)
                if loc is not None and loc.text:
                    loc_url = loc.text.strip()

                    if any(loc_url.startswith(old_domain + slug) for slug in slugs) and \
                       any(fragment in loc_url for fragment in valid_fragments):
                        selected_sitemaps.append(loc_url)

            for sitemap_url in selected_sitemaps:
                try:
                    sub_response = requests.get(sitemap_url, timeout=10)
                    if sub_response.status_code == 200:
                        sub_tree = ET.fromstring(sub_response.content)
                        for url in sub_tree.findall('ns:url/ns:loc', ns):
                            if url is not None and url.text:
                                urls.add(url.text.strip())
                except Exception as e:
                    print(f"❌ Failed to load {sitemap_url}: {e}")
    except Exception as e:
        print(f"❌ Failed to load sitemap index: {e}")

    return urls

# === MAIN REDIRECT MAPPING LOOP ===
for new_domain, slugs in dict_of_shops.items():
    slugs_string = '_'.join(slug.strip('/') for slug in slugs)
    print(f"\n🔁 Generating redirects for: {new_domain} ({slugs_string})")

    # Initialization
    redirects = []
    custom_redirects = set()
    all_old_handles = set()
    redirect_sources = set()

    # Load live URLs from sitemap (only for current language group)
    print("📥 Loading sitemap URLs...")
    sitemap_urls = parse_sitemap_index_filtered(slugs)
    sitemap_paths = {url.replace(old_domain, "") for url in sitemap_urls}
    print(f"🔍 Found {len(sitemap_paths)} URLs in sitemap for {slugs_string}.")

    # Load Excel with handle mappings
    xls = pd.ExcelFile(excel_path)
    sheet_names = [name for name in xls.sheet_names if "skip" not in name.lower()]

    for sheet in sheet_names:
        df = xls.parse(sheet)
        if 'Handle (Old)' not in df.columns:
            continue

        sheet_lower = sheet.lower()
        if "product" in sheet_lower:
            path_prefix = "products/"
        elif "collection" in sheet_lower:
            path_prefix = "collections/"
        elif "blog" in sheet_lower:
            path_prefix = "blogs/articles/"
        else:
            path_prefix = "pages/"

        print(f"🔄 Processing sheet: {sheet} (prefix: /{path_prefix})")

        if 'Handle (New)' in df.columns:
            for _, row in df.iterrows():
                old_handle = str(row['Handle (Old)']).strip()
                new_handle = str(row['Handle (New)']).strip() if pd.notna(row.get('Handle (New)')) else ""
                all_old_handles.add(old_handle)

                if new_handle and not new_handle.startswith(path_prefix):
                    new_handle = path_prefix + new_handle.lstrip("/")
                target_url = urljoin(new_domain + "/", new_handle or "")

                for slug in slugs:
                    source_path = urljoin(slug, path_prefix + old_handle)
                    if is_source_url_valid(source_path):
                        redirects.append((source_path, target_url, sheet))
                        redirect_sources.add(source_path)
                        if new_handle:
                            custom_redirects.add(source_path)
        else:
            for _, row in df.iterrows():
                old_handle = str(row['Handle (Old)']).strip()
                all_old_handles.add(old_handle)
                for slug in slugs:
                    source_path = urljoin(slug, path_prefix + old_handle)
                    if is_source_url_valid(source_path):
                        redirects.append((source_path, new_domain, sheet))
                        redirect_sources.add(source_path)

    # Add fallback redirects for live URLs not in Excel
    sitemap_not_in_redirects = sitemap_paths - redirect_sources
    for path in sitemap_not_in_redirects:
        redirects.append((path, new_domain, "Auto-Fallback"))

    # Statistics
    stats = {
        "Handles in Excel": len(all_old_handles),
        f"Sitemap URLs for {slugs_string}": len(sitemap_paths),
        "Custom redirects (mapped)": len(sitemap_paths & custom_redirects),
        "Fallback redirects (unmapped)": len(sitemap_not_in_redirects),
        "Sitemap URLs not in Excel": len(sitemap_paths - redirect_sources),
        "Total redirects created": len(set(redirects))
    }

    # === EXPORT ===
    os.makedirs(output_dir, exist_ok=True)

    df_redirects = pd.DataFrame(set(redirects), columns=["Redirect from", "Redirect to", "Source"])
    df_redirects.to_csv(os.path.join(output_dir, f"redirects_{slugs_string}.csv"), index=False)

    df_final = df_redirects[["Redirect from", "Redirect to"]]
    df_final.to_csv(os.path.join(output_dir, f"redirects_upload_{slugs_string}.csv"), index=False)

    df_missing = pd.DataFrame(sorted(sitemap_not_in_redirects), columns=["Missing Sitemap URLs"])
    df_missing.to_csv(os.path.join(output_dir, f"missing_{slugs_string}.csv"), index=False)

    df_stats = pd.DataFrame(stats.items(), columns=["Metric", "Value"])
    df_stats.to_csv(os.path.join(output_dir, f"redirect_stats_{slugs_string}.csv"), index=False)

    print(f"✅ Export complete for {slugs_string}.")

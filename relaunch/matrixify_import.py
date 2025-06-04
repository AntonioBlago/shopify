import pandas as pd
from urllib.parse import urlparse

# ─────────────── Settings ─────────────── #
INPUT_FILE = r"./slug_keyword_url_mapping.xlsx"  # Input Excel file with source and target URL mapping
REDIRECT_EXPORT = "redirects_import.csv"         # Output file for redirect import (CSV)
NO_MATCH_EXPORT = "redirects_no_match.xlsx"      # Output file for unmatched entries (Excel)
STATS_EXPORT = "redirects_by_type.xlsx"          # Output file for stats by type (Excel)

MATCH_COLUMN = "matched_final"   # Column with matched (target) URLs
URL_COLUMN = "url"               # Column with original source URLs
TYPE_COLUMN = "type"             # Column indicating content type (optional)

# ─────────────── Helper function ─────────────── #
def get_path(url):
    """Extract the path part from a full URL (e.g. '/products/example')."""
    try:
        return urlparse(str(url)).path
    except:
        return ""

# ─────────────── Load & Filter Data ─────────────── #
df = pd.read_excel(INPUT_FILE)

# Filter out valid matches (everything that is not 'no match')
df_valid = df[df[MATCH_COLUMN].str.lower() != "no match"].copy()

# Filter out rows where no match was found
df_no_match = df[df[MATCH_COLUMN].str.lower() == "no match"].copy()

# ─────────────── Print Redirect Stats ─────────────── #
stats = {
    "Total entries": len(df),
    "Valid redirects": len(df_valid),
    "No match entries removed": len(df_no_match)
}
print("🔢 Redirect Statistics:")
for k, v in stats.items():
    print(f"- {k}: {v}")

# ─────────────── Optional: Count Redirects per Type ─────────────── #
if TYPE_COLUMN in df_valid.columns:
    type_counts = df_valid[TYPE_COLUMN].value_counts().reset_index()
    type_counts.columns = ["Type", "Redirects"]
    print("\n🔎 Redirects by Type:")
    print(type_counts.to_string(index=False))

    # Export type breakdown to Excel
    type_counts.to_excel(STATS_EXPORT, index=False)
    print(f"✅ Type breakdown saved: {STATS_EXPORT}")

# ─────────────── Create Redirect Import File ─────────────── #
df_redirects = pd.DataFrame()

# Columns expected by Matrixify: "Redirect from", "Redirect to", "Redirect Type", "Command"
df_redirects["Redirect from"] = df_valid[URL_COLUMN].apply(get_path)
df_redirects["Redirect to"] = df_valid[MATCH_COLUMN].apply(get_path)

# Use per-entry redirect type if available, otherwise default to 301
if TYPE_COLUMN in df_valid.columns:
    df_redirects["Redirect Type"] = df_valid[TYPE_COLUMN]
else:
    df_redirects["Redirect Type"] = "301"

# Required command column for Matrixify imports
df_redirects["Command"] = "MERGE"

# Export redirect import CSV
df_redirects.to_csv(REDIRECT_EXPORT, index=False)
print(f"✅ Redirect import file saved: {REDIRECT_EXPORT}")

# Save entries that had no match for review
if not df_no_match.empty:
    df_no_match.to_excel(NO_MATCH_EXPORT, index=False)
    print(f"⚠️ No match export saved: {NO_MATCH_EXPORT}")


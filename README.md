# 🛍️ Shopify SEO Scripts by Antonio Blago

This repository contains a curated set of **Shopify-focused Python tools** to support:

- 🔄 Store **relaunches** & multilingual domain migrations  
- 🧠 **SEO automation** and redirect management  
- 📦 **URL mapping** and redirect creation based on sitemaps or handles  
- 📊 Export workflows for Shopify, Screaming Frog & Matrixify

> ⚙️ Built for real-world SEO scenarios in international e-commerce.

---

## 📁 Folder Structure

```

shopify/
├── relaunch/
│   ├── create\_redirect\_maps\_from\_sitemaps\_and\_custom\_handles.py
│   ├── matrixify\_import.py
│   ├── url\_generator\_status\_checker.py
│   └── requirements.txt
├── LICENSE
└── README.md

````

---

## 🚀 Included Scripts

### 🔧 [`url_generator_status_checker.py`](./relaunch/url_generator_status_checker.py)

Generates multilingual Shopify URLs from exported CSVs and checks their live status.

**Features:**
- Parses product, page, collection, and blog exports
- Supports language-specific paths (e.g. `/`, `/de/`, `/fr/`)
- Validates URLs via HTTP status codes
- Exports `.xlsx` files for mapping and `.txt` lists for Screaming Frog

**Use cases:**
- Preparing redirect mapping lists  
- Validating existing page visibility  
- SEO audits for localized content

---

### 🌍 [`create_redirect_maps_from_sitemaps_and_custom_handles.py`](./relaunch/create_redirect_maps_from_sitemaps_and_custom_handles.py)

Creates full redirect mappings by combining:

- 🔎 Shopify sitemap URLs
- 🧾 Excel handle mappings (Old → New)
- 🔄 Fallbacks for all live but unmapped URLs

**Outputs per domain/locale:**
- `redirects_*.csv`: full mapping
- `redirects_upload_*.csv`: clean import version
- `missing_*.csv`: sitemap gaps
- `redirect_stats_*.csv`: structured stats

**Use cases:**
- International relaunches  
- Shopify migration coverage  
- SEO redirect coverage validation

---

### 📤 [`matrixify_import.py`](./relaunch/matrixify_import.py)

Prepares a clean Matrixify import file for bulk redirects into Shopify.

**Features:**
- Converts existing redirect lists to Matrixify-compatible format
- Adds `Redirect from`, `Redirect to`, `Redirect Type`, and `Command`
- Optional: supports dynamic or static redirect types

**Use cases:**
- Shopify-compatible import workflows  
- Bulk redirect upload after relaunch  
- Structured file handover to developers

---

## ⚙️ Tech Stack

- Python 3.8+
- pandas, requests
- openpyxl, lxml
- tqdm (progress bars)
- xml.etree or BeautifulSoup for parsing

---

## 📦 Install Requirements

Install all dependencies via:

```bash
pip install -r relaunch/requirements.txt
````

Content of `requirements.txt`:

```txt
pandas>=1.3.0
requests>=2.26.0
openpyxl>=3.0.0
lxml>=4.9.0
tqdm>=4.64.0
```

---

## 📖 How to Use

1. **Clone the repository**

```bash
git clone https://github.com/AntonioBlago/shopify.git
cd shopify/relaunch
```

2. **Install Python dependencies**

```bash
pip install -r requirements.txt
```

3. **Run any script**

```bash
python url_generator_status_checker.py
```

> Place your exported Shopify data in an `import_data/` directory or adjust paths in the scripts as needed.

---

## 👤 Author

**Antonio Blago**
🔗 [antonioblago.de](https://antonioblago.de)
📬 SEO Automation · Data Workflows · Shopify Migrations

---

## 📄 License

[MIT License](./LICENSE) — free to use, adapt, and contribute.

---

## 🔮 Coming Soon

* 🧩 Liquid template analyzers for SEO issues
* 🔗 Canonical & redirect tag validators
* 📈 Google Search Console (GSC) API & Indexing API integrations
* 🤖 GPT-assisted redirect recommendations
* 📊 Matrixify bulk update with preview mode

---

**💡 Feedback, suggestions, or contributors welcome!**


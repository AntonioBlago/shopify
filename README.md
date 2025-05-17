### 📄 Shopify SEO Scripts

# 🛍️ Shopify Tools by Antonio Blago

This repository is a curated collection of **Shopify-specific scripts** to support:

- 🔄 Store **relaunches** & migrations  
- 📦 Product & content **URL handling**  
- 🧠 SEO automation & technical monitoring  
- 📊 Export & integration workflows (e.g. Screaming Frog, GSC)

> ✨ Built with performance, flexibility, and automation in mind.

---

## 📁 Folder Overview

```

shopify/
├── relaunch/               # Scripts for relaunch prep & URL validation
│   └── url\_generator\_status\_checker.py
├── LICENSE
└── README.md

````

---

## 🚀 Included Scripts

### 🔧 [`url_generator_status_checker.py`](./relaunch/url_generator_status_checker.py)

A multilingual automation script that:
- Generates clean Shopify URLs from exported `.csv` data
- Supports multilingual paths (e.g. `/`, `/de/`, `/fr/`)
- Checks HTTP status codes for each generated URL
- Exports full `.xlsx` mapping and a `.txt` list for Screaming Frog

Ideal for:
- Preparing redirect mappings for relaunches
- Validating availability of localized URLs
- Auditing products, blogs, and custom pages

👉 Full usage docs in the [Wiki](https://github.com/AntonioBlago/shopify/wiki)

---

## 🧪 Tech Stack

- Python 3.8+
- pandas, requests
- openpyxl (for Excel export)
- GitHub + CLI / Screaming Frog integration

---

## 📖 How to Use

1. Clone this repository  
   ```bash
   git clone https://github.com/AntonioBlago/shopify.git


2. Navigate to a module (e.g. `relaunch/`)

   ```bash
   cd shopify/relaunch
   ```

3. Install dependencies

   ```bash
   pip install -r requirements.txt  # or manually: pandas requests openpyxl
   ```

4. Run the script with your exported Shopify data in `import_data/`

---

## 🧠 Author

**Antonio Blago**
[🔗 antonioblago.de](https://antonioblago.de)
SEO Automation • Data Workflows • E-Commerce Analytics

---

## 📄 License

MIT – free to use, modify, and contribute.

---

## 📌 Coming Soon

* Liquid template analyzers
* Google Search Console API integrations
* Automatic canonical & redirect validators


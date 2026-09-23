# 🛒 Supermarket Sales Analysis

A full-stack Python data analytics project that ingests, cleans, analyses, and visualises supermarket sales data across 4 Indian cities through an interactive **Streamlit** dashboard.

---

## 📂 Project Structure

```
Supermarket-Sales/
├── Supermarket-data.csv        # Raw dataset (500 transactions)
├── data_cleaning.py            # Data loading, cleaning & validation
├── analysis.py                 # Business metrics & insights
├── app.py                      # Streamlit dashboard (main entry point)
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── data/
│   └── supermarket_clean.csv   # Cleaned dataset output
└── reports/
    └── Supermarket_Sales_Report.docx
```

---

## 📊 Dataset Overview

| Field | Details |
|---|---|
| **File** | `Supermarket-data.csv` |
| **Rows** | 500 transactions |
| **Columns** | Invoice ID, Date, Branch, City, Customer Type, Gender, Product, Category, Quantity, Unit Price, Payment, Rating, Sales |
| **Branches** | A – Jaipur, B – Delhi, C – Mumbai, D – Bengaluru |
| **Date Range** | Jan 2026 – Jul 2026 |
| **Categories** | Beverages, Personal Care, Dairy, Grocery, Fruits, Snacks, Vegetables, Bakery |

---

## 🚀 Getting Started

### 1. Clone / Download the project

```bash
git clone https://github.com/your-username/supermarket-sales.git
cd supermarket-sales
```

### 2. Create & activate a virtual environment (recommended)

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS / Linux
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Streamlit dashboard

```bash
streamlit run app.py
```

The dashboard opens automatically at **http://localhost:8501**.

---

## 🧹 Data Cleaning Pipeline

Run independently with:

```bash
python data_cleaning.py
```

Steps performed:
- Load raw CSV (500 rows × 13 columns)
- Check and drop missing values
- Remove duplicate rows
- Parse `Date` to `datetime64`
- Validate `Sales = Quantity × Unit Price`
- Derive `Month`, `Month_Name`, `DayOfWeek` columns
- Save clean output to `data/supermarket_clean.csv`

---

## 📈 Business Insights

Run the analysis script standalone:

```bash
python analysis.py
```

| # | Question | Answer |
|---|---|---|
| 1 | Top product by sales? | **Cheese** (₹27,906) |
| 2 | Best performing branch? | **Branch C – Mumbai** (₹72,469) |
| 3 | Top category? | **Beverages** (₹56,108) |
| 4 | Most popular payment? | **UPI** (127 transactions) |
| 5 | Members vs Normal spend? | Members ₹1,43,009 vs Normal ₹1,01,402 |
| 6 | Average customer rating? | **3.99 / 5** |

---

## 🖥️ Dashboard Features

| Section | Charts |
|---|---|
| **KPI Row** | Total Revenue, Transactions, Avg Order Value, Avg Rating, Members, Cities |
| **Product & Branch** | Horizontal bar – Products; Grouped bar – Branches |
| **Category & Payment** | Donut pie – Category share; Bar – Payment methods |
| **Monthly Trend** | Spline line chart – Revenue over time |
| **Customer Insights** | Bar – Member vs Normal; Pie – Gender split; Bar – Rating by branch |
| **Heatmap** | Category × Branch sales matrix |
| **Raw Data** | Filterable, scrollable table (collapsible) |

### Sidebar Filters
- Branch (multi-select)
- Category (multi-select)
- Customer Type (multi-select)
- Payment Method (multi-select)
- Date Range (date picker)

---

## 🛠️ Tech Stack

| Library | Version | Purpose |
|---|---|---|
| pandas | 2.2.2 | Data manipulation |
| numpy | 1.26.4 | Numerical computing |
| streamlit | 1.35.0 | Web dashboard |
| plotly | 5.22.0 | Interactive charts |
| matplotlib | 3.8.4 | Static charting support |
| seaborn | 0.13.2 | Statistical visualisations |
| python-docx | 1.1.2 | Report generation |
| openpyxl | 3.1.2 | Excel export support |

---

## 📄 License

MIT License – free to use and modify.

---

*Built with Python & Streamlit · 2026*

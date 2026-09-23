"""
app.py  –  Supermarket Sales Analysis Dashboard
Run with:  streamlit run app.py
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from data_cleaning import load_and_clean

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Supermarket Sales Dashboard",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Main background */
    .main { background-color: #f8fafc; }

    /* Metric cards */
    [data-testid="metric-container"] {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        padding: 16px 20px;
        box-shadow: 0 1px 4px rgba(0,0,0,0.06);
    }
    [data-testid="stMetricValue"] { font-size: 1.6rem !important; font-weight: 700; }
    [data-testid="stMetricLabel"] { font-size: 0.78rem !important; color: #6b7280; text-transform: uppercase; letter-spacing: .05em; }

    /* Section headers */
    .section-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #1f2937;
        border-left: 4px solid #3b82f6;
        padding-left: 10px;
        margin: 1.4rem 0 0.8rem 0;
    }

    /* Sidebar styling */
    [data-testid="stSidebar"] { background-color: #1e293b !important; }
    [data-testid="stSidebar"] * { color: #f1f5f9 !important; }
    [data-testid="stSidebar"] .stMultiSelect > div { background: #334155 !important; }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


# ── Load data ─────────────────────────────────────────────────────────────────
@st.cache_data(show_spinner="Loading & cleaning data …")
def get_data() -> pd.DataFrame:
    return load_and_clean()


df_full = get_data()

# ── Sidebar filters ───────────────────────────────────────────────────────────
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/shopping-cart.png", width=72)
    st.title("🛒 Filters")
    st.markdown("---")

    branches = st.multiselect(
        "Branch",
        options=sorted(df_full["Branch"].unique()),
        default=sorted(df_full["Branch"].unique()),
        format_func=lambda b: f"Branch {b} – {df_full[df_full['Branch']==b]['City'].iloc[0]}",
    )

    categories = st.multiselect(
        "Category",
        options=sorted(df_full["Category"].unique()),
        default=sorted(df_full["Category"].unique()),
    )

    customer_types = st.multiselect(
        "Customer Type",
        options=sorted(df_full["Customer Type"].unique()),
        default=sorted(df_full["Customer Type"].unique()),
    )

    payment_methods = st.multiselect(
        "Payment Method",
        options=sorted(df_full["Payment"].unique()),
        default=sorted(df_full["Payment"].unique()),
    )

    date_min = df_full["Date"].min().date()
    date_max = df_full["Date"].max().date()
    date_range = st.date_input(
        "Date Range",
        value=(date_min, date_max),
        min_value=date_min,
        max_value=date_max,
    )

    st.markdown("---")
    st.caption("Supermarket Sales Analysis · v1.0")

# ── Apply filters ─────────────────────────────────────────────────────────────
if len(date_range) == 2:
    start_date, end_date = pd.Timestamp(date_range[0]), pd.Timestamp(date_range[1])
else:
    start_date, end_date = df_full["Date"].min(), df_full["Date"].max()

df = df_full[
    df_full["Branch"].isin(branches)
    & df_full["Category"].isin(categories)
    & df_full["Customer Type"].isin(customer_types)
    & df_full["Payment"].isin(payment_methods)
    & df_full["Date"].between(start_date, end_date)
].copy()

# ── Header ────────────────────────────────────────────────────────────────────
st.title("🛒 Supermarket Sales Dashboard")
st.markdown(
    f"Showing **{len(df):,}** transactions · "
    f"Total Revenue **₹{df['Sales'].sum():,.0f}** · "
    f"Date Range: **{start_date.date()}** → **{end_date.date()}**"
)
st.markdown("---")

# ── KPI Row ───────────────────────────────────────────────────────────────────
k1, k2, k3, k4, k5, k6 = st.columns(6)
k1.metric("💰 Total Revenue", f"₹{df['Sales'].sum():,.0f}")
k2.metric("🧾 Transactions", f"{len(df):,}")
k3.metric("📦 Avg Order Value", f"₹{df['Sales'].mean():,.0f}")
k4.metric("⭐ Avg Rating", f"{df['Rating'].mean():.2f}")
k5.metric("👥 Members", f"{(df['Customer Type']=='Member').sum():,}")
k6.metric("🏙️ Cities", f"{df['City'].nunique()}")

st.markdown("---")

# ════════════════════════════════════════════════════════════════════════════
#  ROW 1 – Product Sales  &  Branch Performance
# ════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-title">📊 Product & Branch Performance</div>', unsafe_allow_html=True)
col1, col2 = st.columns(2)

with col1:
    prod = df.groupby("Product")["Sales"].sum().sort_values(ascending=True).reset_index()
    fig = px.bar(
        prod,
        x="Sales", y="Product",
        orientation="h",
        title="Total Sales by Product",
        color="Sales",
        color_continuous_scale="Blues",
        labels={"Sales": "Total Sales (₹)"},
        text_auto=".2s",
    )
    fig.update_layout(
        coloraxis_showscale=False,
        plot_bgcolor="#ffffff",
        paper_bgcolor="#ffffff",
        font=dict(family="Segoe UI", size=12),
        title_font_size=15,
        margin=dict(l=10, r=10, t=40, b=10),
        height=400,
    )
    fig.update_traces(textposition="outside")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    branch = df.groupby(["Branch", "City"])["Sales"].sum().reset_index()
    branch["Label"] = "Branch " + branch["Branch"] + "\n" + branch["City"]
    fig2 = px.bar(
        branch,
        x="Label", y="Sales",
        title="Total Sales by Branch",
        color="Branch",
        color_discrete_sequence=px.colors.qualitative.Set2,
        labels={"Sales": "Total Sales (₹)", "Label": ""},
        text_auto=".2s",
    )
    fig2.update_layout(
        showlegend=False,
        plot_bgcolor="#ffffff",
        paper_bgcolor="#ffffff",
        font=dict(family="Segoe UI", size=12),
        title_font_size=15,
        margin=dict(l=10, r=10, t=40, b=10),
        height=400,
    )
    fig2.update_traces(textposition="outside")
    st.plotly_chart(fig2, use_container_width=True)

# ════════════════════════════════════════════════════════════════════════════
#  ROW 2 – Category Breakdown  &  Payment Methods
# ════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-title">🗂️ Category & Payment Insights</div>', unsafe_allow_html=True)
col3, col4 = st.columns(2)

with col3:
    cat = df.groupby("Category")["Sales"].sum().sort_values(ascending=False).reset_index()
    fig3 = px.pie(
        cat,
        names="Category", values="Sales",
        title="Sales Share by Category",
        color_discrete_sequence=px.colors.qualitative.Pastel,
        hole=0.4,
    )
    fig3.update_layout(
        paper_bgcolor="#ffffff",
        font=dict(family="Segoe UI", size=12),
        title_font_size=15,
        margin=dict(l=10, r=10, t=40, b=10),
        height=380,
        legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=1.0),
    )
    fig3.update_traces(textinfo="percent+label", textposition="inside")
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    pay = df["Payment"].value_counts().reset_index()
    pay.columns = ["Payment", "Count"]
    fig4 = px.bar(
        pay,
        x="Payment", y="Count",
        title="Transaction Count by Payment Method",
        color="Payment",
        color_discrete_sequence=px.colors.qualitative.Set3,
        labels={"Count": "No. of Transactions", "Payment": ""},
        text_auto=True,
    )
    fig4.update_layout(
        showlegend=False,
        plot_bgcolor="#ffffff",
        paper_bgcolor="#ffffff",
        font=dict(family="Segoe UI", size=12),
        title_font_size=15,
        margin=dict(l=10, r=10, t=40, b=10),
        height=380,
    )
    fig4.update_traces(textposition="outside")
    st.plotly_chart(fig4, use_container_width=True)

# ════════════════════════════════════════════════════════════════════════════
#  ROW 3 – Monthly Trend
# ════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-title">📅 Monthly Sales Trend</div>', unsafe_allow_html=True)

monthly = (
    df.groupby("Month")["Sales"]
    .sum()
    .reset_index()
    .sort_values("Month")
    .rename(columns={"Sales": "Total Sales"})
)
fig5 = px.line(
    monthly,
    x="Month", y="Total Sales",
    title="Monthly Revenue Trend",
    markers=True,
    line_shape="spline",
    labels={"Total Sales": "Revenue (₹)", "Month": ""},
    color_discrete_sequence=["#3b82f6"],
)
fig5.update_traces(line=dict(width=2.5), marker=dict(size=7))
fig5.update_layout(
    plot_bgcolor="#ffffff",
    paper_bgcolor="#ffffff",
    font=dict(family="Segoe UI", size=12),
    title_font_size=15,
    margin=dict(l=10, r=10, t=40, b=10),
    height=320,
)
st.plotly_chart(fig5, use_container_width=True)

# ════════════════════════════════════════════════════════════════════════════
#  ROW 4 – Customer Insights
# ════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-title">👥 Customer Insights</div>', unsafe_allow_html=True)
col5, col6, col7 = st.columns(3)

with col5:
    cust = df.groupby("Customer Type")["Sales"].agg(["sum", "mean", "count"]).reset_index()
    cust.columns = ["Customer Type", "Total Sales", "Avg Sales", "Transactions"]
    fig6 = px.bar(
        cust,
        x="Customer Type", y="Total Sales",
        title="Member vs Normal — Total Spend",
        color="Customer Type",
        color_discrete_map={"Member": "#3b82f6", "Normal": "#10b981"},
        text_auto=".2s",
        labels={"Total Sales": "Total Sales (₹)", "Customer Type": ""},
    )
    fig6.update_layout(
        showlegend=False,
        plot_bgcolor="#ffffff",
        paper_bgcolor="#ffffff",
        font=dict(family="Segoe UI", size=12),
        title_font_size=14,
        height=320,
    )
    fig6.update_traces(textposition="outside")
    st.plotly_chart(fig6, use_container_width=True)

with col6:
    gender = df.groupby("Gender")["Sales"].sum().reset_index()
    fig7 = px.pie(
        gender,
        names="Gender", values="Sales",
        title="Sales by Gender",
        color_discrete_map={"Male": "#818cf8", "Female": "#f472b6"},
        hole=0.35,
    )
    fig7.update_layout(
        paper_bgcolor="#ffffff",
        font=dict(family="Segoe UI", size=12),
        title_font_size=14,
        height=320,
        margin=dict(l=10, r=10, t=40, b=10),
    )
    fig7.update_traces(textinfo="percent+label")
    st.plotly_chart(fig7, use_container_width=True)

with col7:
    rating_branch = df.groupby("Branch")["Rating"].mean().reset_index()
    rating_branch["Label"] = "Branch " + rating_branch["Branch"]
    fig8 = px.bar(
        rating_branch,
        x="Label", y="Rating",
        title="Avg Rating by Branch",
        color="Rating",
        color_continuous_scale="RdYlGn",
        range_y=[0, 5],
        text_auto=".2f",
        labels={"Rating": "Avg Rating", "Label": ""},
    )
    fig8.update_layout(
        coloraxis_showscale=False,
        plot_bgcolor="#ffffff",
        paper_bgcolor="#ffffff",
        font=dict(family="Segoe UI", size=12),
        title_font_size=14,
        height=320,
    )
    fig8.update_traces(textposition="outside")
    st.plotly_chart(fig8, use_container_width=True)

# ════════════════════════════════════════════════════════════════════════════
#  ROW 5 – Heatmap: Category × Branch
# ════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-title">🔥 Sales Heatmap — Category × Branch</div>', unsafe_allow_html=True)

pivot = df.pivot_table(values="Sales", index="Category", columns="Branch", aggfunc="sum", fill_value=0)
fig9 = go.Figure(
    go.Heatmap(
        z=pivot.values,
        x=[f"Branch {c}" for c in pivot.columns],
        y=pivot.index.tolist(),
        colorscale="Blues",
        text=[[f"₹{v:,.0f}" for v in row] for row in pivot.values],
        texttemplate="%{text}",
        showscale=True,
    )
)
fig9.update_layout(
    title="Sales Distribution: Category vs Branch",
    paper_bgcolor="#ffffff",
    plot_bgcolor="#ffffff",
    font=dict(family="Segoe UI", size=12),
    title_font_size=15,
    margin=dict(l=10, r=10, t=50, b=10),
    height=400,
)
st.plotly_chart(fig9, use_container_width=True)

# ════════════════════════════════════════════════════════════════════════════
#  Raw Data Table (collapsible)
# ════════════════════════════════════════════════════════════════════════════
st.markdown("---")
with st.expander("📋 View Raw Data Table", expanded=False):
    st.dataframe(
        df[["Invoice ID", "Date", "Branch", "City", "Customer Type",
            "Gender", "Product", "Category", "Quantity", "Unit Price",
            "Sales", "Payment", "Rating"]].sort_values("Date", ascending=False),
        use_container_width=True,
        height=400,
    )
    st.caption(f"Showing {len(df):,} rows after applying current filters.")

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown(
    "<br><hr><center style='color:#9ca3af;font-size:0.78rem;'>"
    "Supermarket Sales Analysis Dashboard · Built with Streamlit & Plotly · 2026"
    "</center>",
    unsafe_allow_html=True,
)

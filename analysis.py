"""
analysis.py
Computes the 6 core business metrics for the Supermarket Sales dataset.
Run standalone to print a full text report; also importable by app.py.
"""

import pandas as pd
from data_cleaning import load_and_clean


def run_analysis(df: pd.DataFrame | None = None) -> dict:
    if df is None:
        df = load_and_clean()

    results = {}

    # ── Metric 1: Top product by total sales ─────────────────────────────
    product_sales = (
        df.groupby("Product")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
        .rename(columns={"Sales": "Total Sales"})
    )
    results["product_sales"] = product_sales
    results["top_product"] = product_sales.iloc[0]["Product"]
    results["top_product_sales"] = product_sales.iloc[0]["Total Sales"]

    # ── Metric 2: Best branch by total sales ─────────────────────────────
    branch_sales = (
        df.groupby(["Branch", "City"])["Sales"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
        .rename(columns={"Sales": "Total Sales"})
    )
    branch_sales["Branch_Label"] = "Branch " + branch_sales["Branch"] + " – " + branch_sales["City"]
    results["branch_sales"] = branch_sales
    results["best_branch"] = branch_sales.iloc[0]["Branch_Label"]
    results["best_branch_sales"] = branch_sales.iloc[0]["Total Sales"]

    # ── Metric 3: Top category by total sales ────────────────────────────
    category_sales = (
        df.groupby("Category")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
        .rename(columns={"Sales": "Total Sales"})
    )
    results["category_sales"] = category_sales
    results["top_category"] = category_sales.iloc[0]["Category"]
    results["top_category_sales"] = category_sales.iloc[0]["Total Sales"]

    # ── Metric 4: Most popular payment method ────────────────────────────
    payment_counts = (
        df["Payment"]
        .value_counts()
        .reset_index()
        .rename(columns={"count": "Count"})
    )
    results["payment_counts"] = payment_counts
    results["top_payment"] = payment_counts.iloc[0]["Payment"]
    results["top_payment_count"] = int(payment_counts.iloc[0]["Count"])

    # ── Metric 5: Member vs Normal spend ─────────────────────────────────
    customer_spend = (
        df.groupby("Customer Type")["Sales"]
        .agg(Total="sum", Average="mean", Transactions="count")
        .reset_index()
    )
    results["customer_spend"] = customer_spend

    # ── Metric 6: Average customer rating ────────────────────────────────
    avg_rating = round(df["Rating"].mean(), 2)
    results["avg_rating"] = avg_rating
    rating_by_branch = (
        df.groupby("Branch")["Rating"]
        .mean()
        .round(2)
        .reset_index()
        .rename(columns={"Rating": "Avg Rating"})
    )
    results["rating_by_branch"] = rating_by_branch

    # ── Extra: monthly trend ──────────────────────────────────────────────
    monthly = (
        df.groupby("Month")["Sales"]
        .sum()
        .reset_index()
        .sort_values("Month")
        .rename(columns={"Sales": "Total Sales"})
    )
    results["monthly_trend"] = monthly

    # ── Extra: gender split ───────────────────────────────────────────────
    gender_sales = (
        df.groupby("Gender")["Sales"]
        .sum()
        .reset_index()
        .rename(columns={"Sales": "Total Sales"})
    )
    results["gender_sales"] = gender_sales

    return results


def print_report(results: dict) -> None:
    sep = "=" * 55
    print(f"\n{sep}")
    print("       SUPERMARKET SALES - BUSINESS INSIGHTS REPORT")
    print(f"{sep}")

    print(f"\n{sep}")
    print("1. TOP PRODUCT BY SALES")
    print(sep)
    print(results["product_sales"].to_string(index=False))
    print(f"\nWinner: {results['top_product']}  (Rs {results['top_product_sales']:,.2f})")

    print(f"\n{sep}")
    print("2. BRANCH PERFORMANCE")
    print(sep)
    print(results["branch_sales"][["Branch_Label", "Total Sales"]].to_string(index=False))
    print(f"\nBest Branch: {results['best_branch']}  (Rs {results['best_branch_sales']:,.2f})")

    print(f"\n{sep}")
    print("3. CATEGORY BREAKDOWN")
    print(sep)
    print(results["category_sales"].to_string(index=False))
    print(f"\nTop Category: {results['top_category']}  (Rs {results['top_category_sales']:,.2f})")

    print(f"\n{sep}")
    print("4. PAYMENT METHOD POPULARITY")
    print(sep)
    print(results["payment_counts"].to_string(index=False))
    print(f"\nMost Used: {results['top_payment']}  ({results['top_payment_count']} transactions)")

    print(f"\n{sep}")
    print("5. MEMBER vs NORMAL CUSTOMERS")
    print(sep)
    print(results["customer_spend"].to_string(index=False))

    print(f"\n{sep}")
    print("6. AVERAGE CUSTOMER RATING")
    print(sep)
    print(f"Overall Average Rating: {results['avg_rating']} / 5")
    print("\nBy Branch:")
    print(results["rating_by_branch"].to_string(index=False))

    print(f"\n{'='*55}\n")


if __name__ == "__main__":
    results = run_analysis()
    print_report(results)

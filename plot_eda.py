"""Reproduce the descriptive summaries and Matplotlib figures in the report.

Requirements: Python 3, pandas, numpy, and matplotlib.
Run from any working directory with: python plot_eda.py

The script uses the included, unmodified UCI CSV. It performs descriptive EDA
only; it does not run the course hypothesis test.
"""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parent
CSV_PATH = ROOT / "data" / "online_shoppers_intention.csv"
FIG_DIR = ROOT / "figures"
TABLE_DIR = ROOT / "tables"

GROUP_ORDER = ["New_Visitor", "Returning_Visitor", "Other"]


def main():
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    TABLE_DIR.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(CSV_PATH)

    required = ["VisitorType", "ProductRelated_Duration"]
    missing_columns = [c for c in required if c not in df.columns]
    if missing_columns:
        raise ValueError(f"Required columns are absent: {missing_columns}")

    # Record the category counts before calculating any duration summaries.
    counts = df["VisitorType"].value_counts(dropna=False).reindex(GROUP_ORDER, fill_value=0)
    print("VisitorType counts from raw CSV:")
    print(counts.to_string())
    counts_table = counts.rename_axis("VisitorType").rename("n").to_frame()
    counts_table["Percent"] = counts_table["n"] / len(df) * 100
    counts_table.to_csv(TABLE_DIR / "visitor_type_counts.csv", float_format="%.6f")

    duration = df["ProductRelated_Duration"].astype(float)
    summaries = []
    for group in GROUP_ORDER:
        values = duration[df["VisitorType"] == group].dropna()
        q1, median, q3 = values.quantile([0.25, 0.50, 0.75]).to_numpy()
        iqr = q3 - q1
        summaries.append({
            "VisitorType": group,
            "n": int(values.count()),
            "Mean": values.mean(),
            "SD_sample": values.std(ddof=1),
            "Median": median,
            "Q1": q1,
            "Q3": q3,
            "Min": values.min(),
            "Max": values.max(),
            "Zero_count": int((values == 0).sum()),
            "Upper_1.5IQR_fence": q3 + 1.5 * iqr,
            "Above_upper_fence_n": int((values > q3 + 1.5 * iqr).sum()),
        })
    summary = pd.DataFrame(summaries)
    summary.to_csv(TABLE_DIR / "product_related_duration_summary.csv", index=False, float_format="%.10g")

    # 1. Visitor-type counts. Keep Other separate from the two test groups.
    fig, ax = plt.subplots(figsize=(8, 5))
    x = np.arange(len(GROUP_ORDER))
    y = counts.reindex(GROUP_ORDER).to_numpy()
    bars = ax.bar(x, y, color="steelblue")
    ax.set_xticks(x, ["New visitor", "Returning visitor", "Other"])
    ax.set_ylabel("Number of sessions")
    ax.set_title("Sessions by visitor type")
    ax.grid(axis="y", alpha=0.3)
    ax.set_axisbelow(True)
    for bar, value in zip(bars, y):
        ax.text(bar.get_x() + bar.get_width() / 2, value, f"{value:,}", ha="center", va="bottom")
    ax.set_ylim(0, max(y) * 1.15)
    fig.tight_layout()
    fig.savefig(FIG_DIR / "visitor_type_counts.png", dpi=160)
    plt.close(fig)

    # 2. Histograms for the two research groups on the original scale. Both
    # panels use the same bins, and each bar is the proportion of its full
    # group in that bin, so the larger Returning group does not dominate.
    comparison_groups = ["New_Visitor", "Returning_Visitor"]
    comparison_values = {
        group: duration[df["VisitorType"] == group].dropna().to_numpy()
        for group in comparison_groups
    }
    pooled_values = np.concatenate([comparison_values[group] for group in comparison_groups])
    linear_limit = float(np.quantile(pooled_values, 0.99))
    original_bins = np.linspace(0, linear_limit, 36)
    fig, axes = plt.subplots(2, 1, figsize=(8, 8), sharex=True, sharey=True)
    for ax, group, label in zip(axes, comparison_groups, ["New visitor", "Returning visitor"]):
        group_values = comparison_values[group]
        visible_values = group_values[group_values <= linear_limit]
        weights = np.full(len(visible_values), 1 / len(group_values))
        ax.hist(visible_values, bins=original_bins, weights=weights,
                color="steelblue", edgecolor="white")
        ax.set_title(f"{label} (n = {len(group_values):,})")
        ax.set_ylabel("Proportion")
        ax.text(0.98, 0.92, f"Above display limit: {(group_values > linear_limit).sum()}",
                transform=ax.transAxes, ha="right", va="top")
        ax.grid(axis="y", alpha=0.3)
        ax.set_axisbelow(True)
    axes[-1].set_xlabel("ProductRelated_Duration (dataset units; UCI gives no unit)")
    fig.suptitle(f"Product-related duration by visitor type (original scale; shown to {linear_limit:,.0f})")
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    fig.savefig(FIG_DIR / "duration_histograms_original.png", dpi=160)
    plt.close(fig)

    # 3. Repeat the same two panels after a log10(1 + value) transformation.
    # The +1 allows zero-duration sessions to remain in the plot.
    log_max = float(np.log10(1 + pooled_values.max()))
    log_bins = np.linspace(0, log_max, 36)
    fig, axes = plt.subplots(2, 1, figsize=(8, 8), sharex=True, sharey=True)
    for ax, group, label in zip(axes, comparison_groups, ["New visitor", "Returning visitor"]):
        group_values = comparison_values[group]
        logged_values = np.log10(1 + group_values)
        weights = np.full(len(logged_values), 1 / len(logged_values))
        ax.hist(logged_values, bins=log_bins, weights=weights,
                color="steelblue", edgecolor="white")
        ax.set_title(f"{label} (n = {len(group_values):,})")
        ax.set_ylabel("Proportion")
        ax.grid(axis="y", alpha=0.3)
        ax.set_axisbelow(True)
    raw_ticks = np.array([0, 10, 100, 1_000, 10_000, 60_000], dtype=float)
    axes[-1].set_xticks(np.log10(1 + raw_ticks), [f"{v:,.0f}" for v in raw_ticks])
    axes[-1].set_xlabel("ProductRelated_Duration (raw-value labels; x-axis is log10(1 + value))")
    fig.suptitle("Product-related duration by visitor type (log-transformed scale)")
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    fig.savefig(FIG_DIR / "duration_histograms_log.png", dpi=160)
    plt.close(fig)

    # 4. A standard raw-scale boxplot keeps Other visible as a third category.
    # Fliers are hidden only in this plot; all observations remain in summaries.
    grouped_values = [duration[df["VisitorType"] == group].dropna().to_numpy() for group in GROUP_ORDER]
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.boxplot(grouped_values, tick_labels=["New visitor", "Returning visitor", "Other"], showfliers=False)
    ax.set_ylabel("ProductRelated_Duration (dataset units)")
    ax.set_title("Product-related duration by visitor type")
    ax.grid(axis="y", alpha=0.3)
    ax.set_axisbelow(True)
    fig.tight_layout()
    fig.savefig(FIG_DIR / "duration_by_visitor_type.png", dpi=160)
    plt.close(fig)

    print(f"Rows: {len(df):,}; columns: {df.shape[1]}; missing cells: {int(df.isna().sum().sum())}")
    print(f"Exact duplicate rows: {int(df.duplicated().sum())}")
    print("Saved tables to", TABLE_DIR)
    print("Saved Matplotlib figures to", FIG_DIR)


if __name__ == "__main__":
    main()

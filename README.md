# STAT1008 EDA package

This folder contains a descriptive EDA report, Matplotlib figures, reproducible code, summary tables, and the original UCI CSV for the STAT1008 online-shopping project.

## Contents

- STAT1008_EDA_report.md — report with embedded relative links to the visitor-count chart, two visitor-group histograms (original and log-transformed scales), and the boxplot.
- data/online_shoppers_intention.csv — original UCI CSV, included unchanged.
- data/STAT1008_UCI_raw_data.xlsx — Excel workbook with the raw UCI records from the earlier project package.
- presentation/STAT1008_presentation_scaffold.pptx — editable slide scaffold from the earlier project package.
- references/STAT1008_GroupPresentation_INSTRUCTIONS.pdf — the supplied course handout used as the governing requirements.
- plot_eda.py — code to recount VisitorType categories, create the descriptive summary CSVs, and regenerate the Matplotlib figures.
- figures/ — generated PNG charts.
- tables/visitor_type_counts.csv — frequency table of visitor categories.
- tables/product_related_duration_summary.csv — groupwise duration sample size, mean, standard deviation, median, quartiles, range, zeros, and upper-fence flags.
- requirements.txt — minimum Python package requirements.

## Reproduce

Install the packages in requirements.txt, then run:

    python plot_eda.py

The script prints raw VisitorType counts before it computes duration summaries. It does not remove Other, duplicate rows, zeros, or extreme values. The original-scale group histograms share a common axis ending at the pooled 99th percentile; the log-transformed view includes the full New/Returning data. It does not calculate the inferential test.

## Source and interpretation

The CSV comes from UCI Machine Learning Repository dataset 468: https://doi.org/10.24432/C5F88Q. UCI reports no missing values, and the script independently checks the downloaded CSV. UCI does not specify the unit for ProductRelated_Duration; the report therefore gives values in dataset units. See the report's reference section and data-quality notes.

The group should independently verify the counts, plots, interpretations, and STAT1008 hypothesis-test calculations. Follow the course handout's AI declaration and originality requirements.

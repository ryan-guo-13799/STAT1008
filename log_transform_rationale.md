# Rationale for using a log scale in the duration EDA

## Short answer

A log transformation is a common and established way to display positive, strongly right-skewed data. It is **not automatically required** whenever a variable is skewed, and it is not a rule that the main analysis must use transformed data. In this project, the log-scale histogram is useful as a *supplementary view* because a few very large durations stretch the raw horizontal axis and make the bulk of sessions harder to compare. The primary summaries and the planned test should remain on the original duration values because the research question asks about arithmetic mean duration.

## Project context

The fixed research question is:

> Do new and returning online shoppers differ in their average time spent viewing product-related pages during an online shopping session?

The response is `ProductRelated_Duration`. In the UCI CSV, the two comparison groups contain 1,694 `New_Visitor` records and 10,551 `Returning_Visitor` records (12,245 in total); 85 `Other` records are kept separate and excluded from this two-group comparison. The value distribution is strongly right-skewed: across all visitor categories, the mean is 1,194.75, the median is 598.94, and the maximum is 63,973.52. These are **dataset units**; UCI does not specify a measurement unit (Sakar and Kastro, 2018).

The dataset also contains zeros: 42 in the New group and 696 in the Returning group. The plotted transform is therefore `log10(1 + x)`, rather than `log10(x)`, so zero values remain defined. The `+1` is a plotting convention; it does not add a meaningful unit of time. Since UCI does not state the duration unit, the transformed horizontal position should not be given a substantive interpretation.

## What the log transformation does

For a duration value `x >= 0`, the supplementary plot uses:

```text
z = log10(1 + x)
```

This compresses large values more than small values. It can make the lower and middle parts of a long-tailed distribution easier to see, while showing where the upper tail extends. Equal distances on a logarithmic axis correspond approximately to equal multiplicative changes in the original values, rather than equal additive changes. The log histogram is therefore useful for inspecting distribution shape and comparing tails; it does not make extreme records disappear.

The original-scale histogram is retained beside the log-scale version. Its New and Returning panels use the same scale within the figure, with the display limit and the number of observations beyond it stated in the report. The log figure shows all New and Returning observations. Both views are descriptive; neither by itself establishes a population difference.

## Is this method standard?

Log transformations are widely used for skewed positive data. For example, Feng et al. (2013) describe log transformation as widely used in biomedical research, while also documenting common misuses and interpretation errors. Keene (1995) discusses circumstances where a log analysis may be useful. These papers show that the method is established in applied statistics, but they do **not** make it compulsory for every skewed variable.

The choice should follow the question and the analysis assumptions. A transformation changes the scale and can change the quantity being compared. It should not be selected only because a normality test or histogram shows skewness.

## Why skewness matters here—and why it does not force a transformation

With a long right tail, a relatively small number of very large sessions can pull the arithmetic mean upward and increase the standard deviation. In this dataset, the means exceed the medians, and the maximum is far above the upper quartile. This makes it useful to report medians, quartiles, and a histogram alongside the means. It also means the group should inspect the extreme observations and explain that the mean is sensitive to the upper tail.

That sensitivity matters because the research question is specifically about **average duration**, operationalised as the population arithmetic mean. Replacing the raw values by logged values and testing their means would answer a different question. A two-sample test on `log10(1 + x)` would compare mean log durations, equivalently a contrast involving geometric means of `1 + x`; it would not test whether the original-scale arithmetic means are equal.

Strong skew in individual observations also does not, by itself, make a raw-scale comparison of means invalid. For sufficiently large independent samples with finite variance, the sampling distribution of a sample mean can be approximately normal even when the observations are not. Lumley et al. (2002) discuss this large-sample behavior for t-tests, including extremely non-normal outcomes. Fagerland (2012) compares two-sample t-tests and rank tests in simulations with skewed distributions and cautions that tests can answer different questions. These results support considering a raw-scale mean analysis in a large dataset, but they are not a guarantee for every data structure: independence, influential values, unequal variances, and how the data were sampled still matter.

For this project, retain the exact two-independent-sample method taught in STAT1008. Check and describe its stated assumptions, especially independence and any equal-variance requirement. The two groups are large, but the Returning group is much larger and has greater observed spread, so do not claim that sample size alone resolves every assumption concern. If the course specifies a particular test, follow that instruction and flag any mismatch between its assumptions and the observed data for the tutor/group to address (Research School of Finance, Actuarial Studies and Statistics, 2026).

## Can the analysis use the raw data without transformation?

**Yes. That is the recommended primary analysis for this fixed question.** Calculate the group means and the course-prescribed two-sample test from the original `ProductRelated_Duration` values. Keep every valid record, including zeros and extreme values; remove an observation only if the group can establish a data error and document the rule. Show the mean and standard deviation because the hypotheses concern means, and add the median, quartiles, and plots so the reader can see the skew and spread.

The central limit theorem provides a reason that a mean-based procedure can work with large independent samples even when the raw values are skewed. Still, the group must assess independence and influential values, and should follow STAT1008's method for standard error and degrees of freedom. If the course's procedure assumes equal population variances, the group should explicitly check and discuss that assumption rather than using the log plot as a substitute for the check.

## Other possible approaches

| Approach | What it can answer | Fit for this project |
|---|---|---|
| Raw-scale two-sample mean test | Difference in original-scale arithmetic means | Best match to the fixed research question and the course method. Keep as primary. |
| Log-scale two-sample mean test | Difference in average log duration; after exponentiation, a relative/geometric-mean contrast on `1 + duration` | A different estimand, so it should not replace the primary test. Use the log display for EDA only unless the research question is formally changed. |
| Mann–Whitney/Wilcoxon rank-sum test | A rank/distribution comparison; it is not generally a test of equality of arithmetic means and is not automatically a test of medians | Not a drop-in replacement for the specified mean comparison. Use only if the research question and course instructions call for that target. |
| Bootstrap interval/test for the raw mean difference | An interval or test for the original-scale mean difference using resampling | Could preserve the mean target, but may be outside the STAT1008 method set. Use only if taught or approved; extreme values and the sampling design still need attention. |
| Robust/trimmed-mean procedure | A contrast between trimmed means, reducing the influence of tail values | Changes the target from the ordinary arithmetic mean and may be beyond the course level. |
| Another transformation (for example, square root or a Box–Cox family) | A transformed-scale comparison, with the particular transformation chosen for a reason | Does not automatically solve skewness and changes interpretation; unnecessary for the primary question here. |

The median and interquartile range are valuable robust **descriptive** summaries. They can show what a typical session looks like, but they do not answer the fixed question about population means. Similarly, switching to a rank test solely because the histogram is skewed risks answering a different question.

## Recommendation for the presentation

1. Show visitor counts and the raw-scale duration summaries by visitor type.
2. Keep the original-scale histogram and boxplot, and show the log-scale histogram as an additional view of the long tails.
3. Explain that the log plot uses `log10(1 + duration)` only to make distribution shape easier to inspect; zero values are retained.
4. Calculate the hypothesis test from the original duration values using the method taught in STAT1008.
5. Interpret any result as a difference or lack of evidence of a difference in **mean dataset-unit duration** between New and Returning sessions. Do not infer a causal effect.

## References

Fagerland, M.W. (2012) ‘t-tests, non-parametric tests, and large studies—a paradox of statistical practice?’, *BMC Medical Research Methodology*, 12, article 78. https://doi.org/10.1186/1471-2288-12-78.

Feng, C., Wang, H., Lu, N. and Tu, X.M. (2013) ‘Log transformation: application and interpretation in biomedical research’, *Statistics in Medicine*, 32(2), pp. 230–239. https://doi.org/10.1002/sim.5486.

Keene, O.N. (1995) ‘The log transformation is special’, *Statistics in Medicine*, 14(8), pp. 811–819. https://doi.org/10.1002/sim.4780140810.

Lumley, T., Diehr, P., Emerson, S. and Chen, L. (2002) ‘The importance of the normality assumption in large public health data sets’, *Annual Review of Public Health*, 23, pp. 151–169. https://doi.org/10.1146/annurev.publhealth.23.100901.140546.

Research School of Finance, Actuarial Studies and Statistics (2026) *STAT1008 Quantitative Research Methods: Group Presentation Project*. Semester 2 course handout.

Sakar, C. and Kastro, Y. (2018) *Online Shoppers Purchasing Intention Dataset*. UCI Machine Learning Repository. https://doi.org/10.24432/C5F88Q.

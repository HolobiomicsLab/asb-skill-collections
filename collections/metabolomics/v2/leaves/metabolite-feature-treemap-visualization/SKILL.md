---
name: metabolite-feature-treemap-visualization
description: Use when after applying mpactr's filter suite (filter_mispicked_ions,
  filter_group, filter_cv, filter_insource_ions) to a peak table, use this skill when
  you need to summarize the overall filtering outcome across all ion categories and
  present a compact, area-proportional view of which ions passed.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0571
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0092
  tools:
  - R
  - ggplot
  - mpactr
  - ggplot2
  - data.table
  - plotly
  techniques:
  - LC-MS
  license_tier: open
derived_from:
- doi: 10.1021/acs.analchem.2c04632
  title: MPACT
evidence_spans:
- To import these data into R, use the mpactr function
- We will be using multiple libraries for data analysis and visualization
- creating an interactive plot of input features and the filters they failed, if any,
  using `ggplot` and `plotly`
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mpactr_cq
    doi: 10.1021/acs.analchem.2c04632
    title: MPACT
  dedup_kept_from: coll_mpactr_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.2c04632
  all_source_dois:
  - 10.1021/acs.analchem.2c04632
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolite-feature-treemap-visualization

## Summary

Visualize the distribution of passing and failing metabolite ions across multiple filter categories (mispicked, group, replicability, insource) as a hierarchical treemap, where tile area represents ion count and labels show filter status and percentage of total ions. This enables rapid assessment of filtering efficacy and identification of which filter categories are removing the most features.

## When to use

After applying mpactr's filter suite (filter_mispicked_ions, filter_group, filter_cv, filter_insource_ions) to a peak table, use this skill when you need to summarize the overall filtering outcome across all ion categories and present a compact, area-proportional view of which ions passed or failed which filters. Particularly useful when comparing filtering strategies or reporting filtering statistics to stakeholders.

## When NOT to use

- Input has not yet been filtered; qc_summary() requires a filtered mpactr object to produce meaningful status categories.
- Seeking to visualize m/z and retention time distributions; treemap is designed for categorical counts, not continuous feature properties.
- Filtering results contain no variation in status (e.g., all ions passed all filters); treemap requires multiple status categories to be informative.

## Inputs

- mpactr object (post-filtering with applied filter_mispicked_ions, filter_group, filter_cv, filter_insource_ions)
- qc_summary() output (data frame containing per-ion filter status across all filter categories)

## Outputs

- treemap visualization (ggplot2 object)
- PNG file (exported treemap image with status, count, and percentage labels)

## How to apply

1. Load the filtered mpactr object and call qc_summary() to extract per-ion filter status across all applied filters (mispicked, group, replicability, insource). 2. Pivot and aggregate the qc_summary() output using data.table grouping operations to count ions per filter status category and calculate the percentage of total ions for each status. 3. Construct a data frame with columns for filter status, ion count, and percentage. 4. Render the treemap using ggplot2, with geom_treemap() to scale tile areas proportionally to ion counts and geom_treemap_text() to overlay filter status labels and percentages on each tile. 5. Export the final treemap as a PNG file for reporting or publication. The treemap area scale communicates the relative magnitude of each filter category's impact, and the percentage labels allow comparison across different filtering scenarios.

## Related tools

- **mpactr** (Extract per-ion filter status via qc_summary() and provide filtered peak data) — https://github.com/mums2/mpactr
- **ggplot2** (Create treemap visualization using geom_treemap() and geom_treemap_text() layers)
- **data.table** (Group and aggregate ion counts and percentages by filter status from qc_summary() output)
- **plotly** (Optional: convert static treemap to interactive plot for exploratory filtering assessment)

## Examples

```
qc_dat <- qc_summary(mpactr_obj); qc_pivot <- qc_dat[, .(count = .N, pct = 100*.N/nrow(qc_dat)), by=.(filter_status)]; ggplot(qc_pivot, aes(area=count, fill=filter_status, label=paste0(filter_status, '\n', count, ' (', round(pct,1), '%)'))) + geom_treemap() + geom_treemap_text(colour='white', place='centre', size=12)
```

## Evaluation signals

- Treemap tiles sum to 100% across all filter status categories (verifies percentage calculation correctness).
- Tile area is proportional to ion count; visually confirm that larger tiles correspond to higher counts in the underlying data frame.
- All filter status categories from qc_summary() (mispicked pass/fail, group pass/fail, replicability pass/fail, insource pass/fail) are represented in the treemap.
- Text labels on tiles are readable and non-overlapping; geom_treemap_text() correctly sizes text to fit tile dimensions.
- PNG export contains no artifacts, has adequate resolution (≥ 300 dpi recommended), and treemap structure matches the underlying data frame when inspected.

## Limitations

- Treemap visualization becomes crowded and difficult to interpret if there are many unique filter status combinations; consider filtering the data frame to top categories or aggregating rare statuses.
- The treemap does not show temporal or sample-level filtering effects—it is a summary statistic. Ion-level or time-series filtering patterns require complementary visualizations (e.g., interactive scatter plots of m/z and retention time).
- Percentage labels may be difficult to read if tiles are very small; consider removing text labels or using an interactive version (plotly) for fine-grained inspection.
- The skill assumes qc_summary() has been called on a fully filtered mpactr object; if filters are applied incrementally without calling qc_summary() between steps, intermediate status information may be lost.

## Evidence

- [other] qc_summary output pivot and grouping rationale: "Ion counts and percentages by status can be computed from qc_summary() output using data.table grouping"
- [other] treemap rendering method: "rendered as a treemap with geom_treemap() and geom_treemap_text() showing status, count, and percentage labels"
- [other] filter status categories from qc_summary: "per-ion filter status (passed/failed for mispicked, group, replicability, insource filters)"
- [methods] workflow step detail from methods: "Visualizing each compound by m/z and retention time, and their fate during filtering may be useful to see if filters are removing features at certain retention time or m/z ranges"
- [readme] mpactr overview of available filters: "filter_mispicked_ions(): removal of mispicked peaks, or those isotopic patterns that are incorrectly split during preprocessing. filter_group(): removal of features overrepresented in a specific"

---
name: mzmine-quantitative-table-parsing
description: Use when you have LC–MS/MS data processed through MZmine2 or MZmine3 and need to construct a feature quantification table for natural product discovery pipelines (e.g., INVENTA prioritization, GNPS networking, or metabolite annotation).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - MZmine2
  - MZmine3
  - timaR
  - CANOPUS
  - MEMO
  - GNPS
  - INVENTA
  techniques:
  - tandem-MS
  - NMR
derived_from:
- doi: 10.3389/fmolb.2022.1028334
  title: Inventa
- doi: 10.1038/s41467-021-23953-9
  title: ''
evidence_spans:
- MZmine output format using only the 'Peak area', 'row m/z' and 'row retention time' columns. -Inventa takes input directly from MZmine2
- Inventa takes input directly from MZmine2 or MZmine 3
- -Inventa takes input directly from MZmine2 or [MZmine 3](http://mzmine.github.io/), is possible to use other processing sofwares
- 'tima_results_filename: timaR reponderated output format. - for performing in silico annotations and taxonomically informed reponderation.'
- 'tima_results_filename: timaR reponderated output format'
- 'Class Component (CC): a score considering the presence of predicted known chemical classes new to the species'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_inventa_cq
    doi: 10.3389/fmolb.2022.1028334
    title: Inventa
  dedup_kept_from: coll_inventa_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.3389/fmolb.2022.1028334
  all_source_dois:
  - 10.3389/fmolb.2022.1028334
  - 10.1038/s41467-021-23953-9
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mzmine-quantitative-table-parsing

## Summary

Extract and standardize peak intensity data (peak area or peak height) with retention time and m/z values from MZmine2 or MZmine3 output files for downstream metabolomics analysis. This is the foundational data ingestion step that supplies feature quantification matrices to prioritization and annotation workflows.

## When to use

You have LC–MS/MS data processed through MZmine2 or MZmine3 and need to construct a feature quantification table for natural product discovery pipelines (e.g., INVENTA prioritization, GNPS networking, or metabolite annotation). This skill is required when the input is raw MZmine output and the analysis goal involves calculating feature-level statistics, comparing extract compositions, or assigning priority scores based on feature specificity and abundance.

## When NOT to use

- Input is already a normalized feature table (e.g., log-transformed, batch-corrected, or aggregated by compound ID) — reparsing would lose normalization.
- Data are from non-LC–MS/MS instruments (e.g., GC–MS, NMR, or other platforms) — this skill is specific to MZmine output format.
- Only annotated features are needed — this skill preserves unannotated features, which are retained for the Feature Component calculation but should not be discarded before annotation filtering.

## Inputs

- MZmine2 or MZmine3 feature quantification export (CSV or TSV format)
- Optional: Ion Identity results if features have been deduplicated

## Outputs

- Cleaned quantitative matrix (rows = features, columns = samples; values = peak area or peak height)
- Metadata linking sample IDs to filenames and experimental conditions

## How to apply

Load the MZmine2 or MZmine3 output file and retain only three columns: 'Peak area' (or alternatively 'Peak height' if area data are unavailable), 'row m/z', and 'row retention time'. Remove non-quantitative metadata columns (e.g., 'Unknown: number' placeholders, identity columns, or other descriptive text). Verify that rows correspond to features and columns to samples, and that all numeric values are present and in expected ranges (m/z typically 50–2000, retention time in minutes or seconds depending on instrument). Handle Ion Identity deduplicated outputs by using the Ion Identity-reduced feature list if available. The resulting table becomes the input to component calculators (Feature Component, Similarity Component) and must have consistent sample labeling across all downstream files (metadata, annotations, GNPS results).

## Related tools

- **MZmine2** (Source software that exports the quantitative feature table; Inventa accepts its output directly)
- **MZmine3** (Modern version of MZmine that exports quantitative tables in the same format as MZmine2; interchangeable input source)
- **GNPS** (Downstream platform that accepts metadata tables paired with feature quantification; provides Ion Identity results for feature deduplication)
- **INVENTA** (Principal consumer of the parsed quantitative table; uses it to calculate Feature Component and feed into Priority Rank scoring) — https://github.com/luigiquiros/inventa

## Examples

```
# In the INVENTA Jupyter notebook, set the quantitative data path and run:
quantitative_data_filename = 'data/mzmine_quant_export.csv'
# The inventa.py script loads this file, retains only ['Peak area', 'row m/z', 'row retention time'],
# and passes it to the Feature Component and downstream calculations.
```

## Evaluation signals

- All numeric values in 'Peak area' / 'Peak height' columns are positive and within expected instrumental range (typically 1e2–1e9); no missing or NaN entries.
- Exactly three columns remain: 'Peak area' (or 'Peak height'), 'row m/z', and 'row retention time'; no extraneous metadata or identity annotations remain.
- Number of rows (features) and column count (samples) match the raw MZmine export; feature IDs are preserved or reconstructed consistently with original peak list.
- Sample column names align exactly with sample identifiers in the companion metadata and GNPS job results; no mismatches or relabeling discrepancies.
- If Ion Identity deduplication was used, the feature count is strictly less than the unannotated input, and each deduplicated feature is mappable back to its constituent unannotated peaks.

## Limitations

- MZmine output format varies between versions; users must verify that 'Peak area' and 'row m/z' / 'row retention time' column names match their specific export version.
- Manual editing is required if MZmine exports contain unexpected columns (e.g., custom metadata, intensity ranges, or identity fields); the README advises users to drop these or modify the function quand_table() in src/inventa.py.
- Only one quantitative metric ('Peak area' or 'Peak height') can be considered at a time; if both are desired, the analysis must be run twice sequentially.
- Ion Identity integration is optional; absence of Ion Identity results does not prevent Feature Component calculation, but may inflate feature count and reduce specificity estimates.
- No built-in validation for retention time consistency across files; users must ensure aligned RT ranges and units (minutes vs. seconds) before concatenating multiple MZmine outputs.

## Evidence

- [other] MZmine output format using only the 'Peak area', 'row m/z' and 'row retention time' columns. -Inventa takes input directly from MZmine2 or MZmine 3: "MZmine output format using only the 'Peak area', 'row m/z' and 'row retention time' columns. -Inventa takes input directly from MZmine2 or MZmine 3"
- [readme] if you prefer 'Peak Height', go to `src/inventa.py` and change it inside the function quand_table(). ONLY ONE of the columns is considered at the time, 'Peak height' or 'Peak area': "if you prefer 'Peak Height', go to `src/inventa.py` and change it inside the function quand_table(). ONLY ONE of the columns is considered at the time"
- [readme] if you did export any other column, like identities, etc,  please remove manually or add the corresponding lines in the funcion quand_table(): "if you did export any other column, like identities, etc,  please remove manually or add the corresponding lines in the funcion quand_table()"
- [readme] Usually, there are columns with the header 'Unkown: number' at the very end of the quantitative table, the scrip takes care of these columns: "Usually, there are columns with the header 'Unkown: number' at the very end of the quantitative table, the scrip takes care of these columns"
- [other] Inventa is capable to performe the calcultions based on the results from Ion Identity, reducing the total number of features.: "Inventa is capable to performe the calcultions based on the results from Ion Identity, reducing the total number of features."
- [methods] The Feature Component (FC) is a ratio of the number of specific non-annotated features over the total number of features of each extract.: "The Feature Component (FC) is a ratio of the number of specific non-annotated features over the total number of features of each extract."

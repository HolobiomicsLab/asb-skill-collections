---
name: feature-table-integration-and-normalization
description: Use when when you have MS1 feature tables from heterogeneous sources—e.g., XCMS peak detection output mixed with vendor software (MS-DIAL, MZmine2) results—and need to merge them into a single, format-normalized table for ISFrag analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3933
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0091
  tools:
  - ISFrag
  - R
  - XCMS
derived_from:
- doi: 10.1021/acs.analchem.1c01644
  title: ISFrag
evidence_spans:
- ISFrag is an R package for identifying and annotating in-source fragments in LCMS metabolite feature table.
- ISFrag is an R package for identifying and annotating in-source fragments in LCMS metabolite feature table
- To install ISFrag package R version 4.0.0 or above is required
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_isfrag_cq
    doi: 10.1021/acs.analchem.1c01644
    title: ISFrag
  dedup_kept_from: coll_isfrag_cq
schema_version: 0.2.0
---

# feature-table-integration-and-normalization

## Summary

Combine MS1 feature tables from multiple sources (XCMS-extracted and/or custom CSV formats from MS-DIAL, MZmine2) into a unified, ISFrag-compatible feature matrix with standardized column structure and intensity values across samples. This skill enables flexible input handling while maintaining data integrity for downstream MS2 annotation and in-source fragment identification.

## When to use

When you have MS1 feature tables from heterogeneous sources—e.g., XCMS peak detection output mixed with vendor software (MS-DIAL, MZmine2) results—and need to merge them into a single, format-normalized table for ISFrag analysis. Specifically, use this skill when the article notes 'Users can choose to use XCMS to extract features from mzXML files (Section 2.1), upload their own feature table in csv format (Section 2.2), or combine both features extracted by XCMS with their own feature table (both Section 2.1 and Section 2.2).'

## When NOT to use

- Feature tables are already aligned and merged from a single source (e.g., already exported from XCMS with all samples)—skip directly to MS2 annotation.
- Input tables use non-standard column orders or missing retention-time bounds (rtmin, rtmax); reconcile schema first before integration.
- You need to perform statistical normalization (e.g., batch-effect correction, log-transformation, relative abundance scaling)—that is a separate normalization skill, not this integration step.

## Inputs

- XCMS-generated feature table (dataframe with columns: mz, rt, rtmin, rtmax, maxo or sample intensities)
- Custom CSV feature table from MS-DIAL, MZmine2, or other vendor software (CSV format with columns: m/z, retention time, min retention time, max retention time, intensity columns)
- One or more mzXML/mzML raw LCMS files (optional, if re-running XCMS extraction)

## Outputs

- Unified ISFrag-compatible feature table (dataframe: mz, rt, rtmin, rtmax, followed by intensity columns for each sample)
- Feature identifier mapping (F1, F2, … corresponding to rows)
- Validation report (optional): duplicate detection, missing-value counts, intensity range statistics

## How to apply

First, ensure all input feature tables conform to the mandatory five-column structure: m/z, retention time (in seconds), minimum retention time, maximum retention time, followed by intensity columns (one per sample or pooled). XCMS output is already in this format after XCMS.featuretable(); custom CSV inputs must be reordered via custom.featuretable() to match this schema. For multi-sample analyses, verify that XCMS has performed peak alignment and missing-value filling. Then use ISFrag's add.features() or combine() function (referenced in Part 2.2 usage) to concatenate or merge tables while preserving row identifiers (feature names like F1, F2, …). Validate the merged table by checking for duplicate m/z–retention-time pairs (which may indicate alignment artifacts or need for deduplication), ensuring all intensity columns are numeric, and confirming that retention time spans (rtmin, rtmax) do not exceed biological plausibility for the chromatography method used.

## Related tools

- **ISFrag** (Primary R package for combining custom and XCMS feature tables and providing add.features() / combine() functions for integration) — https://github.com/HuanLab/ISFrag.git
- **XCMS** (Generates standardized MS1 feature tables (mz, rt, rtmin, rtmax, intensity) via XCMS.featuretable() function) — https://rdrr.io/bioc/xcms/man/
- **R** (Runtime environment for ISFrag and XCMS (version 4.0.0 or above required))

## Examples

```
xcmsFT <- XCMS.featuretable(MS1directory = "path/to/mzXML/folder", type = "single", peakwidth = c(5,20)); customFT <- custom.featuretable(ft_directory = "path/to/csv/folder", ft_name = "featuretable.csv"); mergedFT <- rbind(xcmsFT[,c('mz','rt','rtmin','rtmax')], customFT[,c('mz','rt','rtmin','rtmax')])
```

## Evaluation signals

- All rows in the merged table have exactly five leading columns (mz, rt, rtmin, rtmax) followed by one or more intensity columns; no missing values in these core columns.
- No duplicate m/z–retention-time pairs exist after merging (or duplicates are explicitly documented as expected from isotope/adduct annotation).
- Retention-time bounds are monotonic: rtmin ≤ rt ≤ rtmax for every row, and rtmax − rtmin is consistent with peak-width parameters (typically 5–20 seconds for LCMS).
- Intensity columns are numeric and non-negative; zero intensities are acceptable and indicate missing peaks in specific samples.
- Feature row names follow ISFrag convention (F1, F2, …) and are unique across the table.

## Limitations

- CAMERA adduct and isotope annotation is only available for XCMS-only analysis, not for custom feature tables or merged tables containing custom features.
- Retention-time information must be in seconds; incompatible units (minutes, milliseconds) will cause misalignment.
- Multi-sample peak alignment and filling are performed by XCMS internally; custom CSV tables must already be aligned by the user or the source software before integration.
- The skill assumes no prior statistical normalization (e.g., batch correction, log-transformation); intensity values are treated as raw integrated peak heights and must be normalized separately if required for downstream analysis.

## Evidence

- [readme] Users can choose to use XCMS to extract features from mzXML files (Section 2.1), upload their own feature table in csv format (Section 2.2), or combine both features extracted by XCMS with their own feature table (both Section 2.1 and Section 2.2).: "Users can choose to use `XCMS` to extract features from mzXML files (Section 2.1), upload their own feature table in csv format (Section 2.2), or combine both features extracted by `XCMS` with their"
- [readme] In order for ISFrag to successfully read the provided csv file, it must contain only columns in the following order: m/z, retention time, min retention time, max retention time, followed by an additional column containing the intensities of features detected in each sample.: "In order for `ISFrag` to succesfully read the provided csv file, it must contain only columns in the following order: m/z, retention time, min retention time, max retention time, followed by an"
- [readme] Note: for multi-sample analyses, peak alignment and filling will be performed by XCMS.: "Note: for multi-sample analyses, peak alignment and filling will be performed by XCMS."
- [readme] All three columns containing retention time information should be in seconds.: "all three columns containing retention time information should be in seconds."
- [other] ISFrag includes MS1 feature extraction as Part 2 of its workflow, with XCMS feature extraction as a sub-component (Section 2.1), which produces a feature table that serves as input for downstream MS2 annotation and in-source fragment identification.: "ISFrag includes MS1 feature extraction as Part 2 of its workflow, with XCMS feature extraction as a sub-component (Section 2.1), which produces a feature table that serves as input for downstream MS2"

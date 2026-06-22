---
name: isotopic-pattern-mispicking-detection
description: Use when you have a peak table from tandem MS preprocessing (e.g., MS-DIAL, Metaboscape) and suspect that isotopic patterns have been incorrectly split during feature detection.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0591
  tools:
  - R
  - mpactr
  - MPACT (GUI)
  - data.table
  - ggplot2 / plotly
  techniques:
  - tandem-MS
derived_from:
- doi: 10.1128/mra.00997-24
  title: mpactr
- doi: 10.1021/acs.analchem.2c04632
  title: ''
evidence_spans:
- This table can be used for a variety of analyses that can be conducted in R
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mpactr
    doi: 10.1128/mra.00997-24
    title: mpactr
  dedup_kept_from: coll_mpactr
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1128/mra.00997-24
  all_source_dois:
  - 10.1128/mra.00997-24
  - 10.1021/acs.analchem.2c04632
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# isotopic-pattern-mispicking-detection

## Summary

Detect and correct isotopic patterns that are incorrectly split into separate peaks during mass spectrometry preprocessing. This skill identifies mispicked ions—where a single compound's isotopic distribution has been fragmented into multiple spurious features—and optionally merges them back to recover the true ion signal.

## When to use

Apply this skill when you have a peak table from tandem MS preprocessing (e.g., MS-DIAL, Metaboscape) and suspect that isotopic patterns have been incorrectly split during feature detection. This is especially critical in untargeted metabolomics workflows where preprocessing algorithms may separate monoisotopic and isotopic peaks as distinct features, leading to inflated feature counts and reduced signal intensity for true compounds.

## When NOT to use

- Input peak table has already been curated or merged by another tool; applying an additional isotopic pattern filter risks removing legitimate, validated features.
- Sample contains only singly-charged ions or very simple structures with negligible isotopic fine structure; mispicking is unlikely and the filter may introduce false positives.
- High-resolution MS data where isotopic patterns are already well-resolved at the detector level and preprocessing has not split them; mispicking frequency will be low.

## Inputs

- preprocessed peak table (e.g., from MS-DIAL or Metaboscape output)
- sample metadata table
- mpactr object (loaded via import_data())

## Outputs

- filtered mpactr object with mispicked ions flagged or merged
- filter_summary() named list with failed_ions and passed_ions vectors
- data.table containing compound identifiers and mispick status

## How to apply

Load the preprocessed peak table and metadata into an mpactr object using import_data(). Call filter_mispicked_ions() with appropriate merge parameters (typically merge_peaks=TRUE and merge_method='sum' to combine split isotopic signals). The filter uses compound abundance patterns and isotopic spacing rules to identify suspect peak pairs or clusters. Examine the filter output using filter_summary(data_object, 'mispicked') to review which ions failed (were identified as mispicked) and which passed; convert the results to a data.table for visualization or export. Decide whether to keep the filter applied based on the number and intensity of affected features and domain knowledge about expected isotopic distributions in your sample.

## Related tools

- **mpactr** (R package providing filter_mispicked_ions() and filter_summary() functions for isotopic pattern detection and correction) — https://github.com/mums2/mpactr
- **MPACT (GUI)** (Graphical interface for data import, filtering (including mispicking correction), and visualization in metabolomics workflows) — https://github.com/BalunasLab/mpact
- **data.table** (R package for efficient tabular storage and export of filter results (failed_ions and passed_ions) to CSV)
- **ggplot2 / plotly** (Visualization of which features failed or passed the mispicking filter)

## Examples

```
filter_mispicked_ions(merge_peaks = TRUE, merge_method = "sum")
```

## Evaluation signals

- filter_summary() output is a valid named list with 'failed_ions' and 'passed_ions' components; both are non-empty and vectors of compound identifiers match the input peak table.
- After merging (if merge_peaks=TRUE), the combined feature count is lower than the input peak table, and merged ions have m/z spacing consistent with isotopic differences (typically 1.003 Da for ¹³C, 2.004 for doubly-charged, etc.).
- Visual inspection of failed vs. passed ions shows that mispicked features tend to co-occur in the same samples and have similar retention times and m/z patterns characteristic of isotopic splitting artifacts.
- Downstream analyses (e.g., fold-change, volcano plot) show improved statistical power (lower p-values, higher effect sizes) after removing mispicked ions, indicating recovery of true signal.
- Exported CSV tables (failed_ions and passed_ions) can be cross-referenced against reference databases or manual review to confirm that mispicked ions correspond to known isotopic patterns, not genuine metabolite variants.

## Limitations

- The filter assumes that mispicked ions will show characteristic abundance ratios and isotopic spacing; highly unusual or deuterated samples may confound detection.
- Current implementation requires domain expertise to choose appropriate merge_method ('sum' assumes additive signal; other methods may be needed for complex adducts or fragments).
- Filter performance has been validated on Streptomyces cultures and may generalize poorly to very different sample types (e.g., plant tissue, serum) with different ionization and fragmentation patterns.
- No formal changelog is maintained for the mpactr package, making it difficult to track improvements or bug fixes in the mispicking algorithm across versions.

## Evidence

- [readme] filter_mispicked_ions(): removal of mispicked peaks, or those isotopic patterns that are incorrectly split during preprocessing.: "filter_mispicked_ions(): removal of mispicked peaks, or those isotopic patterns that are incorrectly split during preprocessing."
- [methods] filter_summary() returns a named list containing two components: failed_ions and passed_ions: "filter_summary() returns a named list containing two components: failed_ions and passed_ions, both of which can be displayed as data tables using head()"
- [methods] Call filter_summary(data_object, 'mispicked') with merge parameters: "Call filter_summary(data_object, 'mispicked') to extract a named list containing failed_ions and passed_ions vectors"
- [readme] All filters are independent, meaning they can be used to create a project-specific workflow: "All filters are independent, meaning they can be used to create a project-specific workflow"
- [abstract] Reference semantics enable in-place data updates without copying the entire data object: "operates on reference semantics in which data is updated *in-place*. Compared to a shallow copy, where only data pointers are copied, or a deep copy, where the entire data object is copied in memory"
- [methods] filter_mispicked_ions with merge parameters: "filter_mispicked_ions(merge_peaks = TRUE, merge_method = "sum")"

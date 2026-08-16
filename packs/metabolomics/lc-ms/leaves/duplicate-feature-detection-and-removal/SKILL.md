---
name: duplicate-feature-detection-and-removal
description: Use when you have peak-picked LC-MS data with multiple features that may represent the same metabolite detected at slightly different m/z or retention time values due to instrument precision limits, isotope variants, or adduct forms.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - R
  - metabCombiner
  techniques:
  - LC-MS
derived_from:
- doi: 10.1021/acs.analchem.0c03693
  title: metabCombiner
evidence_spans:
- This is an R package for aligning a pair of disparately-acquired untargeted LC-MS metabolomics.
- This is an R package for aligning a pair of disparately-acquired untargeted LC-MS metabolomics
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metabcombiner_cq
    doi: 10.1021/acs.analchem.0c03693
    title: metabCombiner
  dedup_kept_from: coll_metabcombiner_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.0c03693
  all_source_dois:
  - 10.1021/acs.analchem.0c03693
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# duplicate-feature-detection-and-removal

## Summary

Identify and remove redundant features in LC-MS metabolomics data that fall within close mass-to-charge and retention time distances, reducing false positives in downstream feature alignment. This step is essential after applying retention time and missingness filters to ensure a clean, non-redundant feature set for alignment.

## When to use

Apply this skill when you have peak-picked LC-MS data with multiple features that may represent the same metabolite detected at slightly different m/z or retention time values due to instrument precision limits, isotope variants, or adduct forms. Use it after retention time range and missingness filtering, before feature grouping and pairwise alignment detection.

## When NOT to use

- Input data is already a curated feature table from a targeted assay where all features are known to be distinct.
- Retention time or missingness filters have not yet been applied; apply those first to avoid removing features that may be isolated after filtering.
- m/z and retention time distance thresholds are unknown or not calibrated for your instrument platform—obtain instrument validation data before applying.

## Inputs

- formatted metabData object with mapped mz, rt, id, adduct, and samples columns
- raw LC-MS data frame (before duplicate filtering)

## Outputs

- deduplicated metabData object with redundant features removed
- filtered feature table with unique m/z and retention time combinations

## How to apply

The duplicate filter detects and removes features that co-occur within empirically-defined m/z and retention time distance thresholds (e.g., 0.0025 Da and 0.05 min). Features meeting both distance criteria are flagged as duplicates; typically the lower-intensity or less-complete feature is retained or removed based on a scoring heuristic (e.g., total abundance across samples or feature completeness). This filtering should be applied as part of the Data Formatting and Filtering workflow step in metabCombiner, after loading and column-mapping the raw LC-MS data frame via the metabData constructor. The choice of distance thresholds should reflect your instrument's mass accuracy and chromatographic resolution; stricter thresholds (smaller distances) are appropriate for high-resolution instruments.

## Related tools

- **metabCombiner** (R package providing the metabData constructor and duplicate filter implementation for LC-MS feature deduplication) — github.com/hhabra/metabCombiner
- **R** (Programming language and runtime environment for executing metabCombiner workflows)

## Examples

```
# After loading plasma20 data and mapping columns with metabData,
# the duplicate filter is applied as part of the metabCombiner workflow:
data(plasma20)
x <- metabData(plasma20, mz = "mz", rt = "rt", id = "id", adduct = "adduct", samples = "CHEAR", rtmin = 0, rtmax = 17.25)
# Duplicate filtering occurs internally during the Data Formatting step; output is a deduplicated metabData object.
```

## Evaluation signals

- Verify that no two remaining features share m/z values within 0.0025 Da AND retention time within 0.05 min of each other.
- Check that the output feature count is less than or equal to the input count; a reduction indicates successful duplicate removal.
- Confirm that the deduplicated feature set has the same number of mapped columns (mz, rt, id, adduct, samples) as the input metabData object.
- Validate that feature intensities or abundances in the deduplicated table are reasonable (non-zero, within expected dynamic range for LC-MS).
- Cross-check that features flagged as duplicates have similar chemical properties (e.g., m/z within instrument tolerance, retention time overlap) before removal.

## Limitations

- Distance thresholds (0.0025 Da, 0.05 min) are instrument- and method-specific; thresholds suitable for high-resolution UPLC may be inappropriate for lower-resolution LC, and must be validated empirically.
- The filter may incorrectly merge genuine features (isobars, co-eluting isomers) if thresholds are too permissive, or fail to remove duplicates if thresholds are too strict.
- No explicit guidance in the article on tie-breaking logic when multiple features fall within the distance window; the specific algorithm for choosing which duplicate to retain is not detailed.
- The filter does not account for adduct-specific differences; two features with the same m/z and rt but different adduct annotations may still be treated as duplicates.

## Evidence

- [intro] Duplicate filter definition and parameters: "The duplicate filter detects and removes features within close m/z and RT distances (e.g 0.0025Da & 0.05 min)."
- [intro] Workflow context for duplicate filtering: "5. Apply duplicate filter detecting and removing features within close m/z and retention time distances."
- [intro] metabData column mapping and construction: "For mz, rt, id, adduct, and Q fields, metabData searches for the first column whose name contains the supplied keyword"
- [intro] Data Formatting and Filtering workflow phase: "The workflow we outline here is composed of five major steps: 1) Data Formatting and Filtering"
- [readme] metabCombiner's core alignment approach: "metabCombiner takes peak-picked and conventionally aligned untargeted LC-MS datasets and determines the overlapping <mass-to-charge (m/z), retention time (rt)>  features"

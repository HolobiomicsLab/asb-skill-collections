---
name: two-dimensional-tic-folding
description: Use when immediately after acquiring raw GCxGC-MS data in NetCDF format (.cdf files) and before any signal enhancement (smoothing, baseline correction) or alignment steps.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
  tools:
  - RGCxGC
  - R
derived_from:
- doi: 10.1016/j.microc.2020.104830
  title: RGCxGC
- doi: 10.1371/journal.pntd.0006215
  title: ''
evidence_spans:
- The goal of RGCxGC is to provide an easy-to-use platform to analyze two-dimensional gas chromatography data.
- This is the vignette to explain the implementation of RGCxGC package.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_rgcxgc_cq
    doi: 10.1016/j.microc.2020.104830
    title: RGCxGC
  dedup_kept_from: coll_rgcxgc_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1016/j.microc.2020.104830
  all_source_dois:
  - 10.1016/j.microc.2020.104830
  - 10.1371/journal.pntd.0006215
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# two-dimensional-tic-folding

## Summary

Converts raw GCxGC chromatogram data from NetCDF format into a 2D-TIC (two-dimensional Total Intensity Chromatogram) object by folding the linear retention time axis according to the second-dimension modulation period. This is the foundational preprocessing step that restructures raw instrumental output into a matrix suitable for signal enhancement and multivariate analysis.

## When to use

Apply this skill immediately after acquiring raw GCxGC-MS data in NetCDF format (.cdf files) and before any signal enhancement (smoothing, baseline correction) or alignment steps. The modulation time parameter should match the actual instrument configuration—typically 5 seconds for standard GCxGC setups—to properly fold the linear chromatogram into a 2D representation that preserves the two retention-time dimensions.

## When NOT to use

- Input is already in 2D matrix format or has been previously folded—avoid re-folding, which will corrupt the data structure.
- NetCDF file is corrupted or missing required metadata (instrument configuration, modulation time)—the import will fail or produce invalid retention time mappings.
- Modulation time parameter does not match the actual instrument configuration—folding will misalign retention time dimensions and produce misleading 2D chromatograms.

## Inputs

- NetCDF chromatogram file (.cdf format from GCxGC-MS instrument)
- Modulation time parameter (numeric, in seconds; typically 5 for standard GCxGC)

## Outputs

- Four-slot RGCxGC object containing: 2D-TIC matrix, primary retention times vector, NetCDF file name, and modulation time

## How to apply

Load the RGCxGC package in R and invoke the read_chrom() function with three arguments: the NetCDF file path (e.g., 08GB.cdf), the modulation parameter set to the second-dimension cycle time in seconds (typically 5 seconds for standard instruments), and optionally the file name for validation. The function returns a four-slot object: slot 1 contains the folded 2D-TIC matrix, slot 2 contains the first-dimension (primary) retention times, slot 3 contains the validated NetCDF file name, and slot 4 contains the modulation time. Inspect the resulting object structure to confirm all four slots are populated and that the 2D matrix dimensions are consistent with the input chromatogram length divided by the modulation period.

## Related tools

- **RGCxGC** (R package providing the read_chrom() function to import and fold NetCDF chromatograms into 2D-TIC objects; downstream functions depend on this output for signal preprocessing) — https://github.com/DanielQuiroz97/RGCxGC
- **R** (Programming language runtime environment for executing RGCxGC functions)

## Examples

```
library(RGCxGC); tic_2d <- read_chrom('08GB.cdf', modulation = 5); str(tic_2d)
```

## Evaluation signals

- Returned object has exactly four slots with non-null content in each slot.
- 2D-TIC matrix dimensions are consistent: rows = floor(total_chromatogram_length / modulation_time_samples), columns = modulation_time_samples.
- Primary retention times vector length matches the number of rows in the 2D-TIC matrix (one retention time per primary peak).
- NetCDF file name is correctly validated and stored in slot 3 without truncation or corruption.
- Modulation time in slot 4 matches the input parameter and corresponds to expected instrument cycle time (typically 5 seconds).

## Limitations

- Requires valid NetCDF format input with proper instrument metadata; malformed or legacy chromatogram formats will cause import failure.
- Modulation time must be specified manually by the user; no automatic detection from file metadata is performed, creating risk of user error if instrument configuration is unknown.
- The function does not perform any signal quality checks—noisy, saturated, or incomplete chromatograms are folded without warning, potentially producing uninformative 2D-TIC representations.

## Evidence

- [intro] Import workflow start point: "first, the raw chromatogram is importing from a NetCDF file and is folded into the two-dimensional Total Intensity Chromatogram (2D-TIC)."
- [other] Object structure specification: "The read_chrom function returns a four-slot object where: slot 1 contains the 2D-TIC chromatogram, slot 2 contains retention time in the first dimension, slot 3 contains the NetCDF file name"
- [other] Modulation parameter usage: "Call read_chrom with the 08GB.cdf NetCDF file and modulation parameter set to 5 to fold the raw chromatogram into a 2D-TIC object."
- [readme] Tool purpose and preprocessing context: "The goal of RGCxGC is to provide an easy-to-use platform to analyze two-dimensional gas chromatography data."

---
name: chromatogram-netcdf-file-import
description: Use when you have raw GCxGC-MS chromatogram data in NetCDF (CDF) format from an instrument and need to load it into R for preprocessing (smoothing, baseline correction, peak alignment) and multivariate analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_3520
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

# chromatogram-netcdf-file-import

## Summary

Import raw two-dimensional gas chromatography data from NetCDF files and fold them into a 2D-TIC (Total Intensity Chromatogram) object for downstream preprocessing and analysis. This is the essential entry point for GCxGC-MS workflows, converting instrument output into an R-native data structure.

## When to use

You have raw GCxGC-MS chromatogram data in NetCDF (CDF) format from an instrument and need to load it into R for preprocessing (smoothing, baseline correction, peak alignment) and multivariate analysis. The modulation time parameter must be known from your instrument's acquisition settings (e.g., 5 seconds for typical GCxGC).

## When NOT to use

- Input data is already in a preprocessed feature matrix (e.g., peak intensity table, metabolite abundance table) rather than raw chromatogram.
- NetCDF file is from a one-dimensional (1D) GC or LC instrument, not comprehensive GCxGC.
- Modulation time is unknown or misspecified; incorrect folding parameters will produce a malformed 2D-TIC with wrong dimensions.

## Inputs

- NetCDF file (.cdf) containing raw GCxGC-MS chromatogram data from a two-dimensional gas chromatograph
- modulation time parameter (numeric, in seconds; e.g., 5 for a 5-second second-dimension cycle)

## Outputs

- Four-slot RGCxGC object containing: slot 1 = 2D-TIC chromatogram (matrix), slot 2 = first-dimension retention times (numeric vector), slot 3 = NetCDF file name (character), slot 4 = modulation time (numeric)

## How to apply

Load the RGCxGC package and call the read_chrom function with the NetCDF file path and a modulation parameter matching your instrument's second-dimension cycle time. The function parses the NetCDF file, validates it upon import, and returns a four-slot object: the 2D-TIC matrix in slot 1, first-dimension retention times in slot 2, the validated file name in slot 3, and the modulation time in slot 4. Inspect the returned object structure to confirm all four slots are populated and that the TIC matrix dimensions align with your expected chromatographic resolution (typically hundreds of scans in each dimension for comprehensive GCxGC).

## Related tools

- **RGCxGC** (Provides read_chrom function to parse NetCDF files and construct the 2D-TIC object; part of the wider RGCxGC preprocessing and analysis pipeline) — https://github.com/DanielQuiroz97/RGCxGC
- **R** (Runtime environment for RGCxGC and the read_chrom function)

## Examples

```
library(RGCxGC); chrom_obj <- read_chrom('08GB.cdf', modulation=5)
```

## Evaluation signals

- Returned object has exactly four slots with no NULL or empty values.
- Slot 1 (2D-TIC matrix) has numeric type and dimensions matching expected instrument resolution (e.g., ~500 × ~500 for typical GCxGC scans).
- Slot 3 (file name) exactly matches the input NetCDF file name, confirming successful validation upon import.
- Slot 4 (modulation time) equals the modulation parameter passed to read_chrom.
- Slot 2 (retention times) is a monotonically increasing numeric vector with length matching the first dimension of the 2D-TIC matrix.

## Limitations

- Requires prior knowledge of the instrument's modulation time; incorrect specification will fold the raw chromatogram into wrong 2D dimensions.
- NetCDF file must be valid and readable; corrupted or non-standard instrument formats may fail validation.
- The 2D-TIC object is the raw, unprocessed chromatogram; subsequent preprocessing (baseline correction, smoothing, peak alignment) is required before meaningful pattern detection or multivariate analysis.

## Evidence

- [other] first-dimension retention time validation: "slot 1 contains the 2D-TIC chromatogram, slot 2 contains retention time in the first dimension, slot 3 contains the NetCDF file name (validated upon import), and slot 4 contains the modulation time"
- [intro] read_chrom function workflow: "first, the raw chromatogram is importing from a NetCDF file and is folded into the two-dimensional Total Intensity Chromatogram (2D-TIC)"
- [readme] RGCxGC package purpose: "The goal of RGCxGC is to provide an easy-to-use platform to analyze two-dimensional gas chromatography data"
- [other] modulation parameter specification: "Call read_chrom with the 08GB.cdf NetCDF file and modulation parameter set to 5 to fold the raw chromatogram into a 2D-TIC object"

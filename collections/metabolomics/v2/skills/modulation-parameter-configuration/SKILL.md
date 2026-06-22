---
name: modulation-parameter-configuration
description: Use when you have a raw GCxGC-MS chromatogram in NetCDF format (.cdf file) and need to import it into R as a 2D-TIC object for preprocessing (smoothing, baseline correction, peak alignment) or multivariate analysis.
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

# modulation-parameter-configuration

## Summary

Configure the modulation parameter when importing raw GCxGC-MS chromatograms from NetCDF files to correctly fold the one-dimensional raw signal into a two-dimensional Total Intensity Chromatogram (2D-TIC). The modulation parameter specifies the period (in seconds) of the second dimension, which is critical for proper data structure and subsequent preprocessing.

## When to use

You have a raw GCxGC-MS chromatogram in NetCDF format (.cdf file) and need to import it into R as a 2D-TIC object for preprocessing (smoothing, baseline correction, peak alignment) or multivariate analysis. The modulation parameter must be set to match the instrument's modulation time—the cycle time of the secondary oven in the comprehensive 2D separation.

## When NOT to use

- Input is already a preprocessed 2D chromatogram object or peak table—use read_chrom only for raw NetCDF imports
- Modulation time is unknown or not documented for the instrument—you must obtain this value from instrument metadata or method parameters before calling read_chrom
- Input file is not in NetCDF format (e.g., .mzML, .raw, or ASCII text)—read_chrom is specific to NetCDF chromatogram files

## Inputs

- NetCDF chromatogram file (.cdf format) from GCxGC-MS instrument
- Modulation time parameter (numeric, in seconds)

## Outputs

- Four-slot S4 object containing 2D-TIC chromatogram matrix
- First-dimension retention time vector
- Validated input file name
- Second-dimension modulation time value

## How to apply

Call the read_chrom function with the NetCDF file path and set the modulation parameter to the correct modulation time in seconds. For example, a modulation time of 5 seconds folds the raw chromatogram at 5-second intervals, creating a 2D matrix where the first dimension is the first retention time and the second dimension is the modulation time (secondary oven period). The function validates the NetCDF file upon import and returns a four-slot S4 object: slot 1 contains the 2D-TIC chromatogram matrix, slot 2 contains first-dimension retention times, slot 3 contains the validated file name, and slot 4 contains the modulation time. Verify correct folding by inspecting the object structure and checking that the 2D-TIC dimensions match expected instrument parameters.

## Related tools

- **RGCxGC** (Provides read_chrom function to import and fold NetCDF chromatograms into 2D-TIC objects with configurable modulation parameter) — https://github.com/DanielQuiroz97/RGCxGC
- **R** (Execution environment for RGCxGC package and read_chrom function)

## Examples

```
library(RGCxGC); chrom_obj <- read_chrom('08GB.cdf', modulation=5); str(chrom_obj)
```

## Evaluation signals

- Object class is S4 with exactly four slots accessible via @ accessor
- Slot 1 (2D-TIC matrix) dimensions are consistent with modulation parameter: nrow × ncol matches expected first-dimension × modulation-period folding
- Slot 2 (first-dimension retention times) is a numeric vector with length matching matrix rows
- Slot 3 (file name) exactly matches the input NetCDF file path, confirming validation occurred
- Slot 4 (modulation time) equals the input modulation parameter value

## Limitations

- Modulation parameter must be known or inferred from instrument metadata; incorrect values produce incorrectly folded 2D matrices that will distort subsequent preprocessing and analysis
- read_chrom validates only that the NetCDF file exists and is readable; it does not verify chemical/instrumental correctness of the data or warn if modulation parameter is physically implausible
- The function expects standard NetCDF chromatogram structure; non-standard or corrupted files may fail to import or produce unexpected object structures

## Evidence

- [intro] RGCxGC workflow initiation: "first, the raw chromatogram is importing from a NetCDF file and is folded into the two-dimensional Total Intensity Chromatogram (2D-TIC)"
- [other] read_chrom function behavior and output structure: "The read_chrom function returns a four-slot object where: slot 1 contains the 2D-TIC chromatogram, slot 2 contains retention time in the first dimension, slot 3 contains the NetCDF file name"
- [other] Modulation parameter application: "Call read_chrom with the 08GB.cdf NetCDF file and modulation parameter set to 5 to fold the raw chromatogram into a 2D-TIC object"
- [readme] RGCxGC package scope: "The goal of RGCxGC is to provide an easy-to-use platform to analyze two-dimensional gas chromatography data"

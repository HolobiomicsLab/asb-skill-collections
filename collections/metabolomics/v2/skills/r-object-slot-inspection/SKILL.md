---
name: r-object-slot-inspection
description: Use when after calling a data import function (such as read_chrom on a NetCDF chromatogram file) that returns a structured S4 object, inspect its slots to confirm the object was constructed correctly, validate that retention times and modulation parameters were parsed as expected, and ensure the.
license: CC-BY-4.0
metadata:
  edam_topics: []
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# R Object Slot Inspection

## Summary

Inspect and validate the internal structure of S4 R objects returned by data import functions, verifying that slots contain expected data types, dimensions, and metadata. This skill is essential for confirming correct parsing of instrument output files (e.g., NetCDF chromatograms) before downstream preprocessing.

## When to use

After calling a data import function (such as read_chrom on a NetCDF chromatogram file) that returns a structured S4 object, inspect its slots to confirm the object was constructed correctly, validate that retention times and modulation parameters were parsed as expected, and ensure the file name and metadata are properly stored before proceeding to preprocessing steps like smoothing or baseline correction.

## When NOT to use

- Input is already a preprocessed feature table or peak list; slot inspection is only relevant for raw or minimally processed S4 objects from import functions.
- Working with data formats other than NetCDF (e.g., plain CSV, mzML); this skill is specific to instrument file parsing workflows.
- Object structure is already documented and validated by upstream code; redundant inspection wastes computational time.

## Inputs

- S4 object returned by read_chrom (RGCxGC)
- NetCDF chromatogram file (e.g., *.cdf)

## Outputs

- Validated 2D-TIC chromatogram matrix (slot 1)
- Retention time vector – first dimension (slot 2)
- NetCDF file name / path (slot 3)
- Modulation time scalar (slot 4)

## How to apply

Load the RGCxGC package and call read_chrom with a NetCDF file and modulation parameter (e.g., modulation=5 to fold raw chromatogram data into 2D-TIC). Examine the returned object by printing or indexing its four slots: slot 1 contains the 2D-TIC chromatogram matrix, slot 2 contains retention time values for the first dimension, slot 3 contains the imported NetCDF file name as a character string (used to validate import integrity), and slot 4 contains the modulation time in the second dimension. Check that slot 1 has the expected matrix dimensions, slot 2 and slot 4 are numeric vectors of appropriate length, and slot 3 matches the input file path. This verification step ensures that instrumental artifacts were not introduced during import and that all required metadata is accessible for later preprocessing and alignment.

## Related tools

- **RGCxGC** (Defines the four-slot S4 object returned by read_chrom; provides the read_chrom import function for NetCDF chromatograms.) — https://github.com/DanielQuiroz97/RGCxGC
- **R** (Host language for object slot access and validation using `@` operator and class introspection.)

## Examples

```
library(RGCxGC); chromatogram_obj <- read_chrom('08GB.cdf', modulation=5); chromatogram_obj@slot1; chromatogram_obj@slot2; chromatogram_obj@slot3; chromatogram_obj@slot4
```

## Evaluation signals

- Returned object is of class matching RGCxGC's S4 definition (verify with class()).
- Slot 1 (2D-TIC) is a numeric matrix with non-zero dimensions matching expected folding of raw chromatogram.
- Slot 2 (retention time) is a numeric vector of length equal to first dimension of slot 1; values are in ascending order and positive.
- Slot 3 (file name) is a character string matching the input NetCDF file path or name, confirming file was successfully parsed.
- Slot 4 (modulation time) is a numeric scalar with a value close to the modulation parameter passed to read_chrom (e.g., 5 seconds).

## Limitations

- Slot inspection does not verify chemical correctness or absence of instrumental noise; it only confirms structural integrity.
- Modulation time validation assumes the modulation parameter passed to read_chrom is correct; user must confirm this matches instrument settings.
- The four-slot structure is specific to RGCxGC; other chromatography packages may use different object schemas.

## Evidence

- [other] The read_chrom function returns a four-slot object where: slot 1 contains the 2D-TIC chromatogram, slot 2 contains retention time in the first dimension, slot 3 contains the NetCDF file name (validated upon import), and slot 4 contains the modulation time in the second dimension.: "The read_chrom function returns a four-slot object where: slot 1 contains the 2D-TIC chromatogram, slot 2 contains retention time in the first dimension, slot 3 contains the NetCDF file name"
- [intro] first, the raw chromatogram is importing from a NetCDF file and is folded into the two-dimensional Total Intensity Chromatogram (2D-TIC).: "first, the raw chromatogram is importing from a NetCDF file and is folded into the two-dimensional Total Intensity Chromatogram (2D-TIC)."
- [other] Call read_chrom with the 08GB.cdf NetCDF file and modulation parameter set to 5 to fold the raw chromatogram into a 2D-TIC object.: "Call read_chrom with the 08GB.cdf NetCDF file and modulation parameter set to 5 to fold the raw chromatogram into a 2D-TIC object."

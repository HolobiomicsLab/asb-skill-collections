---
name: methylation-probe-count-validation
description: Use when immediately after loading raw methylation array data using champ.load() or champ.import() to verify data integrity.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3295
  - http://edamontology.org/topic_0654
  tools:
  - ChAMP
  - ChAMPdata
  - minfi
derived_from:
- doi: 10.1093/bioinformatics/btx513
  title: champ
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/epigenomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_champ
    doi: 10.1093/bioinformatics/btx513
    title: champ
  dedup_kept_from: coll_champ
schema_version: 0.2.0
---

# methylation-probe-count-validation

## Summary

Validate that DNA methylation array data has been loaded with the correct total number of probes before quality-based filtering. This skill confirms successful data import and array-type detection by verifying pre-filter probe counts against expected canonical values for HumanMethylation450K and EPIC arrays.

## When to use

Apply this skill immediately after loading raw methylation array data using champ.load() or champ.import() to verify data integrity. Use it when you need confidence that the correct array type was detected and all available probes were successfully imported before any downstream filtering, normalization, or analysis steps.

## When NOT to use

- Data has already been filtered by quality metrics; expected probe counts only apply to unfiltered raw imports.
- Array type is unknown or non-standard (e.g., mouse arrays or custom manifests); canonical probe counts apply only to human 450K and EPIC v1/v2.
- Input is a pre-processed feature table or reduced dataset; this skill requires raw array data at full probe dimensionality.

## Inputs

- .idat files (methylation array raw data)
- beta-valued matrix
- array type specification (450K or EPIC)
- ChAMPdata annotation package (version ≥2.23.1)

## Outputs

- pre-filter probe count integer
- confirmation of array type detection
- validated methylation data object ready for downstream analysis

## How to apply

Load methylation array data from .idat files or a beta-valued matrix using champ.load() with the appropriate array type specification. Extract the pre-filter probe count from the returned data object before any quality-control or filtering steps are applied. Compare the reported probe count against the expected canonical values: 485,512 probes for HumanMethylation450 (450K) arrays and 867,531 probes for EPIC arrays. If the observed count matches the expected value, data import was successful and array-type detection is correct. If counts deviate, investigate array annotation mismatches or file corruption.

## Related tools

- **ChAMP** (Primary tool for loading methylation array data and retrieving pre-filter probe counts via champ.load() and champ.import() functions) — https://github.com/YuanTian1991/ChAMP
- **ChAMPdata** (Provides CpG-probe manifests and array annotations required to resolve probe identities and canonical counts) — https://github.com/YuanTian1991/ChAMPdata
- **minfi** (Alternative methylation array analysis package; provides complementary data import and validation functions)

## Examples

```
library(ChAMP); myLoad <- champ.load(directory='./idat_files/', arraytype='450K'); print(dim(myLoad$beta)[1]); # Should output 485512
```

## Evaluation signals

- Observed pre-filter probe count equals 485,512 for HumanMethylation450 array or 867,531 for EPIC array (exact match indicates correct import).
- Array type in the returned data object metadata matches the input array specification (no silent type mismatch).
- Probe dimensionality in the output matrix matches the reported probe count (no silent loss of probes during import).
- No warnings or errors logged during champ.load() execution indicating file corruption or annotation mismatches.
- Probe count remains unchanged before and after loading, confirming no pre-filtering occurred during import step.

## Limitations

- Canonical probe counts apply only to standard human HumanMethylation450 and EPIC v1/v2 arrays; EPICv2 and other array types may have different expected values.
- This validation step does not detect quality issues, batch effects, or cross-sample contamination; it only confirms structural integrity of the import.
- ChAMP version 2.29.1 and ChAMPdata ≥2.23.1 must be installed; older versions may have different probe counts or array support limitations.
- Validation assumes .idat files are uncorrupted and match the declared array type; file corruption or type mismatch will produce incorrect counts not caught by this skill alone.

## Evidence

- [other] finding: "The ChAMP loading functions should return 485,512 probes for 450K arrays and 867,531 probes for EPIC arrays before any quality-based filtering is applied."
- [other] workflow: "Load HumanMethylation450 test dataset (450K lung tumor data with 8 samples) using champ.load() function. Verify pre-filter probe count equals 485,512 for the 450K array."
- [intro] data_import_method: "a variety of different data import methods (e.g. from .idat files or a beta-valued matrix)"
- [readme] version_requirement: "Current latest version: `2.29.1`, which support EPICv2, but it must be used along with ChAMPdata >= 2.23.1"

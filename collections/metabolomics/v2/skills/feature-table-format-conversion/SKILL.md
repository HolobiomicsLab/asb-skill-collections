---
name: feature-table-format-conversion
description: Use when you have raw feature tables exported from NPP tools (XCMS, MZmine 2, MS-DIAL, OpenMS, etc.) in their native formats and need to compare their peak detection and alignment performance against a mzRAPP benchmark dataset.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - mzRAPP
  - R
  - XCMS
  - MZmine 2
  techniques:
  - mass-spectrometry
derived_from:
- doi: 10.1093/bioinformatics/btab231/6214530
  title: mzRAPP
evidence_spans:
- 'You can now start mzRAPP using: library(mzRAPP); callmzRAPP()'
- The goal of mzRAPP is to allow reliability assessment of non-targeted data pre-processing (NPP)
- library(mzRAPP)
- You can then assess the performance of NPP runs we have performed via XCMS
- Download the XCMS- and MZmine 2-output files from [ucloud]
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mzrapp_cq
    doi: 10.1093/bioinformatics/btab231/6214530
    title: mzRAPP
  dedup_kept_from: coll_mzrapp_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioinformatics/btab231/6214530
  all_source_dois:
  - 10.1093/bioinformatics/btab231/6214530
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# feature-table-format-conversion

## Summary

Convert non-targeted preprocessing (NPP) output feature tables from vendor or tool-specific formats into a standardized CSV schema compatible with benchmark-to-NPP matching workflows. This enables reliable comparison of peak detection and alignment performance across different metabolomics preprocessing tools.

## When to use

You have raw feature tables exported from NPP tools (XCMS, MZmine 2, MS-DIAL, OpenMS, etc.) in their native formats and need to compare their peak detection and alignment performance against a mzRAPP benchmark dataset. Conversion is required before the BM-NPP matching module can assess reliability metrics.

## When NOT to use

- Feature tables are already in mzRAPP-native format or have been previously aligned to a benchmark.
- Input is a raw mzML file rather than a preprocessed feature table; use mzRAPP benchmark generation first.
- Feature table lacks m/z and retention time information; conversion cannot establish the dimensional basis for matching.

## Inputs

- Unaligned feature table CSV from NPP tool (XCMS, MZmine 2, MS-DIAL, OpenMS, or El-MAVEN)
- Aligned feature table CSV from the same NPP tool
- mzRAPP benchmark CSV file (Benchmark.csv with 2870 peaks or equivalent)

## Outputs

- Standardized feature table compatible with mzRAPP matching algorithm
- Matched record CSV table with benchmark peak identifiers, matching status (found/split/missing/misaligned), confidence scores, and isotopologue validation flags

## How to apply

Export unaligned and aligned feature tables from your NPP tool in CSV format, ensuring they contain at minimum m/z values, retention time information, and peak identifiers. Load the exported tables into mzRAPP's Setup NPP assessment tab by specifying the file paths for both unaligned and aligned outputs. mzRAPP internally parses these tables to map them against benchmark peaks using 6 ppm m/z precision tolerance and retention-time windowing. The conversion preserves feature identifiers and metadata while standardizing column interpretation for downstream m/z and RT matching against the benchmark. No manual column remapping is required if tables follow the standard NPP output schema (m/z, RT, peak area/height, feature ID); custom parsers may be needed for non-standard formats.

## Related tools

- **mzRAPP** (Performs feature table parsing, standardization, and BM-NPP matching; loads and validates converted tables against benchmark) — https://github.com/YasinEl/mzRAPP
- **XCMS** (NPP tool whose aligned and unaligned feature table outputs are converted for benchmark assessment)
- **MZmine 2** (NPP tool whose feature table outputs can be exported in CSV and converted for benchmark comparison)
- **R** (Scripting environment for programmatic feature table loading and conversion before mzRAPP assessment)

## Examples

```
library(mzRAPP); callmzRAPP()
```

## Evaluation signals

- Feature table successfully loads into mzRAPP without parsing errors; column headers are recognized.
- m/z and retention time values are numeric and within expected LC-HRMS ranges (e.g., m/z 50–1200, RT in seconds).
- Peak identifiers are unique and preserved from NPP tool output; no rows are dropped during conversion.
- Matching produces non-zero counts in the 'found', 'split', 'missing', or 'misaligned' categories; at least 80–90% of benchmark peaks are classified.
- Confidence scores and isotopologue validation flags are populated; isotopologue ratio bias filtering (< 30% threshold) is applied to matched clusters.

## Limitations

- Conversion assumes feature tables follow standard NPP output schemas (m/z, RT, feature ID columns present); tables from custom or proprietary tools may require manual column mapping or custom parser development.
- m/z matching tolerance is fixed at 6 ppm precision and 5 ppm accuracy; conversion does not adapt to different mass spectrometers or resolution profiles beyond what mzRAPP's instrument selection provides.
- Conversion does not recover missing or incorrectly reported retention time boundaries; feature tables lacking RT information cannot be reliably matched to benchmark peaks.
- Peak shape correlation and isotopologue ratio validation occur post-conversion; conversion itself does not assess peak quality. Degenerated isotopologue ratios (> 30% bias or Pearson r < 0.85 vs. most abundant isotopologue) are filtered by matching, not by the conversion step.
- Alignment-stage matching depends on both unaligned and aligned table quality; if NPP alignment introduces systematic RT drift or feature merging, matching may classify peaks as 'split' or 'misaligned' even after conversion.

## Evidence

- [intro] Export NPP outputs from different tools: "Exporting NPP outputs from different tools"
- [readme] mzRAPP accepts feature tables from multiple NPP tools: "The goal of mzRAPP is to allow reliability assessment of non-targeted data pre-processing (NPP; XCMS, XCMS3, MetaboanalystR 3.0, SLAW, XCMS-online, MZmine 2, MZmine 3, MS-DIAL, OpenMS, El-MAVEN,..)"
- [methods] Matching workflow with standardized m/z and RT criteria: "For each benchmark peak, apply m/z matching with specified precision tolerance (6 ppm) and accuracy threshold (5 ppm) to candidate NPP features. 3. Apply retention-time windowing to narrow candidate"
- [methods] mzRAPP performs benchmark-NPP matching on converted tables: "In the Setup NPP assessment tab, select mzRAPP as the non-targeted tool and specify XCMS_unaligned_run1.csv as the unaligned file and XCMS_aligned_run1.csv as the aligned file. 3. Execute the"
- [methods] Isotopologue validation occurs during matching: "For isotopologue clusters, validate peak shape correlation with the most abundant isotopologue and filter isotopologues where isotopologue ratio bias exceeds 30%"
- [readme] Feature table must include sample, m/z, RT metadata: "Since start- and end-time has to be provided for each compound it is advisable to set those boundaries using a tool for manual peak curation from which peak boundaries can be exported"

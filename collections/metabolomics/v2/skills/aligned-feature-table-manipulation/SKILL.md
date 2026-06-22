---
name: aligned-feature-table-manipulation
description: Use when after multi-sample alignment has been completed in JPA (Part 5), when you have an aligned feature table containing consolidated features across samples and need to extract ion chromatograms, perform CAMERA annotation, or validate feature assignments prior to MS2 annotation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3370
  tools:
  - JPA
  - R
  - XCMS
derived_from:
- doi: 10.3390/metabo12030212
  title: JPA
evidence_spans:
- JPA is a comprehensive and integrated metabolomics data processing software.
- JPA is a comprehensive and integrated metabolomics data processing software
- '''JPA'' is written in R and its source code is publicly available'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_jpa_cq
    doi: 10.3390/metabo12030212
    title: JPA
  dedup_kept_from: coll_jpa_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.3390/metabo12030212
  all_source_dois:
  - 10.3390/metabo12030212
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# aligned-feature-table-manipulation

## Summary

Load and parse aligned metabolomics feature tables (peaklists or feature matrices from multi-sample LC-MS analysis) into R memory structures, extracting feature metadata (m/z, retention time, intensity, sample assignments) for downstream processing in JPA. This skill bridges sample alignment output and post-alignment operations like EIC export or annotation.

## When to use

After multi-sample alignment has been completed in JPA (Part 5), when you have an aligned feature table containing consolidated features across samples and need to extract ion chromatograms, perform CAMERA annotation, or validate feature assignments prior to MS2 annotation.

## When NOT to use

- Input is a single-sample (unalignable) feature table—use custom.featureTable() or XCMS.featureTable() instead on raw data or per-sample CSVs.
- Alignment has not yet been performed—run Part 5 alignment first; aligned feature tables are not acceptable as input to alignment functions.
- Raw or unprocessed LC-MS data without prior feature extraction—use MS1 peak picking (Part 2) or MS2 recognition (Part 3) first.

## Inputs

- Aligned feature table (dataframe or CSV) from JPA Part 5 alignment output
- Feature metadata including m/z, retention time (in seconds), intensity, and sample assignment columns
- Raw or processed mass spectrometry data (mzXML, mzML) referenced by sample identifiers in the feature table

## Outputs

- Parsed feature table dataframe in R with validated columns (mz, rt, rtmin, rtmax, maxo, sample, level)
- Feature metadata structure ready for feature-level queries (e.g., m/z and rt pairs for EIC extraction)
- Sample-to-feature mapping for multi-sample analysis operations

## How to apply

Load the aligned feature table (output from JPA alignment step) into the R environment using JPA data structures. Parse feature metadata columns: m/z, retention time (rt), sample identifiers, and intensity values (maxo or Height). For each feature or user-defined subset of interest, the metadata row provides the exact m/z and retention time needed to query raw mass spectrometry data or generate downstream outputs. Validate that the table structure contains the required columns (mz, rt, rtmin, rtmax, maxo/Height, sample) before proceeding to feature-level operations like EIC extraction. The aligned table differs from single-sample feature tables in that it contains cross-sample feature correspondence already resolved, so duplicate m/z–rt pairs across samples point to the same biological feature.

## Related tools

- **JPA** (R package that generates and manages aligned feature tables; provides data structures and functions to load and parse feature metadata across samples) — https://github.com/HuanLab/JPA.git
- **R** (Host environment for loading, parsing, and manipulating aligned feature table dataframes; required version 4.0.0 or above)
- **XCMS** (Bioconductor package embedded in JPA for initial feature extraction; alignment core used to generate the aligned feature table) — https://rdrr.io/bioc/xcms/man/

## Examples

```
# Load aligned feature table from JPA Part 5 output and parse metadata
alignedTable <- read.csv('aligned_features.csv', header = TRUE, stringsAsFactors = FALSE)
head(alignedTable[, c('mz', 'rt', 'rtmin', 'rtmax', 'maxo', 'sample', 'level')])
```

## Evaluation signals

- Feature table loads into R without errors; dataframe structure is intact with all expected columns (mz, rt, rtmin, rtmax, maxo, sample, level).
- All m/z values are numeric, non-negative, and within expected MS1 range (typically 50–1500 m/z); all retention times are positive and expressed in seconds.
- Sample identifiers in the 'sample' column match the input raw data filenames or provided sample metadata.
- No duplicate mz–rt–sample triplets exist (i.e., each feature is represented once per sample in the aligned table); cross-sample features share the same mz and rt (within alignment tolerance) but differ by sample ID.
- Metadata validation passes: rtmin < rt < rtmax for all rows; maxo (intensity) values are positive and consistent with raw MS data peak intensities.

## Limitations

- Aligned feature tables are sample-specific and cannot be directly re-aligned; if re-processing is needed, start from raw mzXML files or per-sample CSV tables.
- The alignment tolerance used in Part 5 determines the precision of m/z and rt matching across samples; features outside this tolerance are treated as separate features and appear as duplicates in the output.
- Feature table does not contain MS2 spectral data; MS2 annotation (Part 7) requires separate MS2 spectra retrieval or linking to external databases.
- Quality and completeness of the aligned table depend on the earlier feature extraction method (MS1 peak picking, MS2 recognition, or targeted list); errors in extraction are propagated to downstream operations.

## Evidence

- [other] Load aligned feature data (peaklist or feature matrix from prior JPA alignment step) into the R environment using JPA data structures.: "Load aligned feature data (peaklist or feature matrix from prior JPA alignment step) into the R environment using JPA data structures."
- [other] Parse feature metadata (m/z, retention time, intensity, sample assignments) from the feature table.: "Parse feature metadata (m/z, retention time, intensity, sample assignments) from the feature table."
- [readme] for multi-sample analysis, sample alignment is performed after feature extraction. It will be discussed in section 5.: "for multi-sample analysis, sample alignment is performed after feature extraction. It will be discussed in section 5."
- [readme] The input feature table contain only columns in the following order: m/z, retention time, min retention time, max retention time, intensity.: "The input feature table contain only columns in the following order: m/z, retention time, min retention time, max retention time, intensity."
- [readme] The 'level' column shows the level of each feature.: "The 'level' column shows the level of each feature."

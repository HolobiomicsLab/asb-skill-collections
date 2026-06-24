---
name: lc-ms-feature-extraction-and-alignment
description: Use when you have centroid mzML files from LC-MS experiments (converted
  from Thermo .raw or other vendor formats) and need to identify and quantify individual
  chemical features across multiple samples.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3215
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
  tools:
  - Python
  - ThermoRawFileParser
  - Asari
  - khipu
  - PCPFM (Python-Centric Pipeline for Metabolomics)
  techniques:
  - LC-MS
  - GC-MS
  license_tier: restricted
derived_from:
- doi: 10.1371/journal.pcbi.1011912
  title: pcpfm
evidence_spans:
- Python-Centric Pipeline for Metabolomics
- The Python-Centric Pipeline for Metabolomics
- convert Thermo .raw to mzML (ThermoRawFileParser)
- process mzML data to feature tables (Asari)
- pre-annotation to group featues to empirical compounds (khipu)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_pcpfm
    doi: 10.1371/journal.pcbi.1011912
    title: pcpfm
  dedup_kept_from: coll_pcpfm
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1371/journal.pcbi.1011912
  all_source_dois:
  - 10.1371/journal.pcbi.1011912
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# LC-MS Feature Extraction and Alignment

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Automated extraction of chemical features (m/z and retention time peaks) from centroid mzML files and alignment across samples using Asari, producing full and preferred feature tables with configurable mass and time tolerances. This foundational step converts raw LC-MS data into a normalized feature matrix suitable for downstream statistical analysis.

## When to use

You have centroid mzML files from LC-MS experiments (converted from Thermo .raw or other vendor formats) and need to identify and quantify individual chemical features across multiple samples. Use this skill when you are moving from raw acquisition files to a tabular feature table, typically as the first major processing step after format conversion.

## When NOT to use

- Input files are already in feature table format (e.g., from prior Asari run or another peak-picking tool) — skip directly to blank masking or normalization.
- Data are from GC-MS or other non-LC ionization platforms — Asari currently focuses on LC-MS; GC support is under development.
- Raw data are in profile mode rather than centroid mode — Asari requires centroid mzML; profile data must be centroided first.

## Inputs

- mzML files (centroid mode, from Thermo .raw conversion or native format)
- experiment metadata (sample names, ionization mode if not auto-inferred)
- instrument calibration parameters (optional, for m/z tolerance tuning)

## Outputs

- full_feature_table.tsv (all detected features, m/z × sample intensity matrix)
- preferred_feature_table.tsv (refined feature subset, recommended for downstream use)
- feature metadata (retention time, m/z, detection frequency per feature)

## How to apply

Run the Asari feature extraction module via `pcpfm asari` on a set of mzML files. Asari automatically infers the ionization mode and applies default tolerances of 5 ppm for m/z and 2 seconds for retention time to group signal across samples into aligned features. The tool produces two output feature tables: a 'full' table containing all detected features and a 'preferred' table with refined features suitable for downstream analysis. Key decision points include whether to override default mass and time tolerances based on your instrument's calibration and chromatographic resolution, and whether to use the full or preferred feature table for subsequent steps (preferred is recommended for most analyses). The alignment process assumes features with the same nominal m/z and similar retention time across samples represent the same chemical entity.

## Related tools

- **Asari** (Core feature detection and alignment engine; processes centroid mzML files and generates aligned feature tables with configurable m/z and retention-time tolerances) — https://github.com/shuzhao-li/asari
- **ThermoRawFileParser** (Upstream format converter; transforms Thermo .raw instrument files into centroid mzML format suitable for Asari input)
- **PCPFM (Python-Centric Pipeline for Metabolomics)** (Orchestration wrapper; `pcpfm asari` command sequences experiment assembly and Asari invocation within a standardized workflow) — https://github.com/shuzhao-li-lab/PythonCentricPipelineForMetabolomics

## Examples

```
pcpfm asari --experiment_path ./my_experiment --output_path ./results
```

## Evaluation signals

- Feature table dimensions are reasonable: number of features typically ranges from hundreds to tens of thousands depending on sample complexity; number of features should be consistent between full and preferred tables (preferred ⊆ full).
- Retention time values are monotonically increasing or clustered in expected chromatographic windows; no m/z values outside the instrument's scan range (e.g., 50–2000 m/z for typical metabolomics).
- Feature intensity distributions are reproducible across biological or technical replicates; replicate samples should cluster when features are used for ordination (PCA, t-SNE) in downstream QC.
- Visual inspection via Asari's dashboard shows coherent peak shapes and minimal misalignment artifacts; the number of aligned peaks per sample should be similar, indicating consistent feature detection.
- Preferred feature table has fewer rows than full table but retains dominant features; features with high frequency (present in > 50% of samples) should predominate in preferred table after filtering.

## Limitations

- Alignment relies on m/z and retention-time proximity; isobaric compounds or isomers that co-elute may be collapsed into single features, requiring MS/MS data for disambiguation.
- Default tolerances (5 ppm, 2 sec) may require tuning for instruments with poor calibration or atypical chromatographic resolution; user must validate empirically.
- Asari currently supports LC-MS; GC-MS support is noted as under development. Lipidomics data with complex adducts or multiply-charged ions require post-hoc empirical compound grouping via khipu.
- Missing values (features detected in some samples but not others) are common and left unhandled in this step; downstream imputation is required before statistical analysis.
- Feature extraction quality depends critically on mzML file quality; poorly centroided or uncalibrated raw files will produce degraded or misaligned feature tables.

## Evidence

- [other] Asari feature extraction producing full and preferred feature tables: "Asari feature extraction producing full and preferred feature tables; blank masking by comparing sample to blank intensities"
- [other] Default 5 ppm m/z tolerance and 2 sec retention-time tolerance: "with default 5 ppm m/z tolerance and 2 sec retention-time tolerance"
- [readme] Asari supports a visual dashboard to explore and inspect individual features: "Asari supports a visual dashboard to explore and inspect individual features"
- [readme] Process mzML data to feature tables using Asari: "process mzML data to feature tables (Asari)"
- [other] Convert Thermo .raw to centroid mzML format using ThermoRawFileParser: "Convert Thermo .raw files to centroid mzML format using ThermoRawFileParser via pcpfm convert command"

---
name: knime-workflow-orchestration
description: Use when you have raw LC-MS data (mzML, NetCDF) from multiple runs that
  require sequential feature detection, alignment, quantification, and optional filtering
  (e.g., blank exclusion, QC reproducibility, retention-time outlier removal) before
  spatial mapping or annotation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_3520
  tools:
  - KNIME
  - KNIME Analytics Platform
  - OpenMS
  - Python 2.7 + pandas, pymspec, pyopenms
  - ili app
  - GNPS
  techniques:
  - LC-MS
  - direct-infusion-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1038/nprot.2017.122
  title: 3D molecular cartography (Optimus / 'ili)
evidence_spans:
- KNIME Basics
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_3d_molecular_cartography_optimus_ili_cq
    doi: 10.1038/nprot.2017.122
    title: 3D molecular cartography (Optimus / 'ili)
  dedup_kept_from: coll_3d_molecular_cartography_optimus_ili_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/nprot.2017.122
  all_source_dois:
  - 10.1038/nprot.2017.122
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# knime-workflow-orchestration

## Summary

Orchestrate multi-stage LC-MS feature detection, alignment, filtering, and annotation workflows in KNIME by connecting OpenMS nodes, Python integration modules, and data I/O components. This skill enables reproducible, parameterized execution of untargeted metabolomics pipelines across hundreds of LC-MS runs.

## When to use

You have raw LC-MS data (mzML, NetCDF) from multiple runs that require sequential feature detection, alignment, quantification, and optional filtering (e.g., blank exclusion, QC reproducibility, retention-time outlier removal) before spatial mapping or annotation. Use this skill when you need to scale a metabolomics workflow across a cohort and maintain reproducibility via workflow versioning rather than ad-hoc scripting.

## When NOT to use

- Input is already a processed feature table (e.g., peak-picked intensity matrix); skip to normalization/annotation only.
- Data are from targeted MS/MS (MRM/SRM) rather than untargeted LC-MS-based metabolomics; Optimus is designed for feature detection, not transition optimization.
- Direct-infusion MS (no LC separation): Optimus supports DI-MS but retention-time-based filters should be disabled and workflow adapted accordingly.

## Inputs

- LC-MS feature detection input (mzML, NetCDF, or raw instrument files)
- Experimental design file (CSV with sample metadata, run order, QC/blank flags)
- Stub input file (featureXML template or reference feature structure)
- Optional: internal standard list (CSV or GNPS export) for normalization
- Optional: MS/MS spectral library (msp, mgf) for feature annotation

## Outputs

- LC-MS feature table (intensity matrix, features × samples)
- Aligned feature metadata (m/z, retention time, quality metrics)
- Putative molecular annotations (m/z-RT matched to reference list)
- Normalized intensities (TIC-, internal-standard-, or QC-corrected)
- PCA plot (3D sample visualization)
- Feature intensity heatmap (across samples)
- Spatial mapping data (ili-compatible JSON or tabular format)

## How to apply

Install KNIME Analytics Platform (≥2.12) with OpenMS, Python Integration, and JavaScript Views extensions. Load your experimental design file (CSV specifying sample metadata, batch, QC/blank status) and a stub input file (featureXML template) into KNIME file reader nodes. Chain OpenMS nodes (FeatureFinder, FeatureLinker) to detect and align features across all runs, then apply optional filter nodes in sequence—exclusion of blank features, rare features (< N occurrences), features lacking MS/MS spectra, non-reproducible features in QC replicates, or early/late-eluting features. Optionally apply normalization (TIC, internal standards, or QC-based) and export intensities as a feature table matrix. Validate that output schema matches expected dimensions and that feature intensities fall within expected dynamic range. Use KNIME's execution log and temporary file inspection to debug node failures.

## Related tools

- **KNIME Analytics Platform** (Workflow orchestration engine; manages node execution, data flow, and parameterization across LC-MS pipeline stages) — https://www.knime.org
- **OpenMS** (Provides LC-MS feature detection (FeatureFinder), alignment (FeatureLinker), and quantification nodes used in the Optimus pipeline) — http://www.openms.de
- **Python 2.7 + pandas, pymspec, pyopenms** (Enables custom filtering, normalization logic, and data transformation within KNIME Python nodes)
- **ili app** (Web-based visualization tool for interactive 3D spatial mapping of detected LC-MS features) — https://github.com/ili-toolbox/ili
- **GNPS** (Optional source of MS/MS spectral library and putative annotations for molecular identification of features) — http://gnps.ucsd.edu/

## Evaluation signals

- Output feature table dimensions and schema match expected samples × features; no NaN or infinite values in intensity columns.
- Feature count after each optional filter step is documented and sensible (e.g., blank-exclusion removes features present only in blank runs; QC-reproducibility filter retains only high-correlation features across replicate QC).
- Retention-time alignment produces consistent m/z-RT pairs across runs; feature-to-feature distance in aligned space is < 5 ppm mass tolerance and < 30 s retention-time window (configurable).
- Normalized intensities cluster expected samples (e.g., biological replicates, technical replicates) in PCA or heatmap; technical variance is reduced post-normalization vs. raw intensities.
- Temporal plot of internal-standard intensities (if normalization method uses IS) shows minimal drift; outlier runs flagged or removed per QC criteria.

## Limitations

- Requires ≥ 2 GB RAM for small datasets; datasets with ~100+ LC-MS runs require significantly more memory (no hard upper bound stated; depends on instrument resolution, LC run-time, data format).
- MS/MS validation of putative molecular annotations is not provided within Optimus; downstream annotation tools (SIRIUS, MS-FINDER) must be run separately.
- Temporary files created during workflow execution are not auto-deleted; manual cleanup required to reclaim disk space after iterative re-execution.
- Python 2.7 is specified; Python 3 compatibility is not discussed in README.
- Workflow assumes all LC-MS runs share common feature m/z-RT space; significant shifts in calibration or LC parameters across batches may degrade alignment.

## Evidence

- [readme] Optimus is a workflow for LC-MS-based untargeted metabolomics. It can be used for feature detection, quantification, filtering (e.g. removing background features), annotation, normalization and, finally, for spatial mapping of detected molecular features in 2D and 3D using the `ili app`.: "Optimus is a workflow for LC-MS-based untargeted metabolomics. It can be used for feature detection, quantification, filtering (e.g. removing background features), annotation, normalization and,"
- [other] The Optimus workflow requires an experimental design file and a stub input file as inputs to process LC-MS feature tables for analysis and spatial mapping.: "The Optimus workflow requires an experimental design file and a stub input file as inputs to process LC-MS feature tables"
- [readme] Optimus employes the state-of-the-art LC-MS feature detection and quantification algorithms by OpenMS which are joined into a handy pipeline with a modern workflow management software KNIME with additional features implemented by us.: "Optimus employes the state-of-the-art LC-MS feature detection and quantification algorithms by OpenMS which are joined into a handy pipeline with a modern workflow management software KNIME"
- [readme] Detection of LC-MS features in each run. Alignment and quantification of features detected across all the runs. (*Optional*) Exclusion of features that came from blank/control runs. (*Optional*) Exclusion of rarely observed features, i.e. features that occur in a small number of runs only.: "Detection of LC-MS features in each run. Alignment and quantification of features detected across all the runs... (*Optional*) Exclusion of features that came from blank/control runs. (*Optional*)"
- [readme] (*Optional*) Putative molecular annotation of detected features by mz-RT matching to a list of molecules of interest. This implements a molecular identification at the level *putatively annotated compounds*, corresponding to the level 2 of the Metabolomics Standards Initiative: "(*Optional*) Putative molecular annotation of detected features by mz-RT matching to a list of molecules of interest"
- [readme] (*Optional*) Normalization of intensities of detected features. Currently, several normalization methods are available, based on: total ion current (TIC) of each run; internal standards present in all runs; features detected in pooled QC samples.: "(*Optional*) Normalization of intensities of detected features. Currently, several normalization methods are available, based on: total ion current (TIC) of each run; internal standards present in"
- [readme] *RAM*: 2 GB is minimal amount. Generally, it is not enough for analysis of large datasets containing about a hundred or more LC-MS runs.: "*RAM*: 2 GB is minimal amount. Generally, it is not enough for analysis of large datasets containing about a hundred or more LC-MS runs"
- [other] Load the experimental design file and LC-MS feature table into KNIME using the file reader nodes. Execute the Optimus workflow nodes in sequence to perform feature analysis and spatial mapping as defined by the workflow architecture.: "Load the experimental design file and LC-MS feature table into KNIME using the file reader nodes. Execute the Optimus workflow nodes in sequence"

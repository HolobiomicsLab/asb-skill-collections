---
name: lc-ms-dataset-acquisition-and-curation
description: Use when when beginning an untargeted LC-MS metabolomics study and need
  to assemble a cohort of mzML files for processing; particularly when establishing
  performance baselines across sample counts (10, 50, 100+ samples), validating reproducibility,
  or preparing data for publication.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3945
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - asari
  - Python
  - pymzml
  - ThermoRawFileParser
  - ProteoWizard msconvert
  techniques:
  - LC-MS
  - direct-infusion-MS
  license_tier: restricted
derived_from:
- doi: 10.1038/s41467-023-39889-1
  title: asari
evidence_spans:
- Trackable and scalable Python program for high-resolution LC-MS metabolomics data
  preprocessing
- Trackable and scalable Python program for high-resolution metabolomics data processing.
- The default method uses `pymzml` to parse mzML files.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_asari
    doi: 10.1038/s41467-023-39889-1
    title: asari
  dedup_kept_from: coll_asari
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41467-023-39889-1
  all_source_dois:
  - 10.1038/s41467-023-39889-1
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# LC-MS Dataset Acquisition and Curation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Systematic retrieval, preparation, and organization of centroid mzML LC-MS metabolomics datasets from public repositories (MetaboLights, MassIVE) or vendor instruments, with format conversion and sample registry construction to enable downstream feature detection and scalability benchmarking.

## When to use

When beginning an untargeted LC-MS metabolomics study and need to assemble a cohort of mzML files for processing; particularly when establishing performance baselines across sample counts (10, 50, 100+ samples), validating reproducibility, or preparing data for publication. Also apply when converting vendor-native formats (Thermo .RAW, Waters, Bruker) to open mzML format.

## When NOT to use

- If input data are already in profile mode (not centroid) and centroid peak picking has not been performed — asari requires centroid mzML
- If MS/MS spectra are the primary analytical target and no MS1 feature detection is needed — consider specialized MS/MS workflows instead
- If sample cohort size is <10 and scalability benchmarking is the goal — minimum sample counts of 10, 50, 100+ are recommended for valid runtime/memory trend analysis

## Inputs

- Public mzML datasets from MetaboLights or MassIVE repositories
- Vendor raw data files (Thermo .RAW, Waters .raw, Bruker .d)
- Sample metadata (IDs, ionization mode, acquisition settings)

## Outputs

- Organized project directory with centroid mzML files
- Sample registry with metadata and file paths
- Indexed mzML files (if conversion was performed)
- Documentation of MS1 scan structure and m/z/RT ranges

## How to apply

Retrieve centroid mzML datasets from MetaboLights or MassIVE public repositories, or acquire vendor raw files from your instrument. Convert non-mzML vendor formats (e.g. Thermo .RAW) to indexed mzML using ThermoRawFileParser or ProteoWizard msconvert. Organize files in a project directory structure. Build a sample registry by recording metadata (sample ID, instrument mode, acquisition parameters) in a structured format. Verify all files are centroid-mode (not profile) mzML with complete MS1 spectra intact; asari ignores MS/MS spectra in default LC-MS workflow. Document MS1 scan structure, retention time range, and m/z range. If downsampling large cohorts, create replicates at defined sample counts to measure linear or near-linear scaling of runtime and peak memory usage.

## Related tools

- **ThermoRawFileParser** (Convert Thermo .RAW vendor files to mzML format for downstream asari processing) — https://github.com/compomics/ThermoRawFileParser
- **ProteoWizard msconvert** (Convert most vendor data formats and .mzXML files to centroid mzML) — https://proteowizard.sourceforge.io/tools.shtml
- **asari** (Process organized centroid mzML files into feature tables; accepts project directory structure created by this skill) — https://github.com/shuzhao-li/asari
- **pymzml** (Parse mzML files during asari processing; used internally to extract MS1 spectra)

## Examples

```
# Retrieve public test data and organize for asari processing; then profile scaling across sample counts
cd /workspace && wget -r https://github.com/shuzhao-li-lab/data/tree/main/data && ls -la data/*.mzML | head -10 && python3 -m asari.main analyze --input data/sample_001.mzML
```

## Evaluation signals

- All mzML files are centroid-mode (verified via mzML header inspection or asari analyze summary); no profile-mode files present
- Sample registry contains complete metadata (sample ID, ionization mode, file path, acquisition date) for all files
- Directory structure is consistent and navigable; all file paths in registry are valid and resolve without errors
- For cohorts used in scalability benchmarking: runtime and peak memory scale linearly or near-linearly with sample count; 2–3 replicate runs per cohort show mean and standard deviation with <20% relative variability
- mzML files retain full MS1 scan sequence; spot-check a file with pymzml or asari analyze to confirm scan count, m/z range, and retention time span match instrument specifications

## Limitations

- Public datasets (MetaboLights, MassIVE) may have variable metadata quality, missing acquisition parameters, or different instrument configurations — manual curation and documentation are required
- Format conversion (e.g. .RAW to mzML) can introduce subtle artifacts or loss of vendor-specific metadata; always validate the converted mzML files against original vendor software if critical quality metrics are needed
- Large cohorts (100+ samples) require substantial disk space (~1–10 GB per sample depending on instrument and run time); plan storage accordingly
- Scalability benchmarking assumes consistent hardware and system load; timing/memory measurements are sensitive to concurrent processes and disk I/O contention

## Evidence

- [other] Retrieve public mzML datasets from MetaboLights or MassIVE repositories; select or subsample test data to create cohorts of 10, 50, and 100+ samples.: "Retrieve public mzML datasets from MetaboLights or MassIVE repositories; select or subsample test data to create cohorts of 10, 50, and 100+ samples."
- [readme] Input data are centroid mzML files from LC, GC or DI-MS metabolomics.: "Input data are centroid mzML files from LC, GC or DI-MS metabolomics."
- [readme] We use ThermoRawFileParser to convert Thermo .RAW files to .mzML. Msconvert in ProteoWizard can handle the conversion of most vendor data formats and .mzXML files.: "We use ThermoRawFileParser to convert Thermo .RAW files to .mzML. Msconvert in ProteoWizard can handle the conversion of most vendor data formats and .mzXML files."
- [readme] MS/MS spectra are ignored in default LC-MS workflow but handled by alternative workflows.: "MS/MS spectra are ignored in default LC-MS workflow but handled by alternative workflows."
- [methods] Build sample registry; see workflow.process_project, workflow.register_samples.: "Build sample registry; see workflow.process_project, workflow.register_samples."
- [methods] The default method uses `pymzml` to parse mzML files.: "The default method uses `pymzml` to parse mzML files."

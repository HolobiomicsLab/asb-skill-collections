---
name: isotopic-signature-clustering-and-grouping
description: Use when you have a feature table (m/z, drift_time, retention_time, intensity) from LC-IMS-MS or similar multi-dimensional MS acquisition and need to (1) link isotopic variants to their monoisotopic parent features, (2) disambiguate true chemical features from noise or instrumental artifacts, or.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3801
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - DEIMoS
  - Python
  - numpy
  - ProteoWizard msconvert
  techniques:
  - LC-MS
  - ion-mobility-MS
  - tandem-MS
derived_from:
- doi: 10.1021/acs.analchem.1c05017
  title: deimos
evidence_spans:
- Functionality includes feature detection, feature alignment, collision cross section (CCS) calibration, isotope detection, and MS/MS spectral deconvolution
- import deimos
- DEIMoS is a Python application programming interface
- DEIMoS is a Python application programming interface and command-line tool
- import numpy as np
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_deimos_cq
    doi: 10.1021/acs.analchem.1c05017
    title: deimos
  dedup_kept_from: coll_deimos_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.1c05017
  all_source_dois:
  - 10.1021/acs.analchem.1c05017
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# isotopic-signature-clustering-and-grouping

## Summary

Groups detected mass spectrometry features into isotopic clusters by enumerating m/z offsets corresponding to stable isotope substitutions (e.g., C13) and filtering by mass, drift time, and retention time tolerances. This skill enables annotation of monoisotopic and isotopologue features, improving feature characterization and reducing false positive identifications in high-dimensional MS workflows.

## When to use

Apply this skill when you have a feature table (m/z, drift_time, retention_time, intensity) from LC-IMS-MS or similar multi-dimensional MS acquisition and need to (1) link isotopic variants to their monoisotopic parent features, (2) disambiguate true chemical features from noise or instrumental artifacts, or (3) prepare feature annotations that distinguish natural isotope patterns from chemical adducts or charge states. The skill is most valuable when features are already detected but lack isotopic grouping annotations.

## When NOT to use

- Input is already a fully annotated feature table with isotope group membership assigned — re-clustering will produce redundant annotations.
- Charge state is unknown or heterogeneous across features — the skill requires a fixed z specification; use feature deconvolution or charge inference first.
- Features lack drift_time dimension — drift_time tolerance is a key discriminator; absence may cause over-clustering of unrelated features.
- Isotope pattern is not from stable isotope substitution (e.g., adducts, multiply charged species) — the m/z offset model is isotope-specific and will fail to group chemically distinct features.

## Inputs

- Feature table (HDF5 or mzML format) with columns: m/z, drift_time, retention_time, intensity
- Charge state specification (z)
- Maximum number of isotopic substitutions (typically 5)
- Mass tolerance (m/z delta) for isotope enumeration
- Drift time tolerance window
- Retention time tolerance window

## Outputs

- Annotated feature table with isotope group identifiers
- Isotopic clusters mapping each monoisotope to its isotopologues
- Filtered feature list containing only grouped features (≥3 members per group)

## How to apply

Load the detected feature table using deimos.load() specifying m/z, drift_time, retention_time, and intensity columns. For each feature, enumerate expected m/z values for C13 isotopologues by adding 1.003355 Da per substitution (up to 5 maximum), assuming singly charged z=+1 ions. Search for matching peaks in the feature list within a specified m/z tolerance window (e.g., 50 ppm maximum error), then apply cascade filtering: first by m/z tolerance from expected delta, then by drift_time tolerance (exploiting the fact that isotopologues have identical collision cross sections), and finally by retention_time tolerance. Retain only isotopic signatures with at least 3 members (monoisotope plus ≥2 isotopologues) to minimize false clustering. Assign isotope group identifiers to all members and export the annotated table using deimos.save().

## Related tools

- **DEIMoS** (Core API for loading feature tables, enumerating m/z offsets, applying tolerance filters, and exporting annotated clusters) — https://github.com/pnnl/deimos
- **Python** (Programming environment for implementing isotope enumeration loops, tolerance filtering logic, and cluster assignment)
- **numpy** (Vectorized computation of m/z offsets, tolerance comparisons, and cluster membership indexing)
- **ProteoWizard msconvert** (Conversion of proprietary MS formats to mzML for standardized input to DEIMoS)

## Examples

```
import deimos; ms1 = deimos.load('example_data_peaks.h5', key='ms1', columns=['mz', 'drift_time', 'retention_time', 'intensity']); isotopes = deimos.isotope_detection(ms1, mz_delta=1.003355, max_substitutions=5, charge=1, mz_tol=50, dt_tol=1.0, rt_tol=10.0, min_cluster_size=3); deimos.save(isotopes, 'isotope_annotated.h5', key='isotopes')
```

## Evaluation signals

- All isotopic clusters contain exactly 1 monoisotope feature and 1–5 isotopologue features; no cluster has <3 members (verification of minimum cluster size filter).
- m/z differences between successive isotopologues in each cluster equal 1.003355 Da ± specified tolerance; no gaps or deviations exceed the stated m/z error threshold (50 ppm).
- All features within a cluster share identical drift_time values within the specified drift_time tolerance (validates isotope assumption that CCS is unchanged by stable isotope substitution).
- Retention_time spread within each cluster does not exceed the specified retention_time tolerance (validates co-elution assumption).
- No feature appears in more than one isotopic group (validates mutually exclusive cluster membership).
- r² of linear regression between expected and observed m/z values for all clustered features is ≥0.999 (validates mass calibration and clustering accuracy across all groups).

## Limitations

- Isotope detection is limited to singly charged ions (z=+1); multiply charged species require separate analysis or pre-deconvolution.
- Assumes all isotopic variants are C13 substitutions with fixed m/z delta of 1.003355 Da; other isotopes (N15, S34, etc.) or mixed substitutions are not modeled.
- Drift time tolerance filtering assumes that isotopologues have negligible differences in collision cross section, which may fail for very large molecules or unusual structures.
- Retention time tolerance filtering assumes co-elution of isotopologues; reversed-phase or ion-exchange chromatography may cause isotope separation, leading to false negatives.
- Minimum cluster size threshold of 3 members may discard low-abundance isotopologues or features with poor intensity ratios; no weighting by expected natural isotope abundance is applied.
- No changelog available for version tracking or updates to isotope mass constants.
- Performance scales with feature table size; large datasets (>1M features) may require memory optimization or batch processing.

## Evidence

- [other] DEIMoS detects C13 isotopologues by specifying an m/z delta of 1.003355 Da, a maximum of 5 isotopic substitutions, and maximum charge of 1, with initial constraint by m/z tolerance from expected delta, followed by drift time and retention time tolerances, and final downselection by maximum m/z error of 50 ppm.: "m/z delta of 1.003355 Da, a maximum of 5 isotopic substitutions, and maximum charge of 1, with initial constraint by m/z tolerance from expected delta, followed by drift time and retention time"
- [other] For each feature, calculate expected m/z values for C13 isotopologues (monoisotope + 1.003355 Da per carbon, assuming singly charged z=+1).: "calculate expected m/z values for C13 isotopologues (monoisotope + 1.003355 Da per carbon, assuming singly charged z=+1)"
- [other] Filter isotopic signatures to retain only those with at least 3 members (monoisotope plus ≥2 isotopologues).: "retain only those with at least 3 members (monoisotope plus ≥2 isotopologues)"
- [results] A good first screening is to only consider those isotopic signatures with at least 3 members: "only consider those isotopic signatures with at least 3 members"
- [readme] Functionality includes feature detection, feature alignment, collision cross section (CCS) calibration, isotope detection, and MS/MS spectral deconvolution: "Functionality includes feature detection, feature alignment, collision cross section (CCS) calibration, isotope detection, and MS/MS spectral deconvolution"
- [readme] DEIMoS operates on N-dimensional data, largely agnostic to acquisition instrumentation; algorithm implementations simultaneously utilize all dimensions to (i) offer greater separation between features, thus improving detection sensitivity, (ii) increase alignment/feature matching confidence among datasets, and (iii) mitigate convolution artifacts in tandem mass spectra.: "N-dimensional data, largely agnostic to acquisition instrumentation; algorithm implementations simultaneously utilize all dimensions to (i) offer greater separation between features, thus improving"

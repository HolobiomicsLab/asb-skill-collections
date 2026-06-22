---
name: isotopic-signature-detection-and-filtering
description: Use when after DEIMoS isotope detection has assigned potential isotopic signatures to detected features in aligned MS1 data.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3375
  - http://edamontology.org/topic_0121
  tools:
  - DEIMoS
  - Python
  - conda
  - pip
  - HDF5 / h5py
  techniques:
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
- Use `conda <https://www.anaconda.com/download/>`_ to create a virtual environment with required dependencies.
- 'Install DEIMoS using `pip <https://pypi.org/project/pip/>`_: ``pip install -e .``'
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

# isotopic-signature-detection-and-filtering

## Summary

Detection and filtering of isotopic signatures in high-dimensional mass spectrometry data to retain only robust, multi-member isotope patterns. This skill refines feature characterization by eliminating spurious or under-represented isotopic assignments that lack sufficient member count to be considered reliable molecular identity evidence.

## When to use

After DEIMoS isotope detection has assigned potential isotopic signatures to detected features in aligned MS1 data. Use this skill when you need to reduce false-positive isotope calls and ensure that only chemically meaningful isotope clusters (those with sufficient members to represent natural abundance patterns) proceed to downstream analysis or publication.

## When NOT to use

- When isotope detection has not yet been run; apply isotope detection first.
- When input features lack isotopic-signature annotation or group membership information.
- When the analysis goal is exploratory and low-confidence isotope calls are acceptable for hypothesis generation; in that case, defer filtering or use a lower threshold.

## Inputs

- DEIMoS isotope detection output (HDF5 .h5 file with isotope group assignments)
- Feature table with isotopic-signature-ID columns
- Aligned feature matrix with isotope membership counts per signature

## Outputs

- Filtered feature table (isotopic signatures with ≥3 members retained)
- Removed isotope group records (audit trail)
- Updated aligned feature set with spurious isotope calls excised

## How to apply

Apply a membership threshold filter on isotopic signatures, retaining only those with at least 3 member ions. The rationale is grounded in natural isotope abundance: a single isotope peak is ambiguous (could be noise or an unrelated feature), and two peaks may coincide by chance; three or more members establish a statistically defensible isotope envelope. Implement this filter by iterating through the isotope detection output (typically an annotation table or structured array in DEIMoS output .h5 files), counting the number of peaks assigned to each isotopic signature group, and removing groups below the threshold. This filter is applied post-alignment and post-isotope-detection, before final feature export or MS/MS matching.

## Related tools

- **DEIMoS** (Performs isotope detection prior to filtering; isotope detection output is the input to this filtering skill) — http://github.com/pnnl/deimos
- **Python** (Language for implementing isotope membership count logic and threshold filtering)
- **HDF5 / h5py** (Reading and writing filtered isotope annotations from DEIMoS .h5 output files)

## Examples

```
import deimos; data = deimos.load('example_data_peaks.h5', key='isotopes'); filtered = data[data.groupby('isotope_id').size() >= 3]; deimos.save(filtered, 'example_data_peaks_filtered.h5', key='isotopes')
```

## Evaluation signals

- Verify that all retained isotopic signatures have member_count ≥ 3 (check signature table)
- Verify that removed signatures had member_count < 3 (audit trail)
- Inspect natural abundance ratios of retained isotope envelopes (e.g., 13C, 15N, 34S patterns match expected ratios within mass calibration tolerances)
- Compare feature count before and after filtering; expect 5–25% reduction in total features (depending on data quality and noise level)
- Confirm that high-confidence features (high SNR, high alignment score) are retained; low-confidence features are selectively removed

## Limitations

- Threshold of 3 members is a heuristic and may be too stringent for low-abundance compounds or too lenient for noisy data; some use cases may require 4+ members or dynamic thresholding.
- Isotope detection itself can misassign peaks to groups (e.g., due to m/z calibration error or peak overlap); filtering cannot correct upstream detection errors.
- Does not account for instrument-specific isotope resolution or dynamic range; very high-resolution data may resolve additional minor isotopes, requiring per-instrument thresholding.
- Filtering is deterministic and unidirectional; no automatic feedback loop to re-calibrate or re-detect isotopes if filtering removes too many features.

## Evidence

- [results] A good first screening is to only consider those isotopic signatures with at least 3 members: "A good first screening is to only consider those isotopic signatures with at least 3 members"
- [intro] Functionality includes feature detection, feature alignment, collision cross section (CCS) calibration, isotope detection, and MS/MS spectral deconvolution: "Functionality includes feature detection, feature alignment, collision cross section (CCS) calibration, isotope detection, and MS/MS spectral deconvolution"
- [readme] DEIMoS operates on N-dimensional data, largely agnostic to acquisition instrumentation; algorithm implementations simultaneously utilize all dimensions to (i) offer greater separation between features, thus improving detection sensitivity, (ii) increase alignment/feature matching confidence among datasets, and (iii) mitigate convolution artifacts in tandem mass spectra.: "algorithm implementations simultaneously utilize all dimensions to (i) offer greater separation between features, thus improving detection sensitivity"

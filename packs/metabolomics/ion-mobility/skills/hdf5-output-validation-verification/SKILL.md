---
name: hdf5-output-validation-verification
description: Use when after invoking the DEIMoS CLI with a configuration file and allowing the Snakemake workflow to execute, use this skill to confirm successful completion of all workflow rules.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - DEIMoS
  - conda
  - pip
  - Python
  - Snakemake
  techniques:
  - ion-mobility-MS
  - tandem-MS
derived_from:
- doi: 10.1021/acs.analchem.1c05017
  title: deimos
evidence_spans:
- DEIMoS, or Data Extraction for Integrated Multidimensional Spectrometry, is a Python application programming interface and command-line tool
- import deimos
- Use conda to create a virtual environment with required dependencies.
- 'Install DEIMoS using pip: pip install -e .'
- is a Python application programming interface and command-line tool
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_deimos
    doi: 10.1021/acs.analchem.1c05017
    title: deimos
  dedup_kept_from: coll_deimos
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

# HDF5 Output Validation and Verification

## Summary

Verify that a DEIMoS Snakemake workflow has completed successfully by confirming the presence and integrity of HDF5 output files and their internal datasets. This skill ensures that all expected workflow artifacts (ms1, ms2, features, isotopes) are present with non-zero row counts before proceeding to downstream analysis.

## When to use

After invoking the DEIMoS CLI with a configuration file and allowing the Snakemake workflow to execute, use this skill to confirm successful completion of all workflow rules. Apply it when you need assurance that feature detection, alignment, CCS calibration, isotope detection, and MS/MS deconvolution have all produced valid output artifacts before initiating exploratory analysis or interpretation.

## When NOT to use

- When the input HDF5 files have already been validated in a previous run; avoid re-checking identical artifacts unless workflow parameters have changed.
- When running DEIMoS in streaming or interactive mode (not via Snakemake); this skill is specific to Snakemake workflow verification.
- If your analysis goal is to filter or process isotopic signatures downstream; this skill validates presence, not quality or filtering criteria.

## Inputs

- HDF5 output files in output/ directory (ms1.h5, ms2.h5, features.h5, isotopes.h5)
- Workflow completion status (Snakemake exit code and final log messages)

## Outputs

- Validation report confirming presence and non-zero row counts for all expected datasets (ms1, ms2, features, isotopes)
- Boolean flag or exception indicating workflow success or failure

## How to apply

After the Snakemake workflow completes (typically indicated by the CLI returning without errors), inspect the output/ directory to confirm all expected HDF5 files are present. Open each HDF5 file using the deimos.load() function, specifying the key (e.g., 'ms1', 'ms2', 'features', 'isotopes') and any required columns. Validate that each loaded dataset has a non-zero row count, indicating that the corresponding workflow rule executed and populated data. Check that datasets contain the expected dimensional structure (mass, CCS, retention time, intensity for ms1; tandem mass spectra for ms2; isotopic signatures for isotopes). The presence of all four dataset keys and non-empty tables indicates successful end-to-end workflow execution across peak detection, feature alignment, CCS calibration, isotope detection, and MS/MS deconvolution.

## Related tools

- **DEIMoS** (CLI and Python API for executing the feature detection, alignment, CCS calibration, and isotope detection workflow; provides deimos.load() function for reading and validating HDF5 outputs) — http://github.com/pnnl/deimos
- **Snakemake** (Workflow execution engine that orchestrates the complete rule DAG (peak detection, feature alignment, CCS calibration, isotope detection, MS/MS deconvolution) and populates output/ with HDF5 artifacts)
- **conda** (Environment manager used to activate the DEIMoS virtual environment and manage dependencies before workflow execution)

## Examples

```
import deimos
ms1 = deimos.load('output/ms1.h5', key='ms1'); ms2 = deimos.load('output/ms2.h5', key='ms2'); features = deimos.load('output/features.h5', key='features'); isotopes = deimos.load('output/isotopes.h5', key='isotopes')
print('ms1 rows:', len(ms1), 'ms2 rows:', len(ms2), 'features rows:', len(features), 'isotopes rows:', len(isotopes))
assert len(ms1) > 0 and len(ms2) > 0 and len(features) > 0 and len(isotopes) > 0, 'Workflow validation failed: empty datasets'
```

## Evaluation signals

- All expected HDF5 files are present in output/ directory (ms1.h5, ms2.h5, features.h5, isotopes.h5)
- Each HDF5 file can be opened successfully with deimos.load() and returns a DataFrame with non-zero row count
- ms1 and ms2 datasets contain expected dimensional columns (mz, drift_time, retention_time, intensity for ms1; tandem mass spectra for ms2)
- features dataset contains aligned features characterized by mass, CCS, and retention time across all study samples
- isotopes dataset contains isotopic signature assignments with at least 3 members per signature (standard screening criterion mentioned in article)
- Snakemake workflow exit code is 0 with final log message indicating all rules completed successfully

## Limitations

- This skill validates presence and basic integrity of outputs but does not assess data quality, chemical validity, or biological relevance of detected features.
- Non-zero row counts indicate successful execution but do not guarantee that detected features are true positives or represent meaningful biological signals.
- The skill assumes HDF5 file format stability and compatibility with the version of DEIMoS used; changes in HDF5 schema across DEIMoS versions may require schema adaptation.
- Workflow completion as measured by file presence does not account for partial or incomplete feature detection due to parameter mismatch with instrument characteristics or sample composition.

## Evidence

- [other] Verify successful completion by confirming all output HDF5 files are present in output/ and contain expected datasets (ms1, ms2, features, isotopes) with non-zero row counts.: "Verify successful completion by confirming all output HDF5 files are present in output/ and contain expected datasets (ms1, ms2, features, isotopes) with non-zero row counts."
- [other] Snakemake automatically detects input files, executes the complete rule DAG including peak detection, feature alignment, CCS calibration, isotope detection, and MS/MS deconvolution, and populates output/ with HDF5-formatted results.: "Snakemake automatically detects input files, executes the complete rule DAG including peak detection, feature alignment, CCS calibration, isotope detection, and MS/MS deconvolution, and populates"
- [intro] DEIMoS functionality includes feature detection, feature alignment, collision cross section (CCS) calibration, isotope detection, and MS/MS spectral deconvolution, with output comprising detected features aligned across study samples and characterized by mass, CCS, tandem mass spectra, and isotopic signature.: "DEIMoS functionality includes feature detection, feature alignment, collision cross section (CCS) calibration, isotope detection, and MS/MS spectral deconvolution, with output comprising detected"
- [results] A good first screening is to only consider those isotopic signatures with at least 3 members.: "A good first screening is to only consider those isotopic signatures with at least 3 members."

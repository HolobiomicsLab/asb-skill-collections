---
name: mass-spectrometry-feature-deduplication
description: Use when immediately after MZmine feature detection when you have both MGF (MS/MS spectra) and CSV (metadata) output files for one or both ionization modes and wish to construct a deduplicated molecular network.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3370
  tools:
  - MolNotator
  - PyYAML
  - Python
  techniques:
  - LC-MS
derived_from:
- doi: 10.1101/2021.12.21.473622v1
  title: MolNotator
evidence_spans:
- from MolNotator.duplicate_filter import duplicate_filter
- from MolNotator.sample_slicer import sample_slicer
- import yaml
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_molnotator_cq
    doi: 10.1101/2021.12.21.473622v1
    title: MolNotator
  dedup_kept_from: coll_molnotator_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1101/2021.12.21.473622v1
  all_source_dois:
  - 10.1101/2021.12.21.473622v1
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-spectrometry-feature-deduplication

## Summary

Removes duplicate features from MZmine-exported MGF and CSV files for a single ionization mode (NEG or POS) prior to molecular network construction. This preprocessing step eliminates redundant mass spectral entries that would otherwise inflate network complexity and obscure true molecular relationships.

## When to use

Apply this skill immediately after MZmine feature detection when you have both MGF (MS/MS spectra) and CSV (metadata) output files for one or both ionization modes and wish to construct a deduplicated molecular network. Use it as the first step in the MolNotator workflow before sample slicing, fragment annotation, or adduct annotation.

## When NOT to use

- Input is already a deduplicated feature table or network (e.g., from prior deduplication run).
- Ion mode argument (NEG or POS) cannot be clearly determined from your experimental design or data provenance.
- You require preservation of ALL duplicate entries for quantitative ion accounting or charge-state analysis across ionization modes.

## Inputs

- MZmine MGF file (MS/MS spectra) for NEG or POS ionization mode
- MZmine CSV file (feature metadata) for NEG or POS ionization mode
- YAML parameter file (params.yaml) containing duplicate_filter configuration

## Outputs

- Deduplicated MGF file (NEG or POS mode)
- Deduplicated CSV file (NEG or POS mode)

## How to apply

Load the MZmine MGF and CSV files for your target ionization mode (NEG or POS) using Python file I/O. Parse the YAML parameter file containing duplicate-filter configuration using PyYAML to retrieve filter thresholds and output directory settings. Call the duplicate_filter() function from MolNotator.duplicate_filter, passing the loaded params dictionary and the ion_mode argument ('NEG' or 'POS'). The function applies filtering logic internally to identify and remove redundant feature entries while preserving the MGF spectral integrity and CSV metadata structure. Write the deduplicated MGF and CSV outputs to the designated output directory for downstream processing by sample_slicer.

## Related tools

- **MolNotator** (Provides the duplicate_filter() function and orchestrates the complete LC-MS/MS molecular network workflow; duplicate filtering is its first preprocessing step.) — https://github.com/ZzakB/MolNotator
- **PyYAML** (Parses the params.yaml configuration file to retrieve duplicate-filter settings, output directories, and database references.)
- **Python** (Runtime environment for loading MGF/CSV files, calling MolNotator functions, and managing file I/O.)

## Examples

```
from MolNotator.duplicate_filter import duplicate_filter; import yaml; params = yaml.load(open('./params/params.yaml'), Loader=yaml.FullLoader); duplicate_filter(params=params, ion_mode='NEG')
```

## Evaluation signals

- Output MGF file parses without syntax errors and retains valid MS/MS spectrum records.
- Output CSV file contains fewer or equal rows compared to input CSV, with no orphaned feature IDs.
- Ion mode parameter correctly matches the input file source (e.g., NEG for _NEG.mgf / _NEG.csv files).
- Deduplicated outputs can be successfully ingested by downstream MolNotator functions (sample_slicer, fragnotator, adnotator) without runtime errors.
- Feature count reduction is consistent with expected duplicate prevalence in MZmine output (typically 5–20% redundancy).

## Limitations

- Deduplication logic is specific to MZmine MGF and CSV schemas; outputs from other feature detection tools (e.g., XCMS, MS-DIAL) may not be compatible.
- Function operates on a single ionization mode per invocation; NEG and POS modes must be processed separately and merged later via mode_merger().
- No built-in mechanism to customize or inspect the duplicate-filter criteria; all thresholds and heuristics are controlled via the params.yaml file.
- The duplicate_filter function does not generate intermediate reports documenting which features were identified or removed as duplicates.

## Evidence

- [other] duplicate_filter function accepts parameters and an ion_mode argument to filter duplicate features from MZmine's MGF and CSV files for either negative (NEG) or positive (POS) ionization modes.: "The duplicate_filter function accepts parameters and an ion_mode argument to filter duplicate features from MZmine's MGF and CSV files for either negative (NEG) or positive (POS) ionization modes."
- [other] Load the MZmine MGF and CSV files for the specified ionization mode (NEG or POS) using Python file I/O. Parse the YAML parameter file to retrieve duplicate-filter configuration using PyYAML. Apply the duplicate_filter function from MolNotator.duplicate_filter, passing the params dictionary and ion_mode argument.: "Load the MZmine MGF and CSV files for the specified ionization mode (NEG or POS) using Python file I/O. Parse the YAML parameter file to retrieve duplicate-filter configuration using PyYAML. Apply"
- [readme] from MolNotator.duplicate_filter import duplicate_filter: "from MolNotator.duplicate_filter import duplicate_filter"
- [readme] Duplicate filtering on MZmine's MGF and CSV files (NEG): duplicate_filter(params = params, ion_mode = "NEG"): "Duplicate filtering on MZmine's MGF and CSV files (NEG): duplicate_filter(params = params, ion_mode = "NEG")"
- [readme] MolNotator works within a user-defined project folder with a specific file structure including input_files containing MZmine-generated MGF and CSV files for positive, negative or ideally both ionization modes.: "MolNotator works within a user-defined project folder with a specific file structure including input_files containing MZmine-generated MGF and CSV files for positive, negative or ideally both"

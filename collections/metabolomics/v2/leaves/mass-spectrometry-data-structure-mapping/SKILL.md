---
name: mass-spectrometry-data-structure-mapping
description: Use when after feature extraction and peak recognition have produced
  detected MS/MS spectra (precursor m/z, charge, retention time, and fragment ion
  peaks), and you need to export these spectra for external spectral database searching,
  cross-platform comparison, or archival in a format compatible.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Python
  - BreathXplorer
  techniques:
  - LC-MS
  license_tier: open
derived_from:
- doi: 10.1021/jasms.4c00152
  title: BreathXplorer
evidence_spans:
- '[![PyPI](https://img.shields.io/pypi/pyversions/breathXplorer)]'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_breathxplorer_cq
    doi: 10.1021/jasms.4c00152
    title: BreathXplorer
  dedup_kept_from: coll_breathxplorer_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/jasms.4c00152
  all_source_dois:
  - 10.1021/jasms.4c00152
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-spectrometry-data-structure-mapping

## Summary

Convert MS/MS spectra data from internal feature extraction pipelines into standardized MGF (Mascot Generic Format) files for compatibility with spectral library search and tandem MS analysis workflows. This skill bridges BreathXplorer's feature detection output to community-standard MS/MS exchange formats.

## When to use

After feature extraction and peak recognition have produced detected MS/MS spectra (precursor m/z, charge, retention time, and fragment ion peaks), and you need to export these spectra for external spectral database searching, cross-platform comparison, or archival in a format compatible with standard proteomics/metabolomics software.

## When NOT to use

- Input is already in standard MGF or mzML format — use direct format conversion instead
- Only MS1 (precursor mass spectrometry) data available with no tandem spectra — MGF is designed for MS/MS data
- Spectra lack precursor m/z information — PEPMASS field is mandatory in MGF

## Inputs

- Detected MS/MS spectra with precursor m/z values
- Fragment ion peak lists (m/z and intensity pairs)
- Precursor charge states (optional but recommended)
- Retention time metadata (optional)

## Outputs

- MGF (Mascot Generic Format) file containing all MS/MS spectra
- Validated MGF output with correct syntax and required fields

## How to apply

Load the detected MS/MS spectra data from the feature extraction and peak recognition pipeline outputs. For each spectrum, construct an MGF entry by formatting required fields: precursor m/z (PEPMASS), MS level (MSLEVEL=2 for tandem spectra), and all fragment ion m/z and intensity pairs. Write formatted spectra to a single MGF file with proper BEGIN IONS / END IONS delimiters around each spectrum entry. Validate MGF syntax by confirming all spectra contain the required PEPMASS field, correct delimiter placement, and properly formatted m/z–intensity pairs (space-separated, one pair per line).

## Related tools

- **BreathXplorer** (Provides MS/MS spectra export utility (to_mgf function) and feature extraction pipeline that generates spectra data) — https://github.com/wykswr/breathXplorer
- **Python** (Implementation language for the MS/MS spectra export and MGF file writing)

## Examples

```
from breathXplorer import retrieve_tandem; tandem_data = retrieve_tandem('sample.mzML'); tandem_data.to_mgf('output_spectra.mgf')
```

## Evaluation signals

- MGF file opens without parse errors in standard spectral analysis software (e.g., Mascot, MaxQuant, or online MGF validators)
- Every spectrum entry contains BEGIN IONS and END IONS delimiters with exactly one PEPMASS line and one MSLEVEL=2 declaration per entry
- All fragment ion lines follow the format 'm/z intensity' with space separator; no missing or malformed pairs
- Precursor m/z values are numeric and non-zero; retention time (if present) is within expected experimental range
- File structure matches the documented MGF example: multi-spectrum file with consistent field ordering and no orphaned lines outside delimiters

## Limitations

- MGF format does not natively support all BreathXplorer metadata (e.g., RSD values, isotope/adduct annotations); additional metadata must be stored separately or in custom MGF comments
- Charge state inference or manual assignment may be required if not available from the feature extraction pipeline; absent charge information limits some downstream spectral matching algorithms
- MGF files do not preserve scan/spectrum IDs; re-linking exported spectra to source features requires external mapping
- No built-in validation for chemical plausibility (e.g., fragment masses > precursor mass) — syntax validation alone is insufficient for quality control

## Evidence

- [other] Load detected MS/MS spectra data from the feature extraction and peak recognition pipeline outputs. 2. Format each spectrum entry with required MGF fields: precursor m/z, precursor charge, retention time, and fragment ion peaks (m/z and intensity pairs). 3. Write all formatted spectra to a single MGF file with proper header and section delimiters.: "Load detected MS/MS spectra data from the feature extraction and peak recognition pipeline outputs. 2. Format each spectrum entry with required MGF fields: precursor m/z, precursor charge, retention"
- [readme] The file contains the MS/MS spectra of the features, each feature has a PEPMASS (precursor mass) and MSLEVEL field, and the following pairs are the m/z and intensity of the MS/MS spectra.: "The file contains the MS/MS spectra of the features, each feature has a PEPMASS (precursor mass) and MSLEVEL field, and the following pairs are the m/z and intensity of the MS/MS spectra."
- [readme] If you're using tandem MS, you can also export the MS/MS spectra as mgf file using the `to_mgf` function: "If you're using tandem MS, you can also export the MS/MS spectra as mgf file using the `to_mgf` function"
- [other] Validate MGF syntax and verify all spectra contain required fields.: "Validate MGF syntax and verify all spectra contain required fields."

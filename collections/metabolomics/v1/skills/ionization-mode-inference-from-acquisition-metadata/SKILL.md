---
name: ionization-mode-inference-from-acquisition-metadata
description: Use when when beginning preprocessing of a new LC-MS dataset with mzML files or raw acquisitions and you need to determine which ionization mode was used before running feature detection (Asari) or empirical compound grouping (khipu).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3803
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - ThermoRawFileParser
  - khipu
  - Python
  - Asari
derived_from:
- doi: 10.1371/journal.pcbi.1011912
  title: pcpfm
evidence_spans:
- convert Thermo .raw to mzML (ThermoRawFileParser)
- pre-annotation to group featues to empirical compounds (khipu)
- Python-Centric Pipeline for Metabolomics
- The Python-Centric Pipeline for Metabolomics
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_pcpfm
    doi: 10.1371/journal.pcbi.1011912
    title: pcpfm
  dedup_kept_from: coll_pcpfm
schema_version: 0.2.0
---

# ionization-mode-inference-from-acquisition-metadata

## Summary

Infer the ionization polarity (positive or negative) of LC-MS acquisitions from instrument metadata embedded in mzML files or raw acquisition headers, enabling downstream selection of appropriate adduct definitions and annotation rules. This inference is necessary because empirical compound grouping and MS annotation both require knowledge of which ions were actually formed.

## When to use

When beginning preprocessing of a new LC-MS dataset with mzML files or raw acquisitions and you need to determine which ionization mode was used before running feature detection (Asari) or empirical compound grouping (khipu). The ionization mode must be known to select the correct set of adduct definitions (e.g., [M+H]+ vs [M−H]−) and charge state expectations for subsequent steps.

## When NOT to use

- The mzML file or raw header lacks ionization metadata and no experiment metadata file specifies polarity — in this case, manual review of representative spectra or instrument logs is required.
- Mixed-polarity acquisitions (simultaneous positive and negative switching within a single run) — the current workflow assumes single polarity per sample and would require file splitting before inference.
- Data that has already been processed and polarity-specific feature annotation (e.g., adduct assignments) is already locked in — re-inference at that stage risks inconsistency.

## Inputs

- mzML file with ionization mode metadata in header
- Thermo .raw file with instrument metadata
- experiment metadata CSV with polarity column (optional alternative)

## Outputs

- ionization polarity designation (positive or negative mode)
- selected adduct definition list for downstream khipu runs
- experiment.json metadata field documenting inferred polarity

## How to apply

Extract the ionization polarity attribute from the mzML header or raw file metadata during the initial data ingestion phase. Modern mass spectrometry data formats (mzML compliant) encode the ionization mode in structured metadata fields. Once extracted, use this value to select the appropriate adduct list and charge state configuration for khipu's build_empCpds command. The article describes using 'ionization mode' and 'adduct definitions for the detected polarity' as configurable inputs; failure to infer polarity correctly will result in incorrect adduct annotation and grouping of features into empirical compounds. Record the inferred mode as part of the experiment.json metadata for downstream reproducibility.

## Related tools

- **ThermoRawFileParser** (Extract ionization mode metadata from Thermo .raw files prior to mzML conversion)
- **Asari** (Uses inferred ionization mode during feature detection and quality control to set appropriate mass calibration and ion handling rules) — https://github.com/shuzhao-li-lab/asari_pcpfm_tutorials
- **khipu** (Receives ionization mode to select adduct definition list for empirical compound grouping with configurable m/z and retention time tolerances) — https://github.com/shuzhao-li-lab/khipu
- **Python** (Parse mzML headers or raw metadata programmatically and assign polarity values) — https://github.com/shuzhao-li-lab/PythonCentricPipelineForMetabolomics

## Evaluation signals

- Inferred ionization mode matches instrument logbook or operator notes for the run.
- Adduct list selected by downstream khipu step matches the inferred polarity (e.g., [M+H]+, [M+Na]+ for positive; [M−H]−, [M+Cl]− for negative).
- Feature m/z distributions in resulting empirical compounds show expected mass shifts consistent with the inferred adduct patterns (e.g., 1.008 Da differences for proton adducts).
- experiment.json metadata field polarity_mode contains a valid value ('positive' or 'negative') derived from source data.
- No mixed-polarity features appear in the same empirical compound group (would indicate polarity inference failure).

## Limitations

- mzML files created from older raw formats may have incomplete or missing ionization metadata; ThermoRawFileParser conversion quality depends on source instrument compatibility.
- Some custom or legacy instrument configurations may not encode polarity in standard mzML fields, requiring manual metadata curation.
- The workflow currently assumes single polarity per sample; mixed-mode acquisitions (pos/neg switching within one run) are not explicitly handled and would require file-level splitting before inference.
- Inference is deterministic from metadata; if metadata is corrupted or absent, the step will fail silently or require fallback to manual inspection of representative spectra.

## Evidence

- [other] specifying ionization mode and adduct definitions for the detected polarity: "specifying ionization mode and adduct definitions for the detected polarity"
- [other] build_empCpds command groups features into empirical compounds by matching isotopes and adducts with configurable mz tolerance and rt tolerance, producing a JSON file containing grouped features: "The build_empCpds command groups features into empirical compounds by matching isotopes and adducts with configurable mz tolerance (default 5 ppm) and rt tolerance (default 2 seconds), producing a"
- [readme] pre-annotation to group featues to empirical compounds (khipu): "pre-annotation to group featues to empirical compounds (khipu)"
- [readme] Inputs should include a set of raw files (.raw or .mzML) and a csv file for metadata (minimal sample names and file path).: "Inputs should include a set of raw files (.raw or .mzML) and a csv file for metadata (minimal sample names and file path)."
- [readme] designed to take raw LC-MS metabolomics data and ready them for downstream statistical analysis: "designed to take raw LC-MS metabolomics data and ready them for downstream statistical analysis"

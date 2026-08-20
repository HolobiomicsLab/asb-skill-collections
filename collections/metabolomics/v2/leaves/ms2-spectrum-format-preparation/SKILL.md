---
name: ms2-spectrum-format-preparation
description: Use when you have raw or unstructured MS2 spectral data (from untargeted
  tandem mass spectrometry experiments) and plan to run MS2MP inference for KEGG pathway
  prediction.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - MS2MP
  techniques:
  - LC-MS
  license_tier: restricted
derived_from:
- doi: 10.1021/acs.analchem.4c06875
  title: MS2MP
evidence_spans:
- MS2MP is a novel deep learning-based framework for KEGG pathway prediction directly
  from untargeted tandem mass spectrometry(MS2)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ms2mp_cq
    doi: 10.1021/acs.analchem.4c06875
    title: MS2MP
  dedup_kept_from: coll_ms2mp_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.4c06875
  all_source_dois:
  - 10.1021/acs.analchem.4c06875
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# ms2-spectrum-format-preparation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Prepare untargeted tandem mass spectrometry (MS2) spectral data into the file structure and format required by the MS2MP deep learning framework for downstream KEGG pathway prediction. This skill ensures data integrity and compatibility before inference.

## When to use

You have raw or unstructured MS2 spectral data (from untargeted tandem mass spectrometry experiments) and plan to run MS2MP inference for KEGG pathway prediction. Apply this skill when you need to validate and reformat spectra into MS2MP's expected input schema before loading the pre-trained model.

## When NOT to use

- Your data is already in MS2MP's native input format and has been validated.
- You do not plan to use MS2MP for inference; other pathway prediction tools may have different format requirements.
- Input is single MS1 (precursor-only) data without fragment spectra; MS2MP requires tandem mass spectrometry data.

## Inputs

- Raw or partially processed MS2 spectral data (e.g., mzML, mzXML, or vendor-specific MS/MS export)
- MS2 spectrum collection with m/z values, intensity values, and spectrum identifiers
- Metadata or annotation accompanying MS2 spectra

## Outputs

- MS2MP-compatible spectral data file (verified and reformatted)
- Validation report confirming file structure and spectral data integrity
- Spectrum identifier mapping (if renaming or consolidating occurred)

## How to apply

Examine your raw MS2 spectral data and verify that it conforms to MS2MP's required file structure and spectral data format. Check that spectrum identifiers are present and parseable, that m/z and intensity values are correctly formatted, and that metadata fields align with MS2MP expectations. Perform structural validation to catch malformed records, missing fields, or inconsistent data types before submission to the model. Reformat or restructure data as needed to match MS2MP's input specification. Once validation passes, the prepared data can be loaded into MS2MP for inference.

## Related tools

- **MS2MP** (Deep learning framework that consumes the prepared MS2 spectral data for KEGG pathway prediction inference) — https://github.com/ucasaccn/MS2MP

## Evaluation signals

- All spectra have valid, parseable identifiers with no duplicates or null values.
- m/z and intensity values are numeric, non-negative, and within expected mass and abundance ranges.
- File structure matches MS2MP's documented schema (e.g., correct column names, delimiters, or nested object keys).
- Validation script or log reports zero format errors and 100% record completion.
- Prepared data can be successfully loaded by MS2MP without import or parsing errors.

## Limitations

- Preparation workflow assumes availability of complete spectral metadata; sparse or missing annotations may require imputation or record exclusion.
- Format compatibility is specific to MS2MP; data prepared for MS2MP may not be directly compatible with other KEGG or pathway prediction tools.
- Validation does not assess spectral quality (e.g., signal-to-noise ratio or peak count); high-quality spectra still require domain expertise to interpret downstream predictions.

## Evidence

- [other] Prepare MS2 input data in the format required by MS2MP (verify file structure and spectral data integrity).: "Prepare MS2 input data in the format required by MS2MP (verify file structure and spectral data integrity)"
- [readme] MS2MP is a novel deep learning-based framework for KEGG pathway prediction directly from untargeted tandem mass spectrometry(MS2).: "MS2MP is a novel deep learning-based framework for KEGG pathway prediction directly from untargeted tandem mass spectrometry(MS2)"

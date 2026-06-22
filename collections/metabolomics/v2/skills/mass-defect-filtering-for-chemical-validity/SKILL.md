---
name: mass-defect-filtering-for-chemical-validity
description: Use when after loading an MS-DIAL peak list (feature table with m/z, retention time, intensity, and sample assignments) when you need to remove non-organic or chemically implausible features.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0769
  tools:
  - MS-CleanR
  - MS-DIAL
  techniques:
  - LC-MS
  - tandem-MS
derived_from:
- doi: 10.1021/acs.analchem.0c01594
  title: MS-CleanR
evidence_spans:
- MS-CleanR use as input MS-DIAL peak list processed in data dependent analysis
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ms_cleanr_cq
    doi: 10.1021/acs.analchem.0c01594
    title: MS-CleanR
  dedup_kept_from: coll_ms_cleanr_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.0c01594
  all_source_dois:
  - 10.1021/acs.analchem.0c01594
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-defect-filtering-for-chemical-validity

## Summary

Filter out features with mass defect values that fall outside the expected chemical range for organic compounds, removing artefacts and non-metabolite signals from LC-MS peak lists. This step improves feature quality by eliminating signals chemically inconsistent with typical metabolites before downstream annotation.

## When to use

Apply this skill after loading an MS-DIAL peak list (feature table with m/z, retention time, intensity, and sample assignments) when you need to remove non-organic or chemically implausible features. Mass defect filtering is particularly useful when your LC-MS data contains instrumental artefacts, contamination, or noise that exhibits unusual mass defect signatures inconsistent with known metabolite chemistry.

## When NOT to use

- Input data contains MS1-only features without MS/MS spectra; MS-CleanR's generic filtering will crash on MS1-only data.
- You are working with non-organic molecules (e.g., inorganic salts, metal complexes, or synthetic polymers) where standard organic mass defect rules do not apply.
- Mass defect has already been used as a primary feature identifier in your experimental design (e.g., targeted mass defect-based proteomics); applying a second filter may remove true signal.

## Inputs

- MS-DIAL peak list / feature table (m/z, retention time, intensity values, sample class assignments)
- User-defined mass defect window boundaries (lower and upper thresholds in ppm or Da)

## Outputs

- Filtered MS-DIAL peak list with chemically implausible features removed
- Metadata report of removed features and their mass defect values (optional)

## How to apply

Calculate the mass defect for each feature (the difference between the observed m/z and its nominal mass, typically expressed as ppm or as an absolute difference). Define the expected mass defect window for organic compounds in your analytical context (the article does not specify absolute bounds, but these are typically ±50–100 ppm for small molecules). Remove all features whose mass defect values fall outside this user-defined window. The rationale is that true organic metabolites exhibit mass defects within a predictable range determined by the elemental composition rules (primarily C, H, N, O, P, S); signals outside this range are likely instrument noise, multiply-charged species, or in silico artefacts. After filtering, export the resulting feature table for subsequent steps (clustering, annotation).

## Related tools

- **MS-DIAL** (Source peak detection and feature table generation; provides m/z, retention time, and intensity data that serve as input for mass defect filtering) — http://prime.psc.riken.jp/compms/index.html
- **MS-CleanR** (Parent workflow tool that implements mass defect filtering as one of five generic filter steps; provides tunable parameters and GUI for defining mass defect window bounds) — https://github.com/eMetaboHUB/MS-CleanR

## Evaluation signals

- The number of features removed is plausible (typically 5–20% of the input feature table, depending on data quality and window stringency) and does not approach 0% or >50% unexpectedly.
- Removed features cluster visually outside the expected mass defect range when plotted as a histogram or density distribution; retained features cluster tightly within the defined window.
- Downstream annotation results (via MS-FINDER) show improved match quality and reduced number of low-confidence or spurious hits, indicating that artefacts have been successfully filtered.
- The mass defect distribution of retained features aligns with known elemental composition rules for C, H, N, O, P, S metabolites (e.g., mass defect for C6H12O6 ≈ 0.0211 Da or ≈ +3.6 ppm at m/z 180).
- Comparison of filtered vs. unfiltered feature lists shows that known metabolite standards or positive controls remain in the retained set.

## Limitations

- MS-CleanR requires at least 3 blanks and 3 QC samples identified in the MS-DIAL sample list; mass defect filtering alone does not enforce this but context-dependent filtering steps will fail without it.
- The article does not specify absolute mass defect window bounds; practitioners must define these based on their own chemical knowledge or literature; overly narrow windows may remove true signal; overly wide windows may retain artefacts.
- Mass defect filtering is less effective on singly-charged small molecules where mass defect variation is small; multiply-charged or fragment species may exhibit anomalous defects that coincidentally fall within the allowed window.
- The skill assumes that all features have been assigned accurate m/z values by MS-DIAL; calibration errors (>5 ppm) will misalign mass defect distributions and reduce filter efficacy.
- No explicit decision logic is provided for handling edge cases near window boundaries; users must choose between hard cutoffs and soft/probabilistic filtering.

## Evidence

- [other] Filter out features with unusual mass defect values that fall outside the expected chemical range for organic compounds.: "Filter out features with unusual mass defect values that fall outside the expected chemical range for organic compounds."
- [intro] MS-CleanR applies generic filters including blank injection signal subtraction, background ions drift removal, unusual mass defect filtering, and RSD/RMD-based filtering.: "MS-CleanR apply generic filters encompassing blank injection signal subtraction, background ions drift removal, unusual mass defect filtering, relative standard deviation threshold (RSD) based on"
- [other] All these filter options are tunable by the user.: "All these options are tunable by the user."
- [intro] MS-CleanR requires MS-DIAL v4.00 or higher as input for peak detection.: "Needs MS-DIAL (v4.00 or higher) and MS-FINDER (3.30 or higher)"
- [readme] All features without MS/MS will be discarded during the first step. If data contain MS1 only, the first MS-CleanR step will crash.: "All features without MS/MS will be discarded during the first step. If data contain MS1 only, the first MS-CleanR step will crash."

---
name: precursor-mass-tolerance-filtering
description: Use when after cosine similarity or dot-product scoring of experimental MS/MS spectra against a reference library, when you need to eliminate matches whose precursor m/z values deviate too far from the experimental precursor m/z, thereby improving specificity of library matching before final.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3644
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - TandemMatch
  techniques:
  - LC-MS
derived_from:
- doi: 10.1021/jasms.4c00146
  title: PeakQC
evidence_spans:
- 'TandemMatch: MS/MS spectral library matching with support for MSP and CSV library formats.'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_peakqc_cq
    doi: 10.1021/jasms.4c00146
    title: PeakQC
  dedup_kept_from: coll_peakqc_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/jasms.4c00146
  all_source_dois:
  - 10.1021/jasms.4c00146
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# precursor-mass-tolerance-filtering

## Summary

Filter MS/MS spectral library matches by applying a mass tolerance window on precursor m/z to retain only candidate matches within a specified Da or ppm range of the experimental precursor mass. This step reduces false positives and focuses downstream scoring on chemically plausible candidates.

## When to use

After cosine similarity or dot-product scoring of experimental MS/MS spectra against a reference library, when you need to eliminate matches whose precursor m/z values deviate too far from the experimental precursor m/z, thereby improving specificity of library matching before final ranking.

## When NOT to use

- Input spectra lack precursor m/z information (e.g., intact mass is unknown or unavailable).
- Library reference spectra do not include precursor m/z annotations.
- Tolerance window is set too narrowly for the instrument's mass accuracy, causing loss of true positives.

## Inputs

- Experimental MS/MS spectra with precursor m/z and retention time
- Spectral library entries (MSP or CSV format) with reference spectrum identities and fragment m/z values
- Cosine similarity or dot-product match scores between experimental and library spectra
- Mass tolerance threshold (Da or ppm)

## Outputs

- Filtered set of candidate library matches passing the precursor m/z tolerance criterion
- Structured results file (CSV or JSON) containing matched records with spectrum metadata, library accession, match score, and fragment ion assignments

## How to apply

Extract the precursor m/z from each experimental MS/MS spectrum. For each candidate library entry, calculate the absolute mass difference or ppm deviation between the experimental and library precursor m/z values. Retain only matches where this deviation falls within a predefined tolerance window (e.g., ±5 ppm or ±10 Da, depending on instrument resolution). Apply this filter after similarity scoring but before ranking and output to ensure only mass-plausible identifications are reported. The rationale is that precursor mass is a strong physicochemical constraint: compounds with different exact masses are distinct, and deviations beyond instrument accuracy indicate a false match regardless of spectral similarity.

## Related tools

- **TandemMatch** (Applies MS/MS spectral library matching with precursor m/z and mass tolerance filtering to rank matched library spectra) — https://github.com/pnnl/IonToolPack

## Evaluation signals

- Verify that no output matches exceed the specified precursor m/z tolerance window (e.g., all matches ≤ ±5 ppm deviation).
- Check that the proportion of retained candidates is reasonable relative to library size and instrument resolution.
- Confirm that high-scoring matches (similarity > threshold) with precursor m/z outside tolerance are absent from output.
- Validate that matched records report both experimental and library precursor m/z values, enabling post-hoc audit.
- Compare match counts before and after filtering; expect substantial reduction if tolerance is tight or library is large.

## Limitations

- Tolerance window must be tuned to instrument capabilities; too loose and specificity drops, too tight and sensitivity is lost.
- Presumes precursor m/z is accurately measured and annotated in both experimental data and library; missing or incorrect values will cause incorrect filtering.
- Does not account for isotope patterns (e.g., 13C isotope shift ~1 Da) if library entries span multiple isotope variants.
- Relies on library having comprehensive, accurate precursor m/z metadata; older or manually curated libraries may have systematic biases.

## Evidence

- [other] Filter candidate matches using a similarity threshold and mass tolerance window on precursor m/z.: "Filter candidate matches using a similarity threshold and mass tolerance window on precursor m/z."
- [other] Apply cosine similarity or dot-product scoring to compare each experimental MS/MS spectrum against all library entries.: "Apply cosine similarity or dot-product scoring to compare each experimental MS/MS spectrum against all library entries."
- [other] Rank matched library spectra by score and output matched records with spectrum metadata, library accession, match score, and fragment ion assignments to a structured results file (CSV or JSON).: "Rank matched library spectra by score and output matched records with spectrum metadata, library accession, match score, and fragment ion assignments to a structured results file (CSV or JSON)."
- [readme] TandemMatch: MS/MS spectral library matching with support for MSP and CSV library formats.: "TandemMatch: MS/MS spectral library matching with support for MSP and CSV library formats."

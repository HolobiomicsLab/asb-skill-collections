---
name: fragmentation-pattern-spectral-matching
description: Use when when you have detected m/z values from LC-IM-MS/MS that match a candidate CCS prediction database but require structural confirmation. Apply this skill to disambiguate isomers (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3647
  edam_topics:
  - http://edamontology.org/topic_0153
  - http://edamontology.org/topic_3520
  tools:
  - Python
  - Jupyter Notebook
  - RDKit
derived_from:
- doi: 10.1002/anie.202507483
  title: NA
evidence_spans:
- collection of Python scripts
- All functions are implemented in jupyter notebook
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_na_cq
    doi: 10.1002/anie.202507483
    title: NA
  dedup_kept_from: coll_na_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1002/anie.202507483
  all_source_dois:
  - 10.1002/anie.202507483
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# fragmentation-pattern-spectral-matching

## Summary

Match experimental MS/MS fragmentation spectra against theoretical or database spectra to confirm molecular structure identity and isomer stereochemistry. This skill filters candidate identifications by spectral similarity and fragmentation pattern coherence, enabling high-confidence assignment of sterol isomers in LC-IM-MS/MS data.

## When to use

When you have detected m/z values from LC-IM-MS/MS that match a candidate CCS prediction database but require structural confirmation. Apply this skill to disambiguate isomers (e.g., sterol double-bond position and stereochemistry) that have identical or near-identical m/z and CCS values but produce distinguishable fragmentation patterns under MS/MS ionization.

## When NOT to use

- When input is already a curated sterol metabolite library or authenticated reference spectrum collection — no additional matching is needed.
- When experimental MS/MS spectra are of poor signal-to-noise ratio or heavily fragmented such that major diagnostic peaks are absent — spectral matching will be unreliable.
- When sterol candidates differ only in fatty-acid chain composition (not double-bond position or stereochemistry) — MS/MS fragmentation patterns may be too similar to discriminate.

## Inputs

- Experimental MS/MS fragmentation spectrum (m/z, intensity pairs) for a detected feature
- Theoretical MS/MS fragmentation spectra database indexed by sterol structure and N-Me fragmentation pattern
- CCS-filtered candidate list (m/z and structure proposals pre-selected by ion mobility and mass accuracy)

## Outputs

- Annotated sterol identification records (structure, double-bond position, stereochemistry)
- Fragmentation pattern match scores (e.g., cosine similarity or equivalent metric)
- Composite confidence score combining CCS and spectral match quality
- Tissue-specific quantitative sterol data (intensity linked to matched feature)

## How to apply

After m/z matching and CCS tolerance filtering, extract the experimental MS/MS fragmentation spectrum for each candidate feature. Compare it against theoretical MS/MS spectra generated from N-Me derived fragmentation patterns using RDKit-based MS/MS calculation that models double-bond position-specific cleavage. Score spectral similarity using a standard metric (e.g., cosine similarity or dot product). Filter candidates to retain only those whose fragmentation pattern match quality exceeds a defined threshold (specific cutoff not disclosed in article); use the quality of spectral match as a confidence scoring component alongside CCS match quality. Annotate the final identification with the matched sterol structure (including double-bond position and stereochemistry) and a composite confidence score reflecting both CCS and spectral agreement.

## Related tools

- **RDKit** (MS/MS calculation engine that recognizes double bond positions and generates theoretical fragmentation spectra based on N-Me derived fragmentation rules for sterol lipids)
- **Python** (Primary scripting language for implementing fragmentation pattern matching and spectral similarity scoring) — https://github.com/Chen-micslab/QCCAssisted4DSterol
- **Jupyter Notebook** (Notebook environment in which fragmentation pattern matching functions are implemented and executed) — https://github.com/Chen-micslab/QCCAssisted4DSterol

## Evaluation signals

- Spectral match score for accepted identifications should be well above random baseline (i.e., substantially higher than matches to unrelated sterol structures)
- Identified sterol structures should exhibit fragmentation patterns consistent with known N-Me cleavage rules (e.g., breaks flanking or adjacent to double-bond positions)
- Confidence scores derived from fragmentation matching should correlate with external validation (e.g., reference standards or orthogonal chromatographic methods) where available
- Rejected candidates should show spectral match scores below threshold, with fragmentation patterns inconsistent with assigned structure
- Identified sterol isomers with different double-bond positions or stereochemistry should produce visibly distinct MS/MS spectra in diagnostic peak positions

## Limitations

- The skill is only validated on N-Me derived unsaturated sterol lipids; applicability to other sterol modifications or lipid classes is untested
- Spectral matching relies on the completeness and accuracy of the theoretical MS/MS database; missing or mis-calculated fragmentation patterns will reduce sensitivity
- Isomers with very similar fragmentation patterns (e.g., long-chain aliphatic sterols differing only in chain length) may not be resolved by MS/MS matching alone
- The specific spectral match threshold and confidence scoring formula are not provided in the article; implementation requires parameter optimization on reference data

## Evidence

- [other] Filter candidate identifications by CCS tolerance and MS/MS fragmentation pattern matching.: "Filter candidate identifications by CCS tolerance and MS/MS fragmentation pattern matching."
- [readme] The script recognises double bond positions and generates MS/MS based on N-Me fragmentation patterns.: "The script  recognises double bond positions and generates MS/MS based on N-Me fragmentation patterns."
- [other] Annotate matched features with sterol structure (including double-bond position and stereochemistry) and assign confidence scores based on CCS and spectral match quality.: "Annotate matched features with sterol structure (including double-bond position and stereochemistry) and assign confidence scores based on CCS and spectral match quality."
- [readme] The script is written on the basis of RDkit's built-in functions.: "The script is written on the basis of RDkit's built-in functions."

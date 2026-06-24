---
name: ion-species-confirmation-validation
description: Use when after you have identified candidate ion-species pairs through
  pointwise correlation analysis of XIC temporal profiles and exact mass difference
  refinement, and you have MS2 fragment spectra available for those candidates.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3802
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - DBDIpy
  - Python
  - matchms
  techniques:
  - LC-MS
  license_tier: restricted
derived_from:
- doi: 10.1093/bioinformatics/btad088/7036334
  title: DBDIpy
evidence_spans:
- DBDIpy is an open-source Python library for the curation and interpretation of dielectric
  barrier discharge ionisation mass spectrometric datasets
- DBDIpy is an open-source Python library
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_dbdipy_cq
    doi: 10.1093/bioinformatics/btad088/7036334
    title: DBDIpy
  dedup_kept_from: coll_dbdipy_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioinformatics/btad088/7036334
  all_source_dois:
  - 10.1093/bioinformatics/btad088/7036334
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# ion-species-confirmation-validation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Confirm that candidate ion-species pairs originate from the same analyte compound by calculating MS2 spectral similarity scores as the final validation step in DBDIpy's three-step identification procedure. This skill validates putative adduct and fragment assignments after temporal correlation and mass difference refinement.

## When to use

Apply this skill after you have identified candidate ion-species pairs through pointwise correlation analysis of XIC temporal profiles and exact mass difference refinement, and you have MS2 fragment spectra available for those candidates. Use it when you need to confirm that pairs sharing correlated intensity profiles and matching mass offsets actually derive from the same parent analyte rather than being coincidental correlations.

## When NOT to use

- MS2 spectra are not available for the candidate pairs (e.g., MS1-only datasets or MS2 acquisition failure); fall back to two-step identification using correlation and mass difference alone.
- Fragment spectra have insufficient quality or signal-to-noise ratio to compute reliable similarity scores; preprocessing or alternative thresholds may be needed.
- Input pairs are already confirmed by orthogonal methods (e.g., reference standards, retention time matching); validation is redundant.

## Inputs

- MS2 fragment spectra (matched spectra objects from matchms.Spectra or preprocessed spectral arrays)
- Candidate ion-species pair list with base m/z, match m/z, correlation coefficient, and mass difference from prior refinement step
- Acceptance threshold for similarity score (user-defined parameter, typically 0.7–0.9 for cosine similarity)

## Outputs

- Annotated candidate pair table with MS2 spectral similarity scores
- Confirmation status column (boolean or categorical: confirmed/rejected/ambiguous)
- Mapping of confirmed ion pairs to their parent analyte compound identity

## How to apply

Extract and preprocess the MS2 fragment spectra for each candidate ion pair (normalize intensity, remove noise), then calculate the MS2 spectral similarity score between the two fragment profiles using cosine similarity or related spectral matching algorithms. Annotate each pair with its similarity score and flag pairs exceeding your acceptance threshold as confirmed shared-analyte relationships. The threshold selection depends on your mass spectrometry platform resolution and acceptable false-positive rate; higher thresholds (e.g., cosine similarity > 0.7–0.9) reduce false positives but may miss true positive pairs with partial spectral overlap. Output a table mapping candidate pairs to their spectral similarity scores and confirmation status for downstream annotation and visualization.

## Related tools

- **DBDIpy** (Implements the three-step identification procedure including MS2 spectral similarity scoring as the final confirmation step) — https://github.com/leopold-weidner/DBDIpy
- **matchms** (Provides spectral data structures (Spectra objects) and spectral matching algorithms (cosine similarity, related metrics) for MS2 similarity scoring) — https://github.com/matchms/matchms
- **Python** (Programming language in which DBDIpy and matchms are implemented)

## Evaluation signals

- All candidate pairs in the output table have a spectral similarity score value (no missing scores); scores are numeric and in the expected range (0–1 for cosine similarity or 0–100 for normalized percentages).
- Confirmed pairs (above threshold) have significantly higher MS2 similarity scores than rejected pairs; distribution of scores shows clear bimodality or separation at the threshold.
- Confirmed pairs show concordant MS2 fragment patterns (matching peak positions and intensity ratios within mass tolerance) when visually inspected or compared with reference spectra.
- The number and identity of confirmed pairs is consistent with expected adduct/fragment rules (e.g., [M+O+H]+ pairs show mass difference of ~15.99 amu and similar fragmentation patterns).
- Output table contains no duplicate pairs and all row identifiers link back to valid entries in the input candidate list and the original feature table.

## Limitations

- MS2 spectral similarity scoring requires high-quality, well-resolved fragment spectra; low signal-to-noise or heavily suppressed MS2 signals may yield ambiguous or artificially low similarity scores leading to false negatives.
- Cosine similarity and related algorithms assume that matching fragment ion peaks indicate shared analyte origin; in complex mixtures or with overlapping fragmentation patterns, spurious high similarities can occur (false positives).
- The choice of acceptance threshold is user-dependent and data-dependent; no universal threshold is given in the article. Threshold tuning requires validation against reference compounds or orthogonal confirmation methods.
- MS2 spectra must be collected in the same ionization mode and with comparable collision energy/fragmentation conditions as reference spectra; if MS2 data come from different experimental conditions, similarity comparisons may be unreliable.
- The article README notes that runtime optimization is currently under development, suggesting that large-scale similarity scoring for thousands of candidate pairs may be computationally expensive.

## Evidence

- [other] DBDIpy implements a three-step identification procedure in which MS2 spectral similarity scoring is the final step, following pointwise correlation analysis of temporal intensity profiles and exact mass difference refinement, to confirm shared analyte origin of candidate ion pairs.: "DBDIpy implements a three-step identification procedure in which MS2 spectral similarity scoring is the final step, following pointwise correlation analysis of temporal intensity profiles and exact"
- [other] For each candidate pair, extract and preprocess the corresponding MS2 fragment spectra (normalize intensity, remove noise). Calculate MS2 spectral similarity score using cosine similarity or related spectral matching algorithm between fragment profiles.: "For each candidate pair, extract and preprocess the corresponding MS2 fragment spectra (normalize intensity, remove noise). 3. Calculate MS2 spectral similarity score using cosine similarity or"
- [readme] The identification is performed in a three-step procedure (from V > 2.* on, in preparation): calculation of pointwise correlation identifies features with matching temporal intensity profiles through the experiment. (exact) mass differences are used to refine the nature of potential candidates. calculation of MS2 spectral similarity score by ...: "The identification is performed in a three-step procedure (from V > 2.* on, in preparation): calculation of pointwise correlation identifies features with matching temporal intensity profiles through"
- [readme] Major implementation for V2: modification of the former two-step search algorithm towards refinement by MS2 spectral similarity scoring.: "Major implementation for V2: modification of the former two-step search algorithm towards refinement by MS2 spectral similarity scoring"
- [other] Annotate each pair with its similarity score and flag pairs exceeding the acceptance threshold as confirmed shared-analyte relationships. Generate output table mapping candidate pairs to their spectral similarity scores and confirmation status.: "Annotate each pair with its similarity score and flag pairs exceeding the acceptance threshold as confirmed shared-analyte relationships. Generate output table mapping candidate pairs to their"

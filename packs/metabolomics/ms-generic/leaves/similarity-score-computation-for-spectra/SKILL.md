---
name: similarity-score-computation-for-spectra
description: Use when you have a preprocessed unknown sample spectrum (m/z peaks and intensities) and need to identify the most likely species or reference entries by scoring it against a database of known spectra.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3800
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - RapidMass
  techniques:
  - mass-spectrometry
derived_from:
- doi: 10.1021/acs.analchem.4c05062
  title: RapidMass
evidence_spans:
- We have developed a versatile software platform, RapidMass.
- We have developed a versatile software platform, RapidMass
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_rapidmass_cq
    doi: 10.1021/acs.analchem.4c05062
    title: RapidMass
  dedup_kept_from: coll_rapidmass_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.4c05062
  all_source_dois:
  - 10.1021/acs.analchem.4c05062
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Similarity-score computation for spectra

## Summary

Compute quantitative similarity scores between an unknown mass spectrometry sample spectrum and reference spectra in a database using distance or correlation metrics on aligned m/z features. This enables ranking and candidate species assignment for automated sample authentication.

## When to use

You have a preprocessed unknown sample spectrum (m/z peaks and intensities) and need to identify the most likely species or reference entries by scoring it against a database of known spectra. Use this skill when the goal is to produce a ranked candidate list with numerical match scores for direct discrimination of unknowns.

## When NOT to use

- Raw (unpreprocessed) mass spectrometry data — preprocess peaks and intensities first
- When reference database is empty or lacks known spectra for your sample type
- When m/z alignment or feature normalization has not been performed on input spectra

## Inputs

- Preprocessed unknown sample spectrum (m/z peaks and intensities)
- Reference species database (collection of known spectra with species labels and accession identifiers)
- Aligned m/z feature vectors from unknown and reference spectra

## Outputs

- Scored candidate list table (CSV or TSV format)
- Ranked reference entries with columns: rank, species name, reference_id, similarity_score

## How to apply

Load the preprocessed unknown sample spectrum and the reference species database containing known spectra. For each reference spectrum, compute a similarity score using a distance or correlation metric such as cosine similarity or Euclidean distance applied to aligned m/z features. Rank all reference entries by descending score. Output the full scored candidate list in tabular format (CSV or TSV) with columns for rank, species name, reference identifier, and numerical similarity score. The score magnitude and ranking determine confidence in species assignment; higher scores indicate closer matches to reference spectra.

## Related tools

- **RapidMass** (Integrated platform for spectrum preprocessing, similarity scoring, and ranked candidate output; provides multiple built-in database search algorithms and visual interface for result inspection) — https://github.com/Katherine00689/RapidMass

## Evaluation signals

- Output table is sorted in descending order of similarity_score with no missing or NaN values in score column
- Number of rows in output equals number of reference spectra in database; no duplicates
- Similarity scores fall within the valid range for the chosen metric (e.g., 0–1 for cosine similarity)
- Top-ranked candidate matches the expected true species when validated on known-identity samples
- Species assignments are consistent across multiple runs with identical inputs

## Limitations

- Performance depends on quality and completeness of the reference database; absent or poorly characterized species will not be retrieved
- Easily confused plant materials or samples with highly similar spectra may produce ambiguous or low-confidence scores
- The choice of distance metric (cosine similarity vs. Euclidean distance) and m/z alignment parameters affect score magnitude and ranking
- Visual validation outputs are needed to assess biological plausibility of top candidates beyond numerical ranking

## Evidence

- [other] Metric choice and alignment procedure: "For each reference spectrum in the database, compute a similarity score between the unknown sample and the reference using a distance or correlation metric (e.g., cosine similarity or Euclidean"
- [other] Output format and ranking: "Rank all reference entries by descending score and output the full scored candidate list with species names, accession identifiers, and match scores. Return results in a tabular format (CSV or TSV)"
- [readme] Integration of scoring into full workflow: "RapidMass offers several database search algorithms to achieve unknown sample scoring."
- [intro] Visual output for result inspection: "enabling direct discrimination of unknown sample species with intuitive visual outputs"
- [intro] Validation and performance context: "The performance of RapidMass was validated using easily confused plant materials, with satisfactory results."

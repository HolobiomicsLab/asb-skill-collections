---
name: inchikey-structural-similarity-computation
description: Use when you have a ranked list of library candidates (top 2000 by MS2Deepscore) from MS/MS spectral matching and need to re-rank them using structural metadata to distinguish true analogues and exact matches from false positives.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0292
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0593
  tools:
  - MS2Query
  - GitHub
  - MS2Deepscore
  - RDKit
  - Random forest (scikit-learn or equivalent)
  techniques:
  - tandem-MS
derived_from:
- doi: 10.1038/s41467-023-37446-4
  title: ms2query
evidence_spans:
- you want to make some kind of change to the code base
- MS2Query - Reliable and fast MS/MS spectral-based analogue search
- fork the repository to your own Github profile and create your own feature branch off of the latest master commit
- use the search functionality [here](https://github.com/iomega/ms2query/issues)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ms2query_cq
    doi: 10.1038/s41467-023-37446-4
    title: ms2query
  dedup_kept_from: coll_ms2query_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41467-023-37446-4
  all_source_dois:
  - 10.1038/s41467-023-37446-4
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# inchikey-structural-similarity-computation

## Summary

Compute average InChIKey structural similarity scores and neighbourhood scores across candidate MS/MS library matches to enable reliable re-ranking of analogue and exact-match candidates in MS2Query. This skill combines structural fingerprint similarity with spectral context to improve match confidence beyond raw spectral similarity alone.

## When to use

Apply this skill when you have a ranked list of library candidates (top 2000 by MS2Deepscore) from MS/MS spectral matching and need to re-rank them using structural metadata to distinguish true analogues and exact matches from false positives. Use it specifically when candidate spectra are annotated with InChIKey, SMILES, or InChI strings and you want to weight structural similarity as part of a combined scoring model.

## When NOT to use

- Library spectra lack structural metadata (InChIKey, SMILES, or InChI annotations) — scoring cannot be computed.
- Query spectra are unannotated or precursor m/z is missing — re-ranking cannot disambiguate analogues from exact matches.
- Exact matches only are required and high-confidence spectral similarity alone is sufficient (no need for neighbourhood scoring overhead).

## Inputs

- MS/MS candidate matches (top 2000 spectra by MS2Deepscore score)
- Library spectra with annotated InChIKey, SMILES, or InChI metadata
- Query spectrum precursor m/z and experimental MS/MS peak list

## Outputs

- Average InChIKey score per candidate (scalar, 0–1 range)
- Neighbourhood score per candidate (scalar, 0–1 range)
- Re-ranked candidate list with combined structural + spectral scores
- MS2Query model prediction score (0–1) for top match

## How to apply

For each candidate library spectrum matched to a query spectrum, extract or compute the InChIKey (or InChI) from the annotated molecular structure metadata. Compute pairwise structural similarity using InChIKey-based neighbourhood scoring—typically via Tanimoto distance on molecular fingerprints derived from the InChI layer structure. Aggregate the similarity scores across all top candidates (e.g., mean or weighted neighbourhood score). Integrate these structural scores into the MS2Query random forest re-ranking model alongside spectral similarity, precursor m/z difference, and other features. Apply a threshold (e.g., ≥0.7 for high confidence) to filter unreliable matches. The rationale is that true analogues and exact matches exhibit correlated structural and spectral similarity; neighbourhood scoring isolates structural signal to improve precision.

## Related tools

- **MS2Query** (Main platform integrating InChIKey scoring into re-ranking pipeline for MS/MS library search) — https://github.com/iomega/ms2query
- **MS2Deepscore** (Generates top 2000 candidate matches by spectral similarity before structural re-ranking) — https://github.com/iomega/ms2query
- **RDKit** (Computes molecular fingerprints from InChI/SMILES for neighbourhood similarity calculation)
- **Random forest (scikit-learn or equivalent)** (Combines InChIKey score, neighbourhood score, and spectral features for final match ranking)

## Examples

```
from ms2query.run_ms2query import run_complete_folder; from ms2query.ms2library import create_library_object_from_one_dir; ms2library = create_library_object_from_one_dir('./ms2query_library_files'); run_complete_folder(ms2library, './ms2_spectra_directory')
```

## Evaluation signals

- InChIKey score and neighbourhood score outputs fall within [0, 1] range with no NaN or infinite values for valid inputs.
- True exact matches (precursor m/z difference ≈ 0) exhibit neighbourhood scores ≥ 0.9 when library and query have identical or near-identical InChI layers.
- False positives (high spectral similarity but structurally dissimilar) show low neighbourhood scores (<0.3), causing them to drop in re-ranked order.
- Re-ranked candidate lists place annotated true analogues (confirmed via manual inspection or external reference) in top 5 results when neighbourhood score >0.7 and spectral similarity >0.6.
- Unit tests verify that known input candidates (with annotated InChIKey) produce expected output scores without regression in core MS2Query matching pipeline (test via `python setup.py test`).

## Limitations

- InChIKey score computation requires complete, accurate structural metadata (InChIKey, SMILES, or InChI) for all library spectra; missing or malformed annotations cause candidates to be excluded or scored as zero.
- Neighbourhood scoring may conflate regioisomers and stereoisomers that differ in layers 3–4 of the InChI but not in precursor m/z or fragmentation pattern, potentially misranking structurally similar but formally distinct compounds.
- Random forest re-ranking model is trained on GNPS library data (15-Dec-2021); performance on novel chemotypes not well-represented in training set is not validated.
- No preselection on precursor m/z is performed during candidate generation; neighbourhood scoring adds computational overhead for thousands of off-target structural comparisons before filtering.

## Evidence

- [other] MS2Query implements scoring mechanisms for MS/MS spectral-based analogue search to enable reliable candidate matching.: "MS2Query implements scoring mechanisms for MS/MS spectral-based analogue search to enable reliable candidate matching."
- [other] Implement scoring component functions in Python that compute average inchikey score across candidate matches and neighbourhood score based on structural similarity.: "Implement scoring component functions in Python that compute average inchikey score across candidate matches and neighbourhood score based on structural similarity."
- [other] Integrate both scoring components into the MS2Query match ranking pipeline to combine with existing similarity metrics.: "Integrate both scoring components into the MS2Query match ranking pipeline to combine with existing similarity metrics."
- [readme] MS2Query optimizes re-ranking the best analogue or exact match at the top by using a random forest that combines 5 features.: "MS2Query optimizes re-ranking the best analogue or exact match at the top by using a random forest that combines 5 features."
- [readme] It is important that the library spectra are annotated with smiles, inchi's or inchikeys in the metadata otherwise they are not included in the library.: "It is important that the library spectra are annotated with smiles, inchi's or inchikeys in the metadata otherwise they are not included in the library."
- [readme] The top 2000 spectra with the highest MS2Deepscore are selected. In contrast to other analogue search methods, no preselection on precursor m/z is performed.: "The top 2000 spectra with the highest MS2Deepscore are selected. In contrast to other analogue search methods, no preselection on precursor m/z is performed."

---
name: neighbourhood-density-computation
description: Use when after library-matching has produced ranked candidate spectra with MS2Deepscore embeddings.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_3172
  tools:
  - MS2Query
  - MS2Deepscore
  - Python
  techniques:
  - LC-MS
derived_from:
- doi: 10.1038/s41467-023-37446-4
  title: ms2query
evidence_spans:
- MS2Query - Reliable and fast MS/MS spectral-based analogue search
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ms2query
    doi: 10.1038/s41467-023-37446-4
    title: ms2query
  dedup_kept_from: coll_ms2query
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

# neighbourhood-density-computation

## Summary

Compute neighbourhood density scores for candidate MS/MS library matches by evaluating the clustering and proximity of similar candidates in spectral feature space. This metric is combined with InChIKey structural similarity scores to rank library candidates and filter unreliable matches in MS2Query.

## When to use

Apply this skill after library-matching has produced ranked candidate spectra with MS2Deepscore embeddings. Use it when you need to distinguish between high-confidence matches (clustered with many similar candidates) and isolated matches that may be spurious, particularly when a minimum confidence threshold is required to filter results.

## When NOT to use

- The input candidate set is too small (<10 similar matches per candidate) to reliably estimate neighbourhood density.
- Query spectra have no close matches in the library; neighbourhood scores will be uniformly low and provide no discriminative value.
- You require fast single-match retrieval without ranking confidence; neighbourhood computation adds computational overhead.

## Inputs

- Top-ranked candidate library matches (e.g. top 2000 spectra)
- Pre-computed MS2Deepscore embeddings for library spectra
- Candidate match identifiers and metadata
- MS2Deepscore similarity matrix or pairwise distance matrix

## Outputs

- Neighbourhood density score per candidate (numeric, 0–1 range)
- Candidate records with neighbourhood score and structural similarity annotations
- Composite scoring input for random forest re-ranker

## How to apply

After selecting the top-ranked candidates (e.g. top 2000 spectra by MS2Deepscore), compute neighbourhood density by measuring the proximity and clustering density of candidate spectra in the pre-computed MS2Deepscore embedding space. The neighbourhood score reflects how many similar candidates exist near each candidate in the spectral feature space. Candidates surrounded by many structurally or spectrally similar library matches receive higher neighbourhood scores, whereas isolated candidates receive lower scores. Combine the neighbourhood score with the InChIKey structural similarity score into a single composite metric (as input to the random forest re-ranker). Higher neighbourhood density indicates a more reliable match prediction, helping filter out false positives that lack spectral context.

## Related tools

- **MS2Query** (Parent workflow that integrates neighbourhood density computation into candidate re-ranking using a random forest that combines 5 features (including neighbourhood score and InChIKey score)) — https://github.com/iomega/ms2query
- **MS2Deepscore** (Produces pre-computed spectral embeddings and similarity scores used to define neighbourhood proximity in the spectral feature space) — https://github.com/iomega/ms2query
- **Python** (Implementation language for neighbourhood density algorithms and score aggregation; candidates validated via pytest)

## Evaluation signals

- Neighbourhood scores fall in the range [0, 1] and show variation across candidates (not all uniform)
- Candidates with high neighbourhood scores (>0.7) correspond to spectral regions with dense clustering in embedding space; candidates with low scores (<0.3) are isolated
- Composite score (neighbourhood + InChIKey) improves random forest discriminative power (AUC-ROC or precision/recall) over InChIKey score alone on a test set
- Unit tests via pytest pass and validate output record structure (candidate ID, neighbourhood score, InChIKey score, and metadata fields)
- Neighbourhood score distribution shifts higher (median >0.5) when library is large and diverse; shifts lower when library is sparse or query has few similar spectra

## Limitations

- Neighbourhood density is undefined or unreliable when the library is very small or sparse, or when query spectra have no close spectral matches.
- Pre-computed embeddings must be available for all library spectra; missing or outdated embeddings invalidate proximity computations.
- The metric conflates spectral similarity (from MS2Deepscore) with structural similarity (from InChIKey), which may not always align (a spectrally similar compound may have a different structure).
- No preselection on precursor m/z is performed, so neighbourhood density includes structurally unrelated compounds with similar fragmentation patterns, which may obscure true analogue relationships.

## Evidence

- [other] Compute neighbourhood score for each candidate by evaluating the density and proximity of similar candidates in the spectral feature space.: "Compute neighbourhood score for each candidate by evaluating the density and proximity of similar candidates in the spectral feature space."
- [readme] The random forest predicts a score between 0 and 1 between each library and query spectrum and the highest scoring library match is selected. By using a minimum threshold for this score, unreliable matches are filtered out.: "The random forest predicts a score between 0 and 1 between each library and query spectrum and the highest scoring library match is selected. By using a minimum threshold for this score, unreliable"
- [readme] The top 2000 spectra with the highest MS2Deepscore are selected. In contrast to other analogue search methods, no preselection on precursor m/z is performed.: "The top 2000 spectra with the highest MS2Deepscore are selected. In contrast to other analogue search methods, no preselection on precursor m/z is performed."
- [readme] By using pre-computed MS2Deepscore embeddings for library spectra, this full-library comparison can be computed very quickly.: "By using pre-computed MS2Deepscore embeddings for library spectra, this full-library comparison can be computed very quickly."
- [other] Combine both scores into a single candidate record with standardized fields (candidate ID, InChIKey score, neighbourhood score).: "Combine both scores into a single candidate record with standardized fields (candidate ID, InChIKey score, neighbourhood score)."

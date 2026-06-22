---
name: spectrum-similarity-scoring
description: 'Use when you have an unknown MS/MS spectrum (query spectrum with m/z and intensity pairs) and a reference spectral library (local or public: GNPS, MASSBANK, DrugBANK), and you need to identify the -matching compounds by ranking library entries by spectral similarity.'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3802
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3375
  tools:
  - MASSBANK
  - DrugBANK
  - meRgeION2
  - MergeION2
  - GNPS
  techniques:
  - CE-MS
derived_from:
- doi: 10.1021/acs.analchem.2c04343
  title: MeRgeION
evidence_spans:
- search and annotate an unknown spectrum in their local database or public databases (i.e. drug structures in GNPS, MASSBANK and DrugBANK)
- github.com__daniellyz__meRgeION2
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mergeion_cq
    doi: 10.1021/acs.analchem.2c04343
    title: MeRgeION
  dedup_kept_from: coll_mergeion_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.2c04343
  all_source_dois:
  - 10.1021/acs.analchem.2c04343
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# spectrum-similarity-scoring

## Summary

Compute similarity scores between an experimental MS/MS spectrum and library reference spectra using algorithms such as cosine similarity or spectral dot-product to rank and identify best-matching compounds. This is the core computational step that enables automated spectral library search and compound annotation.

## When to use

You have an unknown MS/MS spectrum (query spectrum with m/z and intensity pairs) and a reference spectral library (local or public: GNPS, MASSBANK, DrugBANK), and you need to identify the best-matching compounds by ranking library entries by spectral similarity. Apply this skill when precursor m/z matching alone is insufficient and you require fragment-level pattern matching to distinguish among candidate structures.

## When NOT to use

- Query spectrum is a single m/z peak or lacks sufficient fragmentation pattern (fewer than min_frag_match fragments); similarity scoring requires multiple fragment ions for robust ranking.
- Reference library is empty, severely outdated, or contains spectra collected under incompatible ionization mode (e.g., searching negative-mode query against positive-mode library without conversion).
- Precursor m/z is unknown or unreliable; without accurate precursor mass, use_prec filtering may eliminate true matches or allow false positives.

## Inputs

- Query MS/MS spectrum (two-column matrix: m/z values, intensity values)
- Reference spectral library (GNPS-style library, or entries from GNPS, MASSBANK, or DrugBANK)
- Query parameters list (precursor m/z, use_prec flag, polarity, similarity method, min_frag_match, min_score threshold)

## Outputs

- Ranked list of matched library spectra with cosine similarity or dot-product scores
- Matched compound metadata (compound name, molecular formula, INCHI, INCHIKEY, library accession ID)
- Match scores and filtering statistics
- Mirror plot visualization comparing query and matched reference spectra

## How to apply

Load the query spectrum as a two-column matrix (m/z, intensity) and the reference library. Specify key parameters: precursor m/z tolerance, similarity metric (cosine or dot-product), minimum fragment match count, and similarity score threshold (e.g., min_score = 0). Compute pairwise similarity scores between the query and all candidate library spectra using the selected metric. Filter and rank results by similarity score in descending order, optionally enforcing precursor m/z match by setting use_prec = TRUE. Return ranked candidates with match scores and metadata (compound name, molecular formula, INCHI, library accession ID) for visual inspection via mirror plots or further validation.

## Related tools

- **MergeION2** (R package implementing library_query() function for spectral similarity search and ranking against local or public spectral libraries using cosine or dot-product metrics) — https://github.com/daniellyz/MergeION2
- **GNPS** (Public spectral library repository for reference spectra used in similarity-based compound annotation)
- **MASSBANK** (Public spectral database of reference MS/MS spectra for small-molecule metabolites and natural products)
- **DrugBANK** (Public reference database of approved drug structures and MS/MS spectra for pharmaceutical metabolite identification)

## Examples

```
params.query.sp = list(prec_mz = 369.232, use_prec = T, polarity = "Positive", method = "Cosine", min_frag_match = 6, min_score = 0); search_result = library_query(input_library = library1c, query_spectrum = query.sp, params.query.sp = params.query.sp)
```

## Evaluation signals

- Matched compounds have cosine similarity or dot-product scores above the specified min_score threshold and rank correctly by decreasing similarity.
- Best-matching hit is a known standard or positive control with high similarity score (≥ 0.8–0.95 range typical for high-confidence annotation).
- Mirror plot visualization shows substantial spectral overlap between query and top-ranked match, with major fragments aligned at equivalent m/z.
- Precursor m/z of matched compound aligns with query precursor within expected mass accuracy (typically <5 ppm for high-resolution MS).
- INCHIKEY or molecular formula of top match is biochemically plausible for the sample context (e.g., drug metabolite in pharmacokinetics study).

## Limitations

- Library search performance degrades if query spectrum has low signal-to-noise ratio, sparse fragmentation, or unusual collision-induced dissociation patterns not represented in the reference library.
- Cosine similarity and dot-product metrics are sensitive to relative peak intensities; normalization and scaling can alter rankings, especially for low-abundance or in-source fragments.
- False positives may occur when structurally similar compounds with overlapping fragmentation patterns are present in the library; chemical context and retention time filtering improve specificity.
- Public library repositories (GNPS, MASSBANK) are curated but may contain redundant, duplicated, or lower-quality spectra entries; metadata quality varies across repositories.
- ESI-MS/MS spectra in the pre-compiled library are currently positive-ion mode only; negative-mode or alternative ionization spectra require separate library sources.

## Evidence

- [other] Apply library search algorithm to compute similarity scores (e.g., cosine similarity or spectral dot-product) between query spectrum and candidate library spectra.: "Apply library search algorithm to compute similarity scores (e.g., cosine similarity or spectral dot-product) between query spectrum and candidate library spectra."
- [other] Rank and filter matched spectra by similarity threshold to identify best-matching library entries.: "Rank and filter matched spectra by similarity threshold to identify best-matching library entries."
- [readme] Now it's time to collect query parameters into a R list. Don't be overwhelmed by the long list. Only important parameters to check are the prec_mz, which indicates the precursor mass, and use_prec, which forces precursor mass match in the search output by setting to TRUE: "Only important parameters to check are the prec_mz, which indicates the precursor mass, and use_prec, which forces precursor mass match in the search output by setting to TRUE"
- [readme] The MS/MS spectrum should be read as well into the R environment as a two-column matrix.: "The MS/MS spectrum should be read as well into the R environment as a two-column matrix."
- [readme] We can now print the candidate structure(s) found. In this example only one, and the Cosine spectral similarity is very high at 0.95: "Cosine spectral similarity is very high at 0.95"
- [readme] search_result = library_query(input_library = library1c, query_spectrum = query.sp, params.query.sp = params.query.sp): "search_result = library_query(input_library = library1c, query_spectrum = query.sp, params.query.sp = params.query.sp)"

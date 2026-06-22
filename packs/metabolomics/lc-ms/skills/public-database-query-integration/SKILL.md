---
name: public-database-query-integration
description: Use when you have an experimental MS/MS spectrum (m/z and intensity pairs with known precursor m/z) and need to identify the compound by searching against public repositories or a local reference library.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3802
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - MASSBANK
  - DrugBANK
  - meRgeION2
  - MergeION2
  - GNPS
  - RChemMass
  techniques:
  - LC-MS
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# public-database-query-integration

## Summary

Query and annotate unknown MS/MS spectra against public spectral libraries (GNPS, MASSBANK, DrugBANK) or local databases using spectral similarity algorithms. This skill enables rapid compound identification by matching experimental fragmentation patterns to curated reference spectra with associated metadata.

## When to use

Apply this skill when you have an experimental MS/MS spectrum (m/z and intensity pairs with known precursor m/z) and need to identify the compound by searching against public repositories or a local reference library. Use it when high-confidence annotation is required and reference spectra are available in GNPS, MASSBANK, DrugBANK, or a user-maintained local library.

## When NOT to use

- Query spectrum is in negative ion mode but library contains only positive-mode ESI-MS/MS spectra (e.g., GNPS_MASSBANK_PROCESSED_POS_CONSENSUS1 is positive-ion only).
- Unknown spectrum is from a non-standard ionization method (e.g., APCI, MALDI) and library contains only ESI spectra.
- Precursor m/z is unknown or uncertain; the use_prec parameter forces precursor matching, which will exclude correct hits if precursor is misidentified.

## Inputs

- Query MS/MS spectrum (two-column matrix: m/z and intensity pairs)
- Precursor m/z value
- Spectral library (local GNPS-style .RData object or connection to public database: GNPS, MASSBANK, or DrugBANK)
- Search parameters (polarity, method, min_frag_match, min_score, use_prec flag)

## Outputs

- Ranked list of candidate library matches with similarity scores
- Matched spectrum metadata (compound name, molecular formula, INCHI, InChIKey, library accession ID)
- Mirror-plot visualization comparing query spectrum to top matched library spectrum

## How to apply

Load the query MS/MS spectrum as a two-column matrix (m/z, intensity) into your R environment along with the target spectral library (e.g., GNPS_MASSBANK_PROCESSED consensus library). Assemble a parameters list specifying the precursor m/z, polarity (positive/negative), similarity method (Cosine recommended), minimum fragment matches (typically ≥6), and minimum score threshold. Execute library_query() with the input library, query spectrum, and parameters to compute spectral similarity scores (e.g., Cosine similarity) between the query and all candidate library spectra. Rank results by similarity score and filter by your chosen threshold (commonly ≥0.5–0.7 for confident matches). Retrieve matched entries with metadata (compound name, molecular formula, INCHI, library accession ID) and inspect visually using mirror-plot visualization to confirm fragmentation pattern agreement.

## Related tools

- **MergeION2** (R package implementing library_query() function for spectral library search with Cosine similarity and other algorithms; provides GUI and command-line interface for batch spectral annotation.) — https://github.com/daniellyz/MergeION2
- **GNPS** (Public spectral library and molecular networking platform; hosts and distributes consensus spectra used for reference library compilation and queries.)
- **MASSBANK** (Public MS/MS spectral database of metabolites and natural products; integrated into MergeION's query libraries.)
- **DrugBANK** (Public database of drug structures and approved pharmaceuticals; drug MS/MS spectra included in MergeION's curated reference library.)
- **RChemMass** (R package for chemical mass calculation and structure visualization; used alongside MergeION for molecular formula and structure display in annotation results.)

## Examples

```
search_result = library_query(input_library = library1c, query_spectrum = query.sp, params.query.sp = list(prec_mz = 369.232, use_prec = T, polarity = "Positive", method = "Cosine", min_frag_match = 6, min_score = 0.5))
```

## Evaluation signals

- Top match Cosine similarity score ≥0.7–0.95 indicates strong spectral agreement; scores <0.5 suggest no reliable match.
- Matched InChIKey and compound name remain consistent across replicate queries with the same precursor m/z and polarity.
- Mirror-plot visualization shows visually concordant fragmentation patterns between query and top-ranked library spectrum, with major peaks aligned.
- Number of matched fragments (min_frag_match parameter) meets or exceeds user-defined threshold; typically ≥6 fragments for robust match.
- Precursor m/z of matched library spectrum agrees with query precursor within instrument tolerance (typically ±5 ppm for Orbitrap, ±10 ppm for Q-TOF).

## Limitations

- Library is currently limited to ESI-MS/MS in positive ion mode; negative-mode and alternative ionization methods are not yet supported in the pre-compiled GNPS_MASSBANK_PROCESSED_POS_CONSENSUS1 library.
- Search performance and annotation confidence depend on library completeness and spectrum quality; rare or unstandardized compounds may lack reference spectra.
- Spectral similarity alone may be insufficient for structural disambiguation; isomeric or isobaric compounds with identical precursor m/z may produce similar fragmentation patterns.
- Public databases (GNPS, MASSBANK, DrugBANK) require internet connectivity for queries; offline search requires pre-downloaded local library in GNPS-style .RData format.

## Evidence

- [intro] Public database query and spectrum matching: "search and annotate an unknown spectrum in their local database or public databases (i.e. drug structures in GNPS, MASSBANK and DrugBANK)"
- [other] Spectral library search algorithm and similarity scoring: "library search algorithm to compute similarity scores (e.g., cosine similarity or spectral dot-product) between query spectrum and candidate library spectra"
- [other] Query spectrum format and precursor m/z requirement: "Load the unknown query spectrum (MS/MS data with m/z and intensity pairs) from input file"
- [readme] R implementation with specific parameters: "params.query.sp = list(prec_mz = 369.232, use_prec = T, polarity = "Positive", method = "Cosine", min_frag_match = 6, min_score = 0)"
- [other] Metadata retrieval and annotation output: "Retrieve and annotate matched spectra with metadata (compound name, molecular formula, INCHI, library accession) and output annotated results with match scores"
- [readme] Positive-ion ESI-MS/MS library scope: "Currently ESI-MS/MS spectra in our collection are all in positive ion mode"
- [readme] R invocation example: "search_result = library_query(input_library = library1c, query_spectrum = query.sp, params.query.sp = params.query.sp)"

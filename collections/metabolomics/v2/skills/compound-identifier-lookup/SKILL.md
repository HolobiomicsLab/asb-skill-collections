---
name: compound-identifier-lookup
description: Use when you have an experimental MS/MS spectrum (m/z and intensity pairs in mzML/mzXML format from DDA or targeted acquisition on Thermo, Waters, or Bruker instruments) and need to identify the unknown compound by comparing it against a reference database.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3860
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - MASSBANK
  - DrugBANK
  - meRgeION2
  - MergeION2
  - GNPS
  - RChemMass
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
---

# Reconstruct library search annotation of an unknown spectrum against a local or public database

## Summary

Search and annotate an unknown MS/MS spectrum by matching its fragmentation pattern and precursor m/z against a spectral library (local or public) using cosine similarity or spectral dot-product algorithms. This skill enables confident compound identification without sharing proprietary data to public repositories.

## When to use

You have an experimental MS/MS spectrum (m/z and intensity pairs in mzML/mzXML format from DDA or targeted acquisition on Thermo, Waters, or Bruker instruments) and need to identify the unknown compound by comparing it against a reference database. Typical triggers: precursor m/z falls within a known drug or metabolite mass range, you possess a local spectral library with confidential metadata, or you want to search GNPS, MASSBANK, or DrugBANK for structural confirmation.

## When NOT to use

- Query spectrum is in negative ion mode but your library contains only positive ion mode spectra (e.g., the pre-compiled GNPS_MASSBANK_PROCESSED_POS_CONSENSUS database).
- You lack a precursor m/z value or the query spectrum fragments are insufficiently abundant/resolved; searches may return spurious high-scoring matches.
- Your experimental MS/MS data is from a non-standard acquisition mode or instrument format not convertible to mzML/mzXML (e.g., proprietary binary formats without conversion tools).

## Inputs

- Query MS/MS spectrum (two-column matrix: m/z and intensity pairs)
- Precursor m/z value
- Spectral library (local GNPS-style library file or connection to GNPS/MASSBANK/DrugBANK)
- Search parameters list (prec_mz, use_prec, polarity, method, min_frag_match, min_score, reaction_type)

## Outputs

- Ranked list of candidate library matches with cosine similarity scores
- Annotated metadata for top match(es): compound name, molecular formula, INCHI, INCHIKEY, library accession, cosine similarity score
- Mirror plot visualization comparing query and matched library spectra

## How to apply

Load your query spectrum as a two-column matrix (m/z and intensity). Set key search parameters: precursor m/z (typically enforced by setting use_prec=TRUE for classical compound annotation), polarity (Positive or Negative), similarity method (Cosine recommended), minimum fragment match count (e.g., 6 fragments), and minimum cosine similarity score threshold (e.g., 0.0–1.0 range, with >0.7 generally indicating confident matches). Query the selected library (local GNPS-style, GNPS, MASSBANK, or DrugBANK) using the library_query() function in MergeION. The algorithm computes cosine similarity between the query spectrum and all candidate library spectra, ranks matches by score, and filters by your threshold. Validate results by inspecting the top-ranked match's INCHIKEY, molecular formula, and compound name; use mirror plot visualization to confirm spectral peak correspondence.

## Related tools

- **MergeION2** (R package implementing spectral library search algorithms (cosine similarity, spectral dot-product) and providing library_query() function for compound annotation lookup) — https://github.com/daniellyz/MergeION2
- **GNPS** (Public spectral repository queried for compound annotation; can be searched directly or via local GNPS-style library merged with MassBank and DrugBANK data)
- **MASSBANK** (Public spectral database for small molecule MS/MS spectra; integrated into MergeION library search workflows)
- **DrugBANK** (Public database of drug structures and spectra; searchable via MergeION library lookup for pharmaceutical applications)
- **RChemMass** (R package for chemical structure visualization; used with library_visualizer() to display mirror plots comparing query and library spectra)

## Examples

```
download.file('https://zenodo.org/record/7057435/files/GNPS_MASSBANK_PROCESSED_POS_CONSENSUS1.RData?download=1', 'GNPS_MASSBANK_PROCESSED_POS_CONSENSUS1.RData'); load('GNPS_MASSBANK_PROCESSED_POS_CONSENSUS1.RData'); query.sp <- read.csv('example_cinnarizine.txt', header=F, sep='\t'); params <- list(prec_mz=369.232, use_prec=T, polarity='Positive', method='Cosine', min_frag_match=6, min_score=0); search_result <- library_query(input_library=library1c, query_spectrum=query.sp, params.query.sp=params)
```

## Evaluation signals

- Returned cosine similarity score is ≥0.7 (indicating confident match); top match INCHIKEY, molecular formula, and compound name are consistent with experimental context (e.g., known drug or metabolite in sample).
- Mirror plot visualization shows substantial peak overlap between query and library spectrum at fragment m/z values; major product ions align between spectra.
- Precursor m/z of top match differs from query by <5 ppm (typical MS mass accuracy); fragmentation pattern reproducibility across instrument platforms (if applicable).
- Search returned only one or few top-ranked candidates with well-separated cosine scores (e.g., top score 0.95, second 0.68), indicating unambiguous identification.
- Metadata consistency: compound name, INCHI, molecular formula, and chemical structure all point to same chemical entity; library accession is traceable to GNPS, MASSBANK, or DrugBANK.

## Limitations

- Library search accuracy depends on spectral library completeness and quality; confidential or rare compounds absent from GNPS/MASSBANK/DrugBANK will not be identified.
- Polarity mismatch: pre-compiled database (GNPS_MASSBANK_PROCESSED_POS_CONSENSUS) contains only positive ion mode ESI-MS/MS spectra; negative mode or other ionization methods require alternative libraries.
- Fragmentation pattern variability across instruments and acquisition parameters may reduce cosine similarity scores and increase false negatives, especially for compounds outside the library's training set.
- Isomeric compounds (same molecular formula, different structure) produce similar MS/MS spectra; cosine similarity alone cannot distinguish structural isomers—INCHI or additional orthogonal data required.
- No changelog available for MergeION; algorithm changes, library updates, or reproducibility across versions may not be tracked.

## Evidence

- [readme] Several library search algorithms are available, allowing users to search and annotate an unknown spectrum in their local database or public databases (i.e. drug structures in GNPS, MASSBANK and DrugBANK): "Several library search algorithms are available, allowing users to search and annotate an unknown spectrum in their local database or public databases (i.e. drug structures in GNPS, MASSBANK and"
- [intro] MergeION implements library search algorithms that enable users to search and annotate unknown spectra by matching against a local spectral library or public databases including GNPS, MASSBANK, and DrugBANK.: "Apply library search algorithm to compute similarity scores (e.g., cosine similarity or spectral dot-product) between query spectrum and candidate library spectra"
- [readme] The MS/MS spectrum should be read as well into the R environment as a two-column matrix. In this example, we know the query spectrum corresponds to Cinnarizine.: "The MS/MS spectrum should be read as well into the R environment as a two-column matrix"
- [readme] params.query.sp = list(prec_mz = 369.232, use_prec = T, polarity = "Positive", method = "Cosine", min_frag_match = 6, min_score = 0, reaction_type = "Metabolic"): "prec_mz = 369.232, use_prec = T, polarity = "Positive", method = "Cosine", min_frag_match = 6, min_score = 0"
- [readme] search_result = library_query(input_library = library1c, query_spectrum = query.sp, params.query.sp = params.query.sp): "search_result = library_query(input_library = library1c, query_spectrum = query.sp, params.query.sp = params.query.sp)"
- [readme] in this example only one, and the Cosine spectral similarity is very high at 0.95: "Cosine spectral similarity is very high at 0.95"
- [readme] We have pre-compiled a small molecule spectral database containing MS/MS spectra of 11,642 metabolites, natural products and drugs. The database combines public repositories such as GNPS, MassBank and reference spectra of in-house standards of approved drugs. Currently ESI-MS/MS spectra in our collection are all in positive ion mode.: "Currently ESI-MS/MS spectra in our collection are all in positive ion mode"
- [intro] It is compatible with mzML/mzXML format converted from Thermo, Water or Bruker data files, in either DDA (Data-driven acquisition) or targeted MS/MS-mode: "It is compatible with mzML/mzXML format converted from Thermo, Water or Bruker data files, in either DDA (Data-driven acquisition) or targeted MS/MS-mode"

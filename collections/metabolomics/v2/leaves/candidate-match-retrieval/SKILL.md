---
name: candidate-match-retrieval
description: Use when when you have a query MS/MS spectrum (m/z and intensity pairs)
  and need to find potential structural analogues or exact matches in a large spectral
  library. Apply this skill after preprocessing your spectra (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3767
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - MS2Query
  - MS2Deepscore
  - Spec2Vec
  - MZMine
  - RDKit
  techniques:
  - LC-MS
  license_tier: open
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Candidate Match Retrieval

## Summary

Retrieves a ranked set of library spectral candidates from a SQLite-backed spectral library for a given query MS/MS spectrum using pre-computed embeddings and spectral similarity scoring. This skill bridges rapid full-library comparison with intelligent re-ranking to surface both exact matches and structurally similar analogues.

## When to use

When you have a query MS/MS spectrum (m/z and intensity pairs) and need to find potential structural analogues or exact matches in a large spectral library. Apply this skill after preprocessing your spectra (e.g., via MZMine) and downloading or constructing a library with pre-computed MS2Deepscore embeddings. Use it when your research goal is to identify unknown compounds or validate putative identifications from mass spectrometry data.

## When NOT to use

- Input spectra have not been clustered or quality-filtered—MS2Query does not perform peak picking or peak clustering, so many redundant spectra per feature will slow processing and inflate the candidate list.
- Library spectra are not annotated with SMILES, InChI, or InChIKey metadata—these are required for library construction and molecular classification output.
- Your query spectrum is already known to be a structurally novel compound with no library analogues expected—the skill assumes some degree of structural similarity exists in the library.

## Inputs

- Query MS/MS spectrum (MGF, mzML, msp, json, mzXML, USI, or pickled matchms object)
- MS2Query library object (loaded from SQLite database with pre-computed embeddings)

## Outputs

- CSV results file with ranked candidate matches
- Columns: library identifiers, precursor m/z, precursor m/z difference, MS2Query model prediction score (0–1), MS2Deepscore, molecular structure annotations (SMILES, InChI), estimated molecular class

## How to apply

Load your query spectrum (MGF, mzML, msp, json, or pickled matchms object) and the library object containing SQLite spectral data and pre-computed MS2Deepscore embeddings. MS2Query first calculates MS2Deepscore similarity between the query spectrum and all library spectra without pre-filtering on precursor m/z. Select the top 2000 library spectra ranked by MS2Deepscore. A random forest model then re-ranks these candidates using five combined features (precursor mass tolerance, spectral feature overlap, and derived scores), producing a model prediction score between 0 and 1 for each candidate. Return the ranked candidate list sorted by MS2Query model prediction score; use a minimum threshold (e.g., > 0.7 for high-confidence matches, 0.6–0.7 for cautious analysis) to filter unreliable predictions based on your tolerance for false positives versus false negatives.

## Related tools

- **MS2Query** (Main tool that orchestrates full-library spectral comparison and re-ranking candidate matches using pre-computed embeddings and random forest scoring) — https://github.com/iomega/ms2query
- **MS2Deepscore** (Computes neural network-based spectral similarity embeddings used to retrieve top 2000 candidates before re-ranking)
- **Spec2Vec** (Provides spectral feature vectorization contributing to the five combined features used in re-ranking)
- **MZMine** (Recommended preprocessing tool for clustering and feature selection to reduce redundant MS/MS spectra and generate MGF input files) — https://mzmine.github.io/mzmine_documentation/index.html
- **RDKit** (Used to compute molecular structure annotations (SMILES, InChI, InChIKey) and estimated molecular classes for library spectra)

## Examples

```
ms2query --spectra ./query_spectra.mgf --library ./ms2query_library_files --ionmode positive
```

## Evaluation signals

- MS2Query model prediction score is between 0 and 1 for all returned candidates; candidates with score > 0.7 are designated high-confidence matches.
- Precursor m/z difference for exact matches is near zero (within instrument tolerance); large m/z differences correctly identify analogues.
- Returned candidate list is ordered by MS2Query prediction score in descending order; top rank is the best predicted match.
- For known reference standards in query spectra, the expected library entry appears in the top-ranked results with a model prediction score > 0.7.
- Results CSV contains all required columns (library_id, precursor_mz, ms2query_model_prediction, ms2deepscore, molecular_class annotations) with no missing values for ranked candidates.

## Limitations

- MS2Query does not perform peak picking or clustering of redundant spectra; high-redundancy input files will increase runtime significantly without improving match quality.
- Full-library comparison without precursor m/z pre-filtering can return structurally unrelated candidates if the query spectrum is very dissimilar to the library; in such cases, even top-ranked scores may be below confidence thresholds.
- The random forest re-ranking model was trained on GNPS library data from 2021-12-15 (positive mode) and other GNPS snapshots (negative mode); performance may degrade for compound classes or ionization conditions underrepresented in those training sets.
- No strict minimum score threshold is universally optimal; threshold selection depends on research goals (high recall vs. high precision), requiring manual curation and validation for novel or low-confidence predictions in the 0.6–0.7 range.
- Streamlit web application is no longer actively maintained, limiting interactive exploration for users who prefer graphical interfaces.

## Evidence

- [readme] MS2Query uses MS2 mass spectral data to find the best match in a library and is able to search for both analogues and exact matches.: "MS2Query uses MS2 mass spectral data to find the best match in a library and is able to search for both analogues and exact matches."
- [readme] The workflow for running MS2Query first uses MS2Deepscore to calculate spectral similarity scores between all library spectra and a query spectrum. By using pre-computed MS2Deepscore embeddings for library spectra, this full-library comparison can be computed very quickly. The top 2000 spectra with the highest MS2Deepscore are selected.: "The workflow for running MS2Query first uses MS2Deepscore to calculate spectral similarity scores between all library spectra and a query spectrum. By using pre-computed MS2Deepscore embeddings for"
- [readme] MS2Query optimizes re-ranking the best analogue or exact match at the top by using a random forest that combines 5 features. The random forest predicts a score between 0 and 1 between each library and query spectrum and the highest scoring library match is selected.: "MS2Query optimizes re-ranking the best analogue or exact match at the top by using a random forest that combines 5 features. The random forest predicts a score between 0 and 1 between each library"
- [readme] This column contains a score, which indicates the likelihood that the found match is a good match. This score ranges between 0 and 1, the closer this score is to 1 the more likely that it is a good match/analogue.: "This column contains a score, which indicates the likelihood that the found match is a good match. This score ranges between 0 and 1, the closer this score is to 1 the more likely that it is a good"
- [readme] To give a general indication, a score > 0,7 has many good analogues and exact matches. In the range of 0.6-0.7, the results can still be useful, but should be analysed with more caution and results below 0.6 can often best be discarded.: "To give a general indication, a score > 0,7 has many good analogues and exact matches. In the range of 0.6-0.7, the results can still be useful, but should be analysed with more caution and results"
- [readme] MS2Query does not need two different workflows for searching for analogues and searching for exact matches, it automatically selects the most likely library spectra. If it is important to separate potential exact matches from potential analogues for your research question, the column with the precursor mz difference can be used to separate these results, since exact matches should have no precursor mz difference.: "MS2Query does not need two different workflows for searching for analogues and searching for exact matches, it automatically selects the most likely library spectra. If it is important to separate"
- [readme] MS2Query does not do any peak picking or clustering of similar MS2 spectra. If your files contain many MS2 spectra per feature it is advised to first reduce the number of MS2 spectra by clustering or feature selection.: "MS2Query does not do any peak picking or clustering of similar MS2 spectra. If your files contain many MS2 spectra per feature it is advised to first reduce the number of MS2 spectra by clustering or"
- [readme] Accepted formats are: "mzML", "json", "mgf", "msp", "mzxml", "usi" or a pickled matchms object: "Accepted formats are: "mzML", "json", "mgf", "msp", "mzxml", "usi" or a pickled matchms object"

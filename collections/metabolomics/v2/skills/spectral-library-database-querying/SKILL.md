---
name: spectral-library-database-querying
description: Use when you have one or more MS/MS query spectra (in mzML, mgf, msp,
  mzxml, json, or pickled matchms format) and a pre-built spectral library stored
  in SQLite with precomputed MS2Deepscore embeddings.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3767
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_3520
  tools:
  - MS2Query
  - MS2Deepscore
  - matchms
  - SQLite
  - MZMine
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

# spectral-library-database-querying

## Summary

Query a SQLite-backed spectral library to retrieve candidate MS/MS matches for an unknown query spectrum, ranked by precursor mass tolerance and spectral similarity. This skill bridges raw query spectra and ranked library hits that can be rescored by machine learning models.

## When to use

You have one or more MS/MS query spectra (in mzML, mgf, msp, mzxml, json, or pickled matchms format) and a pre-built spectral library stored in SQLite with precomputed MS2Deepscore embeddings. Use this skill when you need to retrieve the top candidate library matches without restricting by precursor m/z window first, so that both exact and analogue matches can be considered.

## When NOT to use

- Input spectra have not been preprocessed or clustered; MS2Query does not perform peak picking or feature clustering, so reduce redundant MS/MS spectra per feature first (e.g., via MZMine FBMN).
- Library is not stored in SQLite format or lacks precomputed MS2Deepscore embeddings; library creation/training is a separate workflow.
- You require only exact-mass matches with strict precursor tolerance; this skill retrieves analogues without precursor preselection, so the candidate list may include off-mass analogs.

## Inputs

- MS/MS query spectrum (mzML, mgf, msp, mzxml, json, or pickled matchms object)
- SQLite spectral library database (with precomputed MS2Deepscore embeddings)
- Library metadata (precursor masses, identifiers, inchi/smiles annotations)

## Outputs

- Ranked candidate list (CSV or object) with top ≤2000 library matches
- Candidate match records: library_id, precursor_mz, precursor_mz_difference, ms2deepscore_score
- Metadata columns: compound name, inchi, smiles, molecular class estimates (optional)

## How to apply

Load the query spectrum as m/z and intensity pairs in standard MS/MS format. Query the SQLite library database using MS2Deepscore similarity to retrieve the top 2000 spectra candidates ranked by spectral similarity, without preselecting on precursor m/z. For each candidate, calculate the precursor mass difference and spectral feature overlap. Return the ranked candidate list with library identifiers, precursor masses, MS2Deepscore scores, and precursor mass differences. The top candidates (typically 2000 by default) then become inputs for re-ranking by a machine-learning model that combines precursor mass tolerance, spectral similarity, and structural features.

## Related tools

- **MS2Query** (Complete framework for MSMS library matching; orchestrates SQLite querying, MS2Deepscore ranking, and random forest re-ranking for analogue and exact match search) — https://github.com/iomega/ms2query
- **MS2Deepscore** (Neural network model that computes spectral similarity embeddings; precomputed embeddings stored in SQLite for fast candidate retrieval)
- **matchms** (Python library for reading, writing, and manipulating MS/MS spectra in standard formats (mgf, msp, mzML, etc.))
- **SQLite** (Persistent storage backend for spectral library data, precomputed embeddings, and candidate indices)
- **MZMine** (Preprocessing tool for peak picking, feature clustering, and MS/MS spectrum reduction before MS2Query querying) — https://mzmine.github.io/mzmine_documentation/index.html

## Examples

```
from ms2query.ms2library import create_library_object_from_one_dir; ms2library = create_library_object_from_one_dir('./ms2query_library_files'); from ms2query.run_ms2query import run_complete_folder; run_complete_folder(ms2library, './query_spectra')
```

## Evaluation signals

- Number of candidates returned ≤ 2000 and > 0 (should be a full set unless library is small); verify query spectrum was successfully loaded and parsed into m/z–intensity pairs.
- All returned candidates have valid precursor_mz values and library identifiers; no null or malformed rows in output CSV.
- Precursor mass differences are correctly calculated (query_precursor_mz − library_precursor_mz); check for expected range (e.g., ±100 Da for typical spectra).
- Candidates are sorted descending by MS2Deepscore similarity score; spot-check that top candidate has highest score.
- Metadata columns (inchi, smiles, compound names) are present and non-empty for annotated library entries; missing values are acceptable for non-annotated spectra.

## Limitations

- No internal peak picking or MS/MS clustering; input spectra should be preprocessed upstream (e.g., via MZMine) to reduce redundant spectra per feature.
- Precursor m/z preselection is not performed, so candidate list may include off-mass analogues; filtering by precursor mass tolerance must be applied downstream if exact matches only are desired.
- Query spectrum must match the ion mode (positive or negative) of the library; mismatched ion modes will yield low-quality matches but are not explicitly blocked.
- Performance depends on SQLite index quality and precomputed embedding availability; libraries without MS2Deepscore embeddings will be much slower to query.
- Streamlit web app for interactive querying has been deprecated; command-line and Python API are the supported interfaces.

## Evidence

- [other] Load spectral library data from SQLite database according to PR #56 schema: "Load spectral library data from SQLite database according to PR #56 schema"
- [other] Parse input query spectra in standard MS/MS format (m/z and intensity pairs): "Parse input query spectra in standard MS/MS format (m/z and intensity pairs)"
- [readme] The top 2000 spectra with the highest MS2Deepscore are selected. In contrast to other analogue search methods, no preselection on precursor m/z is performed.: "The top 2000 spectra with the highest MS2Deepscore are selected. In contrast to other analogue search methods, no preselection on precursor m/z is performed."
- [other] Rank candidates by precursor mass tolerance and spectral feature overlap: "Rank candidates by precursor mass tolerance and spectral feature overlap"
- [readme] MS2Query does not do any peak picking or clustering of similar MS2 spectra. If your files contain many MS2 spectra per feature it is advised to first reduce the number of MS2 spectra by clustering or feature selection.: "MS2Query does not do any peak picking or clustering of similar MS2 spectra. If your files contain many MS2 spectra per feature it is advised to first reduce the number of MS2 spectra by clustering or"
- [readme] Accepted formats are: 'mzML', 'json', 'mgf', 'msp', 'mzxml', 'usi' or a pickled matchms object: "Accepted formats are: "mzML", "json", "mgf", "msp", "mzxml", "usi" or a pickled matchms object"

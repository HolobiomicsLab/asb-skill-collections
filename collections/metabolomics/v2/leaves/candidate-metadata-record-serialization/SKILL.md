---
name: candidate-metadata-record-serialization
description: Use when after computing InChIKey and neighbourhood scores for library
  match candidates, you need to write results to a persistent format (CSV, JSON, or
  database) for storage, sharing, and interpretation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0335
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - MS2Query
  - Python
  - matchms
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

# candidate-metadata-record-serialization

## Summary

Serialize scored MS/MS candidate matches into structured output records with standardized fields (candidate ID, InChIKey score, neighbourhood score, precursor m/z, molecular class annotations) and metadata, suitable for downstream filtering and interpretation. This skill ensures reproducible, machine-readable results that track match confidence and chemical properties.

## When to use

After computing InChIKey and neighbourhood scores for library match candidates, you need to write results to a persistent format (CSV, JSON, or database) for storage, sharing, and interpretation. Use this skill when you have a set of ranked candidate matches and need to document their quality metrics, structural annotations, and metadata in a format that supports threshold-based filtering (e.g., ms2query_model_prediction > 0.7) and molecular class stratification.

## When NOT to use

- Input spectra have not yet been scored by the MS2Query random forest model—serialize only after scoring is complete.
- You need per-peak or per-fragment annotations—this skill outputs spectrum-level matches only, not fragment-level metadata.
- Results must be stored in a binary machine-learning model format (e.g., .pkl) rather than human-readable CSV—use pickle serialization separately.

## Inputs

- Scored candidate match objects (from MS2Query scoring module)
- InChIKey annotations and structural metadata from library spectra
- Random forest model prediction scores (0–1 per candidate)
- Neighbourhood score metrics from spectral feature space density computation
- Query spectrum IDs and precursor m/z values
- Optional: retention time and feature ID metadata

## Outputs

- CSV results file with one row per query spectrum and its top-ranked match
- Standardized columns: query_spectrum_id, library_match_id, inchikey_score, neighbourhood_score, ms2query_model_prediction, precursor_mz_difference, estimated_molecular_class
- Additional metadata columns (retention_time, feature_id) if requested
- Results directory within the same directory as input spectra

## How to apply

Collect all candidate match records produced by the scoring step, including match identifiers, InChIKey annotations, neighbourhood density metrics, spectral similarity scores, and precursor m/z differences. Assemble each record with standardized fields: query spectrum ID, library spectrum ID, InChIKey score, neighbourhood score, ms2query_model_prediction (random forest score 0–1), precursor m/z difference, and estimated molecular classes inferred from the matched library molecule structure. Write records to CSV (recommended for interpretability) or pickled matchms object format. Include metadata columns such as retention time and feature ID if requested. Validate that all scores fall within expected ranges (0–1 for normalized scores) and that no required fields are null. Document the threshold recommendation (e.g., score > 0.7 for high-confidence hits, 0.6–0.7 for cautious interpretation, < 0.6 for discard) in the results header or README so downstream users know how to filter.

## Related tools

- **MS2Query** (Orchestrates the entire workflow including scoring and result serialization; provides the random forest model and expects results in CSV format with standardized column names.) — https://github.com/iomega/ms2query
- **Python** (Primary implementation language for writing serialization code, CSV/JSON output, and validation via pytest or setuptools.)
- **matchms** (Data structure for spectrum objects; results can optionally be exported as pickled matchms objects or referenced within CSV metadata.)

## Examples

```
# After MS2Query scoring is complete, results are automatically written:
ms2query --spectra ./query_spectra --library ./ms2query_library_files --ionmode positive
# Output: ./query_spectra/results/ms2query_results.csv with columns: query_spectrum_id, library_match_id, ms2query_model_prediction, inchikey_score, neighbourhood_score, precursor_mz_difference, estimated_molecular_class
```

## Evaluation signals

- All output CSV rows have non-null values in required columns (query_spectrum_id, library_match_id, ms2query_model_prediction, inchikey_score, neighbourhood_score).
- Score columns contain only numeric values in range [0, 1]; precursor_mz_difference contains numeric values (can be negative or positive).
- Row count matches the number of input query spectra (one best match per spectrum).
- Molecular class columns are consistent with RDKit structure predictions from the matched library molecule SMILES/InChI.
- Unit tests via `python setup.py test` or pytest validate that output record structure conforms to schema and that no fields are truncated or corrupted.

## Limitations

- MS2Query produces one best match per query spectrum regardless of match quality; a low ms2query_model_prediction score does not prevent a record from being output. Downstream filtering by threshold (e.g., > 0.7) is essential and user-dependent on research goals (high recall vs. high precision).
- Precursor m/z difference is used to distinguish analogues from exact matches, but no automatic classification is provided; users must manually inspect or filter the precursor_mz_difference column.
- Estimated molecular classes rely on accurate SMILES/InChI annotations in the library; missing or incorrect structures result in null or misleading class predictions.
- No preselection on precursor m/z is performed during library matching, so results may include matches with large m/z differences that users must filter manually.
- Retention time and feature ID metadata are optional and not always available; the results will not include these columns unless explicitly requested and provided in input spectra metadata.

## Evidence

- [other] Combine both scores into a single candidate record with standardized fields (candidate ID, InChIKey score, neighbourhood score).: "Combine both scores into a single candidate record with standardized fields (candidate ID, InChIKey score, neighbourhood score)"
- [readme] The results generated by MS2Query, are stored as csv files in a results directory within the same directory as your query spectra.: "The results generated by MS2Query, are stored as csv files in a results directory within the same directory as your query spectra"
- [readme] For each of your input spectra MS2Query predicts a library match. It is important to check the ms2query_model_prediction column. This column contains a score, which indicates the likelihood that the found match is a good match.: "For each of your input spectra MS2Query predicts a library match. It is important to check the ms2query_model_prediction column. This column contains a score, which indicates the likelihood that the"
- [readme] This score ranges between 0 and 1, the closer this score is to 1 the more likely that it is a good match/analogue. It is important to use this score to select only the reliable hits: "This score ranges between 0 and 1, the closer this score is to 1 the more likely that it is a good match/analogue. It is important to use this score to select only the reliable hits"
- [readme] To give a general indication, a score > 0,7 has many good analogues and exact matches. In the range of 0.6-0.7, the results can still be useful, but should be analysed with more caution and results below 0.6 can often best be discarded.: "To give a general indication, a score > 0,7 has many good analogues and exact matches. In the range of 0.6-0.7, the results can still be useful, but should be analysed with more caution and results"
- [readme] The columns completely to the right are estimated molecular classes based on the molecular structure of the predicted library molecule, these columns can be used to get a quick overview of the kind of compounds that were found.: "The columns completely to the right are estimated molecular classes based on the molecular structure of the predicted library molecule, these columns can be used to get a quick overview of the kind"
- [other] Validate output record structure and score ranges using unit tests via Python pytest or setuptools.: "Validate output record structure and score ranges using unit tests via Python pytest or setuptools"

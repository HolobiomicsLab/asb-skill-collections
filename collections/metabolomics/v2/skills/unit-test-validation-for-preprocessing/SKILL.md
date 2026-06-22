---
name: unit-test-validation-for-preprocessing
description: Use when after implementing or modifying basic peak filtering operations (e.g., low-intensity peak removal, intensity normalization) on mass spectrometry spectral data in supported formats (mzML, mzXML, msp, MGF, JSON).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Python
  - pytest
  - matchms
derived_from:
- doi: 10.1186/s13321-024-00878-1
  title: matchms
evidence_spans:
- Matchms is a versatile open-source Python package developed for importing, processing, cleaning, and comparing mass spectrometry data
- make sure the existing tests still work by running ``pytest``
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_matchms_2_cq
    doi: 10.1186/s13321-024-00878-1
    title: matchms
  dedup_kept_from: coll_matchms_2_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1186/s13321-024-00878-1
  all_source_dois:
  - 10.1186/s13321-024-00878-1
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# unit-test-validation-for-preprocessing

## Summary

Validate mass spectrometry data preprocessing operations (peak filtering, normalization, metadata cleaning) by running automated unit tests to confirm that filtering logic preserves data integrity and produces expected output. This ensures reproducible, correct transformation of raw spectral data into cleaned peak lists.

## When to use

After implementing or modifying basic peak filtering operations (e.g., low-intensity peak removal, intensity normalization) on mass spectrometry spectral data in supported formats (mzML, mzXML, msp, MGF, JSON). Apply this skill before exporting pre-processed spectral data to confirm that filtering logic is correct and does not introduce unintended artifacts.

## When NOT to use

- When preprocessing code is not yet implemented; write or modify the code first, then test.
- When input spectra are already validated and in final form; this skill targets pre-processed data quality assurance during pipeline development.
- When only performing exploratory data analysis without modifying preprocessing logic; unit tests are unnecessary for read-only analysis.

## Inputs

- Raw mass spectrometry spectral data (mzML, mzXML, msp, MGF, or JSON format)
- Preprocessing code implementing peak filtering and normalization
- Existing pytest test suite

## Outputs

- Pytest test results (pass/fail status for each test case)
- Coverage report indicating which filtering branches are exercised
- Validated preprocessing code ready for export or integration

## How to apply

Write or extend pytest test cases that validate the output of each peak filtering step applied to representative mass spectra. Tests should verify: (1) low-intensity or noise peaks are removed according to configured thresholds; (2) peak intensity normalization produces values in the expected range (e.g., 0–1 or 0–100); (3) metadata fields remain intact after peak list modification; (4) filtered spectra retain correct m/z and intensity correspondence. Run the full test suite using `pytest` to ensure both new filtering logic and existing preprocessing functionality pass. Verify that test output reports no failures and coverage includes all major filtering branches.

## Related tools

- **pytest** (Execute automated unit tests to validate peak filtering and preprocessing logic correctness) — https://github.com/matchms/matchms
- **matchms** (Provides peak filtering operations and test infrastructure for mass spectrometry preprocessing validation) — https://github.com/matchms/matchms
- **Python** (Language for implementing test cases and preprocessing functions)

## Examples

```
pytest tests/ -v --cov=matchms.filtering
```

## Evaluation signals

- All pytest test cases pass without failures or errors; `pytest` exit code is 0.
- Test coverage report shows ≥80–90% coverage of peak filtering functions, including branches for low-intensity removal and normalization.
- Peak intensity values in filtered spectra fall within expected ranges (e.g., 0–1 after normalization); m/z arrays remain monotonic and aligned with intensity arrays.
- Metadata fields (e.g., precursor_mz, compound name) are preserved unchanged after peak filtering; no unintended loss of spectral annotations.
- Regression tests confirm that existing filtering behavior is not disrupted by new code; previously passing tests continue to pass.

## Limitations

- Unit tests validate logic correctness but do not assess biological or chemical validity of filtered spectra; domain-specific review is still necessary.
- Test suite coverage depends on quality and comprehensiveness of test cases; edge cases (e.g., spectra with very few peaks, extreme m/z ranges) may not be covered by default tests.
- Pytest does not detect performance regressions (e.g., filtering becoming slower); additional profiling tools are needed to monitor runtime.
- Tests validate matchms preprocessing in isolation; integration testing with downstream similarity comparisons or spectral library matching requires separate workflow validation.

## Evidence

- [other] Validate filtered peak lists pass existing pytest test suite to confirm filtering logic is correct: "Validate filtered peak lists pass existing pytest test suite to confirm filtering logic is correct."
- [other] make sure the existing tests still work by running ``pytest``: "make sure the existing tests still work by running ``pytest``"
- [other] Apply basic peak filtering operations including peak removal (e.g., low-intensity or noise peaks) and peak intensity normalization to ensure data accuracy and integrity: "Apply basic peak filtering operations including peak removal (e.g., low-intensity or noise peaks) and peak intensity normalization to ensure data accuracy and integrity."
- [intro] Matchms offers an array of tools for metadata cleaning and validation, alongside basic peak filtering, to ensure data accuracy and integrity: "Matchms offers an array of tools for metadata cleaning and validation, alongside basic peak filtering, to ensure data accuracy and integrity"

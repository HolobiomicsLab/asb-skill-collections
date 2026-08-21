---
name: precursor-m-z-based-filtering
description: 'Use when you have an unknown MS/MS query spectrum with a known or measured
  precursor m/z value and need to search a spectral library (local or public: GNPS,
  MASSBANK, DrugBANK) to annotate the compound.'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - MASSBANK
  - DrugBANK
  - meRgeION2
  - MergeION2
  - GNPS
  techniques:
  - LC-MS
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.analchem.2c04343
  title: MeRgeION
evidence_spans:
- search and annotate an unknown spectrum in their local database or public databases
  (i.e. drug structures in GNPS, MASSBANK and DrugBANK)
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

# precursor-m-z-based-filtering

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Filter and match MS/MS spectra by precursor mass-to-charge ratio (m/z) to reduce the search space during spectral library lookup and improve annotation specificity. This skill is essential when matching unknown query spectra against large spectral libraries or databases where exact precursor m/z alignment is a prerequisite for confident compound identification.

## When to use

Apply this skill when you have an unknown MS/MS query spectrum with a known or measured precursor m/z value and need to search a spectral library (local or public: GNPS, MASSBANK, DrugBANK) to annotate the compound. Use precursor m/z filtering as a gating criterion before computing spectral similarity scores, especially when library size is large or when false-positive annotation risk is high due to similar fragmentation patterns across unrelated compounds.

## When NOT to use

- Precursor m/z is unknown or unavailable from the query spectrum (e.g., for MS1 survey scans without MS/MS fragmentation data).
- You are performing analog or related-compound searches where metabolic derivatives or adducts with different precursor m/z are expected and desirable matches.
- Input is already a pre-filtered, low-complexity spectral subset (e.g., a single-compound reference standard) where m/z-based gating adds no discriminative value.

## Inputs

- query MS/MS spectrum (two-column matrix: m/z and intensity pairs)
- precursor m/z value (float, e.g., 369.232)
- spectral library (GNPS-style RData object, local mzML/mzXML, or public database reference)
- m/z tolerance window (numeric, default in MergeION is implicit)

## Outputs

- filtered candidate spectra list (subset of library matching precursor m/z ± tolerance)
- ranked match results with cosine similarity scores (or spectral dot-product)
- annotated hits with compound metadata (name, molecular formula, INCHI, accession ID)

## How to apply

Extract the precursor m/z value from your query spectrum (e.g., 369.232 for Cinnarizine in the MergeION quick-start example). Set the parameter use_prec = TRUE to enforce precursor mass matching. Define an appropriate m/z tolerance window (MergeION default behavior applies this internally during library_query). The algorithm will pre-filter library candidate spectra to retain only those whose precursor m/z falls within the tolerance window of your query precursor m/z before computing cosine similarity or other spectral dot-product metrics. This step dramatically reduces computational cost and noise by eliminating chemically implausible matches. Rank filtered matches by similarity score and apply a minimum similarity threshold (e.g., min_score = 0.7) to identify high-confidence annotations.

## Related tools

- **MergeION2** (implements library_query() function with use_prec parameter to enforce precursor m/z filtering during spectral library search) — https://github.com/daniellyz/MergeION2
- **GNPS** (public spectral library source for precursor m/z-based matching)
- **MASSBANK** (public spectral library source for precursor m/z-based matching)
- **DrugBANK** (public spectral library source for precursor m/z-based matching of drug compounds)

## Examples

```
params.query.sp = list(prec_mz = 369.232, use_prec = T, polarity = "Positive", method = "Cosine", min_frag_match = 6, min_score = 0); search_result = library_query(input_library = library1c, query_spectrum = query.sp, params.query.sp = params.query.sp)
```

## Evaluation signals

- Verify that all returned candidates have precursor m/z within the specified tolerance window of the query precursor m/z (e.g., ±0.01 Da or ±5 ppm).
- Confirm that the top-ranked match (highest cosine similarity) corresponds to the known or expected compound when validating on standards (e.g., Cinnarizine at cosine ≥ 0.95).
- Inspect the mirror plot visualization between query and matched library spectrum to confirm fragmentation pattern alignment, not just precursor m/z agreement.
- Validate that use_prec = TRUE reduces false-positive matches compared to use_prec = FALSE in benchmark datasets.
- Check that the number of filtered candidates is substantially smaller than the full library size, confirming that precursor m/z filtering successfully reduced search space.

## Limitations

- Precursor m/z filtering may fail or produce no hits if the query precursor m/z is miscalibrated, contains systematic instrument error, or is not present in the target library database.
- ESI-MS/MS spectra in MergeION's pre-compiled library are currently limited to positive ion mode only; negative ion mode queries will not match.
- The method assumes precursor m/z precision and stability; highly variable precursor m/z (e.g., due to poor mass calibration in low-resolution instruments) may yield false negatives if tolerance is set too tight.
- Precursor m/z alone cannot distinguish isobars (e.g., isomeric compounds with identical precursor mass); spectral similarity scoring is necessary as a second-stage filter.

## Evidence

- [readme] Parameters to check: prec_mz (precursor mass) and use_prec (forces precursor mass match): "Only important parameters to check are the _prec_mz_, which indicates the precursor mass, and _use_prec_, which forces precursor mass match in the search output by setting to TRUE"
- [intro] Library search algorithms compute similarity between query and library spectra: "Apply library search algorithm to compute similarity scores (e.g., cosine similarity or spectral dot-product) between query spectrum and candidate library spectra"
- [readme] Precursor m/z is a required input for spectral library lookup: "query.sp = read.csv(...); params.query.sp = list(prec_mz = 369.232, use_prec = T, ...)"
- [intro] Ranking and filtering matched spectra by similarity threshold: "Rank and filter matched spectra by similarity threshold to identify best-matching library entries"
- [readme] High-confidence match example with cosine similarity score: "the Cosine spectral similarity is very high at 0.95"

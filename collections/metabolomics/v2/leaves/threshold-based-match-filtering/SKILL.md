---
name: threshold-based-match-filtering
description: Use when after calculating similarity metrics (e.g. cosine similarity
  or spectral correlation) between query peak networks and a simulated INADEQUATE
  database, when you need to distinguish true metabolite matches from spurious or
  low-confidence assignments and generate a curated list of identified.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0602
  tools:
  - PyINETA
  - Python
  license_tier: open
derived_from:
- doi: 10.1021/acs.analchem.4c03966
  title: PyINETA
evidence_spans:
- This is the documentation for the PyINETA package version 2.0.0.
- '.. automodule:: pyineta.finding :members:'
- pyINETA is a Python package
- python run_pyineta.py <options>
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_pyineta_cq
    doi: 10.1021/acs.analchem.4c03966
    title: PyINETA
  dedup_kept_from: coll_pyineta_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.4c03966
  all_source_dois:
  - 10.1021/acs.analchem.4c03966
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# threshold-based-match-filtering

## Summary

Filter metabolite matches from spectral database searches by applying a similarity threshold to retain only high-confidence assignments. This skill ensures that only metabolites with sufficiently strong spectral correlation to query peak networks are reported, reducing false positives in metabolite identification.

## When to use

After calculating similarity metrics (e.g. cosine similarity or spectral correlation) between query peak networks and a simulated INADEQUATE database, when you need to distinguish true metabolite matches from spurious or low-confidence assignments and generate a curated list of identified metabolites with reliable match scores.

## When NOT to use

- When no similarity metric has yet been computed between query and database spectra—filtering requires pre-calculated scores.
- When the goal is exploratory discovery of all possible matches regardless of confidence; thresholding discards lower-scoring candidates that may be biologically relevant in some contexts.
- When the query spectral data have not been pre-processed (shifted, picked, and clustered into peak networks); filtering assumes clean, validated input peak networks.

## Inputs

- Peak network clusters (from upstream Clustering module)
- Simulated INADEQUATE metabolite database with reference spectral signatures
- Calculated similarity scores (cosine similarity or spectral correlation values) between each query peak network and database metabolites

## Outputs

- Filtered metabolite match table
- Linked peak network identifiers to assigned metabolite names
- High-confidence match scores for retained assignments

## How to apply

Calculate similarity metrics between each query peak network cluster and all reference metabolite signatures in the simulated INADEQUATE database. Define a similarity threshold appropriate to your confidence requirements and spectral data quality (the article and README do not specify a concrete threshold value). Filter the full match set to retain only those peak network–metabolite pairs exceeding this threshold. This filtering step reduces false positive identifications and produces a high-confidence metabolite assignment table. The filtered output links peak network identifiers, assigned metabolite names, and match scores, which can then be used for downstream interpretation or statistical validation.

## Related tools

- **PyINETA** (Python package that implements the complete matching and filtering workflow, including similarity calculation and threshold-based filtering of peak network–metabolite pairs) — https://github.com/edisonomics/PyINETA
- **Python** (Language in which PyINETA and similarity metric computations (cosine similarity, spectral correlation) are implemented)

## Examples

```
python <path_to_pyineta_repo>/run_pyineta.py -c config.ini -s match -o output_dir
```

## Evaluation signals

- Verify that all retained matches have similarity scores ≥ the specified threshold and all discarded matches are below it (threshold consistency check).
- Check that the output table contains only peak networks from the input cluster set and only metabolite names present in the reference database (referential integrity).
- Confirm that match scores in the filtered table are numeric, non-null, and span a reasonable range (e.g. 0–1 for normalized metrics) and are monotonically ordered if sorting is applied.
- Validate that the number of retained matches per peak network is reasonable (e.g. typically 0–5 metabolites, or domain-specific expectations) and that no peak network appears with duplicate metabolite assignments after filtering.
- Cross-check a sample of filtered assignments by manual inspection or independent spectral comparison to ensure retained matches correspond to visually plausible peak network–metabolite alignments.

## Limitations

- The article and README do not specify a recommended similarity threshold value; practitioners must determine this empirically based on their spectral quality, database composition, and acceptable false-positive rate.
- Threshold-based filtering is sensitive to the quality of the input similarity metric; poor peak picking, inadequate peak clustering, or weak database coverage will degrade match quality before filtering is applied.
- The choice of similarity metric (cosine similarity vs. spectral correlation vs. other measures) is not elaborated in the article; different metrics may produce different threshold-dependent results.
- No changelog or version-specific performance notes are provided, limiting guidance on how filtering behavior may vary across PyINETA versions.

## Evidence

- [other] Calculate similarity metrics (e.g., cosine similarity or spectral correlation) between each query peak network and database metabolite signatures.: "Calculate similarity metrics (e.g., cosine similarity or spectral correlation) between each query peak network and database metabolite signatures."
- [other] Filter matches using a similarity threshold to retain high-confidence metabolite assignments.: "Filter matches using a similarity threshold to retain high-confidence metabolite assignments."
- [other] Generate a matched metabolite output table linking peak network identifiers, assigned metabolite names, and match scores using the pyINETA Matching module.: "Generate a matched metabolite output table linking peak network identifiers, assigned metabolite names, and match scores using the pyINETA Matching module."
- [readme] pyINETA matches identified peak networks to a simulated INADEQUATE database of metabolites to identify metabolites present in the query INADEQUATE spectra: "matches to a simulated INADEQUATE database of metabolites to identify metabolites present in the query INADEQUATE spectra"
- [methods] Matching
--------
.. automodule:: pyineta.matching: "Matching
--------
.. automodule:: pyineta.matching"

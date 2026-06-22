---
name: spectral-similarity-metric-computation
description: Use when after clustering peak networks from INADEQUATE spectra and before filtering matches to retain high-confidence metabolite assignments.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3803
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0769
  tools:
  - PyINETA
  - Python
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
  - build: coll_iceberg_cq
    doi: 10.1038/s42256-024-00816-8
    title: ICEBERG
  - build: coll_pyineta_cq
    doi: 10.1021/acs.analchem.4c03966
    title: PyINETA
  dedup_kept_from: coll_pyineta_cq
schema_version: 0.2.0
---

# spectral-similarity-metric-computation

## Summary

Compute similarity metrics (e.g., cosine similarity or spectral correlation) between query INADEQUATE peak networks and simulated metabolite database signatures to rank and filter metabolite matches. This skill enables confidence-weighted matching of experimentally observed spectral patterns to reference metabolite libraries.

## When to use

Apply this skill after clustering peak networks from INADEQUATE spectra and before filtering matches to retain high-confidence metabolite assignments. Use when you have both (1) query peak network clusters extracted from experimental spectra and (2) a simulated reference INADEQUATE database of known metabolite signatures, and you need to quantify which database metabolites best match each observed network.

## When NOT to use

- Peak networks have not yet been clustered or are not available in a format compatible with the database schema.
- The simulated reference database lacks adequate coverage of metabolites expected in the sample, or database signatures have not been generated from consistent acquisition/processing parameters.
- Raw or unfiltered peaks are being matched directly without prior network clustering; apply the Clustering step first.

## Inputs

- Peak network clusters (from pyINETA Clustering module output)
- Simulated INADEQUATE metabolite database (containing reference spectral signatures)

## Outputs

- Matched metabolite output table (linking peak network identifiers, assigned metabolite names, and match scores)
- High-confidence metabolite assignment set (post-threshold filtering)

## How to apply

Load peak network clusters from the upstream Clustering module output and the simulated INADEQUATE metabolite database containing reference spectral signatures. Calculate similarity metrics—such as cosine similarity or spectral correlation—between each query peak network and all database metabolite signatures. Apply a similarity threshold to filter matches and retain only high-confidence metabolite assignments. Output a matched metabolite table linking peak network identifiers, assigned metabolite names, and match scores. The threshold and metric choice should be calibrated based on the spectral resolution and database comprehensiveness; thresholds that are too lenient introduce false positives, while overly stringent thresholds may miss valid metabolites.

## Related tools

- **PyINETA** (Provides the Matching module (pyineta.matching) that implements spectral similarity metric calculation and metabolite assignment workflow) — https://github.com/edisonomics/PyINETA
- **Python** (Runtime environment for executing PyINETA matching functions and similarity calculations)

## Examples

```
python <path_to_pyineta_repo>/run_pyineta.py -c config.ini -s match -o output_dir
```

## Evaluation signals

- Match scores are numeric and bounded (e.g., 0–1 for cosine similarity); verify no missing, infinite, or out-of-range values.
- Every peak network identifier in the query set has at least one match record in the output table (or is explicitly marked as unmatched if no threshold-passing matches exist).
- High-scoring matches (above threshold) correspond to metabolites chemically plausible given the experimental context; low-scoring matches (below threshold) are correctly excluded.
- The number of retained metabolite assignments is consistent with sample complexity and database size; unexpected over- or under-matching suggests threshold miscalibration.
- Duplicate peak-to-metabolite assignments are absent; each peak network is matched to a unique metabolite (or a ranked list if multi-match output is permitted).

## Limitations

- Similarity metrics are sensitive to the quality and comprehensiveness of the simulated reference database; sparse or poorly-representative database signatures reduce matching reliability.
- The choice of metric (cosine similarity vs. spectral correlation) and threshold value are not automatically optimized by the tool; users must validate empirically or use domain knowledge to set appropriate parameters.
- INADEQUATE spectra acquired under different conditions (pulse sequences, field strength, sample preparation) may have incompatible reference databases, leading to poor or spurious matches.
- No changelog found in the repository; version compatibility and changes to matching algorithms across releases are not documented.

## Evidence

- [other] Calculate similarity metrics (e.g., cosine similarity or spectral correlation) between each query peak network and database metabolite signatures.: "Calculate similarity metrics (e.g., cosine similarity or spectral correlation) between each query peak network and database metabolite signatures."
- [other] Filter matches using a similarity threshold to retain high-confidence metabolite assignments.: "Filter matches using a similarity threshold to retain high-confidence metabolite assignments."
- [other] Generate a matched metabolite output table linking peak network identifiers, assigned metabolite names, and match scores using the pyINETA Matching module.: "Generate a matched metabolite output table linking peak network identifiers, assigned metabolite names, and match scores using the pyINETA Matching module."
- [readme] which it then matches to a simulated INADEQUATE database of metabolites to identify metabolites present in the query INADEQUATE spectra: "which it then matches to a simulated INADEQUATE database of metabolites to identify metabolites present in the query INADEQUATE spectra"
- [methods] Matching
--------
.. automodule:: pyineta.matching: "Matching
--------
.. automodule:: pyineta.matching"

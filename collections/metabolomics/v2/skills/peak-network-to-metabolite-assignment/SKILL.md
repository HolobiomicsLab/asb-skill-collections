---
name: peak-network-to-metabolite-assignment
description: Use when after peak clustering has produced peak network groups (ideally from the same compound) and you need to assign chemical identities.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3767
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0153
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
  - build: coll_pyineta_cq
    doi: 10.1021/acs.analchem.4c03966
    title: PyINETA
  dedup_kept_from: coll_pyineta_cq
schema_version: 0.2.0
---

# peak-network-to-metabolite-assignment

## Summary

Match identified peak networks from INADEQUATE NMR spectra to a simulated metabolite database using similarity metrics to assign metabolite identities. This skill bridges clustering output to metabolite identification by correlating experimental peak network signatures against reference spectral data.

## When to use

Apply this skill after peak clustering has produced peak network groups (ideally from the same compound) and you need to assign chemical identities. Use when you have query INADEQUATE spectra with identified peak networks and access to a simulated INADEQUATE database containing reference metabolite signatures with known spectral characteristics.

## When NOT to use

- Query spectra have not yet been clustered into peak networks—run Clustering module first
- Reference database is incomplete or lacks INADEQUATE signatures for metabolites of interest
- Raw, unpicked peaks are provided instead of pre-processed peak networks

## Inputs

- Peak network clusters from pyINETA Clustering module output
- Simulated INADEQUATE metabolite database with reference spectral signatures
- Configuration file specifying matching parameters and thresholds

## Outputs

- Matched metabolite assignment table (peak network ID → metabolite name + match score)
- Match score matrix (query networks × database metabolites)
- Filtered high-confidence metabolite identifications

## How to apply

Load the peak network clusters from the upstream Clustering module output along with a simulated INADEQUATE metabolite database containing reference spectral signatures. Calculate similarity metrics (e.g., cosine similarity or spectral correlation) between each query peak network and all database metabolite signatures. Apply a similarity threshold to filter and retain only high-confidence metabolite assignments. Generate a matched metabolite output table that links peak network identifiers to assigned metabolite names and their corresponding match scores. The threshold selection is critical: set it high enough to exclude false positives but low enough to capture true metabolites present in your sample.

## Related tools

- **PyINETA** (Provides the Matching module that implements peak network–to–database similarity calculation and metabolite assignment) — https://github.com/edisonomics/PyINETA
- **Python** (Runtime language for executing the PyINETA Matching module and similarity metric computation)

## Examples

```
python <path_to_pyineta_repo>/run_pyineta.py -c config.ini -s match -o output_dir
```

## Evaluation signals

- Output table contains one row per query peak network with non-null metabolite assignments and match scores in expected numeric range (0–1 for normalized similarity)
- Match scores for assigned metabolites exceed the configured similarity threshold; unassigned networks have no entries or scores below threshold
- Assigned metabolite identities are present in the simulated database and have valid INADEQUATE spectral signatures
- Peak network identifiers in output match identifiers from Clustering module output (schema consistency)
- Match score distribution shows clear separation between high-confidence (assigned) and low-confidence (unassigned) peak networks, indicating threshold is appropriate

## Limitations

- Matching quality depends critically on the completeness and accuracy of the simulated INADEQUATE reference database—missing or poorly characterized metabolites will not be identified
- Similarity metrics assume peak network features are comparable to database signatures; preprocessing differences (shifting, normalization) between query and database can degrade matching
- Threshold selection requires manual tuning or validation; no principled default is provided in the source documentation
- The package README notes 'No changelog found', suggesting limited version history documentation for reproducibility tracking

## Evidence

- [readme] pyINETA matches identified peak networks to a simulated INADEQUATE database of metabolites to identify metabolites present in the query INADEQUATE spectra: "matches to a simulated INADEQUATE database of metabolites to identify metabolites present in the query INADEQUATE spectra"
- [other] Calculate similarity metrics (e.g., cosine similarity or spectral correlation) between each query peak network and database metabolite signatures: "Calculate similarity metrics (e.g., cosine similarity or spectral correlation) between each query peak network and database metabolite signatures."
- [other] Filter matches using a similarity threshold to retain high-confidence metabolite assignments: "Filter matches using a similarity threshold to retain high-confidence metabolite assignments."
- [other] Generate a matched metabolite output table linking peak network identifiers, assigned metabolite names, and match scores: "Generate a matched metabolite output table linking peak network identifiers, assigned metabolite names, and match scores using the pyINETA Matching module."
- [other] Load peak network clusters from the upstream Clustering module output: "Load peak network clusters from the upstream Clustering module output."

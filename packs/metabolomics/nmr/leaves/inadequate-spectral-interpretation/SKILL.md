---
name: inadequate-spectral-interpretation
description: Use when you have clustered peak networks from INADEQUATE NMR spectra
  (output from the Clustering module) and need to assign metabolite identities by
  comparing them to known spectral signatures.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3633
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0199
  tools:
  - PyINETA
  - Python
  techniques:
  - NMR
  license_tier: open
  provenance_tier: literature
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

# inadequate-spectral-interpretation

## Summary

Match identified peak networks from INADEQUATE NMR spectra to a simulated metabolite database using similarity metrics to assign metabolite identities. This skill enables interpretation of INADEQUATE spectra by connecting query peak networks to reference spectral signatures with configurable confidence thresholds.

## When to use

You have clustered peak networks from INADEQUATE NMR spectra (output from the Clustering module) and need to assign metabolite identities by comparing them to known spectral signatures. Use this skill when you need to determine which metabolites are present in a query sample and require high-confidence assignments with match scores.

## When NOT to use

- Input peak networks have not been properly clustered or contain unfiltered individual peaks rather than grouped networks
- No reference INADEQUATE database is available or the database does not cover the expected metabolites in your sample
- Query spectra have poor signal-to-noise ratio or significant spectral distortion that would compromise similarity calculations

## Inputs

- Peak network clusters (from pyINETA Clustering module output)
- Simulated INADEQUATE metabolite database with reference spectral signatures
- Similarity threshold parameter (user-configurable)

## Outputs

- Matched metabolite assignment table
- Peak network identifiers linked to metabolite names
- Match scores (similarity metrics) for each assignment

## How to apply

Load peak network clusters from the upstream Clustering module output along with a simulated INADEQUATE metabolite database containing reference spectral signatures. Calculate similarity metrics (e.g., cosine similarity or spectral correlation) between each query peak network and database metabolite signatures. Filter matches using a similarity threshold to retain only high-confidence metabolite assignments. The matching process generates a linked output table associating each peak network identifier with assigned metabolite names and their corresponding match scores, which can be further refined by adjusting the similarity threshold based on your confidence requirements.

## Related tools

- **PyINETA** (Performs spectral matching and similarity calculation between query peak networks and simulated INADEQUATE metabolite database signatures) — https://github.com/edisonomics/PyINETA
- **Python** (Underlying language for implementing similarity metrics and database comparison logic)

## Examples

```
python run_pyineta.py -c config.ini -s match -o output_dir
```

## Evaluation signals

- All peak network identifiers from the input clusters are present in the output matched metabolite table with no orphaned networks
- Match scores fall within expected range (0–1 for normalized similarity metrics) and reflect reasonable confidence levels
- High-confidence matches (above the applied threshold) correspond to metabolites chemically plausible given the experimental context
- Consistency check: the same peak network should match to only one metabolite (or a ranked list if degeneracy is acceptable)
- Output table schema is valid: contains columns for peak_network_id, metabolite_name, and match_score with no missing values in high-confidence rows

## Limitations

- Matching accuracy depends critically on the completeness and quality of the simulated INADEQUATE reference database; metabolites absent from the database cannot be identified
- Similarity threshold is user-configurable but no automated threshold optimization is documented; incorrect threshold selection may yield false positives or false negatives
- The method assumes peak networks represent single compounds; co-elution or spectral overlap may produce ambiguous or incorrect matches
- No changelog is available in the repository, limiting documentation of changes to matching algorithms or reference databases across versions

## Evidence

- [intro] pyINETA matches identified peak networks to a simulated INADEQUATE database of metabolites to identify metabolites present in the query spectra.: "matches identified peak networks to a simulated INADEQUATE database of metabolites to identify metabolites present in the query INADEQUATE spectra"
- [other] The matching workflow calculates similarity metrics between query and database signatures, then filters by threshold.: "Calculate similarity metrics (e.g., cosine similarity or spectral correlation) between each query peak network and database metabolite signatures. 4. Filter matches using a similarity threshold to"
- [other] Output includes peak network identifiers, metabolite names, and match scores.: "Generate a matched metabolite output table linking peak network identifiers, assigned metabolite names, and match scores using the pyINETA Matching module."
- [readme] The skill is designed to filter picked peaks to identify networks of peaks from the same compound.: "It is designed to filter these picked peaks to identify networks of peaks (ideally) coming from the same compound"
- [methods] Matching module is one of the core workflow steps in pyINETA pipeline.: "Matching
--------
.. automodule:: pyineta.matching"

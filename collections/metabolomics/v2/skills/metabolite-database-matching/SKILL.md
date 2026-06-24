---
name: metabolite-database-matching
description: Use when after peak networks have been identified and clustered from
  INADEQUATE spectra (typically via the clustering and finding modules), use this
  skill when you need to assign chemical identities to unknown peak networks by comparing
  them against reference spectral signatures in a simulated.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3375
  - http://edamontology.org/topic_0097
  tools:
  - PyINETA
  - Python
  techniques:
  - NMR
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
  - build: coll_george_cq
    doi: 10.1021/acs.analchem.5b03628
    title: geoRge
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

# metabolite-database-matching

## Summary

Match identified peak networks from INADEQUATE NMR spectra against a simulated metabolite database using similarity metrics to assign metabolite identities. This skill bridges spectral clustering and metabolite annotation by scoring and filtering high-confidence peak-to-metabolite assignments.

## When to use

After peak networks have been identified and clustered from INADEQUATE spectra (typically via the clustering and finding modules), use this skill when you need to assign chemical identities to unknown peak networks by comparing them against reference spectral signatures in a simulated INADEQUATE database.

## When NOT to use

- Peak networks have not yet been filtered or clustered — apply clustering and finding modules first
- No reference database is available or the database does not cover the expected metabolite space
- Query spectra contain unfiltered or low-quality peaks that have not been validated as belonging to coherent networks

## Inputs

- Peak network clusters (from clustering module output)
- Simulated INADEQUATE metabolite database with reference spectral signatures
- Query peak network data with spectral features

## Outputs

- Matched metabolite output table (peak network ID, metabolite name, match score)
- Metabolite assignment annotations for query spectra

## How to apply

Load the peak network clusters from the upstream clustering module output and the simulated INADEQUATE metabolite database containing reference spectral signatures. Calculate similarity metrics (e.g., cosine similarity or spectral correlation) between each query peak network and each database metabolite signature. Apply a similarity threshold to filter matches and retain only high-confidence metabolite assignments. Generate a matched metabolite output table that links peak network identifiers, assigned metabolite names, and match scores. The rationale is that peak networks originating from the same compound will exhibit spectral similarity to database reference signatures for that metabolite, enabling identity assignment through quantitative correlation.

## Related tools

- **PyINETA** (Implements the matching module that calculates similarity metrics and performs peak network to metabolite database matching) — https://github.com/edisonomics/PyINETA
- **Python** (Programming language used to implement PyINETA matching routines and execute the matching workflow)

## Examples

```
python run_pyineta.py -c config.ini -o output_dir -s match
```

## Evaluation signals

- Match scores are distributed appropriately (typically between 0 and 1 for normalized similarity metrics) and high-confidence matches exceed the applied similarity threshold
- All query peak networks receive a metabolite assignment with an associated match score; no networks are left unmatched or fail during the matching process
- Matched metabolite names are present in the reference database and correspond to metabolites consistent with the experimental context
- The matched metabolite output table contains no missing values in required columns (peak network ID, metabolite name, match score)
- When visualized, high-scoring matches show spectral feature overlap between query peak networks and database reference signatures

## Limitations

- Matching accuracy depends on the completeness and quality of the simulated INADEQUATE database; metabolites absent from the database cannot be identified
- The similarity threshold is a critical parameter; too high a threshold may result in false negatives (missing true metabolites), while too low a threshold may yield false positives
- Isobaric or near-isobaric metabolites with similar INADEQUATE spectral signatures may be ambiguous or incorrectly assigned
- The matching module uses basic spectral correlation methods (as noted in the README); more sophisticated machine learning approaches are not implemented in the current version

## Evidence

- [intro] pyINETA matches identified peak networks to a simulated INADEQUATE database of metabolites to identify metabolites in query spectra: "pyINETA matches identified peak networks to a simulated INADEQUATE database of metabolites to identify metabolites present in the query INADEQUATE spectra"
- [other] The matching workflow calculates similarity metrics between query peak networks and database signatures, then filters using a threshold: "Calculate similarity metrics (e.g., cosine similarity or spectral correlation) between each query peak network and database metabolite signatures. 4. Filter matches using a similarity threshold to"
- [other] The output of matching is a table linking peak network IDs, metabolite names, and match scores: "Generate a matched metabolite output table linking peak network identifiers, assigned metabolite names, and match scores using the pyINETA Matching module"
- [other] Matching is executed as part of the complete PyINETA pipeline after clustering and finding steps: "Match filtered peak networks against a simulated INADEQUATE metabolite database using the matching module. 7. Generate visualization outputs via the plotting module and export final metabolite"
- [methods] The matching module is documented as a key component of PyINETA: "Matching
--------
.. automodule:: pyineta.matching"

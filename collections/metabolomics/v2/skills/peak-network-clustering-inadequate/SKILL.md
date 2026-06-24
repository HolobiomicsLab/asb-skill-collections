---
name: peak-network-clustering-inadequate
description: Use when you have picked peaks (coordinates and intensities) from INADEQUATE
  spectra and need to distinguish which peaks likely originate from the same metabolite
  before matching to a reference database.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0092
  tools:
  - Python
  - PyINETA
  - pyineta.clustering
  - pyineta.finding
  techniques:
  - NMR
  license_tier: open
derived_from:
- doi: 10.1021/acs.analchem.4c03966
  title: PyINETA
evidence_spans:
- pyINETA is a Python package
- python run_pyineta.py <options>
- This is the documentation for the PyINETA package version 2.0.0.
- '.. automodule:: pyineta.finding :members:'
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

# peak-network-clustering-inadequate

## Summary

Cluster picked peaks from INADEQUATE NMR spectra into networks representing peaks originating from the same compound, enabling subsequent metabolite matching against a simulated database. This skill groups spectral signals based on spectral connectivity patterns to reduce false identifications and improve metabolite assignment accuracy.

## When to use

Apply this skill when you have picked peaks (coordinates and intensities) from INADEQUATE spectra and need to distinguish which peaks likely originate from the same metabolite before matching to a reference database. Use it as the critical filtering step between peak picking and database matching in the PyINETA pipeline.

## When NOT to use

- Input spectra are not INADEQUATE experiments (skill is specific to 2D heteronuclear correlation data from INADEQUATE pulses).
- Peaks have not yet been picked from raw spectra; use the picking module first.
- Peak coordinates or intensities are missing or malformed; pre-validate input structure.

## Inputs

- picked peaks from PyINETA picking module (peak coordinates and intensities)
- INADEQUATE spectra metadata (referencing information)
- cluster/network connectivity configuration

## Outputs

- filtered peak network assignments (structured table)
- network-to-compound groupings
- discarded peaks not meeting network criteria

## How to apply

Load the picked peaks output from the PyINETA picking module (peak coordinates and intensities). Apply network-based clustering logic within the Finding module to group peaks that likely originate from the same compound based on spectral connectivity patterns. Filter and retain only peak networks meeting the module's internal criteria for compound association. The clustering uses spectral relationships to infer compound origin; networks that fail internal coherence criteria are discarded before database matching. Output the filtered peak network assignments as a structured table for downstream matching against the simulated INADEQUATE metabolite database.

## Related tools

- **PyINETA** (Python package providing the clustering and finding modules that implement peak network identification and filtering logic) — https://github.com/edisonomics/PyINETA
- **pyineta.clustering** (PyINETA module that performs the actual network-based clustering of peaks) — https://github.com/edisonomics/PyINETA
- **pyineta.finding** (PyINETA module that filters clustered peaks to identify and retain only networks meeting compound association criteria) — https://github.com/edisonomics/PyINETA

## Examples

```
python run_pyineta.py -c config.ini -s cluster,find -o output_dir
```

## Evaluation signals

- Peak network assignments form connected components where each network corresponds to a single expected metabolite structure.
- Number of output networks is reasonable relative to input peak count; excessive fragmentation (many 1–2 peak networks) or excessive merging (one giant network) may indicate parameter drift.
- Filtered peak networks achieve higher matching scores (cosine similarity, etc.) against the simulated INADEQUATE database compared to unfiltered or randomly grouped peaks.
- Output table is valid and parseable; each network has assigned peaks with coordinates, intensities, and compound association confidence scores.
- Networks discarded by internal criteria are reproducibly the same across independent runs with identical input and configuration.

## Limitations

- pyINETA uses basic shifting for INADEQUATE spectrum referencing; may not be accurate for spectra with strong referencing errors or unconventional solvent conditions.
- Clustering relies on spectral connectivity patterns that may fail when peaks are overlapping, very weak, or in regions of high spectral congestion.
- The simulated INADEQUATE database is limited; matching will fail for metabolites absent from the reference or with unexpected chemical shifts.
- No changelog available, so parameter defaults and filtering thresholds may vary silently across package versions.

## Evidence

- [intro] pyINETA is designed to filter picked peaks to identify networks of peaks ideally coming from the same compound: "It is designed to filter these picked peaks to identify networks of peaks (ideally) coming from the same compound"
- [methods] Clustering module groups signals from the same compound: "Apply network-based clustering logic within the Finding module to group peaks that likely originate from the same compound based on spectral connectivity patterns"
- [intro] Filtered peak networks are matched to a simulated INADEQUATE database of metabolites: "which it then matches to a simulated INADEQUATE database of metabolites to identify metabolites present in the query INADEQUATE spectra"
- [methods] PyINETA workflow includes clustering and finding modules as distinct steps: "Clustering
----------
.. automodule:: pyineta.clustering

Finding
-------
.. automodule:: pyineta.finding"
- [readme] PyINETA performed with run_pyineta.py entry point: "Cluster picked peaks using the clustering module to group signals from the same compound. 5. Filter peak networks in the finding module to identify networks of peaks expected to originate from"

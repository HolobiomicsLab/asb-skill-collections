---
name: compound-peak-association-inference
description: Use when after peak picking on INADEQUATE NMR spectra when you have a set of peak coordinates and intensities and need to determine which peaks belong to the same molecular compound.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_0593
  - http://edamontology.org/topic_3172
  tools:
  - Python
  - PyINETA
  techniques:
  - NMR
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

# compound-peak-association-inference

## Summary

Identify networks of NMR peaks that originate from the same compound by applying spectral connectivity clustering to picked peaks from INADEQUATE spectra. This skill filters noise and spurious peaks to group coherent peak networks prior to metabolite matching.

## When to use

Apply this skill after peak picking on INADEQUATE NMR spectra when you have a set of peak coordinates and intensities and need to determine which peaks belong to the same molecular compound. Use it as an intermediate step before matching peak networks against a simulated INADEQUATE metabolite database to identify unknown metabolites in the query spectrum.

## When NOT to use

- Input peaks have not been picked or baseline-corrected; run the Picking module first.
- You already have metabolite identities or a manually curated peak-to-compound mapping; this skill is for unsupervised inference of peak associations.
- The query spectrum is not INADEQUATE or lacks the expected one-bond carbon coupling topology; network clustering assumes INADEQUATE spectral structure.

## Inputs

- Picked peak coordinates (chemical shift or frequency positions)
- Peak intensities (signal amplitudes)
- INADEQUATE NMR spectrum (reference for connectivity validation)

## Outputs

- Peak network assignments table (peak ID → network/compound ID)
- Filtered peak network clusters (structured output ready for metabolite matching)
- Network connectivity metadata (cluster membership and internal coherence scores)

## How to apply

Load the picked peak coordinates and intensities output from the PyINETA Picking module. Apply network-based clustering logic that groups peaks based on spectral connectivity patterns—peaks are considered networked when they share coherent structural relationships characteristic of a single compound's INADEQUATE splitting pattern. Retain only peak networks that meet the module's internal filtering criteria (e.g., minimum cluster size, connectivity threshold). Output the grouped peak assignments as a structured table linking each peak to its inferred compound network. The rationale is that INADEQUATE spectra show one-bond carbon-carbon couplings, so peaks from the same molecule form a recognizable pattern; clustering exploits this pattern to reject isolated or cross-contaminating peaks.

## Related tools

- **PyINETA** (Provides the Finding module (pyineta.finding) that implements network-based peak clustering and filtering for compound association inference) — https://github.com/edisonomics/PyINETA
- **Python** (Runtime environment for executing PyINETA and the Finding module)

## Examples

```
python <path_to_pyineta_repo>/run_pyineta.py -c config.ini -s find
```

## Evaluation signals

- Peak network table contains no isolated peaks (all peaks assigned to a network with ≥ 2 members) or isolated peaks are explicitly marked as filtered.
- Network assignments are deterministic: running the same picked peaks twice produces identical clustering.
- Peak networks respect INADEQUATE spectral structure: within each network, peak positions should exhibit coherent chemical shift offsets consistent with one-bond C–C couplings (typically 40–80 ppm or 1000–2000 Hz at high field).
- Downstream matching step (PyINETA Matching module) accepts the network output without schema errors and produces metabolite identifications with non-zero match scores.
- Comparison with annotated reference spectra (if available): network assignments should recover known compound-peak mappings with >80% precision or sensitivity (depending on spectral complexity).

## Limitations

- Network clustering assumes input peaks are accurate and complete; false or missed peaks will degrade cluster quality.
- Algorithm performance depends on spectral signal-to-noise ratio and peak density; heavily overlapping or noisy regions may produce unreliable associations.
- The module is designed for metabolite-scale INADEQUATE spectra; very large molecular structures or mixtures with many coeluting compounds may produce ambiguous or fragmented networks.
- No changelog is available to track changes in clustering thresholds or algorithm behavior across PyINETA versions.

## Evidence

- [readme] pyINETA is designed to filter picked peaks to identify networks of peaks (ideally) coming from the same compound: "It is designed to filter these picked peaks to identify networks of peaks (ideally) coming from the same compound"
- [intro] Apply network-based clustering logic within the Finding module to group peaks based on spectral connectivity patterns: "Apply network-based clustering logic within the Finding module to group peaks that likely originate from the same compound based on spectral connectivity patterns"
- [intro] Load picked peaks from the output of the PyINETA Picking module: "Load picked peaks from the output of the PyINETA Picking module (peak coordinates and intensities)"
- [intro] Output the filtered peak network assignments as a structured table: "Output the filtered peak network assignments as a structured table"
- [readme] pyINETA matches identified peak networks to a simulated INADEQUATE database to identify metabolites in query spectra: "which it then matches to a simulated INADEQUATE database of metabolites to identify metabolites present in the query INADEQUATE spectra"

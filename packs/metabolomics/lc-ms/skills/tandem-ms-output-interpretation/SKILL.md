---
name: tandem-ms-output-interpretation
description: Use when you have received spectrum predictions (fragment masses and intensities) from a neural model (ICEBERG, SCARF, or similar) and need to extract structural information, rank candidate molecules, or validate predictions against experimental spectra.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3172
  tools:
  - ICEBERG
  - SCARF
  - PubChem
  - ms-pred repository
  - ICEBERG WebUI
  techniques:
  - LC-MS
derived_from:
- doi: 10.1038/s42256-024-00816-8
  title: ICEBERG
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_iceberg_cq
    doi: 10.1038/s42256-024-00816-8
    title: ICEBERG
  dedup_kept_from: coll_iceberg_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s42256-024-00816-8
  all_source_dois:
  - 10.1038/s42256-024-00816-8
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# tandem-ms-output-interpretation

## Summary

Interpret predicted tandem mass spectra (m/z and intensity pairs) from neural spectrum prediction models to identify molecular fragments and rank candidate structures. This skill bridges model output to structural elucidation by mapping spectrum predictions to chemical composition and fragment genealogy.

## When to use

You have received spectrum predictions (fragment masses and intensities) from a neural model (ICEBERG, SCARF, or similar) and need to extract structural information, rank candidate molecules, or validate predictions against experimental spectra. Use this when predictions are either chemical-formula-level (SCARF) or fragment-level (ICEBERG) and must be mapped to molecular structures or compared against PubChem candidates.

## When NOT to use

- Input spectrum is from a low-resolution instrument without isotopic or fragment-level resolution; model predictions assume high mass accuracy and will not match noisy or poorly resolved data.
- Query molecule has unknown stereochemistry or multiple isomers; SCARF and ICEBERG predictions are sensitive to SMILES canonical form and will differ across stereoisomers.
- Candidate library is incomplete or biased; retrieval ranking depends on comprehensive chemical formula coverage (PubChem is assumed; closed or specialty libraries may produce false negatives).

## Inputs

- predicted spectrum (JSON/CSV with m/z, intensity pairs)
- prediction granularity metadata (e.g., 'chemical_formula' or 'molecular_fragment')
- query molecule (SMILES string or molecular structure)
- experimental tandem mass spectrum (optional, for validation)
- candidate library (PubChem SMILES/InChI subset, optional for retrieval)

## Outputs

- ranked candidate structure list (SMILES, InChI keys, scores)
- annotated spectrum plot (predicted vs. experimental peaks)
- fragment genealogy tree (breakage paths, for ICEBERG)
- retrieval hit rate or top-k accuracy metric

## How to apply

Load the predicted spectrum output (JSON or CSV with fragment m/z and intensity pairs) and the prediction granularity metadata (chemical formula or molecular fragment level). For SCARF outputs, group peaks by chemical subformula to reconstruct fragmentation patterns. For ICEBERG outputs, trace fragment genealogy using the annotated breakage DAG to connect predicted fragments to parent structures. Format predictions into a ranked candidate list by computing similarity metrics (e.g., cosine similarity) against experimental spectra. Filter and rank PubChem candidates using the chemical formula constraint from the query molecule. Validate rankings by comparing predicted vs. experimental peak lists, checking that major predicted peaks appear in experimental data and vice versa.

## Related tools

- **ICEBERG** (generates predicted spectra at molecular fragment level; outputs fragment m/z, intensity, and breakage DAG for structural reconstruction) — https://github.com/coleygroup/ms-pred
- **SCARF** (generates predicted spectra at chemical-formula (subformula) level; outputs m/z and intensity grouped by chemical composition) — https://github.com/coleygroup/ms-pred
- **PubChem** (provides candidate structure library indexed by chemical formula for retrieval-based ranking and validation)
- **ms-pred repository** (provides data structures, I/O utilities, and retrieval pipeline (torchmetrics-based ranking) for spectrum predictions) — https://github.com/coleygroup/ms-pred
- **ICEBERG WebUI** (interactive interface for structural elucidation; accepts chemical formula and experimental spectrum, ranks PubChem candidates) — http://iceberg-ms.mit.edu/

## Evaluation signals

- Predicted m/z values fall within 5 ppm (or instrument tolerance) of experimental peaks for major fragments
- Predicted intensity rank order matches experimental peak intensity ordering (top 3–5 peaks agreement)
- Top-1 or top-10 retrieval accuracy: correct candidate ranked first or within top-k of PubChem subset
- Fragment genealogy is chemically plausible: predicted breakage paths match known neutral losses (H₂O, CO₂, etc.) and charge retention rules
- Cosine similarity between predicted and experimental spectrum vectors exceeds 0.7 (or model-specific threshold)

## Limitations

- SCARF operates only at chemical-formula granularity and cannot distinguish isomeric fragments; use ICEBERG for finer structural detail.
- ICEBERG requires GPU (≥24 GB VRAM for standard training/inference) and pretrained model weights; CPU-only inference is feasible but slower.
- Predictions are specific to collision energy (NIST'20 dataset has collision energy annotations; other spectra may not be comparable without energy normalization).
- Retrieval ranking depends on PubChem completeness; rare or novel compounds outside PubChem will not appear in candidate rankings.
- Model was trained on [M+H]+ ions; ESI-MS/MS with different ionization modes or adducts may produce lower accuracy.
- No changelog available; model version and training date should be verified before publication or critical decisions.

## Evidence

- [intro] ICEBERG predicts spectra at the level of molecular fragments, whereas SCARF predicts spectra at the level of chemical formula.: "ICEBERG predicts spectra at the level of molecular fragments, whereas SCARF predicts spectra at the level of chemical formula."
- [readme] By inputting the chemical formula and your experimental spectrum, the WebUI will rank it against all candidates from PubChem.: "By inputting the chemical formula and your experimental spectrum, the WebUI will rank it against all candidates from PubChem."
- [readme] ICEBERG is our recommended model with a 40% top-1 retrieval accuracy with [M+H]+, benchmarked on the NIST'20 dataset.: "ICEBERG is our recommended model with a 40% top-1 retrieval accuracy with [M+H]+, benchmarked on the NIST'20 dataset."
- [readme] An example of how to use ICEBERG for structural elucidation campaigns can be found at notebooks/iceberg_2025_biorxiv/iceberg_demo_pubchem_elucidation.ipynb.: "An example of how to use ICEBERG for structural elucidation campaigns can be found at notebooks/iceberg_2025_biorxiv/iceberg_demo_pubchem_elucidation.ipynb."
- [other] SCARF predicts spectra at the chemical-subformula level: "Invoke the SCARF model from the ms-pred repository to generate spectrum predictions at the chemical-subformula level."
- [readme] You need two GPUs with at least 24GB RAM to train ICEBERG. If you are trying to train the model on a smaller GPU, try cutting down the batch size.: "You need two GPUs with at least 24GB RAM to train ICEBERG. If you are trying to train the model on a smaller GPU, try cutting down the batch size."

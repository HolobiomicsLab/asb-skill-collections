---
name: tandem-ms-peak-assignment
description: Use when when you have experimental tandem MS spectra (with peak m/z
  and intensity values) and need to annotate each peak with its chemical formula (SCARF)
  or molecular fragment origin (ICEBERG), particularly for structural elucidation
  campaigns where understanding the fragmentation pathway is.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - SCARF
  - ICEBERG
  - ms-pred repository
  - PubChem
  techniques:
  - GC-MS
  license_tier: open
derived_from:
- doi: 10.1021/acs.analchem.3c04654
  title: ICEBERG / fragmentation graph generation
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_iceberg_fragmentation_graph_generation_cq
    doi: 10.1021/acs.analchem.3c04654
    title: ICEBERG / fragmentation graph generation
  dedup_kept_from: coll_iceberg_fragmentation_graph_generation_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.3c04654
  all_source_dois:
  - 10.1021/acs.analchem.3c04654
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# tandem-ms-peak-assignment

## Summary

Assign tandem mass spectrometry peaks to molecular subformulae or fragments by applying spectrum prediction models (SCARF or ICEBERG) that autoregressively reconstruct fragmentations and annotate m/z values with their corresponding chemical formula or substructure origins.

## When to use

When you have experimental tandem MS spectra (with peak m/z and intensity values) and need to annotate each peak with its chemical formula (SCARF) or molecular fragment origin (ICEBERG), particularly for structural elucidation campaigns where understanding the fragmentation pathway is required to rank molecular candidates or validate proposed structures.

## When NOT to use

- Input is a low-resolution spectrum (e.g., nominal m/z only without intensity information); SCARF and ICEBERG require both m/z and intensity data for meaningful predictions.
- The molecular structure is unknown or not representable in SMILES/InChI/formula form; the models require explicit chemical structure as input.
- You need to predict electron ionization (EI) spectra at high mass resolution without fragmentation annotation; ICEBERG and SCARF are optimized for collision-induced dissociation (CID) tandem MS.

## Inputs

- molecular structure (SMILES, InChI, or chemical formula)
- experimental tandem MS spectrum (m/z values and peak intensities)
- pre-trained model weights (SCARF or ICEBERG checkpoint)

## Outputs

- annotated peak list with m/z, predicted intensity, and assigned chemical formula or fragment substructure
- spectral match score (e.g., cosine similarity between predicted and experimental spectrum)
- ranked candidate molecules (for structural elucidation workflows)

## How to apply

Initialize a pre-trained SCARF or ICEBERG model with appropriate weights from the ms-pred repository. Input molecular candidates as SMILES, InChI, or chemical formula along with the experimental tandem MS spectrum. Execute forward inference through the model, which performs subformula classification (SCARF) or fragment graph reconstruction (ICEBERG) to autoregressively predict peaks and assign each predicted peak to its corresponding chemical formula or substructure. Parse the structured output to extract predicted peak m/z values, intensities, and subformula/fragment annotations. Compare predicted peaks against experimental spectrum by calculating cosine similarity or other spectral matching metrics to validate peak assignments and score candidate molecules for structural ranking.

## Related tools

- **SCARF** (Subformula Classification for Autoregressively Reconstructing Fragmentations; predicts tandem MS spectra at the chemical formula level and assigns peaks to subformulae.) — https://github.com/coleygroup/ms-pred
- **ICEBERG** (Inferring CID by Estimating Breakage Events and Reconstructing their Graphs; predicts tandem MS spectra at the molecular fragment level and assigns peaks to substructures.) — https://github.com/coleygroup/ms-pred
- **ms-pred repository** (Provides implementations, pre-trained model weights, and inference pipelines for SCARF, ICEBERG, and baseline spectrum prediction models.) — https://github.com/coleygroup/ms-pred
- **PubChem** (Source database of molecular candidates ranked against experimental spectra during structural elucidation via the ICEBERG WebUI.)

## Evaluation signals

- Predicted spectrum cosine similarity to experimental spectrum exceeds a threshold (typically >0.6 for confident assignments; higher indicates better peak matching).
- Peak m/z predictions match experimental peaks within instrument mass tolerance (typically <5 ppm for high-resolution MS or <0.1 Da for nominal m/z).
- Assigned chemical formulas or fragment substructures are chemically valid (e.g., obey valence rules, preserve molecular mass of parent ion minus expected neutral loss).
- The top-ranked candidate molecule for a given experimental spectrum is the true structure (top-1 retrieval accuracy metric used in paper benchmarks).
- Predicted peak intensities rank correctly relative to observed experimental peak intensities (rank correlation or Spearman ρ > 0.5).

## Limitations

- SCARF predicts spectra only at the chemical formula level, losing substructural detail; if fragment-level annotation is required, ICEBERG is preferred but requires more computational resources.
- Model performance depends on the training dataset: models trained on NIST'20 (commercial, curated dataset with collision energy annotations) outperform models trained on MassSpecGym (publicly available but less manually curated); users must acquire appropriate license or use lower-performing publicly available weights.
- GPU memory requirements scale with batch size and model complexity; ICEBERG requires at least 24 GB GPU RAM for full pipeline training; CPU-only inference is feasible but substantially slower.
- Peak assignment accuracy degrades for structurally novel molecules outside the training set distribution; model predictions are most reliable for molecules similar to NIST'20 or training corpus.
- No GPU is required for ICEBERG structural elucidation via the WebUI, but local inference with full training requires GPU; batch inference with large numbers of candidates benefits significantly from GPU acceleration.

## Evidence

- [other] SCARF is a spectrum predictor model that operates by performing subformula classification to autoregressively reconstruct fragmentations and predict tandem mass spectra at the chemical formula level.: "SCARF is a spectrum predictor model that operates by performing subformula classification to autoregressively reconstruct fragmentations and predict tandem mass spectra at the chemical formula level."
- [readme] ICEBERG predicts spectra at the level of molecular fragments, whereas SCARF predicts spectra at the level of chemical formula.: "ICEBERG predicts spectra at the level of molecular fragments, whereas SCARF predicts spectra at the level of chemical formula."
- [other] Execute forward inference pass through SCARF to generate subformula-level spectrum predictions for each molecule. Parse and format predicted spectra (peak intensities, m/z values, subformula assignments) into structured output table.: "Execute forward inference pass through SCARF to generate subformula-level spectrum predictions for each molecule. Parse and format predicted spectra (peak intensities, m/z values, subformula"
- [readme] By inputting the chemical formula and your experimental spectrum, the WebUI will rank it against all candidates from PubChem.: "By inputting the chemical formula and your experimental spectrum, the WebUI will rank it against all candidates from PubChem."
- [readme] ICEBERG is our recommended model with a 40% top-1 retrieval accuracy with [M+H]+, benchmarked on the NIST'20 dataset.: "ICEBERG is our recommended model with a 40% top-1 retrieval accuracy with [M+H]+, benchmarked on the NIST'20 dataset."
- [readme] You need two GPUs with at least 24GB RAM to train ICEBERG; similarly, all the scripts also feature, but have commented out, the training commands to train on MassSpecGym.: "You need two GPUs with at least 24GB RAM to train ICEBERG (we used NVIDIA A5000 for development)."
- [readme] MassSpecGym has undergone less manual curation and quality control compared to NIST, and the results of new predictions will be different.: "MassSpecGym has undergone less manual curation and quality control compared to NIST, and the results of new predictions will be different."

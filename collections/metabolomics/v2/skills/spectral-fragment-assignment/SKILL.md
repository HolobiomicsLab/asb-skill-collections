---
name: spectral-fragment-assignment
description: Use when when you have an experimental tandem mass spectrum (peaks with m/z and intensity values) and wish to identify which fragments or chemical subformulae each peak corresponds to.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_3520
  tools:
  - ICEBERG
  - SCARF
  - MAGMa algorithm
  - PubChem
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

# Spectral Fragment Assignment

## Summary

Assign observed peaks in a tandem mass spectrum to specific molecular fragments or subformulae using generative or classification models. This skill enables structural elucidation by mapping experimental spectrum intensities to their chemical origins within the intact molecule.

## When to use

When you have an experimental tandem mass spectrum (peaks with m/z and intensity values) and wish to identify which fragments or chemical subformulae each peak corresponds to. Apply this skill to support structure elucidation workflows, especially when comparing candidate molecules or validating proposed fragmentation mechanisms.

## When NOT to use

- Input spectrum is a low-resolution mass spectrum (not tandem MS/MS) — fragment assignment requires high-resolution precursor isolation and CID fragmentation patterns.
- Molecule contains metal coordination centers or unusual bonding not represented in standard SMILES — model training data may not cover such structures.
- Your goal is only neutral mass calculation, not fragmentation mechanism understanding — simpler mass-lookup tools are more efficient.

## Inputs

- SMILES string or molecular structure representation
- Experimental tandem mass spectrum (m/z values and peak intensities)
- Collision energy or ionization conditions (if available)

## Outputs

- Annotated spectrum with peak-to-fragment mappings
- Predicted m/z and intensity values for each assigned fragment
- Fragmentation graph or breakage pathway (for ICEBERG)
- Chemical subformula labels for each peak (for SCARF)

## How to apply

Load the input molecule as a SMILES string or molecular structure and the experimental spectrum (m/z and intensity pairs). Select a prediction model appropriate to your granularity requirement: ICEBERG for molecular-fragment-level assignment or SCARF for chemical-formula-level assignment. Invoke the chosen model from the ms-pred repository to generate predicted fragment-to-peak mappings. The model will output an annotated spectrum in which each observed or predicted peak is linked to its originating fragment or subformula. Evaluate the assignment by comparing predicted peak positions (m/z) and intensities against observed values; high cosine similarity or top-1 ranking accuracy indicates correct assignment.

## Related tools

- **ICEBERG** (Fragment-level spectral prediction and assignment; predicts spectra by inferring molecular breakage events and reconstructing fragmentation graphs) — https://github.com/coleygroup/ms-pred
- **SCARF** (Chemical-subformula-level spectral prediction; assigns peaks to chemical formulae via autoregressive fragment reconstruction) — https://github.com/coleygroup/ms-pred
- **MAGMa algorithm** (Substructure annotation and breakage process labeling used to prepare training data for fragment assignment models) — https://github.com/coleygroup/ms-pred
- **PubChem** (Candidate molecule library for retrieval-based structural elucidation after fragment assignment)

## Examples

```
python src/ms_pred/dag_pred/predict_smis.py --smiles 'CC(=O)Oc1ccccc1C(=O)O' --model iceberg --output predictions.json
```

## Evaluation signals

- Predicted m/z values match observed spectrum peaks within instrument mass accuracy tolerance (typically ±5 ppm for high-resolution MS).
- Predicted peak intensities show high cosine similarity with observed intensities across the full spectrum.
- Top-1 retrieval accuracy: the correct candidate molecule ranks first when predicted spectrum is matched against PubChem library (ICEBERG reports ~40% top-1 accuracy on NIST'20 [M+H]+ ions).
- Fragmentation graph (for ICEBERG) forms a valid directed acyclic graph (DAG) where each node is a valid substructure and edges represent chemically plausible breakages.
- Subformula assignments (for SCARF) satisfy mass balance constraints: sum of predicted fragment masses equals or is close to precursor m/z minus expected neutral losses.

## Limitations

- ICEBERG and SCARF are trained on tandem MS data (typically EI or ESI-MS/MS); performance on other ionization methods or collision energies is not uniformly characterized.
- Models require SMILES input; molecules with ambiguous or non-standard SMILES representations may yield unreliable assignments.
- Pretrained ICEBERG weights are available only for NIST'20 dataset (commercial, requires license) or MassSpecGym (public but less curated); retraining on custom datasets requires substantial GPU resources (≥24 GB RAM).
- Fragment assignments become ambiguous for isomeric molecules with identical molecular formulas but different connectivity; retrieval-based elucidation (ranking candidates) is needed to disambiguate.
- No GPU is required for ICEBERG WebUI inference, but local deployment and retraining demand significant computational resources; CPU-only inference is feasible but slower.

## Evidence

- [intro] ICEBERG predicts spectra at the level of molecular fragments, whereas SCARF predicts spectra at the level of chemical formula.: "ICEBERG predicts spectra at the level of molecular fragments, whereas SCARF predicts spectra at the level of chemical formula."
- [readme] SCARF operates at chemical-subformula granularity by autoregressively reconstructing fragmentations.: "🧣 SCARF 🧣: [Subformula Classification for Autoregressively Reconstructing Fragmentations]"
- [other] Fragment assignment workflow: load molecule, invoke SCARF model, format predicted spectrum into structured output.: "1. Load or define the input molecule (SMILES string or molecular structure). 2. Invoke the SCARF model from the ms-pred repository to generate spectrum predictions at the chemical-subformula level."
- [readme] ICEBERG uses MAGMa algorithm for substructure annotation and breakage labeling.: "to train ICEBERG, we must annotate substructures and create a labeled dataset over the breakage process, which we do with the MAGMa algorithm."
- [readme] ICEBERG retrieval accuracy on NIST'20 benchmark with [M+H]+ ions.: "ICEBERG is our recommended model with a 40% top-1 retrieval accuracy with [M+H]+, benchmarked on the NIST'20 dataset."
- [readme] GPU requirements for local ICEBERG training.: "You need two GPUs with at least 24GB RAM to train ICEBERG (we used NVIDIA A5000 for development)."
- [readme] CPU-only inference feasibility for ICEBERG.: "CPU-only inference is also feasible if you set ``cuda_devices: None``."

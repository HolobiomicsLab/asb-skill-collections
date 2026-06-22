---
name: spectrum-peak-matching
description: Use when you have an experimental tandem mass spectrum (peaks with m/z values and intensities), a chemical formula, and a set of candidate molecular structures retrieved from a database like PubChem.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3631
  edam_topics:
  - http://edamontology.org/topic_0153
  - http://edamontology.org/topic_3520
  tools:
  - ICEBERG
  - PubChem
  - ICEBERG-WebUI
derived_from:
- doi: 10.1021/acs.analchem.3c04654
  title: ICEBERG / fragmentation graph generation
evidence_spans:
- You can run ICEBERG structural elucidation easily at http://iceberg-ms.mit.edu/
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
---

# spectrum-peak-matching

## Summary

Match experimental tandem mass spectrum peaks against predicted fragment-level spectra from candidate molecular structures to rank and identify the correct structure. This skill enables structure elucidation by comparing observed m/z peaks and intensities with in silico predictions from a machine learning model like ICEBERG.

## When to use

You have an experimental tandem mass spectrum (peaks with m/z values and intensities), a chemical formula, and a set of candidate molecular structures retrieved from a database like PubChem. You need to rank candidates by how well their predicted spectra match the observed spectrum to identify the most likely structure.

## When NOT to use

- Input spectrum has no annotated chemical formula or is from an unknown analyte class that was not part of model training (ICEBERG is trained on NIST'20 or MassSpecGym and may not generalize to novel compound classes).
- Candidate library is empty or contains fewer than 2 structures (ranking requires comparison; single structure validation is a different task).
- Spectrum is low-resolution or highly noise-dominated with few distinguishable peaks; fragment-level matching requires sufficient spectral quality.

## Inputs

- experimental mass spectrum (m/z and intensity pairs)
- chemical formula (molecular composition constraint)
- candidate molecular structures (SMILES or MOL format from PubChem)

## Outputs

- ranked list of candidate structures with matching scores
- predicted fragment-level spectrum for top-ranked candidate
- alignment or correspondence between observed and predicted peaks

## How to apply

First, load the experimental spectrum data (m/z and intensity values) and the candidate structures matching the chemical formula. For each candidate, use ICEBERG (or equivalent spectrum predictor) to generate a predicted spectrum at the level of molecular fragments—not just formula-level predictions. Compare the observed m/z peaks to the predicted fragment peaks by computing alignment or similarity metrics (e.g., cosine similarity or spectral matching score). Score each candidate based on how well its predicted peaks align with observed peaks in both position (m/z accuracy) and relative intensity. Rank candidates in descending order by matching score. The highest-ranking candidate whose predicted spectrum best matches the experimental spectrum is selected as the putative structure.

## Related tools

- **ICEBERG** (Neural spectrum prediction model that predicts fragment-level tandem mass spectra from molecular structures for comparison against experimental spectra) — https://github.com/coleygroup/ms-pred
- **PubChem** (Chemical structure database used to retrieve candidate molecules matching the given chemical formula)
- **ICEBERG-WebUI** (Web interface that automates the full structural elucidation workflow including candidate retrieval from PubChem and spectrum-based ranking) — http://iceberg-ms.mit.edu/

## Examples

```
python notebooks/iceberg_2025_biorxiv/iceberg_demo_pubchem_elucidation.ipynb (run Jupyter notebook demonstrating end-to-end ICEBERG structural elucidation with PubChem candidate ranking)
```

## Evaluation signals

- Top-ranked candidate matches the ground truth structure (if known) or has high confidence in literature or experimental validation.
- Predicted fragment peaks align with observed peaks: m/z positions match within tolerance (typically <5 ppm for high-resolution MS) and peak intensities show consistent relative patterns.
- Matching score for the top-ranked candidate is significantly higher than runners-up (e.g., top-1 retrieval accuracy reported at ~40% on NIST'20 for ICEBERG indicates correct structure ranked first in ~40% of cases).
- No contradictory peaks: observed peaks not explained by any predicted fragments from top candidate suggest alternative ranking should be considered.
- Predicted spectrum reproducibility: re-running the same candidate structure through ICEBERG yields identical or near-identical fragment predictions (deterministic model output).

## Limitations

- ICEBERG is trained on collision-induced dissociation (CID) spectra from NIST'20 (commercial, requires license) or MassSpecGym (open but less curated); performance on other ionization methods or spectral sources may degrade.
- Fragment-level predictions depend on the quality of the trained model; novel molecular scaffolds or functional groups not well-represented in training data may yield poor predictions.
- Requires accurate chemical formula input; formula misspecification (e.g., incorrect charge state or adduct) will retrieve wrong candidate set and cause ranking to fail.
- GPU acceleration is optional (CPU inference is feasible) but slower; batch processing of many candidates benefits from GPU memory (tested on NVIDIA RTX 4070M 8GB with batch_size=8 or RTX A5000 24GB).
- Top-1 retrieval accuracy on NIST'20 is ~40%; approximately 60% of experimental spectra do not have the correct structure ranked first, indicating false negatives in elucidation workflows.

## Evidence

- [other] Given a chemical formula and an experimental mass spectrum, how does ICEBERG rank candidate molecular structures retrieved from PubChem?: "Given a chemical formula and an experimental mass spectrum, how does ICEBERG rank candidate molecular structures retrieved from PubChem?"
- [other] ICEBERG predicts spectra at the level of molecular fragments, enabling spectrum-based ranking of PubChem candidates.: "ICEBERG predicts spectra at the level of molecular fragments, enabling spectrum-based ranking of PubChem candidates."
- [other] Run ICEBERG's ranking algorithm to score each candidate structure against the experimental spectrum by predicting fragment-level spectra and comparing to observed peaks.: "Run ICEBERG's ranking algorithm to score each candidate structure against the experimental spectrum by predicting fragment-level spectra and comparing to observed peaks."
- [intro] By inputting the chemical formula and your experimental spectrum, the WebUI will rank it against all candidates from PubChem.: "By inputting the chemical formula and your experimental spectrum, the WebUI will rank it against all candidates from PubChem."
- [intro] ICEBERG predicts spectra at the level of molecular fragments, whereas SCARF predicts spectra at the level of chemical formula.: "ICEBERG predicts spectra at the level of molecular fragments, whereas SCARF predicts spectra at the level of chemical formula."
- [readme] An example of how to use ICEBERG for structural elucidation campaigns can be found at notebooks/iceberg_2025_biorxiv/iceberg_demo_pubchem_elucidation.ipynb.: "An example of how to use ICEBERG for structural elucidation campaigns can be found at notebooks/iceberg_2025_biorxiv/iceberg_demo_pubchem_elucidation.ipynb."
- [readme] ICEBERG is our recommended model with a 40% top-1 retrieval accuracy with [M+H]+, benchmarked on the NIST'20 dataset.: "ICEBERG is our recommended model with a 40% top-1 retrieval accuracy with [M+H]+, benchmarked on the NIST'20 dataset."

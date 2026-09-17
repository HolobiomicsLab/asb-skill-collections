---
name: mass-spectrum-structure-elucidation
description: Use when you have an experimental tandem mass spectrum (collision-induced
  dissociation, CID) and a known chemical formula (or narrow set of candidate formulas),
  and you need to identify the most likely structure(s) by ranking against a large
  candidate library such as PubChem.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3802
  edam_topics:
  - http://edamontology.org/topic_0153
  - http://edamontology.org/topic_3172
  tools:
  - ICEBERG WebUI
  - PubChem
  - ms-pred (coleygroup)
  - MAGMa
  techniques:
  - LC-MS
  - NMR
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1038/s42256-024-00816-8
  title: ICEBERG
evidence_spans:
- You can run ICEBERG structural elucidation easily at http://iceberg-ms.mit.edu/
- By inputting the chemical formula and your experimental spectrum, the WebUI will
  rank it against all candidates from PubChem.
- the WebUI will rank it against all candidates from PubChem
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-spectrum-structure-elucidation

## Summary

Rank candidate molecular structures from a chemical formula library against experimental tandem mass spectra using neural fragment-level prediction and similarity scoring. This skill enables compound identification without requiring GPU resources when used via the ICEBERG WebUI.

## When to use

You have an experimental tandem mass spectrum (collision-induced dissociation, CID) and a known chemical formula (or narrow set of candidate formulas), and you need to identify the most likely structure(s) by ranking against a large candidate library such as PubChem. This is appropriate when spectroscopic or other evidence has narrowed the formula but structure remains ambiguous.

## When NOT to use

- The chemical formula is unknown or highly uncertain (formula must be input to query PubChem; use separate formula prediction if needed first).
- The experimental spectrum is low-quality, uninterpretable, or does not contain recognizable fragment peaks (ICEBERG ranking relies on fragment-level matching; very noisy or artifact-dominated spectra will degrade ranking quality).
- You require real-time or interactive refinement with GPU-accelerated re-prediction during iteration (the WebUI is optimized for single queries; large batch retrieval campaigns should use the command-line notebook interface with local compute resources).

## Inputs

- chemical formula (e.g., 'C8H10N4O2')
- experimental tandem mass spectrum (m/z values and intensities, typically in MGF or HDF5 format)
- optional: collision energy annotation

## Outputs

- ranked list of candidate structures (SMILES or InChI identifiers) with similarity scores
- predicted fragment-level mass spectra for top candidates
- export file containing structure IDs, similarity metrics, and ranked order

## How to apply

Input the chemical formula and experimental tandem mass spectrum into the ICEBERG WebUI (http://iceberg-ms.mit.edu/), which queries PubChem to retrieve all candidate structures matching the formula. ICEBERG predicts fragment-level mass spectra for each candidate by decomposing molecules into fragments via graph-based breakage events and estimating fragment intensities. Candidates are then ranked by cosine similarity (or equivalent spectral similarity metric) between predicted and experimental spectra. The ranked list with similarity scores is exported for manual review or further filtering. Fragment-level prediction, rather than chemical formula–level prediction alone, enables finer discrimination among isomers.

## Related tools

- **ICEBERG WebUI** (web interface for fragment-level mass spectrum prediction and PubChem candidate ranking without GPU requirement) — http://iceberg-ms.mit.edu/
- **ms-pred (coleygroup)** (source repository containing ICEBERG model code, training scripts, demo notebooks, and retrieval pipeline for local deployment and custom experiments) — https://github.com/coleygroup/ms-pred
- **PubChem** (candidate structure library queried by chemical formula to generate retrieval pool)
- **MAGMa** (algorithm used to annotate substructures and label fragmentation breakage process during ICEBERG model training)

## Examples

```
python notebooks/iceberg_2025_biorxiv/iceberg_demo_pubchem_elucidation.ipynb  # or visit http://iceberg-ms.mit.edu/ and input chemical formula and experimental spectrum
```

## Evaluation signals

- Top-ranked candidate structure matches the correct compound (identity known from reference standard or orthogonal confirmation method); typical top-1 retrieval accuracy on NIST'20 benchmark is ~40% for [M+H]+ ions.
- Predicted fragment m/z values and relative intensities for the top-ranked candidate show cosine similarity ≥ 0.7 with experimental spectrum (or domain-specific threshold), indicating good spectral match.
- Similarity score separation between top-ranked candidate and next-best candidate is substantial (≥ 0.1–0.2 on 0–1 cosine scale), reducing ambiguity.
- Exported ranked list can be manually reviewed; top-5 candidates include the true structure or chemically reasonable isomers that can be distinguished by orthogonal methods (NMR, chromatography, etc.).
- Execution completes within <2 minutes on standard hardware via WebUI, confirming no GPU bottleneck.

## Limitations

- Ranking accuracy is limited by PubChem coverage; compounds absent from PubChem cannot be ranked (commercial or unpublished compounds require custom structure library).
- Fragment-level prediction can struggle with unusual fragmentation patterns not well-represented in training data (NIST'20 and MassSpecGym datasets); very reactive or exotic functional groups may yield poor predictions.
- Collision energy (CE) information is beneficial; ICEBERG models trained on annotated datasets (e.g., NIST'20) will perform better than on data lacking CE metadata. MassSpecGym-trained weights show different performance due to less manual curation.
- Isomers with identical chemical formula and highly similar fragmentation patterns may receive similar scores; ranking cannot always distinguish constitutional or stereoisomers without orthogonal data.
- WebUI is optimized for single-query workflows; very large batch retrieval (thousands of spectra) should use local command-line interface with GPU to avoid web service latency and resource contention.

## Evidence

- [other] Given a chemical formula and experimental tandem mass spectrum, can the ICEBERG WebUI rank candidate structures from PubChem to support structural elucidation?: "Given a chemical formula and experimental tandem mass spectrum, can the ICEBERG WebUI rank candidate structures from PubChem to support structural elucidation?"
- [other] The ICEBERG WebUI enables structural elucidation by ranking PubChem candidates based on chemical formula and experimental spectrum input, without requiring GPU resources.: "The ICEBERG WebUI enables structural elucidation by ranking PubChem candidates based on chemical formula and experimental spectrum input, without requiring GPU resources."
- [other] Input the chemical formula and experimental mass spectrum into the ICEBERG WebUI at http://iceberg-ms.mit.edu/. The WebUI queries PubChem to retrieve all candidate structures matching the chemical formula. ICEBERG predicts fragment-level mass spectra for each candidate and ranks them by similarity to the experimental spectrum.: "Input the chemical formula and experimental mass spectrum into the ICEBERG WebUI at http://iceberg-ms.mit.edu/. The WebUI queries PubChem to retrieve all candidate structures matching the chemical"
- [intro] ICEBERG predicts spectra at the level of molecular fragments, whereas SCARF predicts spectra at the level of chemical formula.: "ICEBERG predicts spectra at the level of molecular fragments, whereas SCARF predicts spectra at the level of chemical formula."
- [readme] By inputting the chemical formula and your experimental spectrum, the WebUI will rank it against all candidates from PubChem.: "By inputting the chemical formula and your experimental spectrum, the WebUI will rank it against all candidates from PubChem."
- [readme] You can run ICEBERG structural elucidation easily at http://iceberg-ms.mit.edu/! ... No GPU is required.: "You can run ICEBERG structural elucidation easily at http://iceberg-ms.mit.edu/! ... No GPU is required."
- [readme] ICEBERG is trained in two parts: a learned fragment generator and an intensity predictor.: "ICEBERG is trained in two parts: a learned fragment generator and an intensity predictor."
- [readme] An example of how to use ICEBERG for structural elucidation campaigns can be found at ``notebooks/iceberg_2025_biorxiv/iceberg_demo_pubchem_elucidation.ipynb``.: "An example of how to use ICEBERG for structural elucidation campaigns can be found at ``notebooks/iceberg_2025_biorxiv/iceberg_demo_pubchem_elucidation.ipynb``."
- [readme] ICEBERG is our recommended model with a 40% top-1 retrieval accuracy with [M+H]+, benchmarked on the NIST'20 dataset.: "ICEBERG is our recommended model with a 40% top-1 retrieval accuracy with [M+H]+, benchmarked on the NIST'20 dataset."

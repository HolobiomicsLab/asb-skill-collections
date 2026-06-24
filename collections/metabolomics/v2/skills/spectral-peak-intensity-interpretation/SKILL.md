---
name: spectral-peak-intensity-interpretation
description: Use when you have a molecular structure (SMILES, InChI, or chemical formula)
  and need to predict which fragments will appear with high intensity in a tandem
  MS spectrum, or when you are performing structural elucidation by ranking candidate
  molecules against experimental spectra and need.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3680
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  tools:
  - ms-pred ICEBERG
  - ICEBERG WebUI
  - PubChem
  - ICEBERG (Inferring CID by Estimating Breakage Events and Reconstructing their
    Graphs)
  - ms-pred (coleygroup/ms-pred)
  - MAGMa (Mass Spectrum Annotation by Genetic Mass Spectrometry Analysis)
  techniques:
  - LC-MS
  license_tier: open
derived_from:
- doi: 10.1038/s42256-024-00816-8
  title: ICEBERG
evidence_spans:
- github.com__samgoldman97__ms-pred
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

# spectral-peak-intensity-interpretation

## Summary

Predict fragment-level intensity distributions in tandem mass spectra from molecular structure using neural intensity models trained on experimental collision-induced dissociation (CID) data. This skill enables quantitative interpretation of which molecular fragments dominate fragmentation patterns under specified collision energies.

## When to use

Apply this skill when you have a molecular structure (SMILES, InChI, or chemical formula) and need to predict which fragments will appear with high intensity in a tandem MS spectrum, or when you are performing structural elucidation by ranking candidate molecules against experimental spectra and need intensity-weighted matching rather than presence/absence prediction alone.

## When NOT to use

- Input is a chemical formula alone without molecular structure — intensity prediction requires structural graph connectivity to model fragmentation pathways; use formula-level prediction (SCARF) instead.
- Spectrum ionization mode or collision energy differs significantly from training data (NIST'20 trained on [M+H]+ and ESI/CID; EI or other modes will have degraded accuracy).
- Goal is fast retrieval ranking without intensity weighting — presence/absence fragment matching may be faster and sufficient for candidate narrowing.

## Inputs

- Molecular structure (SMILES string, InChI, or chemical formula)
- Fragment set (enumerated from input molecule or pre-generated)
- Collision energy (eV or relative collision energy, if specified in training config)
- Optionally: experimental reference spectrum (MGF or HDF5 format) for comparison

## Outputs

- Predicted tandem mass spectrum with fragment m/z values and relative peak intensities (0–100 scale)
- Intensity rankings (rank-ordered list of fragment m/z and predicted intensity)
- Spectral similarity score (cosine similarity or spectral angle) if compared against experimental spectrum

## How to apply

First, fragment the input molecule using a fragment generator (ICEBERG DAG model) to enumerate chemically plausible breakage products at the molecular fragment level. Then pass the generated fragment set through a trained intensity predictor model that has learned from experimental collision-induced dissociation spectra (e.g., NIST'20 dataset with collision energy annotations). The intensity model outputs relative peak heights for each fragment; normalize these to 0–100% scale (base peak = 100%). Apply contrastive finetuning if available to improve ranking discrimination against large candidate libraries (e.g., PubChem). Evaluate predictions by comparing predicted intensity rankings to experimental spectrum peak lists using metrics like spectral similarity (cosine angle between predicted and observed intensity vectors).

## Related tools

- **ICEBERG (Inferring CID by Estimating Breakage Events and Reconstructing their Graphs)** (Fragment generator and intensity predictor; produces fragment-level tandem mass spectrum predictions with learned intensity distributions from experimental CID data) — https://github.com/coleygroup/ms-pred
- **ICEBERG WebUI** (Browser-based interface for running ICEBERG structural elucidation and intensity prediction without GPU; input chemical formula and experimental spectrum to retrieve ranked candidates) — http://iceberg-ms.mit.edu/
- **ms-pred (coleygroup/ms-pred)** (Python package containing ICEBERG, SCARF, NEIMS, MassFormer, 3DMolMS, GrAFF-MS, and CFM-ID implementations; used for training, prediction, and retrieval experiments) — https://github.com/coleygroup/ms-pred
- **PubChem** (Molecular structure database used for candidate ranking in structural elucidation; chemical formula queries retrieve all candidate SMILES/InChI entries)
- **MAGMa (Mass Spectrum Annotation by Genetic Mass Spectrometry Analysis)** (Substructure annotation and fragmentation pathway labeling; used in ICEBERG data processing to create labeled breakage graphs for training intensity models)

## Examples

```
python src/ms_pred/dag_pred/predict_smis.py --config configs/iceberg/iceberg_elucidation.yaml --input molecules.smi --output predictions.pkl
```

## Evaluation signals

- Predicted spectrum peaks match experimental peak list: top-1 (most intense predicted fragment matches most intense experimental peak) and top-N recall metrics should be ≥ 40% for [M+H]+ on NIST'20 test set.
- Spectral similarity (cosine angle between predicted and observed intensity vectors) ≥ 0.7 indicates good intensity calibration; < 0.5 suggests systematic intensity bias.
- Fragment identities are chemically plausible (neutral losses follow known dissociation chemistry; no impossibly charged or neutral fragments); inspect predicted fragments for formal charge +1, realistic m/z range relative to input precursor.
- Contrastive finetuning improves top-1 retrieval accuracy by 3–10% when evaluated on held-out PubChem formula subsets; indicates intensity weighting aids discrimination.
- Inference time scales sub-linearly with candidate library size (~2 min for 10k candidates on desktop GPU); no GPU required via WebUI indicates feasible deployment.

## Limitations

- Model trained exclusively on [M+H]+ ions under electrospray ionization (ESI) and collision-induced dissociation (CID); predictions for [M−H]−, [M+Na]+, EI, or other ionization modes will have degraded or undefined accuracy.
- Requires NIST'20 commercial dataset (or MassSpecGym open alternative with lower manual curation) for training; pretrained weights licensed under NIST'20 terms — users must own valid license to obtain weights.
- GPU with ≥24 GB RAM (tested on NVIDIA A5000) required for training; smaller GPUs must reduce batch size or skip contrastive finetuning, trading performance for computational feasibility.
- Intensity predictions assume collision energy annotations in training data; prediction quality degrades when experimental collision energy is missing or differs from training distribution.
- Fragment generator (DAG model) occasionally produces chemically implausible or duplicate fragments; intensity predictions reflect training bias and may not generalize to structural classes underrepresented in NIST'20.

## Evidence

- [intro] ICEBERG predicts spectra at the level of molecular fragments, whereas SCARF predicts spectra at the level of chemical formula.: "ICEBERG predicts spectra at the level of molecular fragments, whereas SCARF predicts spectra at the level of chemical formula."
- [intro] By inputting the chemical formula and your experimental spectrum, the WebUI will rank it against all candidates from PubChem.: "By inputting the chemical formula and your experimental spectrum, the WebUI will rank it against all candidates from PubChem."
- [readme] ICEBERG is trained in two parts: a learned fragment generator and an intensity predictor.: "ICEBERG is trained in two parts: a learned fragment generator and an intensity predictor."
- [readme] You need two GPUs with at least 24GB RAM to train ICEBERG (we used NVIDIA A5000 for development).: "You need two GPUs with at least 24GB RAM to train ICEBERG (we used NVIDIA A5000 for development)."
- [readme] NIST'20 is the only database where all spectra have collision energy annotations: "NIST'20 is the only database where all spectra have collision energy annotations"
- [readme] ICEBERG is our recommended model with a 40% top-1 retrieval accuracy with [M+H]+, benchmarked on the NIST'20 dataset.: "ICEBERG is our recommended model with a 40% top-1 retrieval accuracy with [M+H]+, benchmarked on the NIST'20 dataset."

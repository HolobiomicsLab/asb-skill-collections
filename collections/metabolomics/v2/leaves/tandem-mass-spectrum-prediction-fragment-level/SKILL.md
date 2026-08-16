---
name: tandem-mass-spectrum-prediction-fragment-level
description: Use when you have a molecular structure (SMILES, InChI, or chemical formula)
  and need to predict its collision-induced dissociation (CID) tandem mass spectrum
  with fragment-level resolution. Use this when chemical-formula-level predictions
  (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3634
  edam_topics:
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_3172
  tools:
  - ms-pred ICEBERG
  - ICEBERG WebUI
  - PubChem
  - ms-pred (coleygroup/ms-pred)
  - MAGMa algorithm
  - NIST'20 dataset
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

# tandem-mass-spectrum-prediction-fragment-level

## Summary

Use the ICEBERG model to predict tandem mass spectra at the level of molecular fragments, decomposing a query molecule into fragment structures and intensity estimates rather than chemical formulas alone. This enables more granular structural elucidation and retrieval-based compound identification.

## When to use

You have a molecular structure (SMILES, InChI, or chemical formula) and need to predict its collision-induced dissociation (CID) tandem mass spectrum with fragment-level resolution. Use this when chemical-formula-level predictions (e.g., SCARF) are insufficient and you need to rank candidate compounds from a library (e.g., PubChem) or interpret fragmentation patterns at substructural detail for structural elucidation campaigns.

## When NOT to use

- If you only need chemical-formula-level predictions (no substructural detail), use SCARF instead, as it is more lightweight and formula-agnostic.
- If your input is already an experimental tandem mass spectrum and you need to identify the compound directly without prediction, use retrieval matching or database search rather than prediction.
- If you lack pretrained model weights and cannot obtain them (requires NIST'20+ license or MassSpecGym public weights), local training requires two GPUs with ≥24 GB RAM each and significant computational time.

## Inputs

- molecular structure (SMILES string)
- molecular structure (InChI string)
- chemical formula
- configuration file (YAML) specifying model checkpoint paths, batch size, GPU devices

## Outputs

- predicted tandem mass spectrum (m/z peaks and intensities)
- fragment assignments (SMILES or InChI for each peak)
- retrieval ranking against reference library (e.g., PubChem candidates ranked by cosine similarity or spectral matching)

## How to apply

Input a molecular structure via the ICEBERG WebUI (http://iceberg-ms.mit.edu/) or via local Python API using the ms-pred repository. The ICEBERG pipeline internally trains a learned fragment generator to propose molecular substructures and their cleavage graph, then uses an intensity predictor (including optional contrastive finetuning on PubChem-SMILES mappings) to estimate peak intensities for each fragment. The model outputs predicted spectrum peaks annotated with fragment SMILES/InChI assignments and intensity values. For GPU-constrained environments, batch size and worker counts can be reduced (e.g., batch_size=8, num_workers=6 on 8GB RAM), or CPU-only inference is feasible by setting cuda_devices=None in the config file. Evaluate retrieval accuracy (top-1 hit rate) on held-out test sets or validate against experimental spectra.

## Related tools

- **ICEBERG WebUI** (user-friendly interface for fragment-level tandem mass spectrum prediction without local GPU or coding) — http://iceberg-ms.mit.edu/
- **ms-pred (coleygroup/ms-pred)** (core Python package implementing ICEBERG fragment generator, intensity predictor, and retrieval pipeline; supports local training and inference) — https://github.com/coleygroup/ms-pred
- **PubChem** (library of chemical structures and reference for retrieval-based structural elucidation; provides formula-to-(SMILES, InChIKey) mappings)
- **MAGMa algorithm** (annotates substructures and labels the molecular breakage process (directed acyclic graph) for ICEBERG training)
- **NIST'20 dataset** (commercial reference spectra with collision energy annotations; used for training and benchmarking ICEBERG (40% top-1 retrieval accuracy reported))

## Examples

```
python src/ms_pred/dag_pred/predict_smis.py --config configs/iceberg/iceberg_elucidation.yaml --smiles 'CC(=O)Oc1ccccc1C(=O)O' --output predictions.json
```

## Evaluation signals

- Top-1 retrieval accuracy on held-out test sets (ICEBERG achieves ~40% on NIST'20 [M+H]+ ions); higher accuracy indicates correct fragment and intensity predictions.
- Cosine similarity between predicted and experimental spectra (peaks and intensities); threshold of >0.7 indicates good match.
- Fragment assignments are chemically plausible: each predicted m/z corresponds to a valid substructure of the input molecule with no negative masses or impossible neutral losses.
- No GPU is required for WebUI inference; CPU-only predictions should complete in <2 minutes on a regular desktop.
- Predicted spectrum peaks fall within the mass-to-charge ratio range expected for the parent ion and plausible fragments (e.g., no peaks exceed parent m/z).

## Limitations

- Pretrained model weights require either a commercial NIST'20+ license or use of the public MassSpecGym weights (which have undergone less manual curation than NIST and will yield different predictions).
- Training ICEBERG from scratch requires two GPUs with ≥24 GB RAM each (e.g., NVIDIA A5000); smaller GPUs require batch size reduction and may skip contrastive finetuning, affecting performance.
- Fragment-level predictions depend on accurate MAGMa annotation of the molecular breakage process during training; errors in substructure labeling propagate to inference.
- Model predictions are collision-energy-dependent; prediction accuracy may vary across different ionization methods or collision energies not well represented in the training set.
- Retrieval performance degrades when query molecules are significantly different from training set chemistry or when the reference library (e.g., PubChem) does not contain true candidates.

## Evidence

- [intro] ICEBERG predicts spectra at the level of molecular fragments, whereas SCARF predicts spectra at the level of chemical formula.: "ICEBERG predicts spectra at the level of molecular fragments, whereas SCARF predicts spectra at the level of chemical formula."
- [readme] You can run ICEBERG structural elucidation easily at http://iceberg-ms.mit.edu/. By inputting the chemical formula and your experimental spectrum, the WebUI will rank it against all candidates from PubChem. No GPU is required.: "You can run ICEBERG structural elucidation easily at http://iceberg-ms.mit.edu/! By inputting the chemical formula and your experimental spectrum, the WebUI will rank it against all candidates from"
- [readme] ICEBERG is our recommended model with a 40% top-1 retrieval accuracy with [M+H]+, benchmarked on the NIST'20 dataset.: "ICEBERG is our recommended model with a 40% top-1 retrieval accuracy with [M+H]+, benchmarked on the NIST'20 dataset."
- [readme] You need two GPUs with at least 24GB RAM to train ICEBERG. If you are trying to train the model on a smaller GPU, try cutting down the batch size.: "You need two GPUs with at least 24GB RAM to train ICEBERG (we used NVIDIA A5000 for development). If you are trying to train the model on a smaller GPU, try cutting down the batch size"
- [readme] ICEBERG is trained in two parts: a learned fragment generator and an intensity predictor.: "ICEBERG is trained in two parts: a learned fragment generator and an intensity predictor. The pipeline for training and evaluating this model can be accessed in `run_scripts/iceberg/`."
- [readme] To train ICEBERG, we must annotate substructures and create a labeled dataset over the breakage process, which we do with the MAGMa algorithm.: "In addition to building processed subformulae, to train ICEBERG, we must annotate substructures and create a labeled dataset over the breakage process, which we do with the MAGMa algorithm."

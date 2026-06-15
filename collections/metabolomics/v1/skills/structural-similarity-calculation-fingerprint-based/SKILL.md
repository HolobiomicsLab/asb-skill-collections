---
name: structural-similarity-calculation-fingerprint-based
description: Use when you have a set of compounds (e.g., novel NPS analogues in an evaluation dataset) and need to classify them as structurally similar to or divergent from a reference set (e.g., training compounds).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3672
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3373
  - http://edamontology.org/topic_0209
  tools:
  - RDKit or similar cheminformatics library for molecular fingerprint computation
  - Matplotlib or Seaborn for visualization
  - RDKit
  - Pandas
  - Matplotlib or Seaborn
  - PyTorch or TensorFlow
derived_from:
- doi: 10.1021/acs.analchem.3c05019
  title: ps2ms
evidence_spans:
- structurally diverse or novel NPS analogues
- prediction confidence scores vary across
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ps2ms
    doi: 10.1021/acs.analchem.3c05019
    title: ps2ms
  dedup_kept_from: coll_ps2ms
schema_version: 0.2.0
---

# Structural Similarity Calculation (Fingerprint-Based)

## Summary

Compute pairwise structural similarity between compounds using molecular fingerprints (e.g., ECFP, Tanimoto) to stratify evaluation sets by novelty relative to training data. This skill is essential for assessing whether a deep learning model's confidence varies predictably with structural distance from known compounds.

## When to use

Apply this skill when you have a set of compounds (e.g., novel NPS analogues in an evaluation dataset) and need to classify them as structurally similar to or divergent from a reference set (e.g., training compounds). Use it before aggregating model predictions by novelty stratum, or when validating whether a model's uncertainty correlates with the degree of structural extrapolation.

## When NOT to use

- When structural information is unavailable or unreliable (e.g., poorly curated SMILES, ambiguous stereochemistry).
- When the novelty stratification goal is unrelated to your analysis (e.g., purely clustering compounds by activity class rather than training-set distance).
- When computational cost of pairwise fingerprint comparison prohibits large-scale evaluation (>100k compounds); consider approximations like locality-sensitive hashing instead.

## Inputs

- Molecular structures (SMILES strings, SDF files, or InChI codes)
- Reference compound set (training set structures)
- Evaluation compound set (test or novel analogue structures)
- Fingerprint parameters (e.g., ECFP radius, bit length)

## Outputs

- Pairwise similarity matrix (compounds × reference compounds)
- Per-compound maximum similarity scores
- Stratified compound lists by novelty category (bins)
- Summary statistics (mean, median, std similarity per stratum)
- Visualization (box plots, violin plots of similarity by novelty class)

## How to apply

First, generate molecular fingerprints (e.g., ECFP or similar) for all compounds in both the reference (training) and query (evaluation) sets using a cheminformatics library. Then, compute pairwise Tanimoto similarity scores between each evaluation compound and all reference compounds, selecting the maximum similarity as the compound's structural proximity metric. Stratify evaluation compounds into novelty bins (e.g., high similarity: >0.8, moderate: 0.6–0.8, novel: <0.6) based on this threshold. Finally, aggregate downstream metrics (e.g., prediction confidence scores, detection accuracy) within each stratum to reveal whether model performance degrades gracefully with structural novelty. The rationale is that fingerprint-based similarity captures chemical space distance, allowing you to test whether the model exhibits expected behavior on in-distribution versus out-of-distribution compounds.

## Related tools

- **RDKit** (Compute molecular fingerprints (e.g., ECFP) and Tanimoto similarity scores from SMILES or SDF structures) — https://www.rdkit.org/docs/Install.html
- **Pandas** (Tabular data manipulation, aggregation of similarity scores and statistics by novelty stratum)
- **Matplotlib or Seaborn** (Visualize similarity distributions and prediction metrics across novelty categories using box plots and violin plots)
- **PyTorch or TensorFlow** (Load and run the deep learning model (e.g., PS2MS) to extract prediction confidence scores for compounds in each novelty stratum)

## Examples

```
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit import DataStructs
import pandas as pd

# Load training and evaluation SMILES
train_mols = [Chem.MolFromSmiles(smi) for smi in train_smiles]
eval_mols = [Chem.MolFromSmiles(smi) for smi in eval_smiles]

# Compute ECFP fingerprints
train_fps = [AllChem.GetMorganFingerprintAsBitVect(m, 2, nBits=2048) for m in train_mols]
eval_fps = [AllChem.GetMorganFingerprintAsBitVect(m, 2, nBits=2048) for m in eval_mols]

# Compute max Tanimoto similarity per eval compound
sims = [max([DataStructs.TanimotoSimilarity(ef, tf) for tf in train_fps]) for ef in eval_fps]

# Stratify by novelty: novel (<0.6), moderate (0.6–0.8), similar (>0.8)
novelty = pd.cut(sims, bins=[0, 0.6, 0.8, 1.0], labels=['novel', 'moderate', 'similar'])
print(novelty.value_counts())
```

## Evaluation signals

- Fingerprints are computed without errors or missing values for all compounds in the reference and evaluation sets.
- Similarity scores lie in the expected range [0, 1] (or [0, 100] depending on normalization) with no NaN or infinite values.
- Stratified compound counts per novelty bin are reasonable (e.g., no single stratum contains <5 compounds unless dataset is very small).
- Prediction confidence scores (e.g., softmax probabilities) exhibit an expected trend: mean confidence decreases or uncertainty increases as maximum structural similarity decreases across novelty strata.
- Summary statistics table shows non-zero variance within and between strata, and visual plots (box/violin) clearly distinguish distributions by stratum.

## Limitations

- Fingerprint-based similarity does not capture all aspects of chemical similarity (e.g., 3D shape, electrostatics, biological activity); compounds with high fingerprint similarity may have very different pharmacology.
- Tanimoto similarity is symmetric and does not account for directionality of structural novelty (e.g., does not distinguish whether novel compound is a conservative substitution versus a scaffold hop).
- Threshold choice for novelty bins (e.g., 0.8, 0.6) is arbitrary and dataset-dependent; results are sensitive to binning boundaries, so sensitivity analysis is recommended.
- Fingerprint algorithm (ECFP vs. MACCS, radius, bit length) significantly affects similarity distributions; consistent choice across the workflow is critical but often requires domain knowledge.

## Evidence

- [other] Stratify evaluation compounds by structural similarity to training set compounds using molecular fingerprints (e.g., Tanimoto similarity or ECFP) to classify analogues as structurally similar or novel.: "Stratify evaluation compounds by structural similarity to training set compounds using molecular fingerprints (e.g., Tanimoto similarity or ECFP) to classify analogues as structurally similar or"
- [other] Aggregate confidence scores by structural novelty stratum and compute distributional statistics (mean, median, std, min, max, quartiles).: "Aggregate confidence scores by structural novelty stratum and compute distributional statistics (mean, median, std, min, max, quartiles)."
- [other] Visualize confidence score distributions across novelty categories using box plots or violin plots and produce a summary table of score statistics stratified by structural diversity.: "Visualize confidence score distributions across novelty categories using box plots or violin plots and produce a summary table of score statistics stratified by structural diversity."
- [other] RDKit or similar cheminformatics library for molecular fingerprint computation: "RDKit or similar cheminformatics library for molecular fingerprint computation"
- [readme] The system leverages two deep learning tools, NEIMS and DeepEI, to generate mass spectra and chemical fingerprints, respectively.: "The system leverages two deep learning tools, NEIMS and DeepEI, to generate mass spectra and chemical fingerprints, respectively."

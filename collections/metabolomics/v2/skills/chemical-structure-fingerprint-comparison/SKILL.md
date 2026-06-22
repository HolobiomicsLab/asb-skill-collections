---
name: chemical-structure-fingerprint-comparison
description: Use when when you have MS/MS spectra with known chemical structures (InChIKeys or SMILES) and want to validate whether a novel or existing spectral similarity scoring method actually reflects true chemical structural similarity.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3802
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3172
  tools:
  - matchms
  - gensim
  - Numba
  - Pandas
  - scipy
  - Spec2Vec
  - Word2Vec / gensim
  - PubChem
  - Pandas / NumPy / SciPy
  techniques:
  - LC-MS
  - GC-MS
derived_from:
- doi: 10.1371/journal.pcbi.1008724
  title: Spec2Vec
evidence_spans:
- the implementations for the cosine score and the modified cosine score used can be found in the Python package matchms
- the implementations for the cosine score and the modified cosine score used can be found in the Python package matchms [31] (https://github.com/matchms/matchms)
- A Word2Vec [22] model is trained on all documents of a chosen dataset using gensim [37]
- making extensive use of Numpy [24] and Numba [25]
- by making extensive use of Numpy [24] and Numba [25], the library
- Spec2Vec was optimised by making extensive use of Numpy [24] and Numba [25], the library matching was implemented using Pandas [40]
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: spec2vec_grounded
    doi: 10.1371/journal.pcbi.1008724
    title: Spec2Vec
  dedup_kept_from: spec2vec_grounded
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1371/journal.pcbi.1008724
  all_source_dois:
  - 10.1371/journal.pcbi.1008724
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Chemical Structure Fingerprint Comparison

## Summary

Compare MS/MS spectra to chemical structure similarity using molecular fingerprints (e.g., Tanimoto-based) as a ground-truth benchmark for validating spectral similarity methods. This skill evaluates whether a spectral similarity metric (cosine, Spec2Vec, etc.) correlates with true structural relationships derived from InChIKey planar structure matching.

## When to use

When you have MS/MS spectra with known chemical structures (InChIKeys or SMILES) and want to validate whether a novel or existing spectral similarity scoring method actually reflects true chemical structural similarity. Use this when you need to distinguish between high spectral similarity driven by genuine chemical relationships versus false positives from spectral coincidence.

## When NOT to use

- Spectra lack chemical structure annotation (InChIKey or SMILES) — fingerprint-based ground truth cannot be established.
- Your goal is spectrum-to-spectrum retrieval speed optimization; fingerprint comparison is a validation tool, not a retrieval acceleration method.
- You are working with GC-MS data and need to include neutral losses in the similarity metric; the article explicitly notes Spec2Vec has not been validated on GC-MS because neutral losses are not typically measured in that modality.

## Inputs

- MS/MS spectra collection with precursor m/z and fragment peaks
- InChIKey annotations (or SMILES) for compound structures
- Spectral similarity score matrices (cosine, modified cosine, Spec2Vec, or other methods)
- Molecular structure database (e.g., PubChem for fingerprint computation)

## Outputs

- ROC curves for each spectral similarity method
- True-positive and false-positive rate tables at defined thresholds
- Area-under-curve (AUC) comparison metrics
- Correlation coefficients between spectral and fingerprint-based similarity
- Classification tables (true positives vs. false positives per method)

## How to apply

Obtain or compute molecular fingerprints (e.g., Tanimoto-based structural similarity) for all compound pairs in your reference library using PubChem lookups or in-silico structure databases. Separately compute spectral similarity scores (cosine, modified cosine, Spec2Vec, etc.) for the same spectra pairs. Annotate spectral pairs as true positives (matching InChIKey within first 14 characters / planar structure) or false positives (non-matching structure). Construct receiver-operator-characteristic (ROC) curves plotting true-positive rate versus false-positive rate at multiple similarity thresholds for each spectral method. Calculate area-under-curve (AUC) and compare correlation coefficients between fingerprint-derived structural similarity and each spectral score to determine which method best predicts true chemical relationships.

## Related tools

- **matchms** (Compute cosine and modified cosine spectral similarity scores; import and process MS/MS spectra from mzML, mzXML, msp, MGF, and JSON formats) — https://github.com/matchms/matchms
- **Spec2Vec** (Compute spectral similarity scores using learned embeddings (Word2Vec-based) of fragment ions and neutral losses for comparison against fingerprint-based ground truth) — https://github.com/iomega/spec2vec
- **Word2Vec / gensim** (Train and apply embedding models to learn relationships between mass fragments and neutral losses in spectral data)
- **PubChem** (Retrieve molecular structures and compute or retrieve pre-computed structural fingerprints for chemical structure comparison)
- **Pandas / NumPy / SciPy** (Organize spectral metadata (InChIKey, m/z), construct ROC curves, compute AUC and correlation statistics)

## Examples

```
from matchms import Spectrum
from matchms.similarity import CosineGreedy, ModifiedCosine
from spec2vec import Spec2Vec
from sklearn.metrics import roc_curve, auc
import numpy as np

# Compute spectral similarities and fingerprint-based structural similarity (from PubChem Tanimoto)
cos_scores = [CosineGreedy().pair(spec1, spec2) for (spec1, spec2) in spectrum_pairs]
mod_cos_scores = [ModifiedCosine().pair(spec1, spec2) for (spec1, spec2) in spectrum_pairs]
spec2vec_scores = [Spec2Vec(model).pair(spec1, spec2) for (spec1, spec2) in spectrum_pairs]
true_labels = [1 if spec1.metadata['inchikey'][:14] == spec2.metadata['inchikey'][:14] else 0 for (spec1, spec2) in spectrum_pairs]

# Construct ROC curves
for scores, label in [(cos_scores, 'Cosine'), (spec2vec_scores, 'Spec2Vec')]:
    fpr, tpr, _ = roc_curve(true_labels, scores)
    roc_auc = auc(fpr, tpr)
    print(f'{label} AUC: {roc_auc:.3f}')
```

## Evaluation signals

- ROC curves for fingerprint-based structural similarity show AUC ≥ 0.80, indicating the ground-truth classification (true vs. false positives) is well-separated at most thresholds.
- Spec2Vec or novel method shows statistically higher AUC and true-positive rate at equivalent false-positive thresholds compared to cosine or modified cosine (e.g., 88% accuracy reported in the article).
- Correlation coefficient between high spectral similarity scores and high fingerprint-based structural similarity is positive and substantial (r > 0.6); conversely, cosine methods show lower correlation, confirming that spectral coincidence is decoupled from true chemical similarity.
- Classification confusion matrix shows few false positives (non-matching InChIKeys misclassified as true matches) at the chosen similarity threshold, indicating the spectral method reliably ranks true structural analogues above unrelated spectra.
- Replicate validation on held-out subset of spectra (e.g., 'query' spectra removed from training) produces consistent AUC and true/false-positive ratio estimates.

## Limitations

- Fingerprint-based ground truth requires high-quality, complete chemical structure annotation (InChIKey or SMILES). Missing or incorrect annotations will bias validation results.
- Planar InChIKey matching (first 14 characters) may group structural isomers with identical connectivity but different stereochemistry, potentially conflating true positives with structural variants.
- Spec2Vec requires retraining on large reference datasets to learn fragment relationships; pre-trained models may have poor coverage of novel or rare fragments not present in the training set, limiting applicability to new experimental data.
- Comparison is demonstrated on positive ionization mode LC-MS data only; neutral losses are not reliably measured in GC-MS, so this validation workflow may not apply to gas-phase data without significant method adaptation.
- ROC curve construction assumes a single optimal threshold exists across all compound classes; in practice, optimal similarity thresholds may vary by chemical family (e.g., lipids vs. alkaloids), limiting the generalizability of a global cutoff.

## Evidence

- [other] Spec2Vec resulted in a notably better true/false positive ratio at all thresholds compared to cosine and modified cosine scores during library matching: "Spec2Vec resulted in a notably better true/false positive ratio at all thresholds compared to cosine and modified cosine scores during library matching, achieving up to 88% accuracy and higher"
- [results] Spec2Vec similarity correlates stronger with structural similarity than cosine or modified cosine scores: "high Spec2Vec spectrum similarity score correlates stronger with structural similarity than the cosine or modified cosine scores"
- [other] For each similarity method, rank query spectra against library and classify hits as true positives or false positives: "For each similarity method, rank query spectra against library and classify hits as true positives (matching InChIKey within first 14 characters / planar structure) or false positives (non-matching"
- [results] High false positive rates in cosine and modified cosine similarity scores largely explain poorer correlation with structural similarity: "The poorer correlation between cosine and modified cosine similarity and structural similarity can largely be explained by high false positive rates"
- [discussion] Spec2Vec requires training data and may need retraining on new experimental spectra not covered in initial training set: "one limitation of Spec2Vec as compared to cosine scores is that it needs training data to learn the fragment peak relationships; however, since this not necessarily needs to be library spectra and in"
- [discussion] Spec2Vec performance has only been demonstrated on LC-MS data, not yet assessed for GC-MS where neutral losses are usually not measured: "In the present work, we have only demonstrated performance on LC-MS data and not yet assessed Spec2Vec for GC-MS data. For GC-MS, neutral losses are usually not measured."

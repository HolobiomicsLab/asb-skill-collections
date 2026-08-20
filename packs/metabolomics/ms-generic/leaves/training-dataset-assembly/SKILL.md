---
name: training-dataset-assembly
description: Use when when you have a large list of SMILES strings but lack corresponding experimental mass spectra, and you need to generate 30,000+ training pairs to train a deep learning model for molecular structure prediction.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3172
  tools:
  - Python 3.7
  - CFM-ID
  - Python
  - PyTorch
  techniques:
  - mass-spectrometry
derived_from:
- doi: 10.1038/s42256-025-01140-5
  title: MSGo
evidence_spans:
- 'Python: 3.7'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_msgo_cq
    doi: 10.1038/s42256-025-01140-5
    title: MSGo
  dedup_kept_from: coll_msgo_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s42256-025-01140-5
  all_source_dois:
  - 10.1038/s42256-025-01140-5
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# training-dataset-assembly

## Summary

Assemble large-scale pseudo SMILES-spectrum pairs from raw SMILES lists using in silico fragmentation prediction (CFM-ID) to create training data for molecular structure generation models. This skill is essential when labeled experimental spectra are limited but raw chemical structure databases are available.

## When to use

When you have a large list of SMILES strings but lack corresponding experimental mass spectra, and you need to generate 30,000+ training pairs to train a deep learning model for molecular structure prediction. Particularly relevant when real experimental spectra are expensive, time-consuming to acquire, or limited in diversity (e.g., <300 real spectra available for model validation).

## When NOT to use

- When you already have 300+ high-quality experimental spectra; real spectra should be prioritized for validation and serve as ground truth rather than replaced by pseudo-data.
- When the chemical space of your SMILES list is drastically different from your evaluation spectra (e.g., training on general organic molecules but evaluating on PFAS or lipids); pseudo-data generation will not bridge this domain gap.
- When CFM-ID parameters (ionization mode, collision energy) do not match the experimental conditions of your evaluation dataset; the pseudo spectra will be misaligned with real data.

## Inputs

- Raw SMILES list file (text or CSV with SMILES strings, one per line)
- CFM-ID parameter configuration (ionization mode, collision energy, fragmentation rules)

## Outputs

- Aggregated pseudo SMILES-spectrum pair dataset (≥30,000 pairs)
- Dataset file format compatible with PyTorch DataLoader (e.g., .pkl or .csv with SMILES and spectrum columns)
- Dataset validation report (pair count, schema integrity checks)

## How to apply

Load raw SMILES strings from an input file and invoke CFM-ID to generate in silico mass spectra with fragmentation patterns for each structure. Pair each input SMILES with its CFM-ID-generated spectrum to create pseudo SMILES-spectrum pairs. Aggregate all pairs into a single training dataset file, accumulating at least 30,000+ pairs to provide sufficient diversity and scale for deep learning. Validate the output dataset by confirming: (1) the file contains the expected number of pairs (≥30k), (2) each pair includes both a valid SMILES string and a corresponding spectrum representation (format suitable for torch.nn input), and (3) spectrum distributions match expected fragmentation characteristics. Use Python 3.7 with PyTorch 1.7.1 for downstream model compatibility.

## Related tools

- **CFM-ID** (In silico mass spectra generation from SMILES; produces fragmentation patterns and spectrum predictions for each molecular structure)
- **Python** (Orchestration and aggregation; iterate over SMILES list, invoke CFM-ID, pair results, validate output dataset)
- **PyTorch** (Data format compatibility and downstream model training; ensures pseudo pairs can be loaded into MSGO or similar neural network architectures) — https://github.com/aaronma2020/MSGO

## Examples

```
# Load raw SMILES, generate spectra with CFM-ID, and aggregate pairs:
for smiles in open('raw_smiles.txt'):
    spectrum = cfmid_predict(smiles.strip(), ionization='neg')
    pseudo_pairs.append({'SMILES': smiles.strip(), 'spectrum': spectrum})
import pickle
with open('training_data_30k.pkl', 'wb') as f:
    pickle.dump(pseudo_pairs, f)
print(f'Generated {len(pseudo_pairs)} pseudo SMILES-spectrum pairs')
```

## Evaluation signals

- Output dataset file contains ≥30,000 SMILES-spectrum pairs with no null entries or malformed SMILES strings.
- Each spectrum entry is a valid numeric array or tensor representation compatible with torch.nn models, with consistent dimensionality across all pairs.
- SMILES strings in output pairs are identical to input SMILES strings (verify by checksum or line-by-line comparison).
- Spectrum fragmentation patterns follow expected mass-to-charge (m/z) distributions and peak intensities consistent with CFM-ID predicted fragmentation rules for the corresponding molecular structures.
- Dataset file can be successfully loaded and iterated by a PyTorch DataLoader without shape or type errors when used in the training pipeline (test with `python tools/train.py --id all_trick`).

## Limitations

- CFM-ID-generated spectra are in silico predictions and may not capture all real-world fragmentation complexity, especially for novel or unusual structural motifs. Pseudo-data is best used for pre-training or data augmentation, not as sole training source.
- Assembly quality depends critically on CFM-ID parameter choices (ionization mode, collision energy); mismatch between pseudo-data generation settings and evaluation dataset experimental conditions will degrade model performance.
- Requires valid SMILES strings as input; malformed or invalid SMILES will cause CFM-ID to fail or produce empty spectra. Pre-validation of input SMILES is recommended.
- Computational cost scales linearly with number of SMILES; generating 30,000+ spectra via CFM-ID can be time-intensive; parallelization or batch processing may be necessary for large-scale datasets.
- The 30,000+ threshold is empirical for MSGO; datasets substantially smaller may underprovide coverage of chemical space and lead to overfitting or poor generalization.

## Evidence

- [other] Training data for MSGO consists of 30k+ pseudo SMILES-spectrum pairs generated by CFM-ID from raw SMILES lists.: "Training data for MSGO consists of 30k+ pseudo SMILES-spectrum pairs generated by CFM-ID from raw SMILES lists."
- [readme] For Training, we use 30k+ pseudo smiles-specturm pairs generated by cfmid: "For Training, we use 30k+ pseudo smiles-specturm pairs generated by cfmid"
- [other] For each SMILES string, invoke CFM-ID to generate in silico mass spectra with fragmentation patterns. Pair each input SMILES with its corresponding CFM-ID-generated spectrum to create pseudo SMILES-spectrum pairs.: "For each SMILES string, invoke CFM-ID to generate in silico mass spectra with fragmentation patterns. Pair each input SMILES with its corresponding CFM-ID-generated spectrum to create pseudo"
- [readme] For evaluation, we use 300+ real specturm to verify our method: "For evaluation, we use 300+ real specturm to verify our method"
- [readme] Python: 3.7 \ Torch: 1.7.1: "Python: 3.7 \ Torch: 1.7.1"

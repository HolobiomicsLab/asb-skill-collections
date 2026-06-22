---
name: metabolite-candidate-ranking
description: Use when you have an untargeted mass spectrometry spectrum (MS/MS data) and a set of candidate molecules from PubChem or similar databases, and you need to rank candidates by likelihood of being the true molecular annotation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3258
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - pip
  - CUDA
  - PyTorch
  - DGL (Deep Graph Library)
  - conda / pip
  - CUDA 11.8
  - RDKit
  techniques:
  - tandem-MS
derived_from:
- doi: 10.1093/bioinformatics/btaf354
  title: JESTR
evidence_spans:
- Please set up the environment as per this file using [conda](http://docs.condi.ioen/latest/)/[pip]
- The model was trained and tested on GPU nVidia A100 with CUDA 11.8
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_biotransformer_3_0_cq
    doi: 10.1093/nar/gkac408
    title: BioTransformer 3.0
  - build: coll_deep_ms_ms_similarity_cq
    doi: 10.1021/acs.analchem.8b05405
    title: Deep MS/MS similarity
  - build: coll_jestr_cq
    doi: 10.1093/bioinformatics/btaf354
    title: JESTR
  dedup_kept_from: coll_jestr_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioinformatics/btaf354
  all_source_dois:
  - 10.1093/bioinformatics/btaf354
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolite-candidate-ranking

## Summary

Rank candidate molecules for annotation of untargeted metabolomics spectra using JESTR, a joint embedding space model trained on spectral and molecular graph features. This skill addresses the challenge of identifying the correct molecular structure from large candidate databases when MS/MS spectra alone are ambiguous.

## When to use

Apply this skill when you have an untargeted mass spectrometry spectrum (MS/MS data) and a set of candidate molecules from PubChem or similar databases, and you need to rank candidates by likelihood of being the true molecular annotation. Use it specifically on NPLIB1 dataset spectra or datasets prepared in the same format (containing m/z, intensity arrays, and candidate lists indexed by InChiKey).

## When NOT to use

- Input is a low-resolution MS1 spectrum without MS/MS fragmentation data — JESTR requires spectral intensity information across fragment m/z values.
- Candidate molecules are not indexed by InChiKey or lack corresponding SMILES/molecular structures — the model requires both spectral and molecular graph features.
- The dataset uses CPU-only hardware — released pretrained weights are for GPU (NVIDIA A100 with CUDA 11.8) and may not be compatible or performant on CPU.

## Inputs

- MS/MS spectrum (m/z and intensity arrays)
- Target molecule InChiKey or SMILES
- Candidate molecule list (from PubChem) indexed by InChiKey
- DGL molecular graphs (precomputed or generated on-the-fly from SMILES)
- Pretrained JESTR model weights (PyTorch .pt file)

## Outputs

- Ranked list of candidate molecules with scores
- Embedding-space similarity scores for each candidate
- Structured output file (e.g., CSV or JSON) with ranking predictions

## How to apply

Set up a GPU-compatible PyTorch environment with CUDA 11.8 using the jestr_requirements.txt file. Load the pretrained NPLIB1 weights into the JESTR model (which encodes both spectral features and molecular graph structure via DGL graphs). Prepare input features by loading the NPLIB1 dataset files (data_dict.pkl for spectra, molgraph_dict.pkl for precomputed DGL graphs, cand_dict.pkl for test-set candidates). Execute inference to score each candidate molecule against the query spectrum, producing a ranked list of molecules with embedding-space similarity scores. The model learns a joint embedding space where spectra and molecules with high MS/MS similarity are embedded close together, so higher scores indicate more likely annotations.

## Related tools

- **PyTorch** (Deep learning framework for loading and executing the JESTR model and computing embedding-space ranking scores) — https://pytorch.org
- **DGL (Deep Graph Library)** (Encodes molecular graph structure for candidate molecules; used to precompute or generate molgraph_dict.pkl for runtime efficiency)
- **conda / pip** (Environment and dependency management; install packages from jestr_requirements.txt) — https://docs.conda.io/en/latest/
- **CUDA 11.8** (GPU acceleration for model training and inference on NVIDIA hardware)
- **RDKit** (Generate or validate molecular structures from SMILES; create rdkit mol objects stored in mol_dict.pkl)

## Examples

```
python cand_rank_canopus.py
```

## Evaluation signals

- Output ranking list is non-empty and sorted by descending score (higher scores rank first).
- Scores fall within a reasonable range for embedding-space similarity (e.g., 0–1 or normalized cosine similarity).
- True molecule (known annotation) appears in top-k predictions (compare against ground truth in split.pkl test set); measure mean reciprocal rank (MRR) or top-1 accuracy.
- All candidate molecules in the ranking correspond to valid InChiKeys in mol_dict.pkl and molgraph_dict.pkl.
- Runtime inference completes without out-of-memory errors on the available GPU (output tensor dimensions match input batch size and candidate count).

## Limitations

- Pretrained weights are trained only on NPLIB1 natural products library; performance on other spectral datasets (e.g., drugs, environmental metabolites) is not guaranteed and may require retraining.
- Model was trained and tested on NVIDIA A100 GPU with CUDA 11.8; behavior on other GPU architectures or CUDA versions is untested.
- Other datasets beyond NPLIB1 are under licensing agreements that prohibit public release; users must obtain appropriate licenses to apply the model to proprietary spectral databases.
- Requires precomputed or on-the-fly generation of DGL molecular graphs, which can be memory-intensive for large candidate sets; if molgraph_dict.pkl is not provided, graphs are created at runtime.
- Candidate ranking depends on the quality and coverage of the candidate molecule list; if the true molecule is not in the candidate set, the model cannot rank it correctly.

## Evidence

- [intro] Joint Embedding Space Technique for Ranking Candidate Molecules for the Annotation of Untargeted Metabolomics Data: "Joint Embedding Space Technique for Ranking Candidate Molecules for the Annotation of Untargeted Metabolomics Data"
- [intro] The model was trained and tested on GPU nVidia A100 with CUDA 11.8. The released weights are also for GPU trained models.: "The model was trained and tested on GPU nVidia A100 with CUDA 11.8. The released weights are also for GPU trained models."
- [intro] Load the pretrained NPLIB1 weights into the JESTR PyTorch model. Load the NPLIB1 dataset and prepare input features for ranking. Execute the JESTR ranking inference to score and rank candidate molecules for each query spectrum.: "Load the pretrained NPLIB1 weights into the JESTR PyTorch model. Load the NPLIB1 dataset and prepare input features for ranking. Execute the JESTR ranking inference to score and rank candidate"
- [readme] molgraph_dict.pkl - a dictionary containing mapping from molecule InchiKey to DGL graph for that molecule. This is for runtime optimization. If not provided this will be created on the fly: "molgraph_dict.pkl - a dictionary containing mapping from molecule InchiKey to DGL graph for that molecule. This is for runtime optimization. If not provided this will be created on the fly"
- [readme] cand_dict.pkl - dictionary keys by target molecule InchiKey. Each entry is a list of candidates for that molecule downloaded from PubChem.: "cand_dict.pkl - dictionary keys by target molecule InchiKey. Each entry is a list of candidates for that molecule downloaded from PubChem."
- [intro] The other datasets are under licensing agreements that prohibit their public release: "The other datasets are under licensing agreements that prohibit their public release"

---
name: heterogeneous-graph-embedding-design
description: Use when when building a Graph Transformer model for continuous property prediction on molecules with associated experimental or instrumental metadata (e.g., retention time prediction across different chromatographic columns, methods, or conditions).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0292
  edam_topics:
  - http://edamontology.org/topic_3343
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3318
  tools:
  - Graphormer
  - DGL
  - RDKit
  - PyTorch
  - NumPy
derived_from:
- doi: 10.1021/acs.analchem.4c05859
  title: Graphormer-RT
evidence_spans:
- Graphormer-RT is an extension to the Graphormer package, with documentation, and the original code on Github
- import dgl
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_graphormer_rt_cq
    doi: 10.1021/acs.analchem.4c05859
    title: Graphormer-RT
  dedup_kept_from: coll_graphormer_rt_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.4c05859
  all_source_dois:
  - 10.1021/acs.analchem.4c05859
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# heterogeneous-graph-embedding-design

## Summary

Design and instantiate a heterogeneous graph embedding layer that encodes both molecular structure (atoms, bonds, chirality via DGL) and experimental metadata (column parameters, gradient slopes, solvents via one-hot and normalization) into a composite feature vector for input to a Graph Transformer model. This skill bridges molecular topology and chromatographic operating conditions into a unified embedding space.

## When to use

When building a Graph Transformer model for continuous property prediction on molecules with associated experimental or instrumental metadata (e.g., retention time prediction across different chromatographic columns, methods, or conditions). Use this skill when you have (1) molecular SMILES or graph representations, (2) categorical metadata (company, USP code, solvent type, HPLC type) and numerical parameters (column length, temperature, pH, particle size, dead time, gradient slopes), and (3) a need to jointly encode both modalities into a single forward pass.

## When NOT to use

- Input is already a pre-computed feature table or descriptor matrix (use directly or extract metadata)
- Molecules lack bond-order or chirality information needed for graph construction (consider fallback to SMILES descriptor methods)
- Column metadata is sparse or missing for >20% of samples (imputation or exclusion needed before embedding)

## Inputs

- SMILES strings or RDKit Mol objects for molecules
- DGL heterogeneous graphs with atom/bond attributes
- Categorical column metadata (company_name, usp_code, solvent_A, solvent_B, HPLC_type)
- Numerical column parameters (col_length, col_innerdiam, col_part_size, temp, col_dead, pH_A, pH_B)
- Gradient profile data (time1, time2, time3, time4; grad1, grad2, grad3, grad4)
- Optional additive concentrations and Tanaka/HSMB physicochemical parameters

## Outputs

- One-hot encoded categorical features (binary vectors per column attribute)
- Normalized numerical features (scaled to ~[0,1] range)
- Gradient slope feature tensor (s1, s2, s3 slopes)
- Composite embedding vector (concatenated molecular + column + gradient features)
- Forward pass tensor shapes verified to match model input dimensions

## How to apply

Featurize categorical column parameters using one-hot encoding (company, USP code, solvent composition, HPLC type) and normalize numerical parameters by fixed divisors (length/250, temperature/100, pH/14) to constrain ranges to approximately [0,1]. Compute gradient slope features (s1, s2, s3) as (B_next − B_prev)/(t_next − t_prev) for each time segment. Configure a DGL heterogeneous graph encoder to embed molecules with node attributes (atom types, bond orders, chirality) and edge attributes (bond types). Create a composite embedding by concatenating the DGL molecular graph embedding, the one-hot/normalized column feature vector, and the gradient slope vector. Pass this concatenated representation through the Graphormer backbone (with configured attention heads and encoder layers) to produce a continuous output. Validate tensor shape propagation end-to-end on a sample batch of molecular graphs paired with column metadata before training.

## Related tools

- **DGL** (Graph construction and node/edge attribute encoding for molecular structure) — https://github.com/dmlc/dgl
- **RDKit** (Molecule parsing (SMILES to Mol), atom/bond attribute extraction (type, order, chirality)) — https://github.com/rdkit/rdkit
- **PyTorch** (Tensor operations, concatenation, and gradient computation for embedding layer) — https://github.com/pytorch/pytorch
- **Graphormer** (Graph Transformer backbone that ingests composite embeddings and outputs predictions) — https://github.com/microsoft/Graphormer
- **NumPy** (Batch concatenation and normalization of numerical features) — https://github.com/numpy/numpy

## Examples

```
# Create heterogeneous embedding from molecule and column metadata
from rdkit import Chem
import dgl
import numpy as np
import torch

mol = Chem.MolFromSmiles('CCO')
column_params = {'company': 'Waters', 'usp': 'L1', 'length': 150, 'temp': 25, 'pH_A': 3.0}
company_oh = [1, 0, 0]  # one-hot for Waters
norm_length = 150 / 250
graph = dgl.from_networkx(nx.from_edgelist([(0,1), (1,2)]))  # example graph
composite_emb = np.concatenate([graph.ndata['feat'].flatten(), company_oh, [norm_length]])
```

## Evaluation signals

- One-hot encoded categorical vectors sum to 1 per attribute and contain no NaN values
- Normalized numerical features fall within [0, 1] after division by chosen constants (length/250, temp/100, pH/14)
- Gradient slope computations produce finite values; detect division-by-zero or missing time intervals
- Concatenated composite embedding tensor has expected shape (batch_size, total_feature_dim) matching model input layer
- Forward pass through Graphormer backbone completes without shape mismatches or type errors on sample batch

## Limitations

- One-hot encoding expands dimensionality linearly with categorical cardinality; high-cardinality metadata (e.g., hundreds of unique companies) may bloat the feature vector
- Fixed normalization divisors (250, 100, 14) are empirically chosen for this chromatography domain and may not generalize to other analytical modalities or future instrument designs
- Missing or malformed metadata (empty strings, '2.7 spp' Tanaka codes) require explicit filter/replacement steps; no automatic imputation is described
- Gradient slope calculation assumes at least 3 time points (t1, t2, t3); methods with fewer gradient steps cannot compute s2 and s3
- No guidance provided on handling columns from vendors or USP codes not seen during training

## Evidence

- [other] Column parameters are featurized through one-hot encoding of categorical features (company, USP, solvents), normalization of numerical features (length/250, temperature/100, pH/14), and concatenation of integer and float encodings: "Column parameters are featurized through one-hot encoding of categorical features (company, USP, solvents), normalization of numerical features (length/250, temperature/100, pH/14), and concatenation"
- [other] Create column-parameter embedding layer that accepts one-hot encoded categorical features (company, USP, solvent composition) and normalized numerical features (length/250, temperature/100, pH/14).: "Create column-parameter embedding layer that accepts one-hot encoded categorical features (company, USP, solvent composition) and normalized numerical features (length/250, temperature/100, pH/14)."
- [other] Configure DGL graph featurization pipeline to encode molecules as heterogeneous graphs with node/edge attributes (atom types, bond orders, chirality).: "Configure DGL graph featurization pipeline to encode molecules as heterogeneous graphs with node/edge attributes (atom types, bond orders, chirality)."
- [other] Define gradient-slope feature computation for B and t parameters (slopes s1, s2, s3 as (B_next − B_prev)/(t_next − t_prev)).: "Define gradient-slope feature computation for B and t parameters (slopes s1, s2, s3 as (B_next − B_prev)/(t_next − t_prev))."
- [other] Assemble forward pass that concatenates molecular graph embeddings from DGL encoder, column embeddings, and gradient slopes, passing combined representation through Graphormer transformer backbone: "Assemble forward pass that concatenates molecular graph embeddings from DGL encoder, column embeddings, and gradient slopes, passing combined representation through Graphormer transformer backbone to"
- [results] def one_hot_company(company):
    one_hot = [0] * len(companies)
    one_hot[companies.index(company)] = 1: "def one_hot_company(company):
    one_hot = [0] * len(companies)
    one_hot[companies.index(company)] = 1"
- [results] length = float(column_params[2]) / 250
temp = float(column_params[5]) / 100
pH_A = float(column_params[19]) / 14: "length = float(column_params[2]) / 250
temp = float(column_params[5]) / 100
pH_A = float(column_params[19]) / 14"
- [results] s1 = (B2 - B1) / (t2 - t1)
s2 = (B3 - B2) / (t3 - t2)
s3 = (B3 - B1) / (t3 - t1): "s1 = (B2 - B1) / (t2 - t1)
s2 = (B3 - B2) / (t3 - t2)
s3 = (B3 - B1) / (t3 - t1)"
- [other] Validate model instantiation by checking tensor shapes propagate correctly through forward pass with sample molecular graphs and column-metadata batches.: "Validate model instantiation by checking tensor shapes propagate correctly through forward pass with sample molecular graphs and column-metadata batches."
- [results] tanaka_params = [2.7 if param == '2.7 spp' else param for param in tanaka_params]
tanaka_params = [2.7 if param == '2.6 spp' else param for param in tanaka_params]: "tanaka_params = [2.7 if param == '2.7 spp' else param for param in tanaka_params]
tanaka_params = [2.7 if param == '2.6 spp' else param for param in tanaka_params]"
- [results] if column_params[3] == '':
        diameter = 0
if column_params[20] == '':
        pH_B = 0: "if column_params[3] == '':
        diameter = 0
if column_params[20] == '':
        pH_B = 0"
- [readme] Graphormer-RT is an extension to the Graphormer package, with documentation, and the original code on Github: "Graphormer-RT is an extension to the Graphormer package, with documentation, and the original code on Github"
- [readme] The pickle files (/home/cmkstien/RT_pub/Graphormer_RT/sample_data/HILIC_metadata.pickle, /home/cmkstien/RT_pub/Graphormer_RT/sample_data/RP_metadata.pickle) contain processed column metada generated from RepoRT with the following header: ['company_name', 'usp_code', 'col_length', 'col_innerdiam', 'col_part_size', 'temp', 'col_fl', 'col_dead', 'HPLC_type','A_solv', 'B_solv', 'time1', 'grad1', 'time2', 'grad2', 'time3', 'grad3', 'time4', 'grad4', 'A_pH', 'B_pH': "The pickle files (/home/cmkstien/RT_pub/Graphormer_RT/sample_data/HILIC_metadata.pickle, /home/cmkstien/RT_pub/Graphormer_RT/sample_data/RP_metadata.pickle) contain processed column metada generated"

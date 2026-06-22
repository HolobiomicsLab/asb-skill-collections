---
name: pubchem-structure-retrieval
description: Use when you have an experimental tandem mass spectrum and chemical formula for an unknown compound, and need to identify the true structure among all PubChem entries with that formula.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3431
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3407
  tools:
  - PubChem
  - ICEBERG
  - ms-pred (coleygroup)
  - MAGMa
derived_from:
- doi: 10.1021/acs.analchem.3c04654
  title: ICEBERG / fragmentation graph generation
evidence_spans:
- the WebUI will rank it against all candidates from PubChem
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.3c04654
  all_source_dois:
  - 10.1021/acs.analchem.3c04654
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# PubChem Structure Retrieval and Ranking

## Summary

Retrieve all candidate molecular structures from PubChem matching a given chemical formula, then rank them against experimental tandem mass spectrometry data using fragment-level spectrum prediction. This skill bridges structure databases with MS-based structure elucidation by enabling high-throughput candidate filtration.

## When to use

You have an experimental tandem mass spectrum and chemical formula for an unknown compound, and need to identify the true structure among all PubChem entries with that formula. Use this skill when you want spectrum-based ranking rather than formula-only filtering, and when your candidate set size is manageable (PubChem can return hundreds to thousands of isomers per formula).

## When NOT to use

- Input is a protein or very large biomolecule; PubChem and ICEBERG target small organic molecules with mass < ~1500 Da
- You only have a molecular formula and no experimental mass spectrum; formula-only queries lack discriminatory power for isomer ranking
- Computational budget is extremely tight; ICEBERG inference on thousands of candidates requires GPU acceleration or significant CPU time

## Inputs

- chemical formula (string, e.g. 'C6H12O6')
- experimental tandem mass spectrum (m/z peaks with intensities, typically in .mgf or .msp format)
- pretrained ICEBERG model checkpoint (fragment generator and intensity predictor weights)

## Outputs

- ranked list of candidate structures with scores (sorted descending by ranking metric)
- predicted tandem mass spectra for each candidate (for comparison/visualization)
- retrieval accuracy metrics (e.g., top-1, top-5, top-10 hit rates if ground truth is available)

## How to apply

First, query PubChem to retrieve all candidate structures matching the input chemical formula; this produces a candidate pool of (SMILES, InChIKey) pairs. Second, run ICEBERG's spectrum prediction pipeline on each candidate to predict fragment-level tandem mass spectra by modeling molecular fragmentation as a directed acyclic graph (DAG) of breakage events. Third, compute a ranking score for each candidate by comparing its predicted spectrum to the experimental spectrum (typically via cosine similarity or peak-matching metrics). Finally, sort candidates by score in descending order and return the ranked list. The fragment-level prediction is critical: ICEBERG predicts spectra at the molecular fragment level rather than chemical formula level, enabling fine-grained differentiation between isomers.

## Related tools

- **PubChem** (Structure database queried to retrieve all candidate isomers matching the input chemical formula)
- **ICEBERG** (Fragment-level spectrum prediction model that scores each candidate by predicting and comparing tandem mass spectra) — http://iceberg-ms.mit.edu/
- **ms-pred (coleygroup)** (Reference implementation providing training, inference, and retrieval evaluation pipelines for ICEBERG and baseline models) — https://github.com/coleygroup/ms-pred
- **MAGMa** (Algorithm used to annotate substructures and label fragmentation pathways during ICEBERG training data preparation)

## Examples

```
python notebooks/iceberg_2025_biorxiv/iceberg_demo_pubchem_elucidation.ipynb
```

## Evaluation signals

- Top-1 retrieval accuracy: verify that the ground-truth structure ranks first in the output list (on known test compounds, expect ~40% top-1 hit rate on NIST'20 with [M+H]+ ions)
- Peak matching precision: compare experimental spectrum peaks to predicted spectrum peaks; high-ranking candidates should have predicted peaks with high cosine similarity (typically > 0.7) to observed peaks
- Rank distribution: inspect whether the top-ranked candidate has a substantially higher score than runners-up; large gaps suggest confident prediction
- Candidate pool validation: confirm that all retrieved PubChem entries match the input formula (e.g., via InChI-to-formula recomputation)
- Spectrum prediction consistency: verify that ICEBERG predictions are deterministic given fixed model weights and inputs; re-running the same candidate should yield identical spectra

## Limitations

- ICEBERG requires pretrained model weights (available via NIST'20 license email or MassSpecGym public dataset); training from scratch requires ~24 GB GPU RAM and significant compute time
- Fragment-level prediction accuracy degrades on rare or novel fragmentation patterns not well-represented in NIST'20 training data; MassSpecGym weights have undergone less manual curation and will produce different predictions
- PubChem retrieval can return thousands of candidates for ambiguous formulas; ranking all candidates is computationally expensive without GPU acceleration or batching
- ICEBERG was trained primarily on [M+H]+ ESI-MS/MS data; performance on other ionization modes (e.g., [M-H]−, EI) may degrade
- WebUI does not require GPU, but local batch inference on large candidate sets is substantially faster with GPU (tested on NVIDIA A5000 24 GB and RTX 4070M 8 GB)

## Evidence

- [intro] By inputting the chemical formula and your experimental spectrum, the WebUI will rank it against all candidates from PubChem.: "By inputting the chemical formula and your experimental spectrum, the WebUI will rank it against all candidates from PubChem."
- [intro] ICEBERG predicts spectra at the level of molecular fragments, whereas SCARF predicts spectra at the level of chemical formula.: "ICEBERG predicts spectra at the level of molecular fragments, whereas SCARF predicts spectra at the level of chemical formula."
- [intro] No GPU is required to run ICEBERG structural elucidation via the WebUI: "No GPU is required to run ICEBERG structural elucidation via the WebUI"
- [readme] ICEBERG is our recommended model with a 40% top-1 retrieval accuracy with [M+H]+, benchmarked on the NIST'20 dataset.: "ICEBERG is our recommended model with a 40% top-1 retrieval accuracy with [M+H]+, benchmarked on the NIST'20 dataset."
- [readme] ICEBERG is trained in two parts: a learned fragment generator and an intensity predictor.: "ICEBERG is trained in two parts: a learned fragment generator and an intensity predictor."
- [readme] You need two GPUs with at least 24GB RAM to train ICEBERG: "You need two GPUs with at least 24GB RAM to train ICEBERG"

---
name: molecular-descriptor-extraction
description: Use when you have a collection of chemical structures in SMILES format and need to create paired structure–spectrum training data for a generative model, but do not have experimental MS/MS spectra available.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3802
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_0209
  - http://edamontology.org/topic_3372
  - http://edamontology.org/topic_3407
  tools:
  - Python 3.7
  - cfmid
  - MSGO
  - RDKit
  - Retip
  - rcdk
  - Retip R package
  - Retip Python package (pyRetip)
  techniques:
  - LC-MS
derived_from:
- doi: 10.1038/s42256-025-01140-5
  title: MSGo
- doi: 10.1021/acs.analchem.3c05019
  title: ''
- doi: 10.1021/acs.analchem.9b05765
  title: ''
evidence_spans:
- 'Python: 3.7'
- jhhung/PS2MS
- github.com__oloBion__Retip
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_msgo_cq
    doi: 10.1038/s42256-025-01140-5
    title: MSGo
  - build: coll_ps2ms
    doi: 10.1021/acs.analchem.3c05019
    title: ps2ms
  - build: coll_retip_cq
    doi: 10.1021/acs.analchem.9b05765
    title: Retip
  dedup_kept_from: coll_msgo_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s42256-025-01140-5
  all_source_dois:
  - 10.1038/s42256-025-01140-5
  - 10.1021/acs.analchem.3c05019
  - 10.1021/acs.analchem.9b05765
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# molecular-descriptor-extraction

## Summary

Extract in silico mass spectral descriptors (fragmentation patterns, peaks) from chemical structure inputs using computational fragmentation prediction tools. This enables generation of paired chemical structure–spectrum training datasets for machine learning models that predict molecular identity from tandem MS data.

## When to use

You have a collection of chemical structures in SMILES format and need to create paired structure–spectrum training data for a generative model, but do not have experimental MS/MS spectra available. CFM-ID-based in silico generation is appropriate when you need 30k+ pseudo pairs to achieve sufficient training coverage for deep learning on molecular structure prediction from mass spectra.

## When NOT to use

- Input spectra are already experimental (high-resolution LC–QTOF or other measured data) — use those directly instead of generating pseudo pairs.
- Target molecules contain functional groups or mechanisms outside CFM-ID's fragmentation rule set (e.g., non-standard metal complexes, photochemical reactions).
- You require high chemical accuracy and cannot tolerate systematic differences between in silico and real fragmentation patterns — evaluate baseline model performance first.

## Inputs

- SMILES strings (list or file format)
- Raw SMILES list file

## Outputs

- Pseudo SMILES-spectrum pairs (≥30,000 tuples)
- Training dataset file with paired SMILES and fragmentation spectra

## How to apply

For each SMILES string in your input list, invoke CFM-ID to compute in silico fragmentation patterns and generate a pseudo mass spectrum with fragment peaks. Pair each input SMILES with its corresponding CFM-ID output spectrum to form a (SMILES, spectrum) tuple. Aggregate all tuples into a single training dataset file, validating that the output contains at least 30,000 pairs. Verify schema integrity: each pair must include a valid SMILES string and a corresponding spectrum representation (peak list or tensor encoding). This approach trades experimental fidelity for data scale, enabling training of sequence-to-sequence or beam-search models on a diverse chemical space.

## Related tools

- **cfmid** (In silico fragmentation prediction engine that generates mass spectra and fragmentation patterns from SMILES strings)
- **Python 3.7** (Scripting language for orchestrating SMILES loading, CFM-ID invocation loops, and dataset aggregation)
- **MSGO** (Target deep learning model trained on the generated pseudo SMILES-spectrum pairs for molecular structure generation) — github.com/aaronma2020/MSGO

## Evaluation signals

- Output file contains exactly the expected number of pairs (validate count ≥ 30,000).
- Each pair is a valid (SMILES, spectrum) tuple — verify SMILES parse correctly and spectrum contains ≥1 fragment peak.
- No duplicate SMILES or spectrum entries in the dataset; check for data leakage between train/eval splits.
- CFM-ID execution completes without errors for ≥99% of input SMILES; log and inspect any failures for rule-set incompatibilities.
- Downstream model training (e.g., `python tools/train.py`) converges and achieves baseline performance on held-out real spectra (300+ real spectrum evaluation set).

## Limitations

- CFM-ID fragmentation predictions are in silico approximations; systematic bias versus real MS/MS spectra may reduce model generalization to experimental data.
- Dataset quality depends on the diversity and chemical validity of the input SMILES list; biased or low-quality SMILES will propagate into pseudo pairs.
- Computational cost scales linearly with number of SMILES; generating 30k+ pairs may require hours of CPU/GPU time depending on CFM-ID backend.
- Not suitable for molecules with atypical fragmentation chemistry or non-standard ionization modes not covered by CFM-ID rule sets.

## Evidence

- [other] For each SMILES string, invoke CFM-ID to generate in silico mass spectra with fragmentation patterns: "For each SMILES string, invoke CFM-ID to generate in silico mass spectra with fragmentation patterns."
- [other] Pair each input SMILES with its corresponding CFM-ID-generated spectrum to create pseudo SMILES-spectrum pairs: "Pair each input SMILES with its corresponding CFM-ID-generated spectrum to create pseudo SMILES-spectrum pairs."
- [other] Aggregate all pairs into a single training dataset file, ensuring at least 30,000+ pairs are produced: "Aggregate all pairs into a single training dataset file, ensuring at least 30,000+ pairs are produced."
- [readme] For Training, we use 30k+ pseudo smiles-specturm pairs generated by cfmid: "For Training, we use 30k+ pseudo smiles-specturm pairs generated by cfmid"
- [other] Validate that the output file contains the expected number of pairs and that each pair includes both a valid SMILES string and a corresponding spectrum representation: "Validate that the output file contains the expected number of pairs and that each pair includes both a valid SMILES string and a corresponding spectrum representation."

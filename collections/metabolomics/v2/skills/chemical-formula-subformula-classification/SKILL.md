---
name: chemical-formula-subformula-classification
description: Use when you have tandem mass spectra with known molecular structures (SMILES, InChI, or chemical formula) and aim to train or evaluate a formula-level spectrum predictor.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_0153
  - http://edamontology.org/topic_3172
  tools:
  - ms-pred (SCARF model and MAGMa integration)
  - MAGMa algorithm
  - NIST20 (tandem MS database)
derived_from:
- doi: 10.1021/acs.analchem.3c04654
  title: ICEBERG / fragmentation graph generation
evidence_spans: []
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

# chemical-formula-subformula-classification

## Summary

Assign tandem mass spectrum fragments to chemical subformulae using structural decomposition, enabling formula-level spectrum prediction via autoregressive reconstruction. This preprocessing step converts raw spectra into subformula-labeled training data for models like SCARF.

## When to use

Apply this skill when you have tandem mass spectra with known molecular structures (SMILES, InChI, or chemical formula) and aim to train or evaluate a formula-level spectrum predictor. Subformula classification is essential before training SCARF or similar models that predict spectra autoregressively at the chemical formula level rather than at the molecular fragment level.

## When NOT to use

- Input spectra lack associated molecular structures or SMILES — subformula assignment requires known chemistry.
- Goal is fragment-level prediction (e.g., ICEBERG, which models molecular fragments) rather than formula-level prediction.
- Spectra are already annotated with subformulae or you are only performing retrieval without model training.

## Inputs

- tandem mass spectra (MGF or HDF5 format with peak m/z and intensity)
- molecular structures (SMILES strings, InChI keys, or chemical formulae)
- raw spectrum dataset (e.g., NIST20 .SDF export or MassSpecGym)

## Outputs

- subformula-annotated spectrum dataset (HDF5 with subformula labels per peak)
- two preprocessed variants: magma_subform_50 and no_subform
- structured metadata linking spectra to subformulae and collision energy

## How to apply

Use the MAGMa algorithm or permissive subformula assignment to decompose each molecule into all chemically feasible subformulae. Two variants are produced: `magma_subform_50` strictly labels subformulae based on SMILES structure using MAGMa, while `no_subform` permissively allows all entries to pass through. Each fragment peak in the spectrum is mapped to its corresponding subformula, creating a labeled dataset. Run the assignment pipeline via `data_scripts/forms/assign_subformulae.py` or the batch script `data_scripts/all_assign_subform.sh`, which preprocesses the data into HDF5 or structured format compatible with downstream model training. Verify that subformula assignments are consistent with the molecular structure and that all peaks have valid formula labels.

## Related tools

- **ms-pred (SCARF model and MAGMa integration)** (Loads pre-trained SCARF model weights and executes subformula classification pipeline; stores preprocessed subformula-annotated data) — https://github.com/coleygroup/ms-pred
- **MAGMa algorithm** (Performs strict structural subformula decomposition by SMILES fragmentation rules)
- **NIST20 (tandem MS database)** (Source of raw spectra and molecular structures for preprocessing)

## Examples

```
python data_scripts/forms/assign_subformulae.py --dataset nist20 --output-dir data/spec_datasets/nist20/subformulae
```

## Evaluation signals

- All spectrum peaks are assigned to valid chemical subformulae consistent with the parent molecular formula.
- Subformula-annotated dataset successfully loads into training pipeline without missing or malformed labels.
- magma_subform_50 variant is stricter (fewer assigned peaks) than no_subform; both are non-empty.
- Downstream SCARF model training converges and produces spectrum predictions with comparable or improved accuracy vs. baselines.
- HDF5 output structure matches the expected schema (labels.tsv, spec_files.hdf5 with subformula keys).

## Limitations

- MAGMa-based assignment may fail or produce incomplete labelings for unusual or exotic chemical structures not well-represented in training chemistry.
- Permissive no_subform variant may introduce noise by labeling peaks that do not correspond to chemically feasible fragments, reducing model precision.
- Processing large datasets (e.g., full PubChem) is computationally expensive and requires hours even with parallelization; formula subset generation has been observed to take several hours.
- Subformula classification depends on accurate SMILES or InChI input; incorrect or ambiguous structures will propagate errors downstream.

## Evidence

- [other] SCARF is a spectrum predictor model that operates by performing subformula classification to autoregressively reconstruct fragmentations and predict tandem mass spectra at the chemical formula level.: "SCARF is a spectrum predictor model that operates by performing subformula classification to autoregressively reconstruct fragmentations and predict tandem mass spectra at the chemical formula level."
- [readme] Data should then be assigned to subformulae files using `data_scripts/forms/assign_subformulae.py`, which will preprocess the data. We produce two fragment versions of the molecule, `magma_subform_50` and `no_subform`. The former strictly labels subformula based upon smiles structure and the latter is permissive and allows all entries to pass.: "Data should then be assigned to subformulae files using `data_scripts/forms/assign_subformulae.py`, which will preprocess the data. We produce two fragment versions of the molecule,"
- [readme] Making formula subsets takes longer (on the order of several hours, even parallelized) as it requires converting each molecule in PubChem to a mol / InChI.: "Making formula subsets takes longer (on the order of several hours, even parallelized) as it requires converting each molecule in PubChem to a mol / InChI."
- [intro] ICEBERG predicts spectra at the level of molecular fragments, whereas SCARF predicts spectra at the level of chemical formula.: "ICEBERG predicts spectra at the level of molecular fragments, whereas SCARF predicts spectra at the level of chemical formula."

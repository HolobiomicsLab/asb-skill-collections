---
name: structure-ranking-from-spectral-data
description: Use when you have an experimental tandem mass spectrum (collision-induced dissociation or ESI-MS/MS) and a chemical formula, and you need to identify the correct structure among multiple isomeric candidates in a database like PubChem.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0218
  - http://edamontology.org/topic_3172
  tools:
  - ICEBERG
  - PubChem
  - ICEBERG WebUI
  - SCARF
derived_from:
- doi: 10.1021/acs.analchem.3c04654
  title: ICEBERG / fragmentation graph generation
evidence_spans:
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
---

# structure-ranking-from-spectral-data

## Summary

Rank candidate molecular structures retrieved from a compound database against an experimental tandem mass spectrum by predicting fragment-level spectra and scoring each candidate by similarity to observed peaks. This enables high-throughput structural elucidation when chemical formula alone is insufficient to disambiguate isomers.

## When to use

You have an experimental tandem mass spectrum (collision-induced dissociation or ESI-MS/MS) and a chemical formula, and you need to identify the correct structure among multiple isomeric candidates in a database like PubChem. Use this skill when formula-only filtering leaves >1 candidate and you want to leverage spectral fragmentation patterns to rank them by likelihood.

## When NOT to use

- Experimental spectrum is from a different ionization mode or collision energy than the training data; spectrum predictor accuracy degrades if trained on ESI-MS/MS but applied to EI-MS or at untrained collision energies.
- Chemical formula is ambiguous or uncertain; ranking depends on retrieving the true structure from PubChem first, so formula ambiguity corrupts the candidate pool.
- Candidate library is small (<10 isomers) or trivial; ranking adds minimal value and visual inspection or chemical reasoning may be faster.

## Inputs

- experimental tandem mass spectrum (m/z values and intensities, or .mgf/.mzML format)
- chemical formula (neutral molecular composition, e.g., C6H12O6)
- candidate molecular structure library (SMILES strings or SDF records from PubChem)

## Outputs

- ranked list of candidate structures sorted by ranking score (descending)
- per-candidate predicted spectrum (fragment m/z and intensity)
- per-candidate ranking score (e.g., cosine similarity to experimental spectrum)

## How to apply

Load the experimental spectrum (m/z and intensity pairs) and chemical formula. Query PubChem to retrieve all candidate structures (SMILES) matching the formula. For each candidate, use a trained spectrum predictor (e.g., ICEBERG) to generate predicted fragment masses and intensities by modeling the collision-induced dissociation process at the molecular fragment level. Compare each predicted spectrum to the experimental spectrum using a similarity metric (e.g., cosine similarity or spectral dot product). Sort candidates by ranking score in descending order. The top-ranked candidate is the most likely structure. Optionally apply contrastive finetuning on PubChem SMILES–InChIKey mappings to improve ranking in retrieval scenarios.

## Related tools

- **ICEBERG** (Predicts tandem mass spectra at the molecular fragment level by modeling collision-induced dissociation as a breakage event graph; used to generate predicted spectra for each candidate structure and compute ranking scores.) — https://github.com/coleygroup/ms-pred
- **PubChem** (Retrieves all candidate structures matching a given chemical formula; serves as the structure library for ranking.)
- **ICEBERG WebUI** (Browser-based interface for structural elucidation; accepts chemical formula and experimental spectrum, returns ranked PubChem candidates without requiring GPU or local installation.) — http://iceberg-ms.mit.edu/
- **SCARF** (Alternative spectrum predictor; predicts spectra at the level of chemical formula (subformula classification) rather than molecular fragments; can be used as a baseline or alternative ranking model.) — https://github.com/coleygroup/ms-pred

## Examples

```
python notebooks/iceberg_2025_biorxiv/iceberg_demo_pubchem_elucidation.ipynb
```

## Evaluation signals

- Top-ranked structure matches the ground-truth structure annotation in a reference database (e.g., NIST'20); measure top-1 and top-10 retrieval accuracy.
- Predicted spectrum for the top-ranked candidate shows high cosine similarity (>0.6–0.8) to the experimental spectrum; poor matches indicate either poor spectrum prediction or rank reversal.
- Multiple spectra from different collision energies (if available) are consistent in rank order; instability across energies suggests overfitting or energy-dependent model degradation.
- Ranking scores form a clear separation between correct and incorrect candidates; if scores cluster tightly, discriminative power is low.
- Predicted fragments align with observed m/z peaks and neutral losses consistent with known fragmentation pathways for the structure class.

## Limitations

- Spectrum prediction accuracy depends on training data quality and coverage; NIST'20 is a commercial dataset requiring purchase; publicly available MassSpecGym has undergone less manual curation and may yield different predictions.
- Model performance is collision-energy-dependent; NIST'20 is the only database with annotated collision energies, and applying a model trained at one energy to spectra at another energy degrades ranking accuracy.
- Requires GPU with ≥24 GB RAM for training; inference on WebUI is CPU-compatible but may be slower. Local inference on smaller GPUs requires reduced batch size and skipping contrastive finetuning.
- Ranking relies on complete and accurate retrieval of candidates from PubChem; if the true structure is absent from PubChem or the chemical formula is incorrectly specified, ranking cannot recover it.
- Fragment-level prediction (ICEBERG) outperforms formula-level prediction (SCARF) but is computationally more expensive and requires labeled fragmentation breakage graphs (MAGMa annotations) for training.

## Evidence

- [other] Given a chemical formula and an experimental mass spectrum, how does ICEBERG rank candidate molecular structures retrieved from PubChem?: "Given a chemical formula and an experimental mass spectrum, how does ICEBERG rank candidate molecular structures retrieved from PubChem?"
- [other] ICEBERG predicts spectra at the level of molecular fragments, enabling spectrum-based ranking of PubChem candidates.: "ICEBERG predicts spectra at the level of molecular fragments, enabling spectrum-based ranking of PubChem candidates."
- [other] Query PubChem to retrieve all candidate structures matching the chemical formula. Run ICEBERG's ranking algorithm to score each candidate structure against the experimental spectrum by predicting fragment-level spectra and comparing to observed peaks.: "Query PubChem to retrieve all candidate structures matching the chemical formula. Run ICEBERG's ranking algorithm to score each candidate structure against the experimental spectrum by predicting"
- [intro] By inputting the chemical formula and your experimental spectrum, the WebUI will rank it against all candidates from PubChem.: "By inputting the chemical formula and your experimental spectrum, the WebUI will rank it against all candidates from PubChem."
- [intro] No GPU is required to run ICEBERG structural elucidation via the WebUI: "No GPU is required to run ICEBERG structural elucidation via the WebUI"
- [intro] ICEBERG predicts spectra at the level of molecular fragments, whereas SCARF predicts spectra at the level of chemical formula.: "ICEBERG predicts spectra at the level of molecular fragments, whereas SCARF predicts spectra at the level of chemical formula."
- [readme] To get the PubChem-SMILES mapping that's required for contrastive finetuning, please download pubchem_formulae_inchikey.hdf5: "To get the PubChem-SMILES mapping that's required for contrastive finetuning, please download pubchem_formulae_inchikey.hdf5"
- [readme] ICEBERG is trained in two parts: a learned fragment generator and an intensity predictor.: "ICEBERG is trained in two parts: a learned fragment generator and an intensity predictor."
- [readme] You need two GPUs with at least 24GB RAM to train ICEBERG: "You need two GPUs with at least 24GB RAM to train ICEBERG"

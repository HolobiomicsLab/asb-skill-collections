---
name: pseudo-data-pair-construction
description: Use when when you have a raw list of SMILES strings but lack sufficient
  real mass spectrometry reference data (typically <300 spectra) to train a generative
  model for unknown chemical identification.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0361
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3172
  tools:
  - Python 3.7
  - cfmid
  - MSGO
  techniques:
  - mass-spectrometry
  license_tier: open
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

# pseudo-data-pair-construction

## Summary

Generation of large-scale pseudo SMILES-spectrum pairs by invoking CFM-ID on raw SMILES lists to create synthetic training data for molecular structure inference models. This skill bridges limited real spectroscopic datasets by producing 30k+ paired examples suitable for deep learning on mass spectrometry-to-structure tasks.

## When to use

When you have a raw list of SMILES strings but lack sufficient real mass spectrometry reference data (typically <300 spectra) to train a generative model for unknown chemical identification. Apply this skill to amplify training set size via in silico fragmentation, particularly for underrepresented molecular classes (e.g., PFASs, lipids) in public spectroscopy databases.

## When NOT to use

- You already have >300 real experimental mass spectra for your target molecular class — use real data first to avoid synthetic bias.
- Your SMILES list is incomplete, malformed, or contains non-organic structures that CFM-ID cannot process reliably.
- Your model or downstream task requires retention of isotope patterns or instrument-specific artifacts that in silico fragmentation does not simulate.

## Inputs

- raw SMILES list (text file, one SMILES per line or CSV column)
- CFM-ID executable or API endpoint

## Outputs

- aggregated pseudo SMILES-spectrum pair dataset (≥30,000 pairs)
- training data file (format: paired SMILES and spectrum representation)

## How to apply

Load a SMILES string list into memory and invoke CFM-ID for each SMILES to generate in silico mass spectra with simulated fragmentation patterns. Pair each input SMILES with its CFM-ID-generated spectrum object to form (SMILES, spectrum) tuples. Aggregate all pairs into a single standardized training dataset file, ensuring the output contains ≥30,000 pairs. Each pair must preserve both a valid SMILES string representation and a corresponding spectrum (e.g., m/z intensity array or CFM-ID native format). Validate cardinality (count = expected size), completeness (no null SMILES or spectrum fields), and format consistency before downstream model training.

## Related tools

- **cfmid** (Invoked per SMILES to generate in silico mass spectra with fragmentation patterns)
- **Python 3.7** (Orchestration: SMILES list I/O, CFM-ID invocation loop, pair aggregation, validation)
- **MSGO** (Downstream consumer of generated pseudo SMILES-spectrum pairs for model training) — https://github.com/aaronma2020/MSGO

## Examples

```
# Pseudocode workflow (Python 3.7):
# smiles_list = load_smiles('data/raw_smiles.txt')
# pairs = []
# for smiles in smiles_list:
#     spectrum = invoke_cfmid(smiles)
#     pairs.append((smiles, spectrum))
# save_pairs(pairs, 'data/pseudo_smiles_spectrum_pairs.pkl')
# assert len(pairs) >= 30000, f'Expected >=30k pairs, got {len(pairs)}'
```

## Evaluation signals

- Output file contains exactly ≥30,000 (SMILES, spectrum) pairs with no duplicates or null entries.
- Each SMILES string parses successfully (e.g., via RDKit) and is chemically valid.
- Each spectrum contains expected mass/charge and intensity fields with numeric values in expected ranges (e.g., m/z > 0, intensity ≥ 0).
- Spot-check: manually verify 10–20 SMILES-spectrum pairs by running SMILES through CFM-ID independently and confirming fragment peaks match the paired spectrum.
- Downstream MSGO training converges (loss decreases, validation metrics improve) on the generated dataset with comparable learning curves to published baselines.

## Limitations

- CFM-ID fragmentation patterns may not capture all ionization modes, adducts, or high-energy collision behavior of real instruments.
- Pseudo pairs lack the chemical noise, detector artifacts, and retention-time information present in authentic LC–QTOF data; model trained on pseudo data may overfit to synthetic patterns.
- SMILES list must be curated to avoid invalid or stereochemically ambiguous entries that cause CFM-ID errors or silent failures.
- Generation speed depends on CFM-ID computational cost per SMILES; 30k+ pairs may require hours to days on commodity hardware.

## Evidence

- [other] Training data for MSGO consists of 30k+ pseudo SMILES-spectrum pairs generated by CFM-ID from raw SMILES lists.: "Training data for MSGO consists of 30k+ pseudo SMILES-spectrum pairs generated by CFM-ID from raw SMILES lists."
- [other] For each SMILES string, invoke CFM-ID to generate in silico mass spectra with fragmentation patterns.: "For each SMILES string, invoke CFM-ID to generate in silico mass spectra with fragmentation patterns."
- [other] Pair each input SMILES with its corresponding CFM-ID-generated spectrum to create pseudo SMILES-spectrum pairs.: "Pair each input SMILES with its corresponding CFM-ID-generated spectrum to create pseudo SMILES-spectrum pairs."
- [other] Aggregate all pairs into a single training dataset file, ensuring at least 30,000+ pairs are produced.: "Aggregate all pairs into a single training dataset file, ensuring at least 30,000+ pairs are produced."
- [readme] For Training, we use 30k+ pseudo smiles-specturm pairs generated by cfmid: "For Training, we use 30k+ pseudo smiles-specturm pairs generated by cfmid"

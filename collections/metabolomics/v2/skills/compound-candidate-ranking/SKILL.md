---
name: compound-candidate-ranking
description: Use when after compound database dereplication has produced candidate
  annotations (from SIRIUS or MetFrag) and you need to select the most reliable candidates
  for final annotation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3927
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3407
  tools:
  - RDKit
  - PubChemPy
  - Python
  - SIRIUS
  - MetFrag
  techniques:
  - LC-MS
  license_tier: restricted
derived_from:
- doi: 10.1186/s13321-023-00695-y
  title: MAW
evidence_spans:
- Final candidate selection is done in Python using RDKit and PubChemPy
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_maw_cq
    doi: 10.1186/s13321-023-00695-y
    title: MAW
  dedup_kept_from: coll_maw_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1186/s13321-023-00695-y
  all_source_dois:
  - 10.1186/s13321-023-00695-y
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# compound-candidate-ranking

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Rank and filter metabolite candidates from compound database dereplication (SIRIUS/MetFrag output) using molecular property validation, structural descriptors, and confidence scoring. This skill applies chemical validity checks and descriptor-based selection criteria to produce a curated, scored candidate list for metabolome annotation.

## When to use

Apply this skill after compound database dereplication has produced candidate annotations (from SIRIUS or MetFrag) and you need to select the most reliable candidates for final annotation. Use it when you have CSV or JSON output from dereplication tools and require quality control based on chemical validity, molecular properties, and structural consistency.

## When NOT to use

- Candidates have not yet been dereplicated against a compound database (use this skill after SIRIUS/MetFrag, not before).
- You are working with spectral dereplication results only and have not performed in silico fragmentation scoring.
- All candidates are already manually verified or externally curated; ranking adds no new information.

## Inputs

- SIRIUS or MetFrag dereplication output (CSV or JSON format)
- Precursor mass and MS/MS spectra metadata
- SMILES or InChI strings for candidates
- PubChem database (via PubChemPy query)

## Outputs

- Curated candidate table (CSV) ranked by selection score
- Molecular fingerprints and structural descriptors per candidate
- Chemical validity flags and confidence metrics

## How to apply

Load candidate annotations from SIRIUS or MetFrag dereplication output (CSV or JSON format). Query PubChem via PubChemPy to retrieve molecular properties and validate chemical validity for each candidate. Compute molecular fingerprints and structural descriptors (e.g., Tanimoto similarity, molecular weight, lipophilicity) using RDKit for each candidate. Apply multi-criterion selection filters: (1) chemical validity (e.g., parseable SMILES/InChI), (2) descriptor ranges appropriate to the metabolome context, and (3) PubChem match confidence thresholds. Rank and filter candidates by a composite selection score, then output the curated table to CSV with score metadata for downstream validation.

## Related tools

- **RDKit** (Compute molecular fingerprints, structural descriptors, and validate chemical structure formats (SMILES/InChI parsing)) — https://www.rdkit.org/
- **PubChemPy** (Query PubChem database to retrieve molecular properties and chemical validity for each candidate compound) — https://pubchempy.readthedocs.io/en/latest/
- **SIRIUS** (Upstream tool: performs compound database dereplication to produce candidate annotations for ranking) — https://bio.informatik.uni-jena.de/software/sirius/
- **MetFrag** (Upstream tool: performs compound database dereplication to produce candidate annotations for ranking) — https://ipb-halle.github.io/MetFrag/

## Examples

```
python3.10 Workflow_Python_Script_all_MetFrag.py --msp_file your_file_name/spectral_dereplication/spectral_results.csv --gnps_dir your_file_name/spectral_dereplication/GNPS --hmdb_dir your_file_name/spectral_dereplication/HMDB --mbank_dir your_file_name/spectral_dereplication/MassBank --ms1data your_file_name/insilico/MS1DATA.csv --score_thresh 0.75
```

## Evaluation signals

- All candidates have valid SMILES or InChI strings after RDKit parsing (0% parse failures)
- PubChem queries return property data (molecular weight, logP) for ≥90% of candidates
- Output CSV contains all expected columns: identifier, SMILES, descriptor values, selection_score, and validity_flag
- Selection scores are monotonically ranked (highest score first); no ties unless explicitly tied on all criteria
- Candidates filtered out by selection criteria are documented with reason (e.g., 'invalid_smiles', 'descriptor_out_of_range')

## Limitations

- PubChemPy queries may fail or be rate-limited for very large candidate sets (>1000 compounds); consider batch processing or caching.
- Chemical validity depends on RDKit's ability to parse SMILES/InChI; malformed or non-standard structures may be incorrectly rejected.
- Selection criteria (descriptor ranges, confidence thresholds) are context-dependent and must be tuned for the target metabolome; default ranges may not suit all applications (e.g., natural products vs. pharmaceuticals).
- Candidates present in SIRIUS/MetFrag output but absent from PubChem will be filtered out, potentially losing novel or proprietary compounds.

## Evidence

- [other] Load candidate annotations from SIRIUS or MetFrag dereplication output (CSV or JSON format).: "Load candidate annotations from SIRIUS or MetFrag dereplication output (CSV or JSON format)."
- [other] Query PubChem via PubChemPy to retrieve molecular properties and chemical validity for each candidate.: "Query PubChem via PubChemPy to retrieve molecular properties and chemical validity for each candidate."
- [other] Compute molecular fingerprints and structural descriptors using RDKit for each candidate.: "Compute molecular fingerprints and structural descriptors using RDKit for each candidate."
- [other] Apply selection criteria (e.g., chemical validity, descriptor ranges, PubChem match confidence) to filter and rank candidates.: "Apply selection criteria (e.g., chemical validity, descriptor ranges, PubChem match confidence) to filter and rank candidates."
- [readme] Final candidate selection is done in Python using RDKit and PubChemPy: "Final candidate selection is done in Python using RDKit and PubChemPy"

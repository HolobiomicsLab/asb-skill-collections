---
name: dereplication-candidate-filtering
description: Use when after spectral database dereplication (using Spectra) and compound database dereplication (using SIRIUS or MetFrag) have produced candidate annotations in CSV or JSON format.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_3407
  tools:
  - RDKit
  - PubChemPy
  - Python
  - SIRIUS
  - MetFrag
  techniques:
  - mass-spectrometry
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# dereplication-candidate-filtering

## Summary

Filter and rank compound candidates from mass spectrometry dereplication results (SIRIUS or MetFrag output) using molecular property validation, structural descriptor computation, and PubChem database matching. This skill applies chemical validity checks and selection criteria to curate a final ranked candidate list from intermediate dereplication annotations.

## When to use

After spectral database dereplication (using Spectra) and compound database dereplication (using SIRIUS or MetFrag) have produced candidate annotations in CSV or JSON format. Use this skill when you need to filter spurious or invalid candidates, rank by chemical plausibility, and integrate external chemical validity signals (PubChem structure confirmation) before reporting final metabolite identifications.

## When NOT to use

- Input is already a manually curated or consensus metabolite identification (prior filtering unnecessary).
- Dereplication output lacks sufficient structural information (SMILES, InChI, or molecular formula) for RDKit parsing or PubChem queries.
- Workflow is operating in an offline environment without network access to PubChem API.

## Inputs

- SIRIUS or MetFrag dereplication output (CSV or JSON format with candidate annotations)
- Query molecular structures or InChI/SMILES strings from candidates
- Selection threshold parameters (descriptor ranges, confidence cutoffs)

## Outputs

- Curated candidate table (CSV) ranked by selection score
- Per-candidate molecular descriptors and validation flags
- Final ranked list of metabolite candidates for manual or automated downstream curation

## How to apply

Load candidate annotations from SIRIUS or MetFrag dereplication output (CSV or JSON). For each candidate, query PubChem via PubChemPy to retrieve and validate molecular properties and confirm chemical structure validity. Compute molecular fingerprints and structural descriptors (e.g., molecular weight, logP, H-bond donors/acceptors) using RDKit for each candidate. Apply selection filters based on chemical validity flags, descriptor ranges (e.g., Lipinski rule compliance), and PubChem match confidence thresholds. Rank candidates by a composite selection score integrating these criteria, then output the curated candidate table to CSV format with ranking scores.

## Related tools

- **RDKit** (Compute molecular fingerprints, structural descriptors, and validate chemical structure validity for candidate filtering) — https://www.rdkit.org/
- **PubChemPy** (Query PubChem database to retrieve molecular properties and validate chemical plausibility and PubChem match confidence) — https://pubchempy.readthedocs.io/en/latest/
- **SIRIUS** (Upstream tool providing compound database dereplication output that is filtered and ranked by this skill) — https://bio.informatik.uni-jena.de/software/sirius/
- **MetFrag** (Upstream tool providing compound database dereplication output that is filtered and ranked by this skill) — https://ipb-halle.github.io/MetFrag/
- **Python** (Programming language in which final candidate selection filtering and ranking is implemented)

## Examples

```
python3.10 Workflow_Python_Script_all_MetFrag.py --msp_file your_file_name/spectral_dereplication/spectral_results.csv --gnps_dir your_file_name/spectral_dereplication/GNPS --hmdb_dir your_file_name/spectral_dereplication/HMDB --mbank_dir your_file_name/spectral_dereplication/MassBank --ms1data your_file_name/insilico/MS1DATA.csv --score_thresh 0.75
```

## Evaluation signals

- All candidates in output CSV have valid RDKit-parsed molecular structures (no parsing errors or null SMILES).
- Molecular descriptors (molecular weight, logP, H-bond counts) fall within expected chemical ranges and match PubChem values for validated candidates.
- Selection score is monotonically derived from chemical validity flags and descriptor ranges; candidates with higher scores pass more filters.
- Output table rows are ranked by selection score in descending order; no candidates pass filters that violate descriptor thresholds or PubChem validity checks.
- PubChem query success rate is documented (e.g., % of candidates matched to PubChem structures); missing matches are flagged in confidence columns.

## Limitations

- PubChem query success depends on network availability and SMILES/InChI quality; some candidates may lack PubChem matches if structural identifiers are ambiguous or incomplete.
- Descriptor ranges and selection thresholds are assumed to be pre-defined by user or domain knowledge; no automated threshold optimization is described in the workflow.
- RDKit molecular fingerprints are deterministic but descriptor-based filtering may exclude valid candidates if thresholds are too stringent (e.g., Lipinski rule violations common in natural products).
- MetFrag and SIRIUS output schemas may differ; custom parsing or normalization may be required if input format deviates from expected CSV/JSON structures.

## Evidence

- [other] Load candidate annotations from SIRIUS or MetFrag dereplication output (CSV or JSON format). Query PubChem via PubChemPy to retrieve molecular properties and chemical validity for each candidate. Compute molecular fingerprints and structural descriptors using RDKit for each candidate. Apply selection criteria (e.g., chemical validity, descriptor ranges, PubChem match confidence) to filter and rank candidates.: "Load candidate annotations from SIRIUS or MetFrag dereplication output (CSV or JSON format). Query PubChem via PubChemPy to retrieve molecular properties and chemical validity for each candidate."
- [intro] Final candidate selection is done in Python using RDKit and PubChemPy: "Final candidate selection is done in Python using RDKit and PubChemPy"
- [other] Output curated candidate table ranked by selection score to CSV: "Output curated candidate table ranked by selection score to CSV"
- [intro] The workflow performs spectral database dereplication and compound database dereplication followed by final candidate selection: "The workflow performs spectral database dereplication and compound database dereplication followed by final candidate selection"
- [readme] Download [Docker/MetFrag/Workflow_Python_Script_all_MetFrag.py] and [Docker/SIRIUS5/Workflow_Python_Script_all_SIRIUS.py].: "Download [Docker/MetFrag/Workflow_Python_Script_all_MetFrag.py] and [Docker/SIRIUS5/Workflow_Python_Script_all_SIRIUS.py]."

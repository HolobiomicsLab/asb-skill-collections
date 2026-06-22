---
name: chemical-structure-validation
description: Use when after compound database dereplication with SIRIUS or MetFrag has produced candidate annotations (CSV or JSON format), and you need to filter implausible structures, compute standardized molecular descriptors, and rank candidates by confidence before reporting final metabolite.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3802
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_2275
  tools:
  - RDKit
  - PubChemPy
  - Python
  - SIRIUS
  - MetFrag
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

# chemical-structure-validation

## Summary

Validate chemical structures and compute molecular properties for metabolite candidates using RDKit and PubChemPy after compound database dereplication. This skill filters and ranks candidates by chemical validity, descriptor ranges, and database match confidence to curate final annotations.

## When to use

After compound database dereplication with SIRIUS or MetFrag has produced candidate annotations (CSV or JSON format), and you need to filter implausible structures, compute standardized molecular descriptors, and rank candidates by confidence before reporting final metabolite identifications.

## When NOT to use

- Dereplication output is empty or contains no structural candidates.
- Input candidates lack SMILES, InChI, or other parseable structural notation.
- You need full 3D conformation analysis or quantum properties; RDKit performs 2D fingerprinting only.

## Inputs

- SIRIUS or MetFrag dereplication output (CSV or JSON format)
- Candidate compound annotations with identifiers and predicted structures
- MS1 precursor mass data (for descriptor range filtering)

## Outputs

- Curated candidate table (CSV format)
- Ranked candidates with selection scores
- Molecular descriptors and fingerprints per candidate
- Validation flags (chemical validity, descriptor plausibility)

## How to apply

Load candidate annotations from SIRIUS or MetFrag output. For each candidate, query PubChem via PubChemPy to retrieve molecular properties and verify chemical validity (e.g., SMILES/InChI parsability, formula consistency). Compute molecular fingerprints and structural descriptors using RDKit (e.g., molecular weight, logP, atom counts). Apply selection criteria: reject candidates with invalid structures, filter by descriptor ranges (e.g., molecular weight plausibility for the observed precursor mass), and retain only candidates with high PubChem match confidence. Rank surviving candidates by composite selection score and output the curated table to CSV.

## Related tools

- **RDKit** (Compute molecular fingerprints, structural descriptors (MW, logP, atom counts), and validate SMILES/InChI parsing for chemical validity checks.) — https://www.rdkit.org/
- **PubChemPy** (Query PubChem database to retrieve molecular properties, verify chemical validity, and retrieve match confidence scores for candidate structures.) — https://pubchempy.readthedocs.io/en/latest/
- **SIRIUS** (Upstream tool: performs compound database dereplication to generate candidate annotations that feed into this validation workflow.) — https://bio.informatik.uni-jena.de/software/sirius/
- **MetFrag** (Upstream tool: performs compound database dereplication to generate candidate annotations that feed into this validation workflow.) — https://ipb-halle.github.io/MetFrag/

## Examples

```
python3.10 Workflow_Python_Script_all_MetFrag.py --msp_file spectral_results.csv --gnps_dir ./GNPS --hmdb_dir ./HMDB --mbank_dir ./MassBank --ms1data MS1DATA.csv --score_thresh 0.75
```

## Evaluation signals

- All output candidates parse successfully as valid SMILES/InChI strings in RDKit without errors.
- Molecular weights of retained candidates fall within ±15 ppm of observed precursor m/z (after accounting for adduct mass).
- PubChem match confidence scores (if available) exceed a pre-set threshold (e.g., ≥0.75 per README example).
- Descriptor ranges (e.g., logP, H-bond donors) are consistent with known chemical space for metabolites.
- Final output table contains all required columns: candidate ID, structure (SMILES/InChI), selection score, and validation flags, with no missing values.

## Limitations

- RDKit operates on 2D molecular graphs; it does not validate stereochemistry or 3D conformations—co-elution or isomeric ambiguity may not be resolved.
- PubChemPy queries depend on network availability and PubChem's coverage; novel or rare natural products may lack database entries.
- Descriptor-based filtering (e.g., molecular weight, logP ranges) assumes metabolite chemical space is well-defined; boundary cases may be incorrectly filtered.
- The skill does not account for in-source fragmentation, chemical derivatization, or non-standard adducts; precursor mass plausibility checks may fail for modified compounds.
- Selection score weighting (e.g., relative importance of descriptor ranges vs. PubChem confidence) is user-configurable and must be justified per study context.

## Evidence

- [other] Load candidate annotations from SIRIUS or MetFrag dereplication output (CSV or JSON format). Query PubChem via PubChemPy to retrieve molecular properties and chemical validity for each candidate. Compute molecular fingerprints and structural descriptors using RDKit for each candidate.: "Load candidate annotations from SIRIUS or MetFrag dereplication output (CSV or JSON format). Query PubChem via PubChemPy to retrieve molecular properties and chemical validity for each candidate."
- [other] Apply selection criteria (e.g., chemical validity, descriptor ranges, PubChem match confidence) to filter and rank candidates. Output curated candidate table ranked by selection score to CSV.: "Apply selection criteria (e.g., chemical validity, descriptor ranges, PubChem match confidence) to filter and rank candidates. Output curated candidate table ranked by selection score to CSV."
- [intro] Final candidate selection is done in Python using RDKit and PubChemPy: "Final candidate selection is done in Python using RDKit and PubChemPy"
- [readme] We recommend that the local file should be a csv file with atleast the following columns: "Identifier" "InChI" "SMILES" "molecular_weight". If you don't have information on all columns, these can be calculated with either RDKit or PubChempy automatically: "csv file with atleast the following columns: "Identifier" "InChI" "SMILES" "molecular_weight". If you don't have information on all columns, these can be calculated with either RDKit or PubChempy"
- [readme] python3.10 Workflow_Python_Script_all_MetFrag.py --msp_file your_file_name/spectral_dereplication/spectral_results.csv --gnps_dir your_file_name/spectral_dereplication/GNPS --hmdb_dir your_file_name/spectral_dereplication/HMDB --mbank_dir your_file_name/spectral_dereplication/MassBank --ms1data your_file_name/insilico/MS1DATA.csv --score_thresh 0.75: "python3.10 Workflow_Python_Script_all_MetFrag.py --score_thresh 0.75"

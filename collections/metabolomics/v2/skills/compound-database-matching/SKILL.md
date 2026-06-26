---
name: compound-database-matching
description: Use when you have MS2 .mzML spectral data from untargeted metabolomics
  and need to assign chemical identities to detected precursor ions.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3860
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3407
  tools:
  - Spectra
  - SIRIUS
  - MetFrag
  - R
  - PubChem
  - COCONUT
  - RDKit
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1186/s13321-023-00695-y
  title: MAW
evidence_spans:
- performs spectral database dereplication using R Package
- spectral database dereplication using R Package Spectra
- compound database dereplication using SIRIUS OR MetFrag
- compound database dereplication using SIRIUS
- workflow takes MS2 .mzML format data files as an input in R
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

# compound-database-matching

## Summary

Perform compound database dereplication on MS2 spectral data by dispatching spectra through SIRIUS or MetFrag to generate per-spectrum candidate annotation lists ranked by match score. This skill reduces false-positive identifications and prioritizes putative metabolite assignments for downstream validation.

## When to use

Apply this skill when you have MS2 .mzML spectral data from untargeted metabolomics and need to assign chemical identities to detected precursor ions. Use it after spectral database dereplication (library matching) has been performed, when you want to expand beyond known reference spectra to include in silico predictions from compound structure databases like PubChem or COCONUT.

## When NOT to use

- Input is only MS1 precursor mass data without MS/MS fragmentation spectra — SIRIUS and MetFrag require MS/MS fragment information to score and rank candidates.
- Workflow has already performed final candidate selection (e.g., output is a single assigned compound per spectrum) — this skill is for candidate generation and ranking, not validation.
- Spectral data are in formats other than .mzML (e.g., raw vendor formats, NetCDF, or already-processed peak lists without intensity calibration) — requires conversion upstream.

## Inputs

- MS2 spectral data in .mzML format
- Per-spectrum precursor m/z and intensity
- MS/MS fragment peak list (m/z, intensity) per spectrum
- Compound structure database (CSV: Identifier, InChI, SMILES, molecular_weight) if using MetFrag

## Outputs

- Per-spectrum candidate annotation list (CSV/TSV table)
- Columns: spectrum_id, candidate_identifier, SMILES, InChI, molecular_weight, match_score, rank
- Ranked candidate compounds with structural metadata and scoring metrics

## How to apply

Load processed MS2 spectral data (e.g., from the Spectra R package after spectral library dereplication). For each spectrum with a precursor m/z, dispatch it to either SIRIUS or MetFrag. SIRIUS performs structure elucidation and database searching using MS/MS fragmentation patterns; MetFrag requires a local compound database (CSV with Identifier, InChI, SMILES, molecular_weight columns) and scores candidate structures by fragment peak matching. Collect the ranked candidate matches with association scores for each spectrum. Output the results as a structured table (CSV or TSV) with columns for spectrum ID, candidate compound identifier, structure metadata (SMILES, InChI), calculated/library molecular weight, match score, and rank. Use a score threshold (e.g., 0.75 for MetFrag) in downstream filtering to control false-discovery rate.

## Related tools

- **SIRIUS** (Performs compound database dereplication via structure elucidation and in silico MS/MS matching against PubChem) — https://bio.informatik.uni-jena.de/software/sirius/
- **MetFrag** (Performs compound database dereplication by scoring candidate structures against observed MS/MS fragment peaks) — https://ipb-halle.github.io/MetFrag/
- **Spectra** (R package used to load, parse, and manage MS2 .mzML spectral data prior to database matching) — https://rformassspectrometry.github.io/Spectra/
- **PubChem** (Compound structure database used by SIRIUS for candidate matching)
- **COCONUT** (Local compound structure database (alternative to PubChem) used by MetFrag; provided as CSV) — https://zenodo.org/record/7704937
- **RDKit** (Python library used in post-processing to calculate/validate molecular properties (SMILES, InChI, molecular weight) for candidates) — https://www.rdkit.org/

## Examples

```
Rscript Workflow_R_Script_all_MetFrag.r sample.mzML gnps.rda hmdb.rda mbankNIST.rda 15 TRUE coconut COCONUT_Jan2022.csv sample/insilico/metparam_list.txt MetFragCommandLine-2.5.0.jar
```

## Evaluation signals

- Output table contains one or more ranked candidate rows per input spectrum; no spectrum should return zero candidates unless precursor m/z or fragment data are invalid.
- Match scores are within the expected range for the tool used (e.g., MetFrag scores typically 0–1); scores should correlate with chemical plausibility (higher score = better fragment peak overlap).
- Candidate SMILES and InChI strings are valid and parse without error in RDKit; calculated molecular weights match the candidate's structure within ±0.01 Da.
- Spectrum with higher MS/MS spectral quality (more fragment peaks, higher intensity) should yield candidates with higher match scores than low-quality spectra.
- Candidates ranked #1 should be chemically reasonable for the experimental context (e.g., polar metabolites in aqueous extract should not be rank-1 lipids).

## Limitations

- SIRIUS support in CWL workflows is not yet fully implemented; SIRIUS is available only via Docker containers at present, limiting parallelization options.
- MetFrag performance depends heavily on the completeness and accuracy of the input compound database; missing or incorrect SMILES/InChI will cause low scores or false negatives.
- Both tools assume high-resolution MS/MS data with accurate m/z and intensity calibration; low-resolution or uncalibrated spectra may yield false candidates.
- Computational cost scales with database size and number of spectra; processing time per precursor mass is ~2 minutes on 64 GB RAM Ubuntu system; batching or HPC submission (SLURM) recommended for >10 precursor masses.
- No internal validation that a top-ranked candidate is correct; downstream filtering (e.g., score threshold of 0.75) and orthogonal confirmation (e.g., retention time, biological plausibility) are necessary.

## Evidence

- [other] The workflow performs compound database dereplication by dispatching MS2 spectral data through either SIRIUS or MetFrag tools, which generate per-spectrum candidate annotation lists.: "performs compound database dereplication by dispatching MS2 spectral data through either SIRIUS or MetFrag tools, which generate per-spectrum candidate annotation lists"
- [other] For each spectrum, dispatch to either SIRIUS or MetFrag for compound database dereplication against PubChem. Collect per-spectrum candidate matches with scores and structural metadata. Output ranked candidate annotation list as a structured table (CSV or TSV format).: "dispatch to either SIRIUS or MetFrag for compound database dereplication against PubChem. Collect per-spectrum candidate matches with scores and structural metadata. Output ranked candidate"
- [readme] The workflow takes MS2 .mzML format data files as an input in R. It performs spectral database dereplication using R Package Spectra and compound database dereplication using SIRIUS OR MetFrag.: "workflow takes MS2 .mzML format data files as an input in R. It performs spectral database dereplication using R Package Spectra and compound database dereplication using SIRIUS OR MetFrag"
- [readme] We recommend that the local file should be a csv file with atleast the following columns: 'Identifier' 'InChI' 'SMILES' 'molecular_weight'.: "local file should be a csv file with atleast the following columns: 'Identifier' 'InChI' 'SMILES' 'molecular_weight'"
- [readme] one precursor mass takes 2 minutes on an Ubuntu system with 64GB RAM to run Workflow_R_Script_all_MetFrag.r: "one precursor mass takes 2 minutes on an Ubuntu system with 64GB RAM to run Workflow_R_Script_all_MetFrag.r"
- [readme] SIRIUS is only accomodated with the docker containers, (the workflow will be completely operable in CWL in the future). At the moment, the CWL version can be used with MetFrag.: "SIRIUS is only accomodated with the docker containers. At the moment, the CWL version can be used with MetFrag"

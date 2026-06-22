---
name: candidate-rank-scoring
description: Use when after compound database dereplication has generated per-spectrum candidate lists (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3762
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - Spectra
  - SIRIUS
  - MetFrag
  - R
  - RDKit
  - PubChemPy
  - Python
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Candidate rank scoring

## Summary

Score and rank putative metabolite candidates from compound database dereplication (SIRIUS or MetFrag output) using structural similarity metrics and spectral match quality to select the most likely correct annotation for each MS2 spectrum.

## When to use

After compound database dereplication has generated per-spectrum candidate lists (e.g., from SIRIUS or MetFrag against PubChem or COCONUT), when you need to prioritize candidates by chemical plausibility and spectral evidence quality to reduce false positives and select top-ranked annotations for downstream classification.

## When NOT to use

- When spectral database dereplication has already returned a confident match (high cosine similarity to reference spectrum); use final candidate selection only when spectral dereplication alone is inconclusive.
- When input is raw MS2 .mzML spectral data without prior dereplication; perform spectral and compound database dereplication first.
- When compound database dereplication has not yet been run; this skill operates only on ranked candidate lists, not on raw spectra.

## Inputs

- Per-spectrum candidate annotation lists (from SIRIUS or MetFrag output with match scores)
- Spectral match scores (e.g., fragmentation cosine similarity, in silico prediction score)
- Candidate structural metadata (InChI, SMILES, molecular weight)
- Score threshold parameter (e.g., 0.75)

## Outputs

- Ranked candidate annotation table (CSV or TSV format)
- Top-ranked candidate per spectrum with score, identifier, and structural annotations
- Filtered candidate list meeting score threshold

## How to apply

Load per-spectrum candidate matches with associated scores (fragmentation match score, in silico scoring from the dereplication tool) and structural metadata (InChI, SMILES). Filter candidates by a similarity score threshold (e.g., cosine similarity > 0.75 or tool-specific match score cutoff). Rank remaining candidates by descending score. In the MAW workflow, this is performed in Python using RDKit and PubChemPy to compute structural properties and similarity metrics, then candidates are selected based on score ranking and chemical validity. Output a ranked candidate table with top matches per spectrum, retaining score, molecular weight, and structural identifiers.

## Related tools

- **RDKit** (Compute structural similarity metrics and chemical descriptors from candidate SMILES and InChI; validate candidate molecules for chemical plausibility) — https://www.rdkit.org/
- **PubChemPy** (Query PubChem compound properties and retrieve/calculate missing structural fields (InChI, SMILES, molecular weight) for candidate ranking) — https://pubchempy.readthedocs.io/en/latest/
- **SIRIUS** (Generate initial per-spectrum candidate list with in silico scoring for compound database dereplication) — https://bio.informatik.uni-jena.de/software/sirius/
- **MetFrag** (Generate initial per-spectrum candidate list with fragmentation match scores for compound database dereplication) — https://ipb-halle.github.io/MetFrag/
- **Python** (Execute candidate ranking and scoring workflows using RDKit and PubChemPy libraries)

## Examples

```
python3.10 Workflow_Python_Script_all_MetFrag.py --msp_file spectral_results.csv --gnps_dir ./GNPS --hmdb_dir ./HMDB --mbank_dir ./MassBank --ms1data MS1DATA.csv --score_thresh 0.75
```

## Evaluation signals

- All candidates have valid scores and meet the similarity threshold (e.g., score ≥ 0.75); records below threshold are absent from output.
- Candidates within each spectrum are ordered by descending score; verify rank order is monotonic.
- Each candidate record contains required fields: spectrum ID, rank, score, InChI, SMILES, molecular weight, and candidate identifier; no missing values in core columns.
- Top-ranked candidate per spectrum has the highest score for that spectrum; spot-check 5–10 spectra for correctness.
- Molecular weight of candidate matches (within 1 Da tolerance) the precursor m/z adjusted for charge and adduct type; verify using the precursor mass from the original MS2 spectrum.

## Limitations

- Candidate ranking depends critically on the quality and coverage of the compound database (PubChem, COCONUT, etc.); true metabolite may not be present in the database, leading to low-confidence top hits.
- Score threshold (e.g., 0.75) is heuristic and workflow-dependent; suboptimal thresholds may retain false positives or discard true candidates. Recommend empirical validation on reference standards.
- RDKit and PubChemPy may fail or timeout on large candidate lists (>1000 candidates per spectrum) or rare/exotic molecular structures; consider per-spectrum candidate limits or timeout thresholds.
- Ranking is independent of taxonomic context, sample type, or biological priors; a high-ranking candidate may be biochemically implausible for the organism or tissue being profiled.

## Evidence

- [intro] Final candidate selection is done in Python using RDKit and PubChemPy: "Final candidate selection is done in Python using RDKit and PubChemPy"
- [other] Collect per-spectrum candidate matches with scores and structural metadata; Output ranked candidate annotation list as a structured table: "Collect per-spectrum candidate matches with scores and structural metadata. Output ranked candidate annotation list as a structured table (CSV or TSV format)."
- [readme] Score threshold parameter for filtering candidates: "python3.10 Workflow_Python_Script_all_MetFrag.py --msp_file your_file_name/spectral_dereplication/spectral_results.csv --gnps_dir your_file_name/spectral_dereplication/GNPS --hmdb_dir"
- [readme] Structural validation using chemical descriptor calculation and molecular properties: "If you don't have information on all columns, these can be calculated with either RDKit or PubChempy automatically or can be done manually."

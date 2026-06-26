---
name: psm-record-augmentation
description: Use when your PSM input file (e.g., from MaxQuant or other search engines
  that do not report fixed modifications) lacks modification annotations for residues
  that were chemically modified during sample preparation (e.g., carbamidomethylation
  of cysteines, TMT labeling of lysines and N-termini).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3647
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - MS²Rescore
  - psm_utils
  - DeepLC
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1002/pmic.202300336
  title: MS2Rescore (immunopeptidome rescoring)
evidence_spans:
- MS²Rescore is a tool for rescoring peptide-spectrum matches
- Accepted ProForma modification labels in :py:mod:`psm_utils`
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ms2rescore_immunopeptidome_rescoring_cq
    doi: 10.1002/pmic.202300336
    title: MS2Rescore (immunopeptidome rescoring)
  dedup_kept_from: coll_ms2rescore_immunopeptidome_rescoring_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1002/pmic.202300336
  all_source_dois:
  - 10.1002/pmic.202300336
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Reconstruct and inject fixed modifications into PSM records

## Summary

This skill augments peptide-spectrum match (PSM) records with fixed modifications that were not reported by the search engine by mapping ProForma modification labels to target residues and terminal positions, then inserting them into the peptide sequences using standard ProForma notation.

## When to use

Apply this skill when your PSM input file (e.g., from MaxQuant or other search engines that do not report fixed modifications) lacks modification annotations for residues that were chemically modified during sample preparation (e.g., carbamidomethylation of cysteines, TMT labeling of lysines and N-termini). This is essential before feature generation and rescoring in MS²Rescore workflows, especially when downstream feature generators such as DeepLC require accurate modification formulas.

## When NOT to use

- The search engine output already reports all fixed modifications in the PSM file—augmentation is unnecessary and risks double-annotation.
- You are only interested in variable modifications and fixed modifications are not relevant to downstream analysis (e.g., feature generation does not require modification formulas).
- The input is already an FDR-filtered subset of PSMs; MS²Rescore requires all target and decoy PSMs without FDR-filtering before this step.

## Inputs

- PSM file (TSV, CSV, or format supported by psm_utils; e.g., MaxQuant msms.txt, Sage .sage.tsv)
- Fixed modifications configuration mapping (JSON, TOML, or dict; maps ProForma labels to residue lists)

## Outputs

- Augmented PSM file with ProForma-annotated peptide sequences including fixed modifications
- PSM records with all original fields preserved

## How to apply

Load the PSM file and extract all peptide sequences and their current ProForma modification annotations using psm_utils. Load the fixed_modifications configuration that maps ProForma modification labels (e.g., 'U:Carbamidomethyl', 'U:TMT6plex') to lists of target residues (standard amino acid letters, 'N-term', or 'C-term'). For each PSM, iterate through the fixed_modifications map and insert the specified modifications at the appropriate positions in the sequence using ProForma notation (e.g., 'C[U:Carbamidomethyl]' for carbamidomethylated cysteine) if not already present in the sequence annotation. Write the augmented PSM records with updated peptide sequences back to output, preserving all other PSM fields intact.

## Related tools

- **MS²Rescore** (Modular platform that orchestrates PSM augmentation, feature generation, and rescoring; uses fixed_modifications configuration to augment PSM records before rescoring) — https://github.com/compomics/ms2rescore
- **psm_utils** (Library for parsing PSM files in multiple formats and standardizing modification notation to ProForma; handles ProForma label validation and residue position mapping) — https://github.com/compomics/psm_utils
- **DeepLC** (Feature generator that requires accurate modification formulas for retention time prediction; depends on fixed modifications being properly annotated in PSM records)

## Evaluation signals

- All PSM records in the output contain ProForma notation for fixed modifications (e.g., 'C[U:Carbamidomethyl]') at the correct residue positions matching the fixed_modifications map.
- No duplicate modifications are present in the augmented sequences (i.e., if a modification was already reported, it is not inserted again).
- All non-modification PSM fields (scan number, protein, mass, score, etc.) are identical between input and output records.
- Terminal modifications ('N-term', 'C-term') are represented at the sequence boundaries (e.g., '[U:TMT6plex]-PEPTIDE' or 'PEPTIDE-[U:Amidation]') following ProForma v2 convention.
- The number of output PSM records matches the input (no rows lost or duplicated during augmentation).

## Limitations

- Requires a correctly configured fixed_modifications mapping; incomplete or incorrect mappings will result in incomplete or wrong modification annotations.
- Does not validate whether the modification masses are chemically realistic for the peptide or whether the specified residues were actually modified during the experiment.
- If a PSM already contains a partial annotation (e.g., some cysteines labeled but not all), the augmentation step must not introduce conflicts; edge cases with mixed annotation states may require manual curation.
- ProForma notation and residue position conventions may differ across search engines and psm_utils versions; ensure consistent ProForma version (v2 recommended) is used throughout the pipeline.

## Evidence

- [other] How does MS²Rescore add fixed modifications to peptide sequences when these modifications are not already reported in the PSM file?: "Fixed modifications are configured through a mapping that associates ProForma modification labels (e.g., U:Carbamidomethyl, U:TMT6plex) with lists of residue target positions, including special"
- [other] Workflow step details: "For each PSM, iterate through the fixed_modifications map and insert the specified modifications at the appropriate positions in the sequence using ProForma notation (e.g., 'U:Carbamidomethyl') if"
- [intro] When fixed modifications are not reported: "Some search engines, such as MaxQuant, do not report fixed modifications"
- [intro] Fixed modifications configuration: "fixed modifications that are not reported in the PSM file must be configured separately"
- [intro] Feature generator requirement: "some feature generators (such as DeepLC) require the modification formula"
- [intro] PSM input requirements: "MS²Rescore always needs access to **all target and decoy PSMs, without any FDR-filtering**"
- [intro] Modification notation standard: "MS²Rescore uses the `HUPO-PSI standardized ProForma v2 notation` to represent modified peptides"

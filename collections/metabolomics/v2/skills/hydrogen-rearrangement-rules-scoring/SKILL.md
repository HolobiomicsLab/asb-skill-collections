---
name: hydrogen-rearrangement-rules-scoring
description: Use when after MS-CleanR has filtered and clustered LC-MS features and formatted them for MS-FINDER input (m/z, retention time, MS/MS spectra).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3860
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
  tools:
  - MS-CleanR
  - MS-FINDER
  - MS-DIAL
derived_from:
- doi: 10.1021/acs.analchem.0c01594
  title: MS-CleanR
evidence_spans:
- MS-CleanR use as input MS-DIAL peak list processed in data dependent analysis
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ms_cleanr_cq
    doi: 10.1021/acs.analchem.0c01594
    title: MS-CleanR
  dedup_kept_from: coll_ms_cleanr_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.0c01594
  all_source_dois:
  - 10.1021/acs.analchem.0c01594
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# hydrogen-rearrangement-rules-scoring

## Summary

Apply hydrogen rearrangement rules (HRR) scoring system within MS-FINDER to rank and annotate in silico fragmentation predictions for LC-MS features exported from MS-CleanR. HRR scoring enables probabilistic matching of observed MS/MS spectra against theoretical fragment ion models across metabolite databases.

## When to use

After MS-CleanR has filtered and clustered LC-MS features and formatted them for MS-FINDER input (m/z, retention time, MS/MS spectra). Use this skill when your goal is to obtain compound-level annotations for cleaned features by leveraging hydrogen atom rearrangement chemistry during fragmentation prediction, particularly when querying multiple metabolite databases simultaneously.

## When NOT to use

- Input features lack MS/MS spectra (MS1-only data will cause MS-FINDER annotation to fail or produce no results).
- Features have already been manually validated and annotated by orthogonal methods (re-annotation risks overwriting curated assignments).
- Your LC-MS data were acquired in MS1-only mode without data-dependent or data-independent fragmentation.

## Inputs

- MS-CleanR-filtered and clustered feature set (m/z, retention time, MS/MS spectra)
- Features formatted in MS-FINDER compatible input format
- MS/MS fragmentation spectra for selected features

## Outputs

- Per-feature annotations (compound ID, HRR score, database match, structural predictions)
- Unified annotation table merging results across queried databases
- Optionally: .msp file for mass spectral similarity networking

## How to apply

Configure MS-FINDER annotation parameters to enable the hydrogen rearrangement rules (HRR) scoring system before executing in silico annotation on the exported feature set. The HRR scoring system probabilistically ranks fragmentation hypotheses by modeling how hydrogen atoms rearrange during ionization and dissociation. Select one or more target metabolite databases to query (MS-CleanR supports merging results across multiple databases). Execute MS-FINDER annotation, then parse the output results—which include compound ID, HRR score, matched database, and structural predictions per feature—and consolidate these annotations into a unified annotation table keyed by feature identifier. Prioritize annotations based on database confidence ranking and HRR score magnitude when multiple database matches exist for the same feature.

## Related tools

- **MS-FINDER** (Executes in silico annotation using hydrogen rearrangement rules (HRR) scoring system to rank and assign compound identities to LC-MS features) — http://prime.psc.riken.jp/compms/index.html
- **MS-CleanR** (Filters, clusters, and exports cleaned LC-MS features in MS-FINDER-compatible format prior to HRR-based annotation) — https://github.com/eMetaboHUB/MS-CleanR
- **MS-DIAL** (Produces peak lists and MS/MS spectra from raw LC-MS data files; input to MS-CleanR; version 4.00 or higher required) — http://prime.psc.riken.jp/compms/index.html

## Evaluation signals

- All exported features receive a numeric HRR score for each matched compound hypothesis; scores should be present and non-null for every annotated feature.
- Annotations are consolidated into a single table with consistent schema: feature ID, m/z, retention time, compound name, HRR score, database source, and structural class.
- No feature should lack an HRR score if it was successfully passed to MS-FINDER and had MS/MS spectra.
- When multiple databases are queried, merging logic correctly prioritizes results according to user-specified database ranking without duplicating feature rows.
- Structural predictions (e.g., functional groups, molecular formula) should be chemically plausible given the observed m/z and HRR-predicted fragments.

## Limitations

- Features without MS/MS spectra are discarded and cannot be annotated; MS1-only data will cause the annotation step to fail. At least 3 blank and 3 QC samples are needed for blank ratio analysis in prior MS-CleanR filtering steps.
- MS-FINDER HRR scoring is most reliable for small molecules; performance on large polymers, lipid classes, or non-standard metabolites is not explicitly evaluated in the MS-CleanR paper.
- Database coverage is limited to the selected databases queried at annotation time; compounds absent from chosen databases will receive no match regardless of HRR score quality.
- Known bug in R > 4.2: 'Error: the condition has length > 1' can occur during database annotation result merging, requiring R version downgrade or workaround.
- MS-CleanR is no longer actively maintained; active development has shifted to MS-DIAL 5.x, which integrates some MS-CleanR functionality. A new version accounting for MS-DIAL 5 features is in preparation but not yet published.

## Evidence

- [readme] all selected features are exported to MS-FINDER program for in silico-based annotation using hydrogen rearrangement rules (HRR) scoring system: "all selected features are exported to MS-FINDER program for in silico-based annotation using hydrogen rearrangement rules (HRR) scoring system"
- [readme] At this step, multiple databases can be queried and each annotation results will be handled by MS-CleanR: "At this step, multiple databases can be queried and each annotation results will be handled by MS-CleanR"
- [other] Parse MS-FINDER results and consolidate per-feature annotations (compound ID, score, database match, structural predictions) into a unified annotation table: "Parse MS-FINDER results and consolidate per-feature annotations (compound ID, score, database match, structural predictions) into a unified annotation table"
- [readme] All features without MS/MS will be discarded during the first step. If data contain MS1 only, the first MS-CleanR step will crash.: "All features without MS/MS will be discarded during the first step. If data contain MS1 only, the first MS-CleanR step will crash."
- [readme] Needs MS-DIAL (v4.00 or higher) and MS-FINDER (3.30 or higher): "Needs MS-DIAL (v4.00 or higher) and MS-FINDER (3.30 or higher)"

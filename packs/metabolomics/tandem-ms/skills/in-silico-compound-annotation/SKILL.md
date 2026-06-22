---
name: in-silico-compound-annotation
description: Use when after feature filtering and clustering have been completed in MS-CleanR and you have a cleaned feature set with m/z, retention time, and MS/MS spectra data ready for structural assignment. Use it when you need to identify unknown compounds by querying multiple chemical databases (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3801
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - MS-CleanR
  - MS-FINDER
  - MS-DIAL
  techniques:
  - LC-MS
  - tandem-MS
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

# in-silico-compound-annotation

## Summary

Exports filtered and clustered LC-MS features to MS-FINDER for structure prediction and compound identification using hydrogen rearrangement rules (HRR) scoring across multiple chemical databases. This skill bridges feature detection and annotation, enabling prioritized structural assignment when experimental MS/MS spectra alone are insufficient.

## When to use

Apply this skill after feature filtering and clustering have been completed in MS-CleanR and you have a cleaned feature set with m/z, retention time, and MS/MS spectra data ready for structural assignment. Use it when you need to identify unknown compounds by querying multiple chemical databases (e.g., PubChem, HMDB, MassBank) and want to leverage hydrogen rearrangement rules scoring to rank candidate structures by chemical plausibility.

## When NOT to use

- Input data contain only MS1 spectra without MS/MS; MS-CleanR will discard all features during the first filtering step
- Feature set has already been annotated by another tool and you are seeking only to validate or cross-reference results (use orthogonal scoring instead)
- Dataset contains fewer than 3 blank and 3 QC samples, as these are required for proper blank ratio analysis in the upstream cleaning step

## Inputs

- Cleaned and clustered LC-MS feature set from MS-CleanR (output of filtering and clustering steps)
- Feature metadata: m/z values, retention time, MS/MS spectral data
- MS-FINDER software (v3.30 or higher) with configured database indices

## Outputs

- Per-feature annotation table with compound ID, HRR score, database source, and structural predictions
- Merged annotation results integrated with filtered peak list
- Optional .msp export file for mass spectral similarity networking

## How to apply

Format the cleaned and clustered feature set (m/z, retention time, MS/MS spectra) into MS-FINDER-compatible input format (typically msp or text-based format). Configure MS-FINDER annotation parameters by selecting the hydrogen rearrangement rules (HRR) scoring system and specifying which chemical databases to query. Execute MS-FINDER in silico annotation on the exported features. Parse and consolidate per-feature results (compound ID, HRR score, database match source, structural predictions) into a unified annotation table. Finally, merge annotation results back to the filtered peak list, prioritizing database matches according to user-defined criteria (e.g., highest HRR score, preferred database order).

## Related tools

- **MS-FINDER** (In silico structure prediction and compound identification engine; executes HRR-based scoring and queries multiple chemical databases for candidate structure retrieval) — http://prime.psc.riken.jp/compms/index.html
- **MS-CleanR** (Upstream feature filtering and clustering tool that produces the cleaned feature set exported to MS-FINDER; handles blank subtraction, background removal, RSD/RMD filtering, and modularity-based clustering) — https://github.com/eMetaboHUB/MS-CleanR
- **MS-DIAL** (Peak detection and LC-MS data processing software (v4.00 or higher); generates the input peak lists (DDA or DIA mode) that MS-CleanR requires) — http://prime.psc.riken.jp/compms/index.html

## Evaluation signals

- All selected features from the cleaned peak list appear in the annotation table with non-null compound ID and HRR score fields
- HRR scores are numeric values within the expected range (typically 0–100); presence of score indicates successful MS-FINDER execution
- Database source field is populated and matches one of the queried databases specified in MS-FINDER configuration
- Merged annotation results are correctly joined to the filtered peak list by m/z and retention time without row loss or duplication
- Structural predictions (e.g., SMILES, InChI) are valid and can be visualized; optional .msp export is valid text format readable by networking tools

## Limitations

- Features without MS/MS data are automatically discarded during the first filtering step; MS1-only data will cause the workflow to crash
- At least 3 blank and 3 QC samples must be designated in the MS-DIAL sample list for proper blank ratio analysis; undersized studies will fail
- Sample and class names must not contain spaces or hyphens, and class names must be longer than one character, or the workflow will encounter parsing errors
- Known bug in R > 4.2: 'Error: the condition has length > 1' encountered during database annotation merging; requires workaround or R version downgrade
- MS-CleanR is no longer actively maintained as of MS-DIAL v5.x integration; a new version is planned but not yet released

## Evidence

- [intro] Feature clustering based on MS-DIAL peak character and HRR scoring: "feature clustering method based on MS-DIAL peak character estimation algorithm followed by parental signal extraction using multi-level optimization of modularity algorithm"
- [intro] MS-FINDER export with HRR and multiple database support: "all selected features are exported to MS-FINDER program for in silico-based annotation using hydrogen rearrangement rules (HRR) scoring system. At this step, multiple databases can be queried"
- [readme] Annotation result consolidation workflow: "The final step will merge annotation results to the filtered peak list by prioritizing database annotation depending on user choice"
- [readme] MS/MS requirement for workflow success: "All features without MS/MS will be discarded during the first step. If data contain MS1 only, the first MS-CleanR step will crash"
- [readme] Blank and QC sample requirements: "At least 3 blanks and 3 QCs samples are needed for Blank ratio analysis. These samples must be identified as such in the MS-Dial sample list"
- [readme] MS-FINDER version requirement: "Needs MS-DIAL (v4.00 or higher) and MS-FINDER (3.30 or higher)"

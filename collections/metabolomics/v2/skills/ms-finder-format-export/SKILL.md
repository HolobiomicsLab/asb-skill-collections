---
name: ms-finder-format-export
description: Use when after completing MS-CleanR filtering (blank subtraction, background removal, RSD/RMD thresholding) and feature clustering steps, when you have a consolidated set of representative features and need structural identification via MS/MS spectral matching.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
  tools:
  - MS-FINDER
  - MS-CleanR
  - MS-DIAL
derived_from:
- doi: 10.1021/acs.analchem.0c01594
  title: MS-CleanR
evidence_spans:
- all selected features are exported to MS-FINDER program for in silico-based annotation using hydrogen rearrangement rules (HRR) scoring system
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
---

# MS-FINDER Format Export

## Summary

Convert filtered and clustered LC-MS features from MS-CleanR into MS-FINDER-compatible input format (m/z, retention time, MS/MS spectra) to enable in silico compound annotation using hydrogen rearrangement rules scoring across multiple metabolite databases.

## When to use

After completing MS-CleanR filtering (blank subtraction, background removal, RSD/RMD thresholding) and feature clustering steps, when you have a consolidated set of representative features and need structural identification via MS/MS spectral matching. Use when your data includes MS/MS spectra (DDA or DIA mode with fragment information); MS1-only data will fail at this stage.

## When NOT to use

- Input data contains only MS1 spectra without MS/MS fragments (MS-CleanR will crash in the first filtering step; MS-FINDER requires fragmentation data)
- Features have already been annotated via external tools and merged — skip to results prioritization rather than re-exporting
- LC-MS data acquired in full-scan mode only (no data-dependent or data-independent MS/MS collection)

## Inputs

- MS-CleanR clustered feature set (m/z, retention time, MS/MS spectra per representative feature)
- Feature metadata (sample class, ionization mode origin)
- MS/MS fragmentation spectra (centroided or profile mode)

## Outputs

- MS-FINDER-formatted input file(s) with feature m/z, retention time, and MS/MS spectra
- MS-FINDER annotation results (compound ID, HRR score, database match, structural predictions)
- Unified annotation table (feature → top-ranked compound match with confidence metrics)

## How to apply

Load the cleaned feature set output from MS-CleanR clustering (containing m/z, retention time, and associated MS/MS spectra for each representative feature). Format each feature into MS-FINDER input specification: organize m/z and retention time as continuous values, embed full MS/MS fragmentation spectrum with peak intensities, and structure as a text-based or binary format compatible with MS-FINDER 3.30+. Configure MS-FINDER annotation parameters to activate hydrogen rearrangement rules (HRR) scoring and select target databases (e.g., MassBank, GNPS, in-house libraries). Execute MS-FINDER in silico search and parse output to extract per-feature compound ID, match score, database source, and predicted molecular structure. Consolidate all annotation results into a unified table keyed by feature m/z and retention time.

## Related tools

- **MS-FINDER** (In silico annotation engine using hydrogen rearrangement rules (HRR) scoring to identify compounds from MS/MS spectra against multiple databases) — http://prime.psc.riken.jp/compms/index.html
- **MS-CleanR** (Upstream feature filtering and clustering; produces the cleaned feature set that is exported to MS-FINDER) — https://github.com/eMetaboHUB/MS-CleanR
- **MS-DIAL** (Prerequisite peak detection and MS/MS data processing (v4.00+); generates the peak list input consumed by MS-CleanR) — http://prime.psc.riken.jp/compms/index.html

## Examples

```
# After MS-CleanR filtering and clustering, export features to MS-FINDER format:
# In R, within MS-CleanR workflow:
# mscleanr::export_to_msfinder(cleaned_features, output_file="features_for_msfinder.msp", hrr_scoring=TRUE, databases=c("MassBank", "GNPS"))
```

## Evaluation signals

- MS-FINDER input file is successfully parsed without format errors; feature count and MS/MS spectrum counts match the input feature set
- Annotation results contain non-empty compound IDs and HRR scores for ≥70% of queried features (expected hit rate for known metabolites in populated databases)
- Consolidated annotation table is keyed by feature m/z and retention time with no missing values in score and database origin columns
- Multiple database query results are captured and ranked consistently; database priority prioritization logic is applied correctly during consolidation
- Export can be validated by spot-checking 3–5 features: verify that m/z and retention time in output match input, and that top annotation score is reasonable (HRR scores typically 0–100)

## Limitations

- Requires MS/MS spectra for all features; MS1-only data will cause MS-CleanR to crash before export is attempted
- MS-FINDER annotation quality depends on database completeness and quality; known metabolites will have higher match confidence than unknown compounds
- Hydrogen rearrangement rules (HRR) scoring is optimized for small organic molecules; performance may degrade for large polymers or atypical adducts
- Multiple database querying increases runtime; large feature sets (>10,000 features) with many databases can require hours
- At least 3 blank and 3 QC samples must be labeled in MS-DIAL sample list for proper blank ratio analysis upstream; missing blanks will compromise feature filtering quality before export

## Evidence

- [readme] all selected features are exported to MS-FINDER program for in silico-based annotation using hydrogen rearrangement rules (HRR) scoring system: "all selected features are exported to MS-FINDER program for in silico-based annotation using hydrogen rearrangement rules (HRR) scoring system"
- [readme] multiple databases can be queried and each annotation results will be handled by MS-CleanR: "At this step, multiple databases can be queried and each annotation results will be handled by MS-CleanR"
- [other] Format feature data (m/z, retention time, MS/MS spectra) into MS-FINDER compatible input format: "Format feature data (m/z, retention time, MS/MS spectra) into MS-FINDER compatible input format"
- [readme] All features without MS/MS will be discarded during the first step: "All features without MS/MS will be discarded during the first step. If data contain MS1 only, the first MS-CleanR step will crash"
- [other] Parse MS-FINDER results and consolidate per-feature annotations: "Parse MS-FINDER results and consolidate per-feature annotations (compound ID, score, database match, structural predictions) into a unified annotation table"

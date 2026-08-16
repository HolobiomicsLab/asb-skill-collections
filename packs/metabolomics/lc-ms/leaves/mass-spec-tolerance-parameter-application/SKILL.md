---
name: mass-spec-tolerance-parameter-application
description: Use when when you have a feature table from Orbitrap LC-MS containing m/z, retention time, and intensity columns, and you need to group individual mass features into putative metabolites that represent the same chemical entity across different ionization states and isotopic compositions.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3800
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - khipu
  - Python
  - Asari
  - metDataModel
  techniques:
  - LC-MS
derived_from:
- doi: 10.1371/journal.pcbi.1011912
  title: pcpfm
evidence_spans:
- pre-annotation to group featues to empirical compounds (khipu)
- Python-Centric Pipeline for Metabolomics
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_pcpfm_cq
    doi: 10.1371/journal.pcbi.1011912
    title: pcpfm
  dedup_kept_from: coll_pcpfm_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1371/journal.pcbi.1011912
  all_source_dois:
  - 10.1371/journal.pcbi.1011912
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-spec-tolerance-parameter-application

## Summary

Application of mass-to-charge (m/z) and retention time (RT) tolerances to group co-eluting isotopologues and adducts into empirical compounds during LC-MS feature pre-annotation. This skill operationalizes instrument-specific calibration and chromatographic resolution into concrete tolerance thresholds for metabolite grouping.

## When to use

When you have a feature table from Orbitrap LC-MS containing m/z, retention time, and intensity columns, and you need to group individual mass features into putative metabolites that represent the same chemical entity across different ionization states and isotopic compositions. Apply this skill prior to MS1 or MS2 annotation to reduce redundant annotation attempts and improve downstream compound identification.

## When NOT to use

- Input feature table is already curated or deduplicated by adduct/isotope (risk of over-grouping or incorrect merging)
- Data are from instruments with markedly different mass accuracy (e.g. quadrupole or TOF with <1 ppm calibration stability) — tolerances may require instrument-specific recalibration
- Samples contain heavy isotope labeling or spike-in isotopologues intended to remain separate; standard grouping may conflate labeling pools

## Inputs

- feature table (TSV or similar tabular format) with columns: m/z, retention time (seconds), intensity, and optionally feature ID
- ionization mode specification (positive or negative)

## Outputs

- empirical compound (EmpCpd) JSON structure mapping feature groups to putative metabolites with pre-annotation adduct/isotope labels
- serialized JSON file containing grouped EmpCpd objects for downstream annotation

## How to apply

Initialize khipu with default Orbitrap LC-MS tolerances: m/z tolerance of 5 ppm (parts per million) and retention time tolerance of 2 seconds. These tolerances define the matching criteria for grouping features as isotopologues (13C isotopes up to m+3, charges up to z=3) and common adducts (mode-specific: [M+H]+, [M+Na]+, [M+NH4]+ for positive; [M−H]−, [M+Cl]− for negative). Apply the m/z tolerance as a relative error bound calculated from the nominal mass and the feature's measured m/z; apply the RT tolerance as an absolute window around each feature's observed retention time. Features within both tolerances are grouped together; each resulting group is assigned to a single empirical compound with a pre-annotation label indicating the inferred adduct and isotope state (e.g., '[M+H]+', '[M+13C]+'). The rationale is that Orbitrap mass accuracy and standard reversed-phase chromatographic resolution support these tolerances for typical small-molecule metabolomics without excessive false grouping.

## Related tools

- **khipu** (Core tool implementing grouping logic and pre-annotation of feature groups into empirical compounds using specified m/z and RT tolerances) — https://github.com/shuzhao-li-lab/khipu
- **Asari** (Upstream tool that generates the feature table (m/z, retention time, intensity) consumed by khipu) — https://github.com/shuzhao-li/asari
- **metDataModel** (Provides data structures and schemas for EmpCpd serialization and JSON output format) — https://github.com/shuzhao-li-lab/metDataModel
- **Python** (Programming language and runtime for invoking khipu and orchestrating tolerance parameter application)

## Evaluation signals

- Verify that features grouped into the same EmpCpd have m/z differences ≤ 5 ppm of the nominal m/z and retention time differences ≤ 2 seconds
- Check that pre-annotation labels are correctly assigned: [M+H]+ or [M+Na]+ for positive mode, [M−H]− or [M+Cl]− for negative mode, and isotope annotations match the observed m/z delta (e.g., m+13C ≈ 1.0034 Da per carbon)
- Confirm that all features from the input table are assigned to exactly one EmpCpd group (no orphans or duplicates)
- Validate that empirical compound JSON structure conforms to the metDataModel schema (presence of required fields: mz, rt, adduct, charge, isotope)
- Spot-check a small number of grouped features in the raw feature table against the EmpCpd JSON to ensure coherence (e.g., re-calculate m/z deltas and RT spans manually for a few groups)

## Limitations

- Default 5 ppm and 2 sec tolerances are calibrated for Orbitrap instruments with standard reversed-phase chromatography; other mass analyzers or chromatography modes may require recalibration
- Tolerances do not account for co-eluting isomers or isobars from different metabolites; manual curation or additional MS2 data may be needed to resolve ambiguities
- Very high feature density (>100 features per 2 sec RT window, <5 ppm m/z spread) may cause over-grouping if isotope/adduct patterns overlap; user should assess clustering visually or via dashboard inspection in Asari
- Isotope and adduct patterns are pre-defined; novel or unusual adducts (e.g., [M+2Na−H]+ or very high charges) are not detected without custom parameter modification

## Evidence

- [other] Khipu constructs empirical compounds by grouping features as isotopes and adducts with default parameters: charges up to z=3, m+13C3 isotopologues, common adducts by chromatography mode, 5 ppm mz tolerance, and 2 sec rt tolerance for Orbitrap LC data.: "Khipu constructs empirical compounds by grouping features as isotopes and adducts with default parameters: charges up to z=3, m+13C3 isotopologues, common adducts by chromatography mode, 5 ppm mz"
- [other] Group features by applying m/z tolerance (5 ppm) and retention time tolerance (2 seconds) to identify co-eluting isotopologues and adducts.: "Group features by applying m/z tolerance (5 ppm) and retention time tolerance (2 seconds) to identify co-eluting isotopologues and adducts."
- [other] Initialize khipu with default adducts for the inferred ionization mode (positive or negative) and isotope patterns (m+13C up to 3 carbons, charges up to z=3).: "Initialize khipu with default adducts for the inferred ionization mode (positive or negative) and isotope patterns (m+13C up to 3 carbons, charges up to z=3)."
- [other] Assign each group to an empirical compound with a pre-annotation label indicating the inferred adduct and isotope state.: "Assign each group to an empirical compound with a pre-annotation label indicating the inferred adduct and isotope state."
- [readme] pre-annotation to group featues to empirical compounds (khipu): "pre-annotation to group featues to empirical compounds (khipu)"

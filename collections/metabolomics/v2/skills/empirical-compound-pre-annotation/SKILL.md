---
name: empirical-compound-pre-annotation
description: Use when after feature detection from mzML files (e.g., via Asari) when
  you have a feature table with m/z, retention time, and intensity columns, and before
  MS1 or MS2 annotation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3933
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - khipu
  - Python
  - Asari
  - mass2chem
  - metDataModel
  techniques:
  - LC-MS
  - GC-MS
  license_tier: restricted
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

# empirical-compound-pre-annotation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Group co-eluting LC-MS features into empirical compounds by detecting isotopologues and adducts using mass tolerance and retention time clustering. This pre-annotation step transforms raw feature tables into higher-level metabolite representations suitable for MS1/MS2 annotation.

## When to use

After feature detection from mzML files (e.g., via Asari) when you have a feature table with m/z, retention time, and intensity columns, and before MS1 or MS2 annotation. Use this when working with Orbitrap LC-MS data in positive or negative ionization mode and you need to collapse multiple isotopologues and adducts into single putative metabolite entities for downstream annotation and statistical analysis.

## When NOT to use

- Input is already aggregated at the empirical compound or metabolite level (e.g., already annotated with HMDB IDs or chemical structures).
- Data are from GC-MS, GC-EI, or other non-LC-MS ionization modes not covered by default khipu adduct libraries.
- Retention time information is missing or unreliable (clustering will degrade without RT co-elution confirmation).

## Inputs

- Feature table (TSV or CSV) with m/z, retention time, and intensity columns
- Ionization mode (positive or negative, inferred or specified)
- mzML or raw LC-MS metadata (optional, for parameter inference)

## Outputs

- EmpCpd JSON file (empirical compounds with grouped features and pre-annotation labels)
- Grouped feature-to-compound mapping (internal to EmpCpd structure)

## How to apply

Initialize khipu with default parameters tuned for Orbitrap LC-MS: m/z tolerance of 5 ppm, retention time tolerance of 2 seconds, charge states up to z=3, and isotope patterns including m+13C up to 3 carbons. Load the feature table and infer ionization mode (positive or negative) from the data or metadata. Apply feature grouping by matching m/z and retention time within these tolerances to identify co-eluting isotopologues and common adducts. Assign each grouped cluster a single empirical compound identifier with a pre-annotation label encoding the inferred adduct and isotope state. Serialize the grouped EmpCpd structure to JSON format and save to the experiment's annotations subdirectory for use in downstream annotation workflows.

## Related tools

- **khipu** (Core grouping engine: clusters features into isotopologues and adducts using m/z and RT tolerance; assigns pre-annotation labels to empirical compounds) — https://github.com/shuzhao-li-lab/khipu
- **Asari** (Upstream feature detection tool that produces the feature table input to khipu pre-annotation) — https://github.com/shuzhao-li/asari
- **mass2chem** (Utility library for interpreting mass spectrometry data and adduct annotation rules) — https://github.com/shuzhao-li-lab/mass2chem
- **metDataModel** (Data model framework for representing empirical compounds and feature groupings in standard JSON format) — https://github.com/shuzhao-li-lab/metDataModel
- **Python** (Programming language for scripting khipu workflow and I/O operations)

## Evaluation signals

- EmpCpd JSON file is created and contains valid JSON structure with grouped features and pre-annotation labels.
- Each empirical compound contains ≥1 feature; features within a compound have m/z differences ≤5 ppm and RT differences ≤2 seconds.
- Adduct and isotope state labels are correctly inferred (e.g., '[M+H]+', '[M+Na]+', 'M+13C1', etc.) and match expected ionization mode.
- Feature count in EmpCpd file is ≤ feature count in input table (clustering should not duplicate or lose features).
- JSON schema validation passes against metDataModel EmpCpd specification; no malformed or orphaned feature entries.

## Limitations

- Default parameters (5 ppm m/z, 2 sec RT) are optimized for Orbitrap instruments and may not be appropriate for lower-resolution instruments (e.g., Quadrupole, Ion trap) or very high-resolution systems (e.g., FTICR) without tuning.
- GC-MS and other non-LC ionization modes are not yet supported; support under development.
- Internal spike-in standards for quality control flagging are not yet implemented.
- Clustering performance depends heavily on retention time accuracy; poor or missing RT data will cause false positive groupings across co-eluting metabolites with similar m/z.
- Pre-annotation labels do not constitute biological or chemical validation; they are inferred mass signatures requiring downstream MS1 or MS2 annotation for confirmation.

## Evidence

- [other] Khipu constructs empirical compounds by grouping features as isotopes and adducts with default parameters: charges up to z=3, m+13C3 isotopologues, common adducts by chromatography mode, 5 ppm mz tolerance, and 2 sec rt tolerance for Orbitrap LC data.: "Khipu constructs empirical compounds by grouping features as isotopes and adducts with default parameters: charges up to z=3, m+13C3 isotopologues, common adducts by chromatography mode, 5 ppm mz"
- [other] Group features by applying m/z tolerance (5 ppm) and retention time tolerance (2 seconds) to identify co-eluting isotopologues and adducts.: "Group features by applying m/z tolerance (5 ppm) and retention time tolerance (2 seconds) to identify co-eluting isotopologues and adducts."
- [other] Assign each group to an empirical compound with a pre-annotation label indicating the inferred adduct and isotope state.: "Assign each group to an empirical compound with a pre-annotation label indicating the inferred adduct and isotope state."
- [intro] pre-annotation to group featues to empirical compounds (khipu): "pre-annotation to group featues to empirical compounds (khipu)"
- [readme] This includes feature tables that are optionally blank masked, normalized, batch corrected, annotated or otherwise curated by PCPFM and empirical compounds as a JSON file representing putative metabolites: "empirical compounds as a JSON file representing putative metabolites"
- [intro] We are working to add supports of GC and other data types.: "We are working to add supports of GC and other data types."

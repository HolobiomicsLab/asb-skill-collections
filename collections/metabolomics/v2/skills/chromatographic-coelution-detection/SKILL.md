---
name: chromatographic-coelution-detection
description: Use when after feature detection when you have a feature table with m/z,
  retention time, and intensity columns, and you need to group features into empirical
  compounds (putative metabolites) that account for isotopologue patterns and multiple
  adduct forms arising from a single underlying analyte.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_0639
  - http://edamontology.org/topic_3370
  tools:
  - ThermoRawFileParser
  - khipu
  - Python
  - Asari
  - metDataModel
  - mass2chem
  techniques:
  - LC-MS
  license_tier: open
derived_from:
- doi: 10.1371/journal.pcbi.1011912
  title: pcpfm
evidence_spans:
- convert Thermo .raw to mzML (ThermoRawFileParser)
- pre-annotation to group featues to empirical compounds (khipu)
- Python-Centric Pipeline for Metabolomics
- The Python-Centric Pipeline for Metabolomics
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_pcpfm
    doi: 10.1371/journal.pcbi.1011912
    title: pcpfm
  - build: coll_pcpfm_cq
    doi: 10.1371/journal.pcbi.1011912
    title: pcpfm
  dedup_kept_from: coll_pcpfm
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

# chromatographic-coelution-detection

## Summary

Detect and group coeluting features (isotopes and adducts) within configurable m/z and retention time windows to construct empirical compound clusters. This skill identifies metabolite-related ion signals that share the same chromatographic peak, enabling pre-annotation of putative metabolites before MS2 matching.

## When to use

Apply this skill after feature detection when you have a feature table with m/z, retention time, and intensity columns, and you need to group features into empirical compounds (putative metabolites) that account for isotopologue patterns and multiple adduct forms arising from a single underlying analyte.

## When NOT to use

- Input is already a validated set of empirical compounds or annotated metabolites; skip to MS1/MS2 annotation workflows.
- m/z tolerance or rt tolerance values are unknown and cannot be estimated from your instrument's calibration or literature; consult your analytical method first.
- Feature table is in a non-standard format (not TSV) or lacks retention time information; convert or enrich the table before grouping.

## Inputs

- Feature table (TSV format with m/z, retention time, and intensity columns)
- Ionization mode specification (positive or negative)
- Adduct definitions for the detected polarity

## Outputs

- empCpd.json file containing empirical compound groups
- JSON structure with fields: list_of_features, median_mz, median_rt, pre-annotation

## How to apply

Load the feature table (TSV format) from asari_results and invoke khipu's build_empCpds command, specifying ionization mode and configurable m/z tolerance (default 5 ppm) and retention time tolerance (default 2 seconds). The algorithm clusters features by matching isotope mass differences and charge-state patterns within these windows, then serializes grouped features to JSON with median m/z, median rt, list_of_features, and pre-annotation fields. Validate the output JSON structure to confirm all required fields are present and that feature groupings are chemically plausible (e.g., isotope spacing matches expected Δm/z for 13C, 2H, etc.).

## Related tools

- **khipu** (Constructs empirical compound groups from feature tables using configurable m/z and retention time tolerances; performs clustering of isotopes and adducts based on mass difference patterns) — https://github.com/shuzhao-li-lab/khipu
- **Asari** (Produces the feature table (TSV format) that serves as input to the coelution detection workflow) — https://github.com/shuzhao-li/asari
- **Python** (Execution environment and scripting for invoking khipu commands and validating JSON output)

## Examples

```
khipu build_empCpds preferred_Feature_table.tsv --mz_tolerance 5 --rt_tolerance 2 --ionization_mode positive --adduct_definitions default
```

## Evaluation signals

- JSON output file is valid and parseable with all required fields (list_of_features, median_mz, median_rt, pre-annotation) present for each empirical compound group.
- Grouped features within each empirical compound satisfy the specified m/z tolerance (default 5 ppm) and retention time tolerance (default 2 seconds) constraints.
- Observed mass differences between grouped features match expected isotope shifts (e.g., 1.003 Da for 13C–12C, 0.5 Da for doubly charged ions) or known adduct mass differences (e.g., 0.495 Da for [M+Na]+ vs [M+H]+).
- No singleton features are incorrectly merged across distinct empirical compounds; verify that feature groups are chemically coherent.
- Median m/z and median rt values calculated from list_of_features align with the consensus values in the JSON output.

## Limitations

- Default tolerances (5 ppm m/z, 2 seconds rt) may require tuning for instruments with different mass accuracy or chromatographic resolution; users with high-resolution or narrow-window chromatography should validate empirically.
- Coelution detection assumes that isotope and adduct patterns follow standard ionization chemistry; unusual or atypical ion formations (e.g., dimers, in-source fragmentation) may produce false groupings or negatives.
- Retention time tolerance is absolute (in seconds) rather than relative, which may cause under-grouping in long gradient methods where retention time drift is significant.
- Pre-annotation assigns labels based on mass difference heuristics but does not validate against reference standards or MS2 spectra; chemical plausibility should be confirmed downstream.

## Evidence

- [other] The build_empCpds command groups features into empirical compounds by matching isotopes and adducts with configurable mz tolerance (default 5 ppm) and rt tolerance (default 2 seconds), producing a JSON file containing grouped features with their mz and rt values.: "grouping features into empirical compounds by matching isotopes and adducts with configurable mz tolerance (default 5 ppm) and retention time tolerance (default 2 seconds)"
- [other] Invoke khipu via the build_empCpds command with configurable m/z tolerance (default 5 ppm) and retention time tolerance (default 2 seconds), specifying ionization mode and adduct definitions for the detected polarity.: "Invoke khipu via the build_empCpds command with configurable m/z tolerance (default 5 ppm) and retention time tolerance (default 2 seconds), specifying ionization mode and adduct definitions"
- [other] Serialize the empirical compound collection to JSON format, including list_of_features, median m/z, median rt, and pre-annotation fields for each group.: "Serialize the empirical compound collection to JSON format, including list_of_features, median m/z, median rt, and pre-annotation fields"
- [intro] pre-annotation to group featues to empirical compounds (khipu): "pre-annotation to group featues to empirical compounds (khipu)"
- [other] Load the preferred feature table (TSV format) from the asari_results subdirectory.: "Load the preferred feature table (TSV format) from the asari_results subdirectory"

---
name: empirical-compound-construction-from-feature-clustering
description: Use when after feature detection and quality control have produced a feature table in TSV format from Asari or equivalent preprocessing.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3767
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0625
  tools:
  - ThermoRawFileParser
  - khipu
  - Python
  - Asari
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
  dedup_kept_from: coll_pcpfm
schema_version: 0.2.0
---

# empirical-compound-construction-from-feature-clustering

## Summary

Groups individual LC-MS features into empirical compounds by clustering features within configurable m/z and retention time windows, then annotates isotopologues and adducts based on observed mass differences and charge state patterns. This pre-annotation step produces a structured JSON representation of putative metabolites ready for downstream MS1 and MS2 annotation.

## When to use

Apply this skill after feature detection and quality control have produced a feature table in TSV format from Asari or equivalent preprocessing. Use it when you need to collapse thousands of individual features (adducts, isotopologues, fragments) into fewer, biologically coherent empirical compound groups before MS1/MS2 annotation or when you want a JSON-serialized empirical compound collection for standardized downstream analysis.

## When NOT to use

- Input is already annotated at the compound level with metabolite identities — this skill groups unannotated features, not compounds.
- m/z and retention time information is unavailable or missing from the feature table — clustering requires both dimensions.
- You need final, validated metabolite identifications — this produces pre-annotation only; MS1 and MS2 annotation steps are required afterward.

## Inputs

- Feature table in TSV format from Asari (containing m/z, retention time, intensity columns)
- Ionization mode specification (positive or negative polarity)
- Adduct definitions list for the detected polarity

## Outputs

- empCpd.json file containing grouped empirical compounds with list_of_features, median m/z, median rt, and pre-annotation fields
- JSON structure with one empirical compound object per cluster

## How to apply

Load the preferred feature table (TSV format) from the asari_results subdirectory. Invoke khipu's build_empCpds command, specifying the ionization mode (positive or negative) and adduct definitions for the detected polarity. Configure two key tolerances: m/z tolerance (default 5 ppm, controls which features group together on mass axis) and retention time tolerance (default 2 seconds, controls temporal co-elution clustering). The command clusters features within these windows, assigns isotopologue and adduct annotations based on observed mass differences (e.g., 1.003 Da for [13C], 0.998 Da for [M+H]→[M-H]) and charge state patterns, then serializes each group to JSON with fields: list_of_features, median m/z, median rt, and pre-annotation. Validate the output JSON structure to confirm all required fields are populated and feature counts are non-zero.

## Related tools

- **khipu** (Performs feature clustering into empirical compounds via build_empCpds command with configurable m/z and rt tolerances; annotates isotopologues and adducts based on mass differences and charge state patterns) — https://github.com/shuzhao-li-lab/khipu
- **Asari** (Upstream feature detection and quality control producing the TSV feature table input to empirical compound construction) — https://github.com/shuzhao-li/asari
- **Python** (Scripting environment and runtime for executing khipu and post-processing JSON output)

## Examples

```
khipu build_empCpds --feature_table asari_results/preferred_Feature_table.tsv --mode positive --mz_tolerance 5 --rt_tolerance 2 --output_json annotations/empCpd.json
```

## Evaluation signals

- JSON output is valid and parses without structural errors; all expected fields (list_of_features, median_mz, median_rt, pre_annotation) are present in every empirical compound object.
- Median m/z and rt values for each empirical compound fall within the union of their constituent feature values, confirming correct aggregation.
- No empirical compound contains features with pairwise m/z differences exceeding the configured tolerance (default 5 ppm) or rt differences exceeding the configured tolerance (default 2 seconds).
- Pre-annotation labels correctly reflect observed mass offsets (e.g., [M+H], [M+Na], [13C]isotopologues) consistent with the ionization mode and adduct definitions supplied.
- Feature count per empirical compound is non-zero and total feature count across all empirical compounds matches the input feature table row count.

## Limitations

- Tolerance parameters (5 ppm m/z, 2 seconds rt) are defaults and may require manual tuning for different instrument types, chromatographic methods, or metabolite classes; overly strict tolerances risk fragmenting true compounds, while overly loose tolerances merge distinct features.
- Adduct annotation relies on exact mass differences; modifications or in-source fragments not captured in the adduct definition list will be treated as separate empirical compounds or misannotated.
- Pre-annotation is heuristic and does not constitute final metabolite identification; requires subsequent MS1 and MS2 annotation steps for validation.
- The skill assumes feature table input is already quality-controlled (blanks masked, low-intensity features filtered) — poor upstream QC will propagate spurious features into empirical compounds.

## Evidence

- [other] The build_empCpds command groups features into empirical compounds by matching isotopes and adducts with configurable mz tolerance (default 5 ppm) and rt tolerance (default 2 seconds), producing a JSON file containing grouped features with their mz and rt values.: "build_empCpds command groups features into empirical compounds by matching isotopes and adducts with configurable mz tolerance (default 5 ppm) and rt tolerance (default 2 seconds), producing a JSON"
- [other] Construct feature groups by clustering features within the specified m/z and rt windows, assigning isotopologue and adduct annotations based on observed mass differences and charge state patterns.: "clustering features within the specified m/z and rt windows, assigning isotopologue and adduct annotations based on observed mass differences and charge state patterns"
- [intro] pre-annotation to group featues to empirical compounds (khipu): "pre-annotation to group featues to empirical compounds (khipu)"
- [readme] This includes feature tables that are optionally blank masked, normalized, batch corrected, annotated or otherwise curated by PCPFM and empirical compounds as a JSON file representing putative metabolites that can be annotated with MS1, MS2, or authentic standards.: "empirical compounds as a JSON file representing putative metabolites that can be annotated with MS1, MS2, or authentic standards"
- [other] Load the preferred feature table (TSV format) from the asari_results subdirectory. Invoke khipu via the build_empCpds command with configurable m/z tolerance (default 5 ppm) and retention time tolerance (default 2 seconds), specifying ionization mode and adduct definitions for the detected polarity.: "Load the preferred feature table (TSV format) from the asari_results subdirectory. Invoke khipu via the build_empCpds command with configurable m/z tolerance (default 5 ppm) and retention time"
- [other] Serialize the empirical compound collection to JSON format, including list_of_features, median m/z, median rt, and pre-annotation fields for each group.: "Serialize the empirical compound collection to JSON format, including list_of_features, median m/z, median rt, and pre-annotation fields for each group"

---
name: feature-table-moniker-registration-and-versioning
description: Use when after Asari completes feature detection and produces multiple feature table variants (full and quality-filtered preferred tables) from centroid mzML files within a PCPFM experiment.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3941
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - Asari
  - Python
  - metDataModel
  techniques:
  - LC-MS
derived_from:
- doi: 10.1371/journal.pcbi.1011912
  title: pcpfm
evidence_spans:
- pcpfm asari -i ./my_experiment
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

# feature-table-moniker-registration-and-versioning

## Summary

Register and version multiple feature table outputs from LC-MS preprocessing (Asari) into a persistent experiment object using semantic monikers ('full', 'preferred') to enable downstream traceability and alternative analysis paths. This skill ensures feature tables are discoverable, versioned, and ready for normalization, annotation, and quality control without manual file management.

## When to use

After Asari completes feature detection and produces multiple feature table variants (full and quality-filtered preferred tables) from centroid mzML files within a PCPFM experiment. Use this skill when you need to track which feature table version was used for downstream analysis, support reproducibility across QC and statistical workflows, or enable retrospective comparison between full and filtered feature sets.

## When NOT to use

- Input feature tables are not Asari outputs (use this skill only after Asari feature detection is complete; manual feature tables require different registration logic)
- Only a single feature table is available (moniker registration is most valuable when tracking multiple related versions; single-table workflows need only basic file reference)
- Feature tables are already integrated into a downstream statistical or annotation tool that does not support external experiment object registration

## Inputs

- PCPFM experiment object (initialized with mzML metadata and ionization mode)
- Asari full feature table (TSV) — all detected features
- Asari preferred feature table (TSV) — quality-filtered features

## Outputs

- Experiment object with registered feature table monikers ('full', 'preferred')
- Moniker-to-file mapping stored in experiment.json
- Feature tables accessible for downstream normalization and annotation

## How to apply

Upon completion of Asari processing on the converted_acquisitions directory, retrieve both the full feature table and the preferred (quality-filtered) feature table from the asari_results directory. Register each table in the experiment object (a persistent data container that holds experiment metadata, sample annotations, and linked outputs) using semantic monikers: 'full' for the complete unfiltered feature table and 'preferred' for features meeting Asari's built-in quality thresholds. The registration step stores the table reference and moniker in the experiment object's metadata, making both tables accessible by name for subsequent normalization, batch correction, annotation, and quality-control steps. This approach decouples the analysis branching decision (which table to use) from the file system, enabling multiple analyses to reference the same underlying data via consistent naming.

## Related tools

- **Asari** (Performs LC-MS feature detection from centroid mzML files and generates full and preferred feature tables registered by this skill) — https://github.com/shuzhao-li/asari
- **metDataModel** (Provides the experiment object data structure for storing moniker-to-table mappings and experiment-wide metadata) — https://github.com/shuzhao-li-lab/metDataModel
- **Python** (Programming language used to invoke registration methods on the experiment object and serialize monikers to experiment.json)

## Examples

```
experiment.register_feature_table(moniker='full', path='./asari_results/export/full_feature_table.tsv'); experiment.register_feature_table(moniker='preferred', path='./asari_results/preferred_Feature_table.tsv'); experiment.save()
```

## Evaluation signals

- Verify both 'full' and 'preferred' monikers are present in experiment.json and map to valid file paths in asari_results/
- Confirm downstream workflow steps (e.g., normalization, annotation) can retrieve feature tables by moniker name without hardcoding file paths
- Check that experiment object's feature_tables dictionary includes entries keyed by 'full' and 'preferred' with correct row/column dimensions matching Asari output
- Validate that re-loading the experiment object from disk restores all registered monikers and file references without loss
- Ensure audit trail in experiment.json records Asari parameters (m/z tolerance: 5 ppm, RT tolerance: 2 sec) used to generate each registered table

## Limitations

- Moniker registration assumes Asari has already been run and both full and preferred tables exist; if Asari fails or is not invoked, registration will fail.
- The schema does not version tables within a moniker (e.g., if Asari is re-run with different parameters, the old 'preferred' table is overwritten); users must manually archive old tables if comparison is needed.
- Registration is tied to the local experiment directory structure; moving or renaming asari_results subdirectory after registration breaks file path references unless experiment.json is updated.
- No built-in support for custom monikers or multiple feature tables from alternative tools; registration workflow is optimized for Asari output and may require adaptation for khipu-grouped or user-created feature tables.

## Evidence

- [other] Asari generates two feature table monikers upon completion: 'full' for the complete feature table and 'preferred' for a filtered feature table suitable for downstream analysis.: "Asari generates two feature table monikers upon completion: 'full' for the complete feature table and 'preferred' for a filtered feature table suitable for downstream analysis."
- [other] Register both feature tables in the experiment object with monikers 'full' and 'preferred' respectively, making them accessible for subsequent normalization, annotation, and quality control steps.: "Register both feature tables in the experiment object with monikers 'full' and 'preferred' respectively, making them accessible for subsequent normalization, annotation, and quality control steps."
- [other] Asari outputs a full feature table containing all detected features and a preferred feature table with quality-filtered features, both stored in the asari_results directory.: "Asari outputs a full feature table containing all detected features and a preferred feature table with quality-filtered features, both stored in the asari_results directory."
- [readme] Outputs are intended to be immediately usable for downstream analysis (e.g. MetaboAnalyst or common tools in R, Python etc.). This includes feature tables that are optionally blank masked, normalized, batch corrected, annotated or otherwise curated by PCPFM: "Outputs are intended to be immediately usable for downstream analysis (e.g. MetaboAnalyst or common tools in R, Python etc.). This includes feature tables that are optionally blank masked,"

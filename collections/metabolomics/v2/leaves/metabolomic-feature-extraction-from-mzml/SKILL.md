---
name: metabolomic-feature-extraction-from-mzml
description: Use when you have centroid mzML files from LC-MS acquisitions and need
  to detect, group, and quantify metabolomic features for a PCPFM experiment. Use
  it as the first feature-level processing step after file format conversion from
  raw instrument files (e.g., .raw to mzML via ThermoRawFileParser).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3557
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - Asari
  - Python
  - ThermoRawFileParser
  - PCPFM (Python-Centric Pipeline for Metabolomics)
  techniques:
  - LC-MS
  - GC-MS
  license_tier: open
  provenance_tier: literature
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

# metabolomic-feature-extraction-from-mzml

## Summary

Extract and table metabolomic features from centroid mzML files using Asari, producing both a complete feature table and a quality-filtered preferred table suitable for downstream analysis. This skill converts raw mass spectrometry acquisition data into quantified, grouped features with m/z and retention time identifiers.

## When to use

Apply this skill when you have centroid mzML files from LC-MS acquisitions and need to detect, group, and quantify metabolomic features for a PCPFM experiment. Use it as the first feature-level processing step after file format conversion from raw instrument files (e.g., .raw to mzML via ThermoRawFileParser). This skill is required if your downstream goal is normalization, annotation, or statistical analysis of metabolomic data.

## When NOT to use

- Input files are already in feature table format (TSV, CSV) — skip directly to normalization or annotation
- Input files are non-centroided profile mzML; Asari requires centroid mzML input
- Support for GC-MS data is under development and should not be assumed production-ready

## Inputs

- centroid mzML files (ionization-mode-specific, e.g., positive or negative mode)
- PCPFM experiment object with inferred ionization mode
- mzML file header metadata specifying polarity

## Outputs

- full feature table (all detected features, TSV format)
- preferred feature table (quality-filtered features, TSV format)
- registered feature tables in experiment.json with monikers 'full' and 'preferred'

## How to apply

Load the PCPFM experiment object and infer the ionization mode (positive or negative) from the mzML file headers to match the mass spectrometry acquisition polarity. Invoke Asari on the converted_acquisitions subdirectory containing centroid mzML files, using default grouping parameters (5 ppm m/z tolerance and 2 second retention time tolerance for feature grouping). Asari will output two feature tables in the asari_results directory: a 'full' table containing all detected features and a 'preferred' table with quality-filtered features. Register both tables in the experiment object with their respective monikers, ensuring they are accessible for subsequent normalization, annotation, and quality control steps.

## Related tools

- **Asari** (Primary tool for feature detection, grouping, and quantification from centroid mzML files; supports ionization mode inference and outputs dual feature tables) — https://github.com/shuzhao-li/asari
- **ThermoRawFileParser** (Upstream tool to convert Thermo .raw files to centroid mzML format before Asari processing)
- **PCPFM (Python-Centric Pipeline for Metabolomics)** (Experiment orchestration framework that manages Asari invocation, ionization mode inference, and feature table registration) — https://github.com/shuzhao-li-lab/PythonCentricPipelineForMetabolomics
- **Python** (Programming environment for PCPFM experiment object manipulation and Asari invocation scripting)

## Examples

```
from pcpfm import Experiment; exp = Experiment.load('path/to/experiment.json'); exp.infer_ionization_mode(); exp.run_asari(mzml_dir='converted_acquisitions', ppm_tol=5, rt_tol=2)
```

## Evaluation signals

- Both 'full' and 'preferred' feature tables are present in asari_results/export/ and asari_results/ directories respectively
- Feature tables contain expected columns: m/z, retention time, feature intensity values across all samples, and feature identifiers
- Preferred feature table row count is less than full feature table row count (quality filtering applied)
- Feature table is registered in experiment.json under monikers 'full' and 'preferred' with file paths resolvable
- Asari visual dashboard (if invoked) displays individual features with m/z and retention time grouping consistent across samples

## Limitations

- Requires ionization mode to be correctly inferred or specified; mismatched polarity will produce irrelevant features
- Default parameters (5 ppm m/z tolerance, 2 second RT tolerance) may not be optimal for all instrument types or sample types; user override is not documented in the provided context
- GC-MS and other data types are not yet supported as of the article publication
- Internal spike-in standard QC support is flagged as 'TO BE IMPLEMENTED' and is not currently available
- Sample names that do not match their mzML file names required a bug fix as of 2/28/24; older versions may fail silently

## Evidence

- [other] Asari generates two feature table monikers upon completion: 'full' for the complete feature table and 'preferred' for a filtered feature table suitable for downstream analysis.: "Asari generates two feature table monikers upon completion: 'full' for the complete feature table and 'preferred' for a filtered feature table suitable for downstream analysis."
- [other] Load the PCPFM experiment object and infer the ionization mode (positive or negative) from the mzML file headers.: "Load the PCPFM experiment object and infer the ionization mode (positive or negative) from the mzML file headers."
- [other] Invoke Asari with the inferred ionization mode on the converted_acquisitions subdirectory containing centroid .mzML files, using default parameters (5 ppm m/z tolerance, 2 second retention time tolerance for feature grouping).: "Invoke Asari with the inferred ionization mode on the converted_acquisitions subdirectory containing centroid .mzML files, using default parameters (5 ppm m/z tolerance, 2 second retention time"
- [other] Asari outputs a full feature table containing all detected features and a preferred feature table with quality-filtered features, both stored in the asari_results directory.: "Asari outputs a full feature table containing all detected features and a preferred feature table with quality-filtered features, both stored in the asari_results directory."
- [readme] process mzML data to feature tables (Asari): "process mzML data to feature tables (Asari)"
- [readme] Asari supports a visual dashboard to explore and inspect individual features.: "Asari supports a visual dashboard to explore and inspect individual features."
- [readme] there was an issue regarding sample names that do not match their mzML file names. This has been fixed as of 2/28/24: "there was an issue regarding sample names that do not match their mzML file names. This has been fixed as of 2/28/24"
- [readme] We are working to add supports of GC and other data types.: "We are working to add supports of GC and other data types."

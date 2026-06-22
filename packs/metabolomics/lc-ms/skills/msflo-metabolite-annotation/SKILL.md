---
name: msflo-metabolite-annotation
description: Use when after MS-DIAL has completed feature detection and peak alignment on .mzML LC-HRMS data, producing an aligned feature table. Use MSFLO when you need to assign metabolite identities to detected features and filter results by significance criteria before downstream interpretation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3803
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - MSFLO
  - Docker
  - Nextflow
  - Singularity
  - MS-DIAL
  techniques:
  - LC-MS
  - CE-MS
derived_from:
- doi: 10.1021/jasms.4c00364
  title: nextflow4msdial
evidence_spans:
- containerized workflow MS-DIAL -> MSFLO
- Both Docker and Singularity (for high-performance computing) are supported
- Both Docker and Singularity (for high-performance computing) are supported.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_nextflow4msdial_cq
    doi: 10.1021/jasms.4c00364
    title: nextflow4msdial
  dedup_kept_from: coll_nextflow4msdial_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/jasms.4c00364
  all_source_dois:
  - 10.1021/jasms.4c00364
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# msflo-metabolite-annotation

## Summary

MSFLO is a containerized metabolite annotation module that processes aligned LC-HRMS feature tables from MS-DIAL to assign metabolite identities and perform statistical analysis. This skill encapsulates the post-feature-detection annotation and filtering stage within reproducible Nextflow4MS-DIAL workflows.

## When to use

Apply this skill after MS-DIAL has completed feature detection and peak alignment on .mzML LC-HRMS data, producing an aligned feature table. Use MSFLO when you need to assign metabolite identities to detected features and filter results by significance criteria before downstream interpretation.

## When NOT to use

- Raw .mzML or .abf mass spectrometry files have not yet undergone MS-DIAL feature detection and alignment — use MS-DIAL first.
- Reference spectral libraries (MS1 and MS2) are not available or not in the required text/MSP formats.
- The input is already a fully annotated and statistically validated metabolite table; MSFLO is redundant at that stage.

## Inputs

- Aligned feature table (TSV format) from MS-DIAL containing m/z, retention time, and intensity values across samples
- MS1 reference spectral library (ms1_lib.txt)
- MS2 reference spectral library (ms2_lib.msp)
- MSFLO parameters configuration file (msflo_params.ini)

## Outputs

- Annotated feature table (TSV format) with metabolite identities, annotation scores, and statistical metrics
- Filtered feature set meeting significance and annotation confidence thresholds

## How to apply

After the Nextflow4MS-DIAL pipeline has routed aligned features through the containerized MS-DIAL module, pass the resulting feature table through the containerized MSFLO module by specifying MSFLO parameters in a configuration file named `msflo_params.ini` and placing it in the `data/` folder. MSFLO accepts the aligned feature table from MS-DIAL and uses reference MS1 and MS2 spectral libraries (named `ms1_lib.txt` and `ms2_lib.msp` in the `data/` folder) to annotate features with metabolite identities. The module applies annotation filtering and statistical tests to produce a final annotated feature table suitable for metabolomics interpretation. Configuration and library setup must be validated before pipeline execution to ensure correct annotation parameters and library formats.

## Related tools

- **Nextflow** (Workflow orchestration engine that manages containerized MSFLO execution across Docker and Singularity runtimes) — https://www.nextflow.io/
- **Docker** (Container runtime for local execution of containerized MSFLO module) — https://docs.docker.com/engine/installation/
- **Singularity** (Container runtime for MSFLO execution on high-performance computing systems) — https://www.sylabs.io/guides/3.0/user-guide/
- **MS-DIAL** (Upstream feature detection and alignment module that produces the aligned feature table consumed by MSFLO)

## Examples

```
nextflow run main.nf -profile docker
```

## Evaluation signals

- Output feature table contains metabolite annotations (non-null metabolite names or IDs) for a high proportion of input features, indicating successful library matching.
- MSFLO annotation scores or cosine similarity metrics meet expected ranges relative to reference spectral library quality and completeness.
- Statistical filtering results in a reasonable retention rate (e.g., features surviving p-value or fold-change thresholds) consistent with the biological replicate structure.
- Output file format is valid TSV with expected column headers (metabolite name, m/z, retention time, annotation confidence score, p-value, etc.).
- Pipeline execution log contains no errors during the MSFLO containerized process and reports completion of annotation and statistical steps.

## Limitations

- MSFLO annotation accuracy depends critically on the completeness and quality of the provided MS1 and MS2 reference spectral libraries; incomplete or poorly curated libraries will result in low annotation coverage.
- Configuration file parameters (msflo_params.ini) must be manually validated and pre-tested; incorrect parameter settings may produce silently incorrect results or filtered-out features.
- The workflow has been tested successfully on macOS 13.5.1 with Intel Core i7 and 16 GB memory, and on HiPerGator (Red Hat Enterprise Linux 8.8); performance and compatibility on other systems are not documented.
- Special characters in data file names are not supported and will cause errors; only underscores are safe.

## Evidence

- [other] Route aligned features through the containerized MSFLO module for annotation and statistical processing.: "Route aligned features through the containerized MSFLO module for annotation and statistical processing."
- [other] Nextflow4MS-DIAL implements a containerized workflow that routes .mzML LC-MS metabolomics data through MS-DIAL followed by MSFLO.: "Nextflow4MS-DIAL implements a containerized workflow that routes .mzML LC-MS metabolomics data through MS-DIAL followed by MSFLO, with support for both Docker and Singularity container runtimes."
- [readme] Add the MS1 and MS2 libraries to the `data/` folder and name them `ms1_lib.txt` and `ms2_lib.msp`.: "Add the MS1 and MS2 libraries to the `data/` folder and name them `ms1_lib.txt` and `ms2_lib.msp`. Example library files are available in `functional_test/sample_data/`."
- [readme] Add the MS-DIAL and MS-FLO configuration files to the `data/` folder and name them `msdial_params.txt` and `msflo_params.ini`.: "Add the MS-DIAL and MS-FLO configuration files to the `data/` folder and name them `msdial_params.txt` and `msflo_params.ini`. Example configuration files are available in"
- [readme] Both Docker and Singularity (for high-performance computing) are supported.: "Both Docker and Singularity (for high-performance computing) are supported"
